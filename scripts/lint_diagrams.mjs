/**
 * Geometry lint for the generated diagrams.
 *
 * `enc validate` checks that a diagram spec is well formed. It cannot check
 * that the result is *legible*, because legibility is a property of rendered
 * glyphs, not of YAML. The renderer estimates text widths from a per-character
 * advance, and an estimate that is fifteen per cent low is exactly enough to
 * push the last word of a label through the side of its box — silently, and
 * only in the browser.
 *
 * So: render every diagram in a real browser, measure every text node, and fail
 * on the three ways a figure can be wrong without anyone noticing.
 *
 *   overflow   text extends past the edge of its own SVG, so it is clipped
 *   spill      text extends past the box or panel it belongs to
 *   collision  two pieces of text overlap enough to be unreadable
 *
 * Run:  node scripts/lint_diagrams.mjs [--theme both] [--json report.json]
 * Exit: 0 clean, 1 findings, 2 could not run
 */

import { chromium } from 'playwright';
import { readFileSync, writeFileSync, readdirSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { execFileSync } from 'node:child_process';

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..');

// How much two text boxes may overlap before it counts. Descenders and the
// odd kerned pair touch legitimately; a word sitting on another word does not.
const OVERLAP_TOLERANCE = 6.0;   // px² of intersection, scaled by box size
const EDGE_TOLERANCE = 1.5;      // px a glyph box may exceed a container by

function entriesWithDiagrams() {
  const dir = join(ROOT, 'content', 'entries');
  const out = [];
  for (const file of readdirSync(dir)) {
    if (!file.endsWith('.md')) continue;
    const text = readFileSync(join(dir, file), 'utf8');
    const fm = text.split('---')[1] ?? '';
    if (/^diagrams?:/m.test(fm)) out.push(file.replace(/\.md$/, ''));
  }
  return out.sort();
}

/** Render every diagram to one harness page, via the project's own renderer. */
function buildHarness(slugs) {
  const py = `
import sys, json, yaml
sys.path.insert(0, "tools")
from encyclopedia import diagrams
out = []
for slug in ${JSON.stringify(slugs)}:
    meta = yaml.safe_load(open(f"content/entries/{slug}.md", encoding="utf-8").read().split("---", 2)[1])
    specs = ([meta["diagram"]] if meta.get("diagram") else []) + (meta.get("diagrams") or [])
    for i, spec in enumerate(specs):
        out.append({"slug": slug, "index": i, "svg": diagrams.render(spec)})
print(json.dumps(out))
`;
  const raw = execFileSync('python3', ['-c', py], {
    cwd: ROOT, maxBuffer: 256 * 1024 * 1024, encoding: 'utf8',
  });
  return JSON.parse(raw);
}

function page(figures, css) {
  const body = figures
    .map((f, n) => `<figure class="dgm-fig" data-fig="${n}" data-slug="${f.slug}">${f.svg}</figure>`)
    .join('\n');
  return `<!doctype html><meta charset="utf-8"><style>
${css}
body { margin: 0; padding: 24px; background: var(--paper); }
figure.dgm-fig { width: 928px; margin: 0 0 40px; }
</style><body class="md-typeset">${body}</body>`;
}

const MEASURE = ({ tolEdge, tolOverlap }) => {
  const findings = [];
  for (const fig of document.querySelectorAll('figure.dgm-fig')) {
    const slug = fig.dataset.slug;
    const svg = fig.querySelector('svg.dgm');
    if (!svg) continue;
    const frame = svg.getBoundingClientRect();
    const scale = frame.width / svg.viewBox.baseVal.width || 1;

    const texts = [...svg.querySelectorAll('text')].filter(t => (t.textContent || '').trim());
    const boxes = texts.map(t => ({ el: t, r: t.getBoundingClientRect(), s: t.textContent.trim() }));

    // 1. anything outside the figure's own frame is clipped
    for (const b of boxes) {
      if (!b.r.width) continue;
      const over = Math.max(
        frame.left - b.r.left, b.r.right - frame.right,
        frame.top - b.r.top, b.r.bottom - frame.bottom,
      );
      if (over > tolEdge) {
        findings.push({ slug, kind: 'overflow', text: b.s, px: +(over / scale).toFixed(1) });
      }
    }

    // 2. anything wider than the box it sits inside.
    // Grounds are excluded: a panel, a plot frame, a shaded band or a bar
    // track is something drawn *behind* the figure, not a box the label is
    // supposed to fit within. Counting them produces noise, not findings.
    const GROUND = /dgm-(panel|plotframe|plotband|plane|segtrack|track)\b/;
    const containers = [...svg.querySelectorAll('rect')]
      .filter(r => !GROUND.test(r.getAttribute('class') || ''))
      .map(r => ({ el: r, r: r.getBoundingClientRect() }));
    for (const b of boxes) {
      if (!b.r.width) continue;
      const cx = (b.r.left + b.r.right) / 2, cy = (b.r.top + b.r.bottom) / 2;
      // the tightest rect whose centre contains this label
      let host = null;
      for (const c of containers) {
        if (cx > c.r.left && cx < c.r.right && cy > c.r.top && cy < c.r.bottom) {
          if (!host || c.r.width * c.r.height < host.r.width * host.r.height) host = c;
        }
      }
      if (!host) continue;
      const spill = Math.max(host.r.left - b.r.left, b.r.right - host.r.right);
      if (spill > tolEdge) {
        findings.push({
          slug, kind: 'spill', text: b.s, px: +(spill / scale).toFixed(1),
          container: host.el.getAttribute('class') || 'rect',
        });
      }
    }

    // 3. two labels sitting on top of each other
    for (let i = 0; i < boxes.length; i++) {
      for (let j = i + 1; j < boxes.length; j++) {
        const a = boxes[i].r, b = boxes[j].r;
        const w = Math.min(a.right, b.right) - Math.max(a.left, b.left);
        const h = Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top);
        if (w <= 0 || h <= 0) continue;
        // ignore the hairline touch of adjacent baselines
        if (h < 3 || w < 3) continue;
        const area = (w * h) / (scale * scale);
        if (area > tolOverlap) {
          findings.push({
            slug, kind: 'collision', text: boxes[i].s, other: boxes[j].s,
            px: +area.toFixed(0),
          });
        }
      }
    }
  }
  return findings;
};

const args = process.argv.slice(2);
const themes = args.includes('--theme') ? [args[args.indexOf('--theme') + 1]] : ['light', 'dark'];
const jsonOut = args.includes('--json') ? args[args.indexOf('--json') + 1] : null;

const slugs = entriesWithDiagrams();
if (!slugs.length) { console.log('no diagrams to lint'); process.exit(0); }

const figures = buildHarness(slugs);
const css = readFileSync(join(ROOT, 'theme', 'stylesheets', 'encyclopedia.css'), 'utf8');
const html = page(figures, css);

const browser = await chromium.launch({
  executablePath: process.env.PLAYWRIGHT_CHROMIUM || undefined,
});
const all = [];
for (const theme of themes) {
  const ctx = await browser.newContext({ viewport: { width: 1100, height: 900 } });
  const p = await ctx.newPage();
  await p.setContent(html, { waitUntil: 'load' });
  if (theme === 'dark') {
    await p.evaluate(() => document.documentElement.setAttribute('data-md-color-scheme', 'slate'));
  }
  await p.waitForTimeout(350);           // let webfonts settle before measuring
  const found = await p.evaluate(MEASURE,
    { tolEdge: EDGE_TOLERANCE, tolOverlap: OVERLAP_TOLERANCE });
  all.push(...found.map(f => ({ ...f, theme })));
  await ctx.close();
}
await browser.close();

if (jsonOut) writeFileSync(jsonOut, JSON.stringify(all, null, 2));

const counts = all.reduce((m, f) => ((m[f.kind] = (m[f.kind] || 0) + 1), m), {});
console.log(`${figures.length} figures from ${slugs.length} entries, ${themes.join(' + ')}`);

if (!all.length) {
  console.log('clean — no overflow, spill or collision');
  process.exit(0);
}

const byEntry = {};
for (const f of all) (byEntry[f.slug] ||= []).push(f);
for (const [slug, list] of Object.entries(byEntry)) {
  console.log(`\n${slug}`);
  for (const f of list) {
    const detail = f.kind === 'collision'
      ? `"${f.text}" over "${f.other}" (${f.px}px²)`
      : `"${f.text}" by ${f.px}px${f.container ? ` out of ${f.container}` : ''}`;
    console.log(`  ${f.kind.padEnd(9)} ${f.theme.padEnd(5)} ${detail}`);
  }
}
console.log(`\n${all.length} findings: ` +
  Object.entries(counts).map(([k, v]) => `${v} ${k}`).join(', '));
process.exit(1);

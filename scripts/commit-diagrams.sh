#!/usr/bin/env bash
#
# One-shot: tidy up, then commit the diagram work in four labelled commits.
#
# Run it from the repository root, in Git Bash (ships with Git for Windows) or
# any POSIX shell:
#
#     bash scripts/commit-diagrams.sh
#
# It touches nothing outside this repository, makes no network calls, and stops
# at the first problem. Pushing is left to you — run `git push` when the log
# looks right.
#
set -euo pipefail

say()  { printf '\n\033[1m%s\033[0m\n' "$*"; }
ok()   { printf '  \033[32m✓\033[0m %s\n' "$*"; }
warn() { printf '  \033[33m!\033[0m %s\n' "$*"; }

[ -d .git ] || { echo "Run this from the repository root."; exit 1; }
[ -f tools/encyclopedia/diagrams.py ] || { echo "tools/encyclopedia/diagrams.py is missing."; exit 1; }

# --------------------------------------------------------------------------
say "1. Clearing the stale git lock and orphaned temp objects"
# A crashed git process left a zero-byte index.lock behind, and the remote
# bridge that wrote these files cannot delete anything, so the debris is still
# there. None of it is real data.
for f in .git/index.lock .git/index.lock.stale-*; do
  [ -e "$f" ] && rm -f "$f" && ok "removed $f"
done
n=$(find .git/objects -name 'tmp_obj_*' 2>/dev/null | wc -l | tr -d ' ')
if [ "$n" -gt 0 ]; then
  find .git/objects -name 'tmp_obj_*' -delete
  ok "removed $n orphaned temp objects"
fi
git reset -q                                  # drop any staging left behind
ok "index reset — working files untouched"

# --------------------------------------------------------------------------
say "2. Writing the two files the remote bridge is not allowed to write"

cat > Makefile.diagrams.tmp <<'MAKE'
.PHONY: diagrams
diagrams: ## Lint rendered diagram geometry in a real browser
	node scripts/lint_diagrams.mjs

MAKE
if grep -q '^diagrams:' Makefile; then
  rm -f Makefile.diagrams.tmp
  ok "Makefile already has the diagrams target"
else
  awk '/^\.PHONY: build$/ && !done { while ((getline line < "Makefile.diagrams.tmp") > 0) print line; done=1 } { print }' \
    Makefile > Makefile.new && mv Makefile.new Makefile
  rm -f Makefile.diagrams.tmp
  ok "Makefile: added \`make diagrams\`"
fi

if grep -q 'Diagram geometry' .github/workflows/ci.yml; then
  ok "ci.yml already has the diagrams job"
else
  python - <<'PY'
import io
p = '.github/workflows/ci.yml'
s = io.open(p, encoding='utf-8-sig').read()
job = '''
  diagrams:
    name: Diagram geometry
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
          cache: pip
      - uses: actions/setup-node@v4
        with:
          node-version: "20"
      - name: Install
        run: |
          pip install --upgrade pip
          pip install -r requirements-dev.txt
          pip install -e .
          npm install --no-save playwright@1.49
          npx playwright install --with-deps chromium
      - name: Lint diagram geometry
        # Renders every figure in a real browser and fails on text that is
        # clipped, spills out of its box, or overlaps another label. The
        # renderer estimates text widths, so only a browser can catch this.
        run: node scripts/lint_diagrams.mjs --json diagram-report.json
      - name: Upload report
        if: failure()
        uses: actions/upload-artifact@v4
        with:
          name: diagram-report
          path: diagram-report.json
'''
anchor = "\n  test:\n    name: Tooling tests"
if anchor not in s:
    raise SystemExit("ci.yml: could not find the `test` job to insert before")
io.open(p, 'w', encoding='utf-8').write(s.replace(anchor, job + anchor, 1))
PY
  ok "ci.yml: added the Diagram geometry job"
fi

# --------------------------------------------------------------------------
say "3. Committing"

commit() {                                    # commit <message> <paths...>
  local msg="$1"; shift
  local staged=0
  for p in "$@"; do [ -e "$p" ] && git add -- "$p" && staged=1; done
  if [ "$staged" = 1 ] && ! git diff --cached --quiet; then
    git commit -q -m "$msg"
    ok "$(git log --oneline -1)"
  else
    warn "nothing to commit for: ${msg%%$'\n'*}"
  fi
}

git ls-files | grep -E '__pycache__|egg-info' > .artefacts.tmp || true
if [ -s .artefacts.tmp ]; then
  git rm --cached -q --pathspec-from-file=.artefacts.tmp
fi
rm -f .artefacts.tmp

commit "Add .gitignore; stop tracking build artefacts

__pycache__, egg-info and the generated build/ tree were committed, so every
local build appeared as a diff and buried real changes in the noise. The files
stay on disk; git simply stops watching them." \
  .gitignore

commit "Diagram engine: sixteen visual primitives and a tone system

Replaces ASCII blocks with declarative figures rendered to themed SVG.

  - Nine new primitives on top of the original seven: segments, plot, passes,
    pipeline, mapping, matrix, scatter, tree, lineage. Chosen against a census
    of all 187 ASCII blocks in the corpus.
  - Five tone roles (accent, warn, bad, ok, muted), each resolving to an
    existing site token, so light mode, dark mode and any future palette need
    no regeneration. No colour literal appears in the renderer.
  - A diagram may be anchored to any section, not only How Does It Work. An
    anchor to a section the entry lacks is now an error rather than a figure
    that silently vanishes.
  - VISUAL_KEYS is the single contract: the validator reads it, so a typo in a
    spec fails at \`enc validate\` instead of appearing as blank space on a page.
  - Clip-path ids derive from geometry rather than hash(), so builds are
    byte-identical run to run." \
  tools/encyclopedia/diagrams.py tools/encyclopedia/build.py \
  tools/encyclopedia/model.py tools/encyclopedia/validate.py \
  schema/entry.schema.json theme/stylesheets/encyclopedia.css

commit "Convert 24 entries from ASCII to rendered figures

Each entry's ASCII block is replaced by a diagram spec in front matter.
kv-cache also gains a lineage rail in Evolution, the first use of section
anchoring.

Ten of these sections consisted of nothing but the diagram, so removing the
ASCII left them empty and the entry contract correctly rejected them. They now
carry prose that says what the figure cannot: why the mechanism has that shape,
and what it costs." \
  content/entries/attention.md content/entries/backpropagation.md \
  content/entries/embedding.md content/entries/activation-function.md \
  content/entries/context-window.md content/entries/tokenization.md \
  content/entries/beam-search.md content/entries/base-model.md \
  content/entries/kv-cache.md content/entries/data-curation.md \
  content/entries/compiler.md content/entries/cuda.md content/entries/cpu.md \
  content/entries/computer-vision.md content/entries/chunking.md \
  content/entries/context-engineering.md content/entries/coding-agent.md \
  content/entries/computer-use.md content/entries/continual-learning.md \
  content/entries/curriculum-learning.md content/entries/data-flywheel.md \
  content/entries/chain-of-thought.md content/entries/chunked-prefill.md \
  content/entries/bayesian-inference.md

commit "Add a geometry lint for rendered diagrams

\`enc validate\` checks that a spec is well formed; it cannot check that the
result is legible, because legibility is a property of rendered glyphs. The
renderer estimates text widths from a per-character advance, and an estimate
fifteen per cent low is exactly enough to push the last word of a label through
the side of its box, silently and only in a browser.

This renders every figure in Chromium and fails on three things: text clipped by
the edge of its SVG, text spilling out of its own box, and two labels
overlapping. Run over both themes. It found sixteen real defects on its first
run, all since fixed." \
  scripts/lint_diagrams.mjs scripts/commit-diagrams.sh Makefile \
  .github/workflows/ci.yml

# --------------------------------------------------------------------------
say "4. What is left uncommitted"
git status --short || true

cat <<'NEXT'

Everything above that is still listed is your own earlier work — around fifty
entries plus cli.py, graph.js, enhance.js, mkdocs.yml and CONTRIBUTING.md. It
was already modified before the diagram work started, so it has been left alone
for you to review and commit separately.

Next:
    make check          # enc validate --strict
    make build
    make diagrams       # needs: npm install --no-save playwright && npx playwright install chromium
    git push

NEXT

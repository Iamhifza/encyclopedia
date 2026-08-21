"""Generate the site and the JSON API from ``content/``.

Nothing in ``build/`` is edited by hand -- it is disposable output. The eight
reader-facing views (search, topics, A-Z, timeline, graph, compare, learn,
system view) are all projections of the same records, which is what keeps a
single canonical entry reachable from many paths without duplication.
"""

from __future__ import annotations

import json
import re
import shutil
from collections import defaultdict
from datetime import date
from pathlib import Path
from typing import Any

import yaml

from .graph import ConceptGraph
from .model import (
    DIFFICULTY_BADGE,
    ENCOUNTERED_LABEL,
    HISTORICAL_PERIODS,
    SECTION_ORDER,
    SOURCE_LABEL,
    STATUS_NOTE,
    STATUS_ORDER,
    Corpus,
    Entry,
)

ROOT = Path(__file__).resolve().parents[2]


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------

def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def link(entry: Entry, prefix: str = "..") -> str:
    return f"[{entry.term}]({prefix}/terms/{entry.slug}.md)"


def sort_key(entry: Entry) -> tuple[str, str]:
    return (re.sub(r"^[^A-Za-z0-9]+", "", entry.term).lower(), entry.term)


def first_letter(entry: Entry) -> str:
    head = re.sub(r"^[^A-Za-z0-9]+", "", entry.term)[:1].upper()
    return head if head.isalpha() else "#"


class Builder:
    def __init__(self, corpus: Corpus, out_dir: Path, site_url: str = "") -> None:
        self.corpus = corpus
        self.graph = ConceptGraph(corpus)
        self.docs = out_dir / "docs"
        self.api = out_dir / "docs" / "api"
        self.out_dir = out_dir
        self.site_url = site_url
        self.nav: list[Any] = []

    # -- entry point --------------------------------------------------
    def run(self) -> dict[str, Any]:
        if self.docs.exists():
            shutil.rmtree(self.docs)
        self.docs.mkdir(parents=True)

        self.copy_static()
        self.build_home()
        self.build_topics()
        self.build_entries()
        self.build_az()
        self.build_timeline()
        self.build_graph_page()
        self.build_comparisons()
        self.build_learning_paths()
        self.build_system_view()
        self.build_meta()
        self.build_api()
        self.write_mkdocs_config()
        return self.graph.stats()

    # -- static -------------------------------------------------------
    def copy_static(self) -> None:
        theme = ROOT / "theme"
        for sub in ("stylesheets", "javascripts"):
            src = theme / sub
            if src.exists():
                shutil.copytree(src, self.docs / "assets" / sub, dirs_exist_ok=True)
        for name, target in [
            ("CONTRIBUTING.md", "contributing.md"),
            ("CODE_OF_CONDUCT.md", "code-of-conduct.md"),
            ("CHANGELOG.md", "changelog.md"),
        ]:
            src = ROOT / name
            if src.exists():
                shutil.copy(src, self.docs / target)

    # -- home ---------------------------------------------------------
    def build_home(self) -> None:
        counts = {c: len(v) for c, v in self.corpus.by_category().items()}
        total = len(self.corpus.entries)
        rows = []
        for cat in self.corpus.taxonomy.get("categories", []):
            n = counts.get(cat["id"], 0)
            rows.append(
                f"| `{cat['number']}` | [{cat['name']}](topics/{cat['id']}.md) | {n} | {cat['summary']} |"
            )
        body = f"""# The AI &amp; Computing Encyclopedia

A map of the field, not a word list. Every concept gets one canonical entry
that answers *what is this*, and then keeps going: why it exists, what it
replaced, what replaced it, what it is confused with, and where you will
meet it.

There are **{total} entries** across **{len(rows)} domains**, connected by
**{len(self.graph.edges)} typed relationships**.

## Eight ways in

| | View | Question it answers |
|---|---|---|
| :material-magnify: | Search (press <kbd>/</kbd>) | What does this mean? |
| :material-bookshelf: | [Topics](topics/index.md) | How is the field organised? |
| :material-alphabetical: | [A-Z](az/index.md) | Find this specific term. |
| :material-clock-outline: | [Timeline](timeline/index.md) | How did this evolve? |
| :material-graph-outline: | [Concept graph](graph/index.md) | How does this connect to everything else? |
| :material-scale-balance: | [Compare](compare/index.md) | What is the difference between these? |
| :material-school-outline: | [Learning paths](learn/index.md) | What should I learn next? |
| :material-layers-triple: | [System view](system-view.md) | Where does this fit in a real system? |

## Start here

If you have never heard the term you just read, the entry will take you from
a one-sentence definition to prerequisites, history, differences and further
reading. Try [Harness](terms/harness.md), [KV Cache](terms/kv-cache.md) or
[Vibe Coding](terms/vibe-coding.md).

## Domains

| # | Domain | Entries | Scope |
|---|--------|--------:|-------|
{chr(10).join(rows)}

## How this is written

* **One canonical entry per concept.** Categories, paths, the graph and the
  A-Z index are all views over the same record -- nothing is duplicated.
* **Uncertainty is labelled, not hidden.** Terms like *harness*, *scaffold*
  and *context engineering* genuinely mean different things to different
  teams. Those entries carry a `contested` status and a Terminology Note
  that reports the disagreement instead of inventing a consensus.
* **Slang counts.** *Vibe coding* and *AI slop* shape how engineers talk, so
  they are documented and clearly labelled as informal.
* **Primary sources first.** Papers, specifications and official
  documentation before commentary.
* **Dates on everything.** Every entry records when it was last reviewed,
  because half of this vocabulary is younger than most codebases.

See [Editorial standards](meta/standards.md) for the full policy and
[Coverage](meta/coverage.md) for what is still missing.
"""
        write(self.docs / "index.md", body)

    # -- topics -------------------------------------------------------
    def build_topics(self) -> None:
        by_cat = self.corpus.by_category()
        cats = self.corpus.taxonomy.get("categories", [])

        lines = [
            "# Topics",
            "",
            "The field organised the way it is actually structured: from silicon up to",
            "culture. Each domain lists its entries with a one-line definition.",
            "",
        ]
        for cat in cats:
            entries = by_cat.get(cat["id"], [])
            lines.append(f"## {cat['number']}. [{cat['name']}]({cat['id']}.md)")
            lines.append("")
            lines.append(cat["summary"])
            lines.append("")
            if entries:
                names = ", ".join(
                    f"[{e.term}](../terms/{e.slug}.md)" for e in sorted(entries, key=sort_key)
                )
                lines.append(f"**{len(entries)} entries:** {names}")
            else:
                lines.append("*No entries yet. This domain is scoped but unwritten -- "
                             "see [Coverage](../meta/coverage.md).*")
            lines.append("")
        write(self.docs / "topics" / "index.md", "\n".join(lines))

        nav_children = []
        for cat in cats:
            entries = sorted(by_cat.get(cat["id"], []), key=sort_key)
            page = [f"# {cat['number']}. {cat['name']}", "", cat["summary"], ""]

            subs = cat.get("subcategories", [])
            grouped: dict[str | None, list[Entry]] = defaultdict(list)
            for entry in entries:
                grouped[entry.subcategory].append(entry)

            if not entries:
                page += [
                    "!!! note \"Scoped, not yet written\"",
                    "",
                    "    This domain is part of the map but has no entries yet.",
                    "    Contributions are welcome -- see [Contributing](../contributing.md).",
                    "",
                ]

            for sub in subs:
                items = grouped.get(sub["id"], [])
                if not items:
                    continue
                page.append(f"## {sub['name']}")
                page.append("")
                if sub.get("summary"):
                    page += [sub["summary"], ""]
                page += self._entry_table(items)
                page.append("")

            loose = grouped.get(None, []) + [
                e
                for k, v in grouped.items()
                if k is not None and k not in {s["id"] for s in subs}
                for e in v
            ]
            if loose:
                if subs:
                    page += ["## Other", ""]
                page += self._entry_table(sorted(loose, key=sort_key))
                page.append("")

            write(self.docs / "topics" / f"{cat['id']}.md", "\n".join(page))
            nav_children.append({cat["name"]: f"topics/{cat['id']}.md"})

        self._topics_nav = nav_children

    def _entry_table(self, entries: list[Entry]) -> list[str]:
        rows = ["| Term | Definition | Status | Level |", "|---|---|---|---|"]
        for entry in entries:
            mark = " ·&nbsp;*seed*" if entry.is_seed else ""
            rows.append(
                f"| [{entry.term}](../terms/{entry.slug}.md){mark} | {entry.one_liner} | "
                f"`{entry.status}` | {DIFFICULTY_BADGE[entry.difficulty].split()[0]} |"
            )
        return rows

    # -- entries ------------------------------------------------------
    def build_entries(self) -> None:
        path_index: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for p in self.corpus.paths.get("paths", []):
            for i, step in enumerate(p["steps"], start=1):
                path_index[step["term"]].append({"path": p, "position": i})

        compare_index: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for comp in self.corpus.comparisons:
            for side in comp.get("sides", []):
                compare_index[side].append(comp)

        timeline_index: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for era in self.corpus.timeline.get("eras", []):
            for event in era.get("events", []):
                if event.get("term"):
                    timeline_index[event["term"]].append({"era": era, "event": event})

        for slug, entry in sorted(self.corpus.entries.items()):
            write(
                self.docs / "terms" / f"{slug}.md",
                self._render_entry(entry, path_index, compare_index, timeline_index),
            )

        lines = ["# All entries", "", "Every canonical entry, newest review first.", ""]
        lines += ["| Term | Domain | Depth | Status | Reviewed |", "|---|---|---|---|---|"]
        for entry in sorted(
            self.corpus.entries.values(), key=lambda e: (str(e.meta.get("updated", "")), e.term), reverse=True
        ):
            cat = self.corpus.category_meta(entry.category)
            lines.append(
                f"| [{entry.term}]({entry.slug}.md) | [{cat['name']}](../topics/{cat['id']}.md) | "
                f"{'seed' if entry.is_seed else 'full'} | `{entry.status}` | {entry.meta.get('updated', '')} |"
            )
        write(self.docs / "terms" / "index.md", "\n".join(lines))

    def _render_entry(
        self,
        entry: Entry,
        path_index: dict[str, list[dict[str, Any]]],
        compare_index: dict[str, list[dict[str, Any]]],
        timeline_index: dict[str, list[dict[str, Any]]],
    ) -> str:
        cat = self.corpus.category_meta(entry.category)
        out: list[str] = []

        out.append(f"# {entry.term}")
        out.append("")
        if entry.aliases:
            out.append("*Also known as: " + ", ".join(f"**{a}**" for a in entry.aliases) + "*")
            out.append("")

        badges = [
            f"[{cat['name']}](../topics/{cat['id']}.md)",
            f"`{entry.status}`",
            DIFFICULTY_BADGE[entry.difficulty],
        ]
        if entry.meta.get("updated"):
            badges.append(f"reviewed {entry.meta['updated']}")
        out.append(" · ".join(badges))
        out.append("")

        if entry.meta.get("disputed"):
            out += [
                "!!! warning \"Contested term\"",
                "",
                "    This term is used with materially different meanings by different",
                "    teams. Read the Terminology Note before assuming which one someone",
                "    means.",
                "",
            ]

        out += ["!!! abstract \"One-line definition\"", "", f"    {entry.one_liner}", ""]

        if entry.is_seed:
            out += [
                "!!! note \"Seed entry\"",
                "",
                "    This is a lookup record: canonical name, definition and its place in",
                "    the concept graph. The full treatment -- how it works, why it exists,",
                "    worked examples, history and confusions -- is not written yet.",
                "",
                "    [Expand this entry](../contributing.md) or open an issue if something",
                "    here is wrong.",
                "",
            ]

        if entry.prerequisites:
            names = ", ".join(
                f"[{self.corpus.entries[p].term}]({p}.md)" for p in entry.prerequisites
            )
            out += [
                "!!! tip \"Read these first\"",
                "",
                f"    {names}",
                "",
            ]

        for heading in SECTION_ORDER:
            if heading in ("One-Line Definition",):
                continue
            body = entry.sections.get(heading)
            if body:
                out += [f"## {heading}", "", body, ""]

        for heading in entry.section_order:
            if heading not in SECTION_ORDER and entry.sections.get(heading):
                out += [f"## {heading}", "", entry.sections[heading], ""]

        # -- generated: relations
        neighbours = self.graph.neighbours(entry.slug)
        if neighbours:
            out += ["## Related Concepts", ""]
            for key, targets in neighbours.items():
                label = self.graph.label_for(key)
                out.append(f"**{label}**")
                out.append("")
                for target in targets:
                    other = self.corpus.entries[target]
                    out.append(f"- [{other.term}]({target}.md) — {other.one_liner}")
                out.append("")

        # -- generated: comparisons
        comps = compare_index.get(entry.slug, [])
        if comps:
            out += ["## Side-by-side", ""]
            for comp in comps:
                others = [
                    self.corpus.entries[s].term for s in comp["sides"] if s != entry.slug
                ]
                out.append(
                    f"- [{comp['title']}](../compare/{comp['id']}.md) — versus "
                    + ", ".join(others)
                )
            out.append("")

        # -- generated: learning paths
        steps = path_index.get(entry.slug, [])
        if steps:
            out += ["## Where This Sits in a Learning Path", ""]
            for item in steps:
                p = item["path"]
                total = len(p["steps"])
                out.append(
                    f"- **[{p['name']}](../learn/{p['id']}.md)** — step {item['position']} of {total}"
                )
            out.append("")

        # -- generated: further reading
        if entry.sources:
            out += ["## Further Reading", ""]
            for src in entry.sources:
                label = SOURCE_LABEL.get(src["type"], src["type"].title())
                year = f" ({src['year']})" if src.get("year") else ""
                note = f" — {src['note']}" if src.get("note") else ""
                out.append(f"1. *{label}*{year}: [{src['title']}]({src['url']}){note}")
            out.append("")

        # -- generated: metadata footer
        out += ["## Entry Metadata", "", '<div class="entry-meta" markdown>', ""]
        origin = entry.meta.get("origin") or {}
        if origin:
            bits = []
            if origin.get("year"):
                bits.append(("circa " if origin.get("circa") else "") + str(origin["year"]))
            if origin.get("attribution"):
                bits.append(origin["attribution"])
            out.append(f"**Origin** — {'; '.join(bits)}")
            out.append("")
        if entry.meta.get("historical_period"):
            label = dict(HISTORICAL_PERIODS).get(entry.meta["historical_period"], "")
            out.append(
                f"**Era** — [{entry.meta['historical_period'].replace('-', ' ')}]"
                f"(../timeline/index.md#{entry.meta['historical_period']}) ({label})"
            )
            out.append("")
        out.append(f"**Status** — `{entry.status}`: {STATUS_NOTE[entry.status]}")
        out.append("")
        out.append(f"**Difficulty** — {DIFFICULTY_BADGE[entry.difficulty]}")
        out.append("")
        if entry.meta.get("encountered_in"):
            where = ", ".join(
                ENCOUNTERED_LABEL.get(x, x) for x in entry.meta["encountered_in"]
            )
            out.append(f"**Where you will meet it** — {where}")
            out.append("")
        if entry.tags:
            out.append("**Tags** — " + " ".join(f"`{t}`" for t in entry.tags))
            out.append("")

        eras = timeline_index.get(entry.slug, [])
        if eras:
            marks = ", ".join(
                f"{i['event']['year']} ({i['era']['label']})" for i in eras
            )
            out.append(f"**On the timeline** — {marks}")
            out.append("")

        routes = [
            f"[A-Z → {first_letter(entry)}](../az/index.md#{first_letter(entry).lower()})",
            f"[{cat['name']}](../topics/{cat['id']}.md)",
            f"[Concept graph](../graph/index.md?focus={entry.slug})",
        ]
        for item in steps:
            routes.append(f"[{item['path']['name']}](../learn/{item['path']['id']}.md)")
        out.append("**Reachable from** — " + " · ".join(routes))
        out += ["", "</div>"]

        return "\n".join(out)

    # -- A-Z ----------------------------------------------------------
    def build_az(self) -> None:
        buckets: dict[str, list[tuple[str, str, bool]]] = defaultdict(list)
        for entry in self.corpus.entries.values():
            buckets[first_letter(entry)].append((entry.term, entry.slug, False))
            for alias in entry.aliases:
                head = re.sub(r"^[^A-Za-z0-9]+", "", alias)[:1].upper()
                head = head if head.isalpha() else "#"
                buckets[head].append((alias, entry.slug, True))

        letters = sorted(buckets)
        jump = " · ".join(f"[{c}](#{c.lower()})" for c in letters)
        lines = [
            "# A-Z index",
            "",
            "Lookup, not learning. Aliases and acronyms redirect to the canonical entry,",
            "so *MHA*, *Multi-Head Attention* and *multihead attention* all land in the",
            "same place. To learn a subject in order, use the",
            "[learning paths](../learn/index.md) instead.",
            "",
            jump,
            "",
        ]
        for letter in letters:
            lines += [f"## {letter}", ""]
            for name, slug, is_alias in sorted(buckets[letter], key=lambda x: x[0].lower()):
                entry = self.corpus.entries[slug]
                if is_alias:
                    lines.append(f"- **{name}** → see [{entry.term}](../terms/{slug}.md)")
                else:
                    lines.append(f"- [{name}](../terms/{slug}.md) — {entry.one_liner}")
            lines.append("")
        write(self.docs / "az" / "index.md", "\n".join(lines))

    # -- timeline -----------------------------------------------------
    def build_timeline(self) -> None:
        lines = [
            "# Timeline",
            "",
            "The field did not start in 2020. Most of what looks new is an old idea that",
            "finally got the hardware, the data or the name it needed.",
            "",
        ]
        by_period: dict[str, list[Entry]] = defaultdict(list)
        for entry in self.corpus.entries.values():
            if entry.meta.get("historical_period"):
                by_period[entry.meta["historical_period"]].append(entry)

        for era in self.corpus.timeline.get("eras", []):
            lines += [f"## {era['label']} {{ #{era['id']} }}", "", era["summary"], ""]
            events = era.get("events", [])
            if events:
                lines += ["| Year | What happened | Entry |", "|---|---|---|"]
                for event in events:
                    ref = (
                        f"[{self.corpus.entries[event['term']].term}](../terms/{event['term']}.md)"
                        if event.get("term") in self.corpus.entries
                        else "—"
                    )
                    lines.append(f"| {event['year']} | {event['what']} | {ref} |")
                lines.append("")
            members = sorted(by_period.get(era["id"], []), key=sort_key)
            if members:
                names = ", ".join(f"[{e.term}](../terms/{e.slug}.md)" for e in members)
                lines += [f"**Entries from this era:** {names}", ""]

        chains = self.graph.lineage_chains()
        if chains:
            lines += [
                "## Lineages",
                "",
                "Old concept → evolution → modern form, derived from the `evolved_into`",
                "and `predecessor_of` edges in the concept graph.",
                "",
            ]
            for chain in chains:
                lines.append("```text")
                for i, slug in enumerate(chain):
                    term = self.corpus.entries[slug].term
                    lines.append(term if i == 0 else "  ↓\n" + term)
                lines.append("```")
                lines.append("")
                lines.append(
                    "Read: "
                    + " → ".join(
                        f"[{self.corpus.entries[s].term}](../terms/{s}.md)" for s in chain
                    )
                )
                lines.append("")
        write(self.docs / "timeline" / "index.md", "\n".join(lines))

    # -- graph --------------------------------------------------------
    def build_graph_page(self) -> None:
        stats = self.graph.stats()
        rows = "\n".join(
            f"| `{k}` | {v} |" for k, v in stats["edges_by_type"].items()
        )
        hubs = "\n".join(
            f"| [{self.corpus.entries[h['slug']].term}](../terms/{h['slug']}.md) | {h['degree']} |"
            for h in stats["hubs"]
        )
        body = f"""# Concept graph

Definitions in isolation are trivia. The value is in the edges: what a concept
depends on, what replaced it, what it is confused with.

Drag to explore, click a node to open its entry, filter by domain. Relationships
are typed, and inverse edges are derived automatically -- a contributor states
`evolved_into` once and both entries show the link.

<div id="graph-app" data-src="../api/graph.json"></div>

## Relationship vocabulary

| Edge | Count |
|---|--:|
{rows}

## Most connected concepts

| Concept | Degree |
|---|--:|
{hubs}

## Query it yourself

The same graph is available as JSON at [`api/graph.json`](../api/graph.json),
and the CLI can answer "how are these two related?":

```console
$ enc path attention vllm
attention → kv-cache → paged-attention → vllm
```
"""
        write(self.docs / "graph" / "index.md", body)

    # -- comparisons --------------------------------------------------
    def build_comparisons(self) -> None:
        comps = sorted(self.corpus.comparisons, key=lambda c: c["title"])
        lines = [
            "# Compare",
            "",
            "Most confusion in this field is not about what a term means, it is about",
            "how it differs from the term next to it. These pages take the pairs people",
            "actually mix up.",
            "",
            "| Comparison | The question |",
            "|---|---|",
        ]
        for comp in comps:
            lines.append(f"| [{comp['title']}]({comp['id']}.md) | {comp.get('question', '')} |")
        write(self.docs / "compare" / "index.md", "\n".join(lines))

        for comp in comps:
            page = [f"# {comp['title']}", ""]
            if comp.get("question"):
                page += ["!!! question \"The question\"", "", f"    {comp['question']}", ""]
            sides = [self.corpus.entries[s] for s in comp["sides"]]
            page += ["| | " + " | ".join(e.term for e in sides) + " |"]
            page += ["|---" * (len(sides) + 1) + "|"]
            page += [
                "| **In one line** | "
                + " | ".join(e.one_liner for e in sides)
                + " |"
            ]
            page += [
                "| **Entry** | "
                + " | ".join(f"[{e.term}](../terms/{e.slug}.md)" for e in sides)
                + " |"
            ]
            page += ["", comp["body"], ""]
            write(self.docs / "compare" / f"{comp['id']}.md", "\n".join(page))

    # -- learning paths -----------------------------------------------
    def build_learning_paths(self) -> None:
        paths = self.corpus.paths.get("paths", [])
        lines = [
            "# Learning paths",
            "",
            "An encyclopedia answers questions you already know how to ask. A path tells",
            "you what to ask next. Each is an ordered walk through existing entries --",
            "no new content, just a route.",
            "",
        ]
        for p in paths:
            lines += [
                f"## [{p['name']}]({p['id']}.md)",
                "",
                f"**For:** {p['audience']}  ",
                f"**Effort:** {p.get('estimated_effort', 'self-paced')}  ",
                f"**Steps:** {len(p['steps'])}",
                "",
                p["summary"],
                "",
                "```text",
                "\n  ↓\n".join(
                    self.corpus.entries[s["term"]].term for s in p["steps"]
                ),
                "```",
                "",
            ]
        write(self.docs / "learn" / "index.md", "\n".join(lines))

        for p in paths:
            page = [
                f"# {p['name']}",
                "",
                f"**For:** {p['audience']}  ",
                f"**Effort:** {p.get('estimated_effort', 'self-paced')}",
                "",
                p["summary"],
                "",
            ]
            for i, step in enumerate(p["steps"], start=1):
                entry = self.corpus.entries[step["term"]]
                flag = " *(optional)*" if step.get("optional") else ""
                page += [
                    f"## {i}. [{entry.term}](../terms/{entry.slug}.md){flag}",
                    "",
                    f"{DIFFICULTY_BADGE[entry.difficulty]} · `{entry.status}`",
                    "",
                    f"> {entry.one_liner}",
                    "",
                ]
                if step.get("why"):
                    page += [f"**Why now:** {step['why']}", ""]
            write(self.docs / "learn" / f"{p['id']}.md", "\n".join(page))

    # -- system view --------------------------------------------------
    def build_system_view(self) -> None:
        def band(tag: str) -> str:
            items = sorted(
                (e for e in self.corpus.entries.values() if tag in e.tags), key=sort_key
            )
            return ", ".join(f"[{e.term}](terms/{e.slug}.md)" for e in items) or "—"

        body = f"""# System view

Where does any of this actually sit? A production AI system is a stack, and most
terms in this encyclopedia belong to exactly one layer of it. When you meet an
unfamiliar term, finding its layer is usually enough to guess what it does.

```text
┌──────────────────────────────────────────────────────────────┐
│  PRODUCT SURFACE        chat UI · IDE · coding agent · API   │
├──────────────────────────────────────────────────────────────┤
│  AGENT LAYER            harness · agent loop · planning ·    │
│                         tools · memory · sub-agents          │
├──────────────────────────────────────────────────────────────┤
│  PROTOCOL LAYER         function calling · MCP · A2A ·       │
│                         structured outputs · gateways        │
├──────────────────────────────────────────────────────────────┤
│  CONTEXT LAYER          prompts · retrieval · RAG · vector   │
│                         DBs · rerankers · context engineering│
├──────────────────────────────────────────────────────────────┤
│  MODEL LAYER            transformer · attention · MoE ·      │
│                         reasoning models · multimodal        │
├──────────────────────────────────────────────────────────────┤
│  ADAPTATION LAYER       pretraining · SFT · RLHF · DPO ·     │
│                         LoRA · distillation · scaling laws   │
├──────────────────────────────────────────────────────────────┤
│  SERVING LAYER          prefill/decode · KV cache ·          │
│                         PagedAttention · batching · vLLM     │
├──────────────────────────────────────────────────────────────┤
│  SYSTEMS LAYER          parallelism · NCCL · CUDA kernels ·  │
│                         schedulers · clusters                │
├──────────────────────────────────────────────────────────────┤
│  HARDWARE LAYER         GPU · NPU · memory hierarchy ·       │
│                         interconnect                         │
└──────────────────────────────────────────────────────────────┘
   Cutting across every layer: evaluation, safety, observability,
   interpretability, cost.
```

## Layers, with the entries that live there

**Hardware and systems** — {band('hardware')}

**Model** — {band('architecture')}

**Adaptation** — {band('training')}

**Serving and inference** — {band('inference')}

**Context and retrieval** — {band('retrieval')}

**Protocol** — {band('protocol')}

**Agent** — {band('agents')}

**Cross-cutting: evaluation and safety** — {band('safety')}

**Cross-cutting: culture and practice** — {band('culture')}

## A request, traced through the stack

```text
user types a question
   │
   ├─▶ harness assembles context   ── context engineering, RAG, prompt
   │
   ├─▶ request hits the server     ── scheduler, continuous batching
   │
   ├─▶ prefill                     ── whole prompt, one pass, compute-bound
   │      └─ writes the KV cache   ── PagedAttention blocks
   │
   ├─▶ decode, token by token      ── memory-bandwidth-bound, sampling
   │
   ├─▶ model emits a tool call     ── function calling, MCP, structured output
   │      └─ harness runs the tool, appends result, loops
   │
   └─▶ answer returned             ── TTFT and TPOT measured, traced, evaluated
```

Every named step above is an entry. Follow the one you do not recognise.
"""
        write(self.docs / "system-view.md", body)

    # -- meta ---------------------------------------------------------
    def build_meta(self) -> None:
        by_status: dict[str, list[Entry]] = defaultdict(list)
        by_diff: dict[str, list[Entry]] = defaultdict(list)
        for entry in self.corpus.entries.values():
            by_status[entry.status].append(entry)
            by_diff[entry.difficulty].append(entry)

        by_cat = self.corpus.by_category()
        counts = {c: len(v) for c, v in by_cat.items()}
        full_counts = {
            c: len([e for e in v if not e.is_seed]) for c, v in by_cat.items()
        }
        cat_rows = "\n".join(
            f"| `{c['number']}` | [{c['name']}](../topics/{c['id']}.md) | "
            f"{full_counts.get(c['id'], 0)} | {counts.get(c['id'], 0) - full_counts.get(c['id'], 0)} | "
            f"{counts.get(c['id'], 0)} |"
            for c in self.corpus.taxonomy.get("categories", [])
        )
        seeds = [e for e in self.corpus.entries.values() if e.is_seed]
        status_rows = "\n".join(
            f"| `{s}` | {len(by_status.get(s, []))} | {STATUS_NOTE[s]} |"
            for s in STATUS_ORDER
            if by_status.get(s)
        )
        stale = sorted(
            (e for e in self.corpus.entries.values() if e.meta.get("review_by")),
            key=lambda e: str(e.meta["review_by"]),
        )
        stale_rows = (
            "\n".join(
                f"| [{e.term}](../terms/{e.slug}.md) | {e.meta['updated']} | {e.meta['review_by']} |"
                for e in stale
            )
            or "| — | — | — |"
        )
        orphan = self.graph.stats()["orphans"]

        write(
            self.docs / "meta" / "coverage.md",
            f"""# Coverage

Generated on every build. This page is the honest account of what the
encyclopedia does and does not cover yet.

**{len(self.corpus.entries)} entries · {len(self.graph.edges)} declared relationships ·
{len(self.corpus.comparisons)} comparisons · {len(self.corpus.paths.get('paths', []))} learning paths**

## By domain

| # | Domain | Full | Seed | Total |
|---|---|--:|--:|--:|
{cat_rows}

**{len(self.corpus.entries) - len(seeds)} full entries · {len(seeds)} seed entries.**
A *seed* is a lookup record — canonical name, aliases, one-line definition and
its place in the concept graph — awaiting the full treatment. Seeds are listed
by `enc todo`, and expanding one is the most useful contribution available.

## By status

| Status | Entries | Meaning |
|---|--:|---|
{status_rows}

## By level

| Level | Entries |
|---|--:|
{chr(10).join(f'| {DIFFICULTY_BADGE[d]} | {len(by_diff.get(d, []))} |' for d in DIFFICULTY_BADGE)}

## Review schedule

Fast-moving terminology carries a re-review date. Anything past it is flagged by
`enc validate`.

| Entry | Last reviewed | Review by |
|---|---|---|
{stale_rows}

## Disconnected entries

{("`" + "`, `".join(orphan) + "`") if orphan else "None. Every entry is reachable through the concept graph."}
""",
        )

        write(
            self.docs / "meta" / "standards.md",
            """# Editorial standards

## One canonical entry per concept

A concept is written once. Categories, the A-Z index, learning paths, the
timeline and the graph are *views* over that single record. If a term seems to
belong in two domains, pick the one where it was born and add relations for the
rest.

## Say what is uncertain

A large part of current AI vocabulary has no agreed definition. Where teams
disagree, the entry carries `status: contested` or `disputed: true` and a
**Terminology Note** that reports the competing usages, with dates and sources.
Inventing a clean definition for a messy term is the failure mode this
encyclopedia exists to avoid.

## Slang is documented, not smuggled

Terms like *vibe coding*, *AI slop* and *superworker* shape how engineers talk
and hire, so they get entries. They are labelled `slang`, `informal` or
`marketing`, and the entry says plainly which parts are technical claims and
which are vibes.

## New terminology is triaged, not hoarded

Before a new term earns an entry, it must survive seven questions:

1. Is it genuinely new, or an old idea renamed?
2. Does it name something a practitioner must be able to talk about?
3. Is it used outside the organisation that coined it?
4. Does it have a stable enough meaning to define?
5. Do different communities use it incompatibly? (Then say so.)
6. Is it marketing, slang, or technical vocabulary?
7. Will someone plausibly meet it in a paper, repo, job ad or interview?

A term that fails 2 and 3 is a buzzword. It gets a line in
[the watchlist](watchlist.md), not an entry.

## Sources, in order of preference

1. Original research papers
2. Official specifications and standards
3. Official documentation
4. Official repositories
5. Technical reports from the organisation that built the thing
6. High-quality secondary explanations
7. Community discussion — acceptable *only* for emerging terminology, and
   labelled as such

## Dates on everything

Every entry records `updated`. Fast-moving entries also carry `review_by`.
An unreviewed entry about a two-year-old term is a liability.

## Prose rules

* The one-line definition must be understandable by someone who has never
  worked in AI. No jargon, no nested clauses.
* The simple explanation assumes basic computing knowledge and nothing more.
* The technical definition must be precise enough for a practitioner.
* Explain every symbol in every formula.
* Prefer an ASCII diagram over a paragraph describing a diagram.
* Comparisons state what each option optimises for, not which is "better".
""",
        )

        write(
            self.docs / "meta" / "watchlist.md",
            """# Watchlist

Terms under observation that have **not** earned an entry yet. Each is recorded
with the date it was first noticed and the reason it is being held back. This
list exists so that the encyclopedia can be current without becoming a buzzword
dump.

| Term | First noticed | Why it is waiting |
|---|---|---|
| Agentic commerce | 2025-06 | Mostly vendor positioning; no stable technical referent yet. |
| Context rot | 2025-07 | Real phenomenon (long-context degradation), competing names. Watch whether this label wins. |
| Agent mesh | 2025-09 | Marketing overlay on multi-agent systems and service meshes. |
| Neurosymbolic revival | 2025-10 | Genuine research direction; the *label* is old, the current usage is not yet settled. |
| Model welfare | 2025-11 | Discussed seriously by labs; definition still forming. |
| Continuous learning agent | 2026-01 | Overlaps continual learning, online learning, agent memory. Needs disambiguation before an entry. |
| World model agent | 2026-03 | Two incompatible usages (predictive-model-based control vs. LLM with a scene graph). |

## Promotion criteria

A watchlist term becomes an entry when it is used by at least two independent
organisations *and* either has a primary source defining it or has a usage
stable enough to describe honestly. Terms that fade are deleted from this list
with a note in the changelog.
""",
        )

    # -- api ----------------------------------------------------------
    def build_api(self) -> None:
        entries = [e.as_dict() for e in sorted(self.corpus.entries.values(), key=lambda x: x.slug)]
        for record in entries:
            record["derived_relations"] = self.graph.neighbours(record["slug"])

        payloads = {
            "entries.json": {"count": len(entries), "entries": entries},
            "graph.json": self.graph.export(),
            "taxonomy.json": self.corpus.taxonomy,
            "learning-paths.json": self.corpus.paths,
            "timeline.json": self.corpus.timeline,
            "comparisons.json": {
                "comparisons": [
                    {k: v for k, v in c.items() if k != "path"} for c in self.corpus.comparisons
                ]
            },
            "search-index.json": {
                "documents": [
                    {
                        "slug": e.slug,
                        "term": e.term,
                        "aliases": e.aliases,
                        "one_liner": e.one_liner,
                        "category": e.category,
                        "status": e.status,
                        "difficulty": e.difficulty,
                        "tags": e.tags,
                        "url": e.url,
                        "text": " ".join(e.sections.values()),
                    }
                    for e in sorted(self.corpus.entries.values(), key=lambda x: x.slug)
                ]
            },
            "aliases.json": self.corpus.alias_map(),
            "stats.json": self.graph.stats(),
        }
        for name, data in payloads.items():
            write(self.api / name, json.dumps(data, indent=2, ensure_ascii=False, default=str))

        write(
            self.api / "index.md",
            f"""# JSON API

The site is one consumer of the data, not the data itself. Every view is
generated from these files, and so can yours -- an editor plugin, a RAG corpus,
a printed book, a Slack bot.

Built {date.today().isoformat()} · schema version 1.

| File | Contents |
|---|---|
| [`entries.json`](entries.json) | Every entry: metadata, prose sections, declared and derived relations. |
| [`graph.json`](graph.json) | Nodes and typed edges for the concept graph. |
| [`search-index.json`](search-index.json) | Flattened text for your own search. |
| [`aliases.json`](aliases.json) | Every alias and acronym mapped to its canonical slug. |
| [`taxonomy.json`](taxonomy.json) | Domains and subcategories. |
| [`learning-paths.json`](learning-paths.json) | Ordered paths over entries. |
| [`timeline.json`](timeline.json) | Eras and dated events. |
| [`comparisons.json`](comparisons.json) | Side-by-side pages. |
| [`stats.json`](stats.json) | Counts, hubs, orphans. |

```python
import json, urllib.request

url = "{self.site_url or 'https://Iamhifza.github.io/encyclopedia'}/api/entries.json"
data = json.load(urllib.request.urlopen(url))
kv = next(e for e in data["entries"] if e["slug"] == "kv-cache")
print(kv["one_liner"])
print(kv["derived_relations"])
```

Stability: the field names in `entries.json` follow `schema/entry.schema.json`.
Additive changes are minor releases; removals are major. See the
[changelog](../changelog.md).
""",
        )

    # -- mkdocs config -------------------------------------------------
    def write_mkdocs_config(self) -> None:
        base = yaml.safe_load((ROOT / "mkdocs.yml").read_text(encoding="utf-8"))
        cats = self.corpus.taxonomy.get("categories", [])
        by_cat = self.corpus.by_category()

        topics_nav: list[Any] = [{"All domains": "topics/index.md"}]
        for cat in cats:
            children: list[Any] = [{"Overview": f"topics/{cat['id']}.md"}]
            for entry in sorted(by_cat.get(cat["id"], []), key=sort_key):
                children.append({entry.term: f"terms/{entry.slug}.md"})
            topics_nav.append({f"{cat['number']}. {cat['name']}": children})

        compare_nav: list[Any] = [{"All comparisons": "compare/index.md"}]
        for comp in sorted(self.corpus.comparisons, key=lambda c: c["title"]):
            compare_nav.append({comp["title"]: f"compare/{comp['id']}.md"})

        learn_nav: list[Any] = [{"All paths": "learn/index.md"}]
        for p in self.corpus.paths.get("paths", []):
            learn_nav.append({p["name"]: f"learn/{p['id']}.md"})

        base["nav"] = [
            {"Home": "index.md"},
            {"Topics": topics_nav},
            {"A-Z": "az/index.md"},
            {"Timeline": "timeline/index.md"},
            {"Concept graph": "graph/index.md"},
            {"Compare": compare_nav},
            {"Learn": learn_nav},
            {"System view": "system-view.md"},
            {
                "Project": [
                    {"Editorial standards": "meta/standards.md"},
                    {"Coverage": "meta/coverage.md"},
                    {"Watchlist": "meta/watchlist.md"},
                    {"JSON API": "api/index.md"},
                    {"Contributing": "contributing.md"},
                    {"Code of conduct": "code-of-conduct.md"},
                    {"Changelog": "changelog.md"},
                    {"All entries": "terms/index.md"},
                ]
            },
        ]
        base["docs_dir"] = "docs"
        if self.site_url:
            base["site_url"] = self.site_url
        write(
            self.out_dir / "mkdocs.yml",
            "# Generated by `enc build`. Edit ../mkdocs.yml instead.\n"
            + yaml.safe_dump(base, sort_keys=False, allow_unicode=True),
        )


def build(corpus: Corpus, out_dir: Path, site_url: str = "") -> dict[str, Any]:
    return Builder(corpus, out_dir, site_url).run()

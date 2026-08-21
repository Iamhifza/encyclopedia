"""``enc`` -- the command line for the encyclopedia.

    enc validate [--strict]      check the corpus
    enc build [--serve]          generate build/docs and build/api
    enc new "Speculative Decoding" --category llm-inference
    enc batch --limit 20         create seed entries from the backlog queue
    enc todo                     which seeds most deserve the full treatment
    enc promote "Beam Search"    turn a seed into a full entry
    enc path attention vllm      how are two concepts connected?
    enc stats                    corpus and graph statistics
    enc lint-links               check external links resolve (needs network)
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

from .build import build as build_site
from .graph import ConceptGraph
from .loader import ContentError, load_corpus
from .model import STATUS_ORDER
from .validate import validate as validate_corpus

ROOT = Path(__file__).resolve().parents[2]
CONTENT = ROOT / "content"
BUILD = ROOT / "build"

GREEN, RED, YELLOW, DIM, RESET = "\033[32m", "\033[31m", "\033[33m", "\033[2m", "\033[0m"


def slugify(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return re.sub(r"-{2,}", "-", slug)


def _load():
    try:
        return load_corpus(CONTENT)
    except ContentError as exc:
        print(f"{RED}content error{RESET}: {exc}", file=sys.stderr)
        raise SystemExit(2) from exc


def cmd_validate(args) -> int:
    corpus = _load()
    report = validate_corpus(corpus)
    for issue in report.issues:
        colour = RED if issue.severity == "error" else YELLOW
        print(f"{colour}{issue}{RESET}")
    ok = report.ok(strict=args.strict)
    summary = (
        f"{len(corpus.entries)} entries · "
        f"{len(report.errors)} errors · {len(report.warnings)} warnings"
    )
    print(f"\n{GREEN if ok else RED}{'PASS' if ok else 'FAIL'}{RESET}  {summary}")
    if args.strict and report.warnings and not report.errors:
        print(f"{DIM}(strict mode: warnings are fatal){RESET}")
    return 0 if ok else 1


def cmd_build(args) -> int:
    corpus = _load()
    report = validate_corpus(corpus)
    if report.errors:
        for issue in report.errors:
            print(f"{RED}{issue}{RESET}")
        print(f"\n{RED}FAIL{RESET}  refusing to build with errors")
        return 1

    stats = build_site(corpus, BUILD, site_url=args.site_url or "")
    print(f"{GREEN}built{RESET}  {BUILD / 'docs'}")
    print(
        f"       {stats['entries']} entries · {stats['declared_edges']} edges · "
        f"{len(report.warnings)} warnings"
    )
    if args.serve or args.site:
        cmd = ["mkdocs", "serve" if args.serve else "build", "-f", str(BUILD / "mkdocs.yml")]
        if args.site:
            cmd += ["-d", str(ROOT / "site")]
        try:
            return subprocess.call(cmd)
        except FileNotFoundError:
            print(
                f"{YELLOW}mkdocs not installed{RESET}: pip install -r requirements.txt",
                file=sys.stderr,
            )
            return 1
    return 0


TEMPLATE = """---
term: {term}
aliases: []
category: {category}
status: emerging
difficulty: intermediate
one_liner: TODO one plain sentence a non-specialist could read aloud.
origin:
  year: {year}
  circa: true
  attribution: TODO who introduced it
historical_period: agentic
prerequisites: []
relations:
  related_to: []
tags: []
encountered_in: []
sources: []
updated: {today}
---

## Simple Explanation

TODO. Assume basic computing knowledge and nothing else.

## Technical Definition

TODO. Precise enough for a practitioner to act on.

## Why Does It Exist?

TODO. What was painful before this existed?

## What Problem Does It Solve?

TODO.

## How Does It Work?

TODO. Step by step.

## Mental Model

TODO. One analogy that survives contact with the details.

## Example

TODO. Concrete, with numbers or code.

## Real-World Usage

TODO. Named systems, not hand-waving.

## Common Confusions

TODO.

## Why Should I Care?

TODO.
"""


def cmd_new(args) -> int:
    slug = args.slug or slugify(args.term)
    path = CONTENT / "entries" / f"{slug}.md"
    if path.exists():
        print(f"{RED}exists{RESET}: {path}", file=sys.stderr)
        return 1
    path.write_text(
        TEMPLATE.format(
            term=args.term,
            category=args.category,
            today=date.today().isoformat(),
            year=date.today().year,
        ),
        encoding="utf-8",
    )
    print(f"{GREEN}created{RESET} {path.relative_to(ROOT)}")
    print(f"{DIM}next: fill the TODOs, then `enc validate`{RESET}")
    return 0


SEED_TEMPLATE = """---
term: {term}
{aliases}category: {category}
{subcategory}depth: seed
status: {status}
difficulty: {difficulty}
one_liner: {one_liner}
{tags}{relations}sources: []
updated: {today}
---
"""


def _yaml_block(key: str, value, indent: str = "") -> str:
    if not value:
        return ""
    if isinstance(value, list):
        return f"{key}: [{', '.join(value)}]\n"
    if isinstance(value, dict):
        lines = [f"{key}:"]
        for rel, targets in value.items():
            lines.append(f"  {rel}: [{', '.join(targets)}]")
        return "\n".join(lines) + "\n"
    return f"{key}: {value}\n"


def cmd_batch(args) -> int:
    """Create seed entries in bulk from the backlog queue."""
    import yaml

    backlog_path = Path(args.backlog)
    if not backlog_path.exists():
        print(f"{RED}no backlog{RESET}: {backlog_path}", file=sys.stderr)
        return 1

    backlog = yaml.safe_load(backlog_path.read_text(encoding="utf-8")) or {}
    queue = backlog.get("terms", [])
    existing = {p.stem for p in (CONTENT / "entries").glob("*.md")}

    if args.category:
        queue = [item for item in queue if item.get("category") == args.category]

    created, skipped = [], []
    for item in queue:
        slug = item.get("slug") or slugify(item["term"])
        if slug in existing:
            skipped.append(slug)
            continue
        if args.limit and len(created) >= args.limit:
            break

        text = SEED_TEMPLATE.format(
            term=item["term"],
            aliases=_yaml_block("aliases", item.get("aliases")),
            category=item["category"],
            subcategory=_yaml_block("subcategory", item.get("subcategory")),
            status=item.get("status", "established"),
            difficulty=item.get("difficulty", "intermediate"),
            one_liner=json.dumps(item["one_liner"], ensure_ascii=False),
            tags=_yaml_block("tags", item.get("tags")),
            relations=_yaml_block("relations", item.get("relations")),
            today=date.today().isoformat(),
        )
        target = CONTENT / "entries" / f"{slug}.md"
        if args.dry_run:
            print(f"{DIM}would create{RESET} {slug}")
        else:
            target.write_text(text, encoding="utf-8")
        created.append(slug)

    verb = "would create" if args.dry_run else "created"
    print(f"{GREEN}{verb}{RESET} {len(created)} seed entries · {len(skipped)} already existed")
    if created and not args.dry_run:
        print(f"{DIM}next: `enc validate`, then `enc todo` to see what to expand{RESET}")
    return 0


def cmd_todo(args) -> int:
    """List seed entries awaiting the full treatment, most connected first."""
    corpus = _load()
    graph = ConceptGraph(corpus)
    seeds = [e for e in corpus.entries.values() if e.is_seed]
    if args.category:
        seeds = [e for e in seeds if e.category == args.category]
    seeds.sort(key=lambda e: (-graph.degree(e.slug), e.term))

    if not seeds:
        print(f"{GREEN}no seed entries{RESET} — every entry has the full treatment")
        return 0

    total = len(corpus.entries)
    print(f"{len(seeds)} seed entries of {total} ({100 * len(seeds) // total}%)\n")
    print(f"{DIM}ranked by graph degree: the most connected are the most worth writing{RESET}\n")
    for entry in seeds[: args.limit]:
        print(f"  {graph.degree(entry.slug):>3}  {entry.term:<34} {entry.category}")
    if len(seeds) > args.limit:
        print(f"\n{DIM}...and {len(seeds) - args.limit} more{RESET}")
    return 0


def cmd_promote(args) -> int:
    """Turn a seed entry into a full one by appending the section skeleton."""
    corpus = _load()
    aliases = corpus.alias_map()
    slug = aliases.get(args.term.lower(), slugify(args.term))
    entry = corpus.entries.get(slug)
    if entry is None:
        print(f"{RED}no such entry{RESET}: {args.term}", file=sys.stderr)
        return 1
    if not entry.is_seed:
        print(f"{YELLOW}already a full entry{RESET}: {slug}")
        return 0

    path = CONTENT / "entries" / f"{slug}.md"
    text = path.read_text(encoding="utf-8")
    text = text.replace("depth: seed\n", "depth: full\n")
    body = TEMPLATE.split("---\n", 2)[2]
    path.write_text(text.rstrip() + "\n" + body, encoding="utf-8")
    print(f"{GREEN}promoted{RESET} {slug} to a full entry")
    print(f"{DIM}fill the TODOs in content/entries/{slug}.md, then `enc validate --strict`{RESET}")
    return 0


def cmd_path(args) -> int:
    corpus = _load()
    graph = ConceptGraph(corpus)
    aliases = corpus.alias_map()
    start = aliases.get(args.start.lower(), args.start)
    goal = aliases.get(args.goal.lower(), args.goal)
    trail = graph.shortest_path(start, goal)
    if not trail:
        print(f"{YELLOW}no path{RESET} between '{args.start}' and '{args.goal}'")
        return 1
    print(" → ".join(corpus.entries[s].term for s in trail))
    for a, b in zip(trail, trail[1:], strict=False):
        for key, targets in graph.neighbours(a).items():
            if b in targets:
                print(f"{DIM}  {corpus.entries[a].term} --{key}--> {corpus.entries[b].term}{RESET}")
                break
    return 0


def cmd_stats(args) -> int:
    corpus = _load()
    graph = ConceptGraph(corpus)
    stats = graph.stats()
    if args.json:
        print(json.dumps(stats, indent=2))
        return 0
    print(f"entries        {stats['entries']}")
    print(f"declared edges {stats['declared_edges']}")
    print(f"comparisons    {len(corpus.comparisons)}")
    print(f"paths          {len(corpus.paths.get('paths', []))}")
    print("\nby status")
    counts = {s: 0 for s in STATUS_ORDER}
    for entry in corpus.entries.values():
        counts[entry.status] += 1
    for status, n in counts.items():
        if n:
            print(f"  {status:<14} {n}")
    print("\nedges by type")
    for key, n in stats["edges_by_type"].items():
        print(f"  {key:<16} {n}")
    print("\nmost connected")
    for hub in stats["hubs"][:5]:
        print(f"  {corpus.entries[hub['slug']].term:<28} {hub['degree']}")
    if stats["orphans"]:
        print(f"\n{YELLOW}orphans{RESET}: {', '.join(stats['orphans'])}")
    return 0


def cmd_lint_links(args) -> int:
    import urllib.error
    import urllib.request

    corpus = _load()
    seen: dict[str, int] = {}
    bad = 0
    for entry in corpus.entries.values():
        for src in entry.sources:
            url = src["url"]
            if url in seen:
                continue
            request = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "enc-linkcheck"})
            try:
                with urllib.request.urlopen(request, timeout=15) as response:
                    seen[url] = response.status
            except urllib.error.HTTPError as exc:
                seen[url] = exc.code
            except Exception:  # noqa: BLE001 - network flakiness is not a content bug
                seen[url] = 0
            if seen[url] >= 400 or seen[url] == 0:
                bad += 1
                print(f"{YELLOW}{seen[url] or 'unreachable'}{RESET}  {entry.slug}: {url}")
    print(f"\nchecked {len(seen)} urls · {bad} suspicious")
    return 1 if bad and args.strict else 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="enc", description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("validate", help="check the corpus")
    p.add_argument("--strict", action="store_true", help="treat warnings as errors")
    p.set_defaults(func=cmd_validate)

    p = sub.add_parser("build", help="generate build/docs and build/api")
    p.add_argument("--serve", action="store_true", help="serve with mkdocs after building")
    p.add_argument("--site", action="store_true", help="render static HTML into site/")
    p.add_argument("--site-url", default="", help="canonical URL for the published site")
    p.set_defaults(func=cmd_build)

    p = sub.add_parser("new", help="scaffold a new entry")
    p.add_argument("term")
    p.add_argument("--category", required=True)
    p.add_argument("--slug")
    p.set_defaults(func=cmd_new)

    p = sub.add_parser("batch", help="create seed entries in bulk from the backlog")
    p.add_argument("backlog", nargs="?", default=str(CONTENT / "backlog.yaml"))
    p.add_argument("--category", help="only terms in this domain")
    p.add_argument("--limit", type=int, default=0, help="stop after N new entries")
    p.add_argument("--dry-run", action="store_true")
    p.set_defaults(func=cmd_batch)

    p = sub.add_parser("todo", help="seed entries awaiting the full treatment")
    p.add_argument("--category")
    p.add_argument("--limit", type=int, default=25)
    p.set_defaults(func=cmd_todo)

    p = sub.add_parser("promote", help="turn a seed entry into a full one")
    p.add_argument("term")
    p.set_defaults(func=cmd_promote)

    p = sub.add_parser("path", help="shortest path between two concepts")
    p.add_argument("start")
    p.add_argument("goal")
    p.set_defaults(func=cmd_path)

    p = sub.add_parser("stats", help="corpus statistics")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_stats)

    p = sub.add_parser("lint-links", help="check source URLs resolve")
    p.add_argument("--strict", action="store_true")
    p.set_defaults(func=cmd_lint_links)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())

"""Validate the corpus.

Two severities:

* **error**   -- the build is wrong and CI fails.
* **warning** -- the entry is publishable but incomplete. ``--strict`` promotes
  warnings to errors; the repository runs strict mode on ``main``.
"""

from __future__ import annotations

import json
from collections.abc import Iterable
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from .model import (
    ALL_KNOWN_SECTIONS,
    GENERATED_SECTIONS,
    RECOMMENDED_SECTIONS,
    RELATIONS,
    REQUIRED_SECTIONS,
    Corpus,
)

SCHEMA_DIR = Path(__file__).resolve().parents[2] / "schema"


@dataclass
class Issue:
    severity: str      # "error" | "warning"
    where: str
    message: str

    def __str__(self) -> str:
        mark = "ERROR" if self.severity == "error" else "warn "
        return f"{mark}  {self.where}: {self.message}"


class Report:
    def __init__(self) -> None:
        self.issues: list[Issue] = []

    def error(self, where: str, message: str) -> None:
        self.issues.append(Issue("error", where, message))

    def warn(self, where: str, message: str) -> None:
        self.issues.append(Issue("warning", where, message))

    @property
    def errors(self) -> list[Issue]:
        return [i for i in self.issues if i.severity == "error"]

    @property
    def warnings(self) -> list[Issue]:
        return [i for i in self.issues if i.severity == "warning"]

    def ok(self, strict: bool = False) -> bool:
        return not self.errors and (not strict or not self.warnings)


def _load_schema(name: str) -> dict[str, Any]:
    return json.loads((SCHEMA_DIR / name).read_text(encoding="utf-8"))


def _subschema(collections: dict[str, Any], key: str) -> dict[str, Any]:
    schema = dict(collections["$defs"][key])
    schema["$defs"] = collections["$defs"]
    return schema


def _detect_cycle(graph: dict[str, Iterable[str]]) -> list[str] | None:
    """Return one cycle as a node list, or None."""
    WHITE, GREY, BLACK = 0, 1, 2
    colour = {node: WHITE for node in graph}
    stack: list[str] = []

    def visit(node: str) -> list[str] | None:
        colour[node] = GREY
        stack.append(node)
        for nxt in graph.get(node, []):
            if nxt not in colour:
                continue
            if colour[nxt] == GREY:
                return stack[stack.index(nxt):] + [nxt]
            if colour[nxt] == WHITE:
                found = visit(nxt)
                if found:
                    return found
        stack.pop()
        colour[node] = BLACK
        return None

    for node in list(graph):
        if colour[node] == WHITE:
            found = visit(node)
            if found:
                return found
    return None


def _check_body(entry, report: Report, where: str) -> None:
    """Prose contract, applied to full entries only."""
    for heading in REQUIRED_SECTIONS:
        if not entry.sections.get(heading):
            report.error(where, f"missing required section '## {heading}'")
    for heading in RECOMMENDED_SECTIONS:
        if not entry.sections.get(heading):
            report.warn(where, f"missing recommended section '## {heading}'")
    for heading in entry.section_order:
        if heading in GENERATED_SECTIONS:
            report.error(
                where,
                f"'## {heading}' is generated from front matter; remove it from the body",
            )
        elif heading not in ALL_KNOWN_SECTIONS:
            report.warn(where, f"non-standard section '## {heading}'")


def validate(corpus: Corpus, today: date | None = None) -> Report:
    report = Report()
    today = today or date.today()

    entry_schema = _load_schema("entry.schema.json")
    collections = _load_schema("collections.schema.json")
    entry_validator = Draft202012Validator(entry_schema)

    known_categories: dict[str, set[str]] = {}
    for cat in corpus.taxonomy.get("categories", []):
        known_categories[cat["id"]] = {
            sub["id"] for sub in cat.get("subcategories", [])
        }

    # -- collections ----------------------------------------------------
    for name, key, data in [
        ("taxonomy.yaml", "taxonomy", corpus.taxonomy),
        ("learning-paths.yaml", "learningPaths", corpus.paths),
        ("timeline.yaml", "timeline", corpus.timeline),
    ]:
        if not data:
            report.error(name, "file is missing or empty")
            continue
        validator = Draft202012Validator(_subschema(collections, key))
        for err in sorted(validator.iter_errors(data), key=lambda e: list(e.path)):
            location = "/".join(str(p) for p in err.path) or "(root)"
            report.error(name, f"{location}: {err.message}")

    # -- entries --------------------------------------------------------
    slugs = set(corpus.entries)
    alias_owner: dict[str, str] = {}

    for slug, entry in sorted(corpus.entries.items()):
        where = f"entries/{slug}.md"

        if slug != slug.lower() or not slug.replace("-", "").isalnum():
            report.error(where, "filename must be a lowercase, hyphenated slug")

        for err in sorted(entry_validator.iter_errors(entry.meta), key=lambda e: list(e.path)):
            location = "/".join(str(p) for p in err.path) or "(front matter)"
            report.error(where, f"{location}: {err.message}")

        if "term" not in entry.meta or "category" not in entry.meta:
            continue  # schema already complained; skip semantic checks

        # taxonomy membership
        if known_categories and entry.category not in known_categories:
            report.error(where, f"unknown category '{entry.category}' (not in taxonomy.yaml)")
        elif entry.subcategory and entry.subcategory not in known_categories.get(entry.category, set()):
            report.error(
                where,
                f"unknown subcategory '{entry.subcategory}' under '{entry.category}'",
            )

        # alias hygiene
        for name in [entry.term, *entry.aliases]:
            key = name.lower()
            owner = alias_owner.get(key)
            if owner and owner != slug:
                report.error(where, f"name '{name}' already claimed by '{owner}'")
            alias_owner[key] = slug

        # relations point somewhere real
        for rel_key, targets in entry.relations.items():
            if rel_key not in RELATIONS:
                report.error(where, f"unknown relation type '{rel_key}'")
                continue
            for target in targets:
                if target == slug:
                    report.error(where, f"relation '{rel_key}' points at itself")
                elif target not in slugs:
                    report.error(where, f"relation '{rel_key}' points at missing entry '{target}'")
                # Inverse edges, including the symmetric ones, are derived by
                # graph.py at build time. A relation is therefore declared once,
                # from whichever side reads more naturally.

        for prereq in entry.prerequisites:
            if prereq not in slugs:
                report.error(where, f"prerequisite '{prereq}' does not exist")
            elif prereq == slug:
                report.error(where, "entry lists itself as a prerequisite")

        # body contract -- seeds are lookup records and carry no prose
        if entry.is_seed:
            if entry.sections:
                report.warn(
                    where,
                    "seed entry has prose sections; set 'depth: full' and "
                    "complete the contract, or move the prose out",
                )
        else:
            _check_body(entry, report, where)

        # editorial checks
        one_liner = entry.one_liner
        if one_liner and not one_liner.rstrip().endswith((".", "!", "?")):
            report.warn(where, "one_liner should be a complete sentence")
        if one_liner.lower().startswith(entry.term.lower() + " is a "):
            report.warn(where, "one_liner restates the term; lead with the idea instead")

        if not entry.sources and not entry.is_seed:
            report.warn(where, "no sources; entries should cite at least one primary source")
        if entry.status in {"emerging", "contested", "slang", "informal", "marketing"} and not entry.is_seed:
            if not entry.meta.get("origin"):
                report.warn(where, f"status '{entry.status}' needs an 'origin' with a date")
            if not any(
                h in entry.sections for h in ("Terminology Note", "Common Confusions", "Differences")
            ):
                report.warn(
                    where,
                    f"status '{entry.status}' needs a 'Terminology Note' explaining the "
                    "disagreement rather than asserting one definition",
                )
        if entry.meta.get("disputed") and not entry.is_seed and "Terminology Note" not in entry.sections:
            report.error(where, "disputed entries must include '## Terminology Note'")

        review_by = entry.meta.get("review_by")
        if review_by and str(review_by) < today.isoformat():
            report.warn(where, f"review overdue (review_by {review_by})")

        # connectivity
        inbound = any(
            slug in targets
            for other in corpus.entries.values()
            if other.slug != slug
            for targets in list(other.relations.values()) + [other.prerequisites]
        )
        if not entry.relations and not inbound:
            report.warn(where, "orphan: no relations in or out, so the graph cannot reach it")

    # -- cycles ---------------------------------------------------------
    prereq_graph = {s: e.prerequisites for s, e in corpus.entries.items()}
    cycle = _detect_cycle(prereq_graph)
    if cycle:
        report.error("prerequisites", "cycle: " + " -> ".join(cycle))

    hierarchy = {
        s: [t for k in ("is_a", "part_of") for t in e.relations.get(k, [])]
        for s, e in corpus.entries.items()
    }
    cycle = _detect_cycle(hierarchy)
    if cycle:
        report.error("relations", "is_a/part_of cycle: " + " -> ".join(cycle))

    # -- learning paths -------------------------------------------------
    for path in corpus.paths.get("paths", []):
        where = f"learning-paths.yaml:{path.get('id', '?')}"
        seen: set[str] = set()
        for step in path.get("steps", []):
            term = step.get("term")
            if term not in slugs:
                report.error(where, f"step '{term}' is not an entry")
                continue
            if term in seen:
                report.warn(where, f"step '{term}' appears twice")
            seen.add(term)
            for prereq in corpus.entries[term].prerequisites:
                if prereq in {s.get("term") for s in path["steps"]} and prereq not in seen:
                    report.warn(
                        where,
                        f"'{term}' comes before its prerequisite '{prereq}'",
                    )

    # -- timeline -------------------------------------------------------
    for era in corpus.timeline.get("eras", []):
        for event in era.get("events", []):
            term = event.get("term")
            if term and term not in slugs:
                report.error(f"timeline.yaml:{era['id']}", f"event links missing entry '{term}'")

    # -- comparisons ----------------------------------------------------
    for comp in corpus.comparisons:
        where = f"comparisons/{comp['id']}.md"
        sides = comp.get("sides") or []
        if len(sides) < 2:
            report.error(where, "a comparison needs at least two 'sides'")
        for side in sides:
            if side not in slugs:
                report.error(where, f"side '{side}' is not an entry")
        if not comp.get("question"):
            report.warn(where, "missing 'question' front-matter field")
        if "## Verdict" not in comp.get("body", ""):
            report.warn(where, "comparisons should end with a '## Verdict' section")

    return report

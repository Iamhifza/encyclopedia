"""Domain model for the encyclopedia.

Everything downstream -- validation, the site, the graph, the JSON API -- reads
its vocabulary from this module. Adding a relation type or a status means
editing here and in ``schema/entry.schema.json``, nowhere else.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

# --------------------------------------------------------------------------
# Relation vocabulary
# --------------------------------------------------------------------------
# Each relation declares a human label and its inverse. Inverse edges are
# derived at build time, so a contributor only ever states a relation from one
# side. `symmetric` relations must be declared on both entries and the
# validator will say so.

@dataclass(frozen=True)
class Relation:
    key: str
    label: str            # how it reads on the source entry
    inverse_key: str      # relation key materialised on the target entry
    inverse_label: str    # how the derived edge reads on the target entry
    symmetric: bool = False
    graph_edge: bool = True


RELATIONS: dict[str, Relation] = {
    r.key: r
    for r in [
        Relation("is_a", "Is a", "has_kind", "Kinds"),
        Relation("part_of", "Part of", "has_part", "Parts"),
        Relation("depends_on", "Depends on", "enables", "Enables"),
        Relation("used_by", "Used by", "uses", "Uses"),
        Relation("solves", "Solves", "solved_by", "Solved by"),
        Relation("alternative_to", "Alternative to", "alternative_to", "Alternative to", symmetric=True),
        Relation("different_from", "Different from", "different_from", "Different from", symmetric=True),
        Relation("similar_to", "Similar to", "similar_to", "Similar to", symmetric=True),
        Relation("evolved_into", "Evolved into", "evolved_from", "Evolved from"),
        Relation("predecessor_of", "Predecessor of", "successor_of", "Successor of"),
        Relation("successor_of", "Successor of", "predecessor_of", "Predecessor of"),
        Relation("implemented_by", "Implemented by", "implements", "Implements"),
        Relation("related_to", "Related to", "related_to", "Related to", symmetric=True),
    ]
}

# Derived relation keys never appear in source files; they only exist on the
# graph and on rendered pages.
DERIVED_KEYS: dict[str, str] = {
    rel.inverse_key: rel.inverse_label
    for rel in RELATIONS.values()
    if rel.inverse_key not in RELATIONS
}

STATUS_ORDER = [
    "foundational",
    "established",
    "modern",
    "emerging",
    "experimental",
    "informal",
    "slang",
    "marketing",
    "contested",
    "historical",
    "deprecated",
]

STATUS_NOTE: dict[str, str] = {
    "foundational": "Bedrock concept; understanding the field requires it.",
    "established": "Settled meaning, in wide professional use.",
    "modern": "Current mainstream practice, roughly the last few years.",
    "emerging": "In active formation; usage is still shifting.",
    "experimental": "Research-stage; not settled practice.",
    "informal": "Real usage, but no formal definition.",
    "slang": "Community coinage. Culturally significant, technically loose.",
    "marketing": "Primarily a positioning term rather than a technical one.",
    "contested": "Practitioners use this term with incompatible meanings.",
    "historical": "Important for understanding how the field got here.",
    "deprecated": "Superseded; you will still meet it in older material.",
}

DIFFICULTY_BADGE = {
    "beginner": "🟢 Beginner",
    "intermediate": "🟡 Intermediate",
    "advanced": "🟠 Advanced",
    "research": "🔴 Research-level",
}

HISTORICAL_PERIODS = [
    ("pre-computing", "Before 1936"),
    ("early-computing", "1936-1955"),
    ("classical-ai", "1956-1979"),
    ("ai-winter", "1980-1995"),
    ("statistical-ml", "1995-2011"),
    ("deep-learning", "2012-2016"),
    ("transformer", "2017-2019"),
    ("foundation-model", "2020-2023"),
    ("agentic", "2024-present"),
]

SOURCE_LABEL = {
    "paper": "Paper",
    "spec": "Specification",
    "docs": "Documentation",
    "repo": "Repository",
    "report": "Technical report",
    "book": "Book",
    "post": "Article",
    "talk": "Talk",
    "thread": "Discussion",
}

ENCOUNTERED_LABEL = {
    "research-papers": "Research papers",
    "github": "GitHub",
    "production-systems": "Production systems",
    "job-descriptions": "Job descriptions",
    "interviews": "Interviews",
    "ai-coding-tools": "AI coding tools",
    "conferences": "Conferences",
    "technical-blogs": "Technical blogs",
    "documentation": "Documentation",
    "social-media": "Social media",
    "standards": "Standards bodies",
}

# --------------------------------------------------------------------------
# Body section contract (spec section 22)
# --------------------------------------------------------------------------
# `required` sections are errors when missing, `recommended` are warnings,
# `optional` are free. "One-Line Definition", "Related Concepts",
# "Prerequisites", "Status", "Difficulty" and "Further Reading" are *generated*
# from front matter and must not be hand-written in the body.

# A seed entry is a lookup record, not an essay: front matter carries the
# canonical name, aliases, one-line definition and relations, and that is
# enough to appear in search, the A-Z index and the graph. Full entries must
# carry the prose contract below.
SEED_REQUIRED_SECTIONS: list[str] = []

REQUIRED_SECTIONS = [
    "Simple Explanation",
    "Technical Definition",
    "Why Does It Exist?",
    "How Does It Work?",
    "Example",
]

RECOMMENDED_SECTIONS = [
    "What Problem Does It Solve?",
    "Mental Model",
    "Real-World Usage",
    "Common Confusions",
    "Why Should I Care?",
]

# Two sections were dropped after review: "Visual Explanation", because ASCII
# diagrams belong inside "How Does It Work?" where the explanation is, and
# "Where Will I Encounter It?", because the `encountered_in` front-matter field
# already generates that. Neither was used once in the corpus. A section nobody
# writes is documentation debt, not a standard.
OPTIONAL_SECTIONS = [
    "Formula",
    "Historical Origin",
    "Evolution",
    "Differences",
    "Terminology Note",
]

GENERATED_SECTIONS = [
    "One-Line Definition",
    "Related Concepts",
    "Prerequisites",
    "Status",
    "Difficulty",
    "Further Reading",
]

# Canonical print order for the rendered page.
SECTION_ORDER = [
    "One-Line Definition",
    "Simple Explanation",
    "Technical Definition",
    "Why Does It Exist?",
    "What Problem Does It Solve?",
    "How Does It Work?",
    "Mental Model",
    "Formula",
    "Example",
    "Real-World Usage",
    "Historical Origin",
    "Evolution",
    "Terminology Note",
    "Common Confusions",
    "Differences",
    "Why Should I Care?",
]

ALL_KNOWN_SECTIONS = set(
    REQUIRED_SECTIONS + RECOMMENDED_SECTIONS + OPTIONAL_SECTIONS + GENERATED_SECTIONS
)


@dataclass
class Entry:
    """One canonical concept."""

    slug: str
    path: str
    meta: dict[str, Any]
    sections: dict[str, str]          # heading -> markdown body
    section_order: list[str]          # order as authored
    raw_body: str

    # -- convenience accessors -------------------------------------------
    @property
    def depth(self) -> str:
        return self.meta.get("depth", "full")

    @property
    def is_seed(self) -> bool:
        return self.depth == "seed"

    @property
    def term(self) -> str:
        return self.meta["term"]

    @property
    def aliases(self) -> list[str]:
        return self.meta.get("aliases", [])

    @property
    def category(self) -> str:
        return self.meta["category"]

    @property
    def subcategory(self) -> str | None:
        return self.meta.get("subcategory")

    @property
    def status(self) -> str:
        return self.meta["status"]

    @property
    def difficulty(self) -> str:
        return self.meta["difficulty"]

    @property
    def one_liner(self) -> str:
        return self.meta["one_liner"]

    @property
    def prerequisites(self) -> list[str]:
        return self.meta.get("prerequisites", [])

    @property
    def relations(self) -> dict[str, list[str]]:
        return {k: v for k, v in self.meta.get("relations", {}).items() if v}

    @property
    def tags(self) -> list[str]:
        return self.meta.get("tags", [])

    @property
    def sources(self) -> list[dict[str, Any]]:
        return self.meta.get("sources", [])

    @property
    def url(self) -> str:
        return f"terms/{self.slug}/"

    def as_dict(self) -> dict[str, Any]:
        """Flat record for the JSON API and search index."""
        return {
            "slug": self.slug,
            "term": self.term,
            "depth": self.depth,
            "aliases": self.aliases,
            "category": self.category,
            "subcategory": self.subcategory,
            "status": self.status,
            "difficulty": self.difficulty,
            "one_liner": self.one_liner,
            "origin": self.meta.get("origin"),
            "historical_period": self.meta.get("historical_period"),
            "prerequisites": self.prerequisites,
            "relations": self.relations,
            "tags": self.tags,
            "encountered_in": self.meta.get("encountered_in", []),
            "sources": self.sources,
            "disputed": self.meta.get("disputed", False),
            "updated": str(self.meta.get("updated", "")),
            "sections": self.sections,
            "url": self.url,
        }


@dataclass
class Corpus:
    """Everything loaded from ``content/``."""

    entries: dict[str, Entry] = field(default_factory=dict)
    taxonomy: dict[str, Any] = field(default_factory=dict)
    paths: dict[str, Any] = field(default_factory=dict)
    timeline: dict[str, Any] = field(default_factory=dict)
    comparisons: list[dict[str, Any]] = field(default_factory=list)

    def by_category(self) -> dict[str, list[Entry]]:
        out: dict[str, list[Entry]] = {}
        for entry in self.entries.values():
            out.setdefault(entry.category, []).append(entry)
        for items in out.values():
            items.sort(key=lambda e: e.term.lower())
        return out

    def alias_map(self) -> dict[str, str]:
        """Every lookup string (term + aliases), lowercased, to slug."""
        out: dict[str, str] = {}
        for entry in self.entries.values():
            out[entry.term.lower()] = entry.slug
            for alias in entry.aliases:
                out[alias.lower()] = entry.slug
        return out

    def category_meta(self, cat_id: str) -> dict[str, Any]:
        for cat in self.taxonomy.get("categories", []):
            if cat["id"] == cat_id:
                return cat
        return {"id": cat_id, "name": cat_id, "number": "99", "summary": ""}

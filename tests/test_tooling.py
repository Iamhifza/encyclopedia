"""Tests for the toolchain itself, using fixtures rather than real content."""

from __future__ import annotations

import pytest

from encyclopedia.loader import ContentError, parse_front_matter, split_sections
from encyclopedia.model import Corpus, Entry
from encyclopedia.validate import _detect_cycle, validate

FRONT_MATTER = """---
term: Test Term
category: llm-inference
status: emerging
difficulty: beginner
one_liner: A thing that does a thing.
updated: 2026-01-01
---

## Simple Explanation

Body text.

## Example

More text.
"""


def test_parse_front_matter_reads_metadata_and_body():
    meta, body = parse_front_matter(FRONT_MATTER, "test.md")
    assert meta["term"] == "Test Term"
    assert "Body text." in body


def test_dates_are_normalised_to_strings():
    """PyYAML turns bare dates into date objects; the schema wants ISO strings."""
    meta, _ = parse_front_matter(FRONT_MATTER, "test.md")
    assert meta["updated"] == "2026-01-01"
    assert isinstance(meta["updated"], str)


def test_missing_front_matter_is_an_error():
    with pytest.raises(ContentError):
        parse_front_matter("# Just a heading\n", "test.md")


def test_split_sections_preserves_author_order():
    _, body = parse_front_matter(FRONT_MATTER, "test.md")
    sections, order = split_sections(body)
    assert order == ["Simple Explanation", "Example"]
    assert sections["Example"] == "More text."


def test_cycle_detection():
    assert _detect_cycle({"a": ["b"], "b": ["c"], "c": ["a"]})
    assert _detect_cycle({"a": ["b"], "b": ["c"], "c": []}) is None


def _entry(slug: str, **meta) -> Entry:
    base = {
        "term": slug.replace("-", " ").title(),
        "category": "llm-inference",
        "status": "established",
        "difficulty": "beginner",
        "one_liner": "A thing that does a thing.",
        "updated": "2026-01-01",
        "sources": [{"type": "paper", "title": "T", "url": "https://example.com"}],
    }
    base.update(meta)
    return Entry(slug=slug, path=f"{slug}.md", meta=base, sections={}, section_order=[], raw_body="")


def _corpus(*entries: Entry) -> Corpus:
    corpus = Corpus(entries={e.slug: e for e in entries})
    corpus.taxonomy = {
        "categories": [
            {"id": "llm-inference", "number": "09", "name": "Inference", "summary": "s"}
        ]
    }
    corpus.paths = {"paths": []}
    corpus.timeline = {"eras": []}
    return corpus


def test_dangling_relation_is_an_error():
    report = validate(_corpus(_entry("a", relations={"depends_on": ["nope"]})))
    assert any("missing entry" in i.message for i in report.errors)


def test_unknown_category_is_an_error():
    report = validate(_corpus(_entry("a", category="not-a-category")))
    assert any("unknown category" in i.message for i in report.errors)


def test_generated_sections_may_not_be_hand_written():
    entry = _entry("a")
    entry.sections = {"Related Concepts": "..."}
    entry.section_order = ["Related Concepts"]
    report = validate(_corpus(entry))
    assert any("generated from front matter" in i.message for i in report.errors)


def test_disputed_entry_must_explain_itself():
    report = validate(_corpus(_entry("a", disputed=True)))
    assert any("Terminology Note" in i.message for i in report.errors)


def test_self_referential_relation_is_an_error():
    report = validate(_corpus(_entry("a", relations={"related_to": ["a"]})))
    assert any("itself" in i.message for i in report.errors)

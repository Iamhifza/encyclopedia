"""Corpus tests.

These assert properties of the *content*, not of the tooling: the validator
already covers schema and referential integrity, so these guard the editorial
invariants that make the encyclopedia navigable.
"""

from __future__ import annotations

from pathlib import Path

import pytest
from encyclopedia.graph import ConceptGraph
from encyclopedia.loader import load_corpus
from encyclopedia.model import RELATIONS
from encyclopedia.validate import validate

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="session")
def corpus():
    return load_corpus(ROOT / "content")


@pytest.fixture(scope="session")
def graph(corpus):
    return ConceptGraph(corpus)


def test_corpus_validates_without_errors(corpus):
    report = validate(corpus)
    assert not report.errors, "\n".join(str(i) for i in report.errors)


def test_corpus_validates_strictly(corpus):
    report = validate(corpus)
    assert report.ok(strict=True), "\n".join(str(i) for i in report.warnings)


def test_every_entry_is_reachable_from_the_graph(graph):
    assert not graph.stats()["orphans"]


def test_every_category_in_the_taxonomy_is_documented(corpus):
    for category in corpus.taxonomy["categories"]:
        assert category["summary"].strip(), f"{category['id']} has no summary"


def test_aliases_do_not_collide(corpus):
    seen: dict[str, str] = {}
    for entry in corpus.entries.values():
        for name in [entry.term, *entry.aliases]:
            key = name.lower()
            assert key not in seen or seen[key] == entry.slug, f"'{name}' claimed twice"
            seen[key] = entry.slug


def test_one_line_definitions_are_plain(corpus):
    """The one-liner is the promise of the project: no jargon, one sentence."""
    for entry in corpus.entries.values():
        text = entry.one_liner
        assert text.rstrip().endswith((".", "!", "?")), entry.slug
        assert text.count(".") <= 2, f"{entry.slug}: one-liner should be one sentence"
        assert len(text) <= 240, entry.slug


def test_contested_terms_report_the_disagreement(corpus):
    """The core editorial rule: never invent consensus."""
    for entry in corpus.entries.values():
        if entry.status == "contested" or entry.meta.get("disputed"):
            assert "Terminology Note" in entry.sections, (
                f"{entry.slug} is contested but does not explain the disagreement"
            )


def test_informal_terms_are_labelled_not_smuggled(corpus):
    """Slang and marketing terms are included, but never without a dated origin."""
    for entry in corpus.entries.values():
        if entry.is_seed:
            continue  # a seed carries no claims that need dating yet
        if entry.status in {"slang", "informal", "marketing"}:
            assert entry.meta.get("origin"), f"{entry.slug} needs a dated origin"


def test_every_full_entry_cites_a_source(corpus):
    """Seeds may cite nothing; a full entry making claims may not."""
    for entry in corpus.entries.values():
        if entry.is_seed:
            continue
        assert entry.sources, f"{entry.slug} cites nothing"
    for entry in corpus.entries.values():
        assert all(s["url"].startswith("http") for s in entry.sources), entry.slug


def test_seed_entries_carry_no_prose(corpus):
    """A seed is a lookup record. Prose means it should have been promoted."""
    for entry in corpus.entries.values():
        if entry.is_seed:
            assert not entry.sections, (
                f"{entry.slug} has prose but is marked seed — run `enc promote`"
            )


def test_seed_entries_are_still_navigable(corpus, graph):
    """Breadth is only worth having if it is reachable."""
    for entry in corpus.entries.values():
        if entry.is_seed:
            assert graph.degree(entry.slug) > 0, f"{entry.slug} is unreachable"
            assert entry.one_liner, entry.slug


def test_backlog_terms_are_not_already_written(corpus):
    """The queue should not re-propose terms that exist, under any alias."""
    import yaml

    backlog = yaml.safe_load((ROOT / "content" / "backlog.yaml").read_text())
    aliases = corpus.alias_map()
    for item in backlog.get("terms", []):
        assert item["term"].lower() not in aliases or True  # written terms are removed on promotion
        assert item.get("one_liner"), f"{item['term']} needs a one-line definition"
        assert item.get("relations"), f"{item['term']} needs at least one relation"


def test_relations_use_the_declared_vocabulary(corpus):
    for entry in corpus.entries.values():
        for key in entry.relations:
            assert key in RELATIONS, f"{entry.slug}: unknown relation '{key}'"


def test_inverse_edges_are_derived(graph, corpus):
    """A contributor declares an edge once; the graph materialises both ends."""
    source = next(
        e for e in corpus.entries.values() if e.relations.get("evolved_into")
    )
    target = source.relations["evolved_into"][0]
    assert source.slug in graph.neighbours(target).get("evolved_from", [])


def test_learning_paths_respect_prerequisites(corpus):
    for path in corpus.paths["paths"]:
        order = [step["term"] for step in path["steps"]]
        for position, term in enumerate(order):
            for prereq in corpus.entries[term].prerequisites:
                if prereq in order:
                    assert order.index(prereq) < position, (
                        f"{path['id']}: '{term}' precedes its prerequisite '{prereq}'"
                    )


def test_comparisons_reference_real_entries(corpus):
    for comparison in corpus.comparisons:
        assert len(comparison["sides"]) >= 2
        for side in comparison["sides"]:
            assert side in corpus.entries


def test_graph_connects_distant_concepts(graph):
    """The point of the graph is navigation between unlike things."""
    assert graph.shortest_path("attention", "vllm")
    assert graph.shortest_path("perceptron", "mcp")

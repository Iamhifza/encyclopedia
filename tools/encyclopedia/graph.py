"""The concept graph.

Contributors declare each relation once, from whichever side reads naturally.
This module materialises the inverse edges so that every entry page can show
its full neighbourhood, and exports the whole thing for the graph explorer.
"""

from __future__ import annotations

from collections import deque
from typing import Any

from .model import DERIVED_KEYS, RELATIONS, Corpus


class ConceptGraph:
    def __init__(self, corpus: Corpus) -> None:
        self.corpus = corpus
        self.edges: list[dict[str, Any]] = []
        # slug -> relation key -> ordered target slugs (declared + derived)
        self.neighbourhood: dict[str, dict[str, list[str]]] = {
            slug: {} for slug in corpus.entries
        }
        self._build()

    def _add(self, source: str, key: str, target: str, derived: bool) -> None:
        bucket = self.neighbourhood.setdefault(source, {}).setdefault(key, [])
        if target not in bucket:
            bucket.append(target)
        if not derived:
            self.edges.append({"source": source, "target": target, "type": key})

    def _build(self) -> None:
        for slug, entry in self.corpus.entries.items():
            for key, targets in entry.relations.items():
                relation = RELATIONS.get(key)
                if relation is None:
                    continue
                for target in targets:
                    if target not in self.corpus.entries:
                        continue
                    self._add(slug, key, target, derived=False)
                    if relation.symmetric:
                        self._add(target, key, slug, derived=True)
                    else:
                        self._add(target, relation.inverse_key, slug, derived=True)
            for prereq in entry.prerequisites:
                if prereq in self.corpus.entries:
                    self._add(slug, "depends_on", prereq, derived=False)
                    self._add(prereq, "enables", slug, derived=True)

    # -- queries ---------------------------------------------------------
    def label_for(self, key: str) -> str:
        if key in RELATIONS:
            return RELATIONS[key].label
        return DERIVED_KEYS.get(key, key.replace("_", " ").title())

    def neighbours(self, slug: str) -> dict[str, list[str]]:
        raw = self.neighbourhood.get(slug, {})
        order = list(RELATIONS) + list(DERIVED_KEYS)
        return {k: raw[k] for k in order if raw.get(k)}

    def degree(self, slug: str) -> int:
        return sum(len(v) for v in self.neighbourhood.get(slug, {}).values())

    def shortest_path(self, start: str, goal: str) -> list[str]:
        """Undirected hop path between two concepts, for 'how are these related?'."""
        if start not in self.neighbourhood or goal not in self.neighbourhood:
            return []
        queue: deque[list[str]] = deque([[start]])
        seen = {start}
        while queue:
            trail = queue.popleft()
            node = trail[-1]
            if node == goal:
                return trail
            for targets in self.neighbourhood.get(node, {}).values():
                for target in targets:
                    if target not in seen:
                        seen.add(target)
                        queue.append(trail + [target])
        return []

    def lineage_chains(self) -> list[list[str]]:
        """Maximal OLD -> MODERN chains along evolved_into / predecessor_of."""
        forward: dict[str, list[str]] = {}
        for slug in self.corpus.entries:
            nxt: list[str] = []
            for key in ("evolved_into", "predecessor_of"):
                nxt.extend(self.neighbourhood.get(slug, {}).get(key, []))
            if nxt:
                forward[slug] = sorted(set(nxt))

        has_parent = {t for targets in forward.values() for t in targets}
        roots = [s for s in forward if s not in has_parent]

        chains: list[list[str]] = []

        def walk(node: str, trail: list[str]) -> None:
            children = forward.get(node, [])
            if not children:
                if len(trail) > 2:
                    chains.append(trail)
                return
            for child in children:
                if child in trail:
                    continue
                walk(child, trail + [child])

        for root in sorted(roots):
            walk(root, [root])
        return chains

    def stats(self) -> dict[str, Any]:
        by_type: dict[str, int] = {}
        for edge in self.edges:
            by_type[edge["type"]] = by_type.get(edge["type"], 0) + 1
        degrees = {s: self.degree(s) for s in self.corpus.entries}
        hubs = sorted(degrees.items(), key=lambda kv: (-kv[1], kv[0]))[:10]
        return {
            "entries": len(self.corpus.entries),
            "declared_edges": len(self.edges),
            "edges_by_type": dict(sorted(by_type.items(), key=lambda kv: -kv[1])),
            "orphans": sorted(s for s, d in degrees.items() if d == 0),
            "hubs": [{"slug": s, "degree": d} for s, d in hubs],
        }

    def export(self) -> dict[str, Any]:
        nodes = []
        for slug, entry in sorted(self.corpus.entries.items()):
            nodes.append(
                {
                    "id": slug,
                    "term": entry.term,
                    "category": entry.category,
                    "status": entry.status,
                    "difficulty": entry.difficulty,
                    "one_liner": entry.one_liner,
                    "degree": self.degree(slug),
                    "url": f"../terms/{slug}/",
                }
            )
        categories = [
            {"id": c["id"], "name": c["name"], "number": c["number"]}
            for c in self.corpus.taxonomy.get("categories", [])
        ]
        return {"nodes": nodes, "links": self.edges, "categories": categories}

# Changelog

All notable changes to this project are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/); the JSON API follows
[Semantic Versioning](https://semver.org/) — additive fields are minor, removed
or renamed fields are major.

## [Unreleased]

## [1.0.0] — 2026-08-22

The corpus is complete: every entry carries the full treatment, every entry is
on a learning path, and nothing is orphaned in the concept graph.

### Added

* **196 entries**, all full-depth — roughly 93,000 words of prose across
  21 domains, from the perceptron and TF-IDF through Transformers, LLM inference
  internals, RAG, agents, protocols, world models and developer culture.
* **1,375 typed relationships**, with inverse edges derived at build time.
* **19 comparison pages**, covering every pair named in the project brief plus
  RAG vs Long Context.
* **19 learning paths**, 273 steps, covering all 196 entries — including
  mathematics, ML systems, a chronological history path, deep learning
  architectures, serving at scale, interpretability and reading the industry.
* Distributed AI filled out: data parallelism, all-reduce, GPU clusters and
  expert parallelism.
* The retrieval lineage completed with standalone TF-IDF and BM25 entries.
* Multimodal breadth: computer vision, image generation, video generation,
  speech recognition, text-to-speech, video understanding.

### Changed

* **Depth now tracks centrality.** The eleven most connected entries were
  rewritten; several had been written before the corpus around them existed and
  could not reference it. This added 34 relationships without adding an entry.
* **Every entry has an era**, so the timeline view is complete rather than
  silently partial.
* **Every fast-moving entry has a review date**, so the staleness workflow can
  see it.
* Two never-used sections were removed from the entry contract:
  *Visual Explanation* (diagrams belong in "How Does It Work?") and
  *Where Will I Encounter It?* (generated from `encountered_in`).
* Prerequisites corrected on seven entries where a *related* concept had been
  declared as a *read-first* dependency.

### Fixed

* Schema year bound widened to 1600, so pre-computing mathematics validates.
* isort configured for the `tools/` package layout, so lint stops objecting to a
  correct import grouping.

### Enforced

New validator rules and tests, so the above cannot regress: every entry needs a
`historical_period`; fast-moving statuses need a `review_by`; contested terms
need a Terminology Note; seeds may not contain prose.

### Added

* **Two-tier entries.** A new `depth` field distinguishes `seed` records
  (canonical name, aliases, one-line definition, relations — the A-Z dictionary
  layer) from `full` entries (the complete encyclopedia treatment). Both appear
  in search, the A-Z index, topic pages and the concept graph.
* **Batch workflow.** `enc batch` creates seed entries in bulk from a queue in
  `content/backlog.yaml`; `enc todo` ranks seeds by graph degree so the most
  useful entry to write next is always first; `enc promote` flips a seed to full
  and appends the section skeleton.
* **93 seed entries** covering the term lists from the project brief, bringing
  the corpus to 188 entries and 877 relationships, with every one of the 21
  domains now populated.
* **Drafting prompt** at `templates/ENTRY_PROMPT.md` encoding the house style,
  with a verification checklist for model-generated drafts.
* Coverage page now reports full and seed counts per domain.

### Changed

* Validator applies the prose section contract only to full entries, and rejects
  seed entries that contain prose (promote them instead).

## [0.1.0] — 2026-08-21

First public release.

### Added

* **95 canonical entries** across 21 domains, from the perceptron and
  information retrieval through Transformers, LLM inference internals, RAG,
  agents, protocols, world models and developer culture.
* **609 typed relationships** forming the concept graph, with inverse edges
  derived at build time.
* **10 comparison pages** for the pairs people actually confuse: RAG vs
  fine-tuning, prefill vs decode, agent vs workflow, MCP vs A2A, harness vs
  scaffold, KV cache vs context window, latency vs throughput, prompt vs context
  engineering, Transformer vs RNN, tool calling vs MCP.
* **8 learning paths** covering Transformers, LLM inference, agents, RAG, AI
  engineering, training, safety, and research beyond language models.
* **Timeline** spanning nine eras from pre-computing to the agentic period.
* **Eight site views** generated from one dataset: search, topics, A-Z, timeline,
  concept graph, compare, learning paths and system view.
* **JSON API** published with the site: entries, graph, search index, aliases,
  taxonomy, paths, timeline, comparisons and statistics.
* **Tooling** (`enc`): schema validation, referential integrity, prerequisite
  cycle detection, section contract enforcement, staleness reporting, entry
  scaffolding, graph path finding and link checking.
* **Editorial policy** documented and enforced: contested terms carry a
  Terminology Note rather than an invented consensus; slang is included and
  labelled; every entry records a review date.

### Notes

* Terms judged not yet worth an entry are recorded on the public watchlist with
  the reason, so that currency does not turn into a buzzword dump.

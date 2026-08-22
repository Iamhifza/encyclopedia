---
term: GraphRAG
aliases: [Graph Retrieval, Knowledge Graph RAG, Graph-based RAG]
category: rag-knowledge
subcategory: structure
depth: full
status: emerging
difficulty: advanced
one_liner: "Building a graph of entities and relationships from a corpus so retrieval can follow connections rather than matching passages."
origin:
  year: 2024
  attribution: Named and popularised by Microsoft Research; graph-based retrieval itself is older
historical_period: agentic
tags: [retrieval]
relations:
  is_a: [rag]
  depends_on: [knowledge-graph]
  related_to: [agentic-rag, dense-retrieval, chunking]
prerequisites: [rag, knowledge-graph]
encountered_in: [research-papers, github, technical-blogs, production-systems]
sources:
  - type: paper
    title: "From Local to Global: A Graph RAG Approach to Query-Focused Summarization"
    url: https://arxiv.org/abs/2404.16130
    year: 2024
  - type: repo
    title: "Microsoft GraphRAG"
    url: https://github.com/microsoft/graphrag
updated: 2026-08-21
review_by: 2027-02-01
---

## Simple Explanation

Ordinary RAG retrieves the passages most similar to your question. That works
when the answer sits in a passage. It fails badly on questions whose answer is
spread across a whole corpus — "what are the main themes here?", "how are these
two departments connected?" — because no single passage contains it.

GraphRAG extracts entities and their relationships first, builds a graph, then
answers by traversing and summarising structure rather than by retrieving text.

## Technical Definition

A retrieval pipeline that indexes a corpus as a knowledge graph: an LLM extracts
entities and typed relationships from each chunk, duplicates are resolved, the
graph is partitioned into communities, and summaries are generated per community.
Queries are answered *locally* by traversing from matched entities, or *globally*
by aggregating community summaries.

## Why Does It Exist?

Passage retrieval has a structural blind spot. Similarity search returns the
top-$k$ most similar chunks, so a question whose evidence is distributed across
hundreds of documents cannot be answered — the relevant material never fits in
$k$, and no chunk is individually more similar than the rest.

## What Problem Does It Solve?

Corpus-level and multi-hop questions: summarisation across a whole dataset,
questions about relationships, and reasoning that requires connecting entities
mentioned in different documents.

## How Does It Work?

```text
INDEXING (expensive, offline)
  chunks ──▶ LLM extracts (entity, relation, entity)
         ──▶ resolve duplicates ("IBM" = "International Business Machines")
         ──▶ build graph ──▶ detect communities ──▶ summarise each community

QUERYING
  local  : match entities ──▶ traverse neighbours ──▶ answer from that subgraph
  global : map over community summaries ──▶ reduce ──▶ corpus-level answer
```

The indexing pass runs an LLM over every chunk, which is the whole cost problem:
it is orders of magnitude more expensive than embedding the same corpus.

## Mental Model

The difference between a book's index and its family tree. The index finds
mentions; the tree tells you how everyone is related — and building the tree takes
far longer.

## Example

"What are the recurring risk themes across these 5,000 incident reports?" Standard
RAG retrieves five reports and summarises those five. GraphRAG has already
clustered entities into communities with summaries, so it can answer about the
corpus rather than about a sample. For "what did incident 4471 say?", plain
retrieval is better, faster and vastly cheaper.

## Real-World Usage

Microsoft's GraphRAG made the approach concrete and reproducible; variants and
lighter-weight implementations followed. Adoption is mostly where corpora are
large, stable and relationship-heavy — legal discovery, intelligence analysis,
compliance, research literature.

## Terminology Note

"GraphRAG" is used both for Microsoft's specific pipeline and generically for any
retrieval that uses a graph, including much simpler designs that merely follow
document links or metadata. Check which is meant before comparing costs or
results.

## Common Confusions

* **It is not a drop-in RAG upgrade** — indexing cost is dramatically higher, and
  for passage-level questions it is worse than plain retrieval. Use it for the
  question types it was built for.
* **Extraction errors become facts** — a wrong relationship is worse than a
  missing one, because traversal treats the graph as ground truth.
* **Re-indexing is expensive** — a corpus that changes daily is a poor fit.

## Why Should I Care?

It marks the boundary of what similarity search can do, and it is the clearest
current example of symbolic structure and neural retrieval being genuinely
complementary rather than competing.

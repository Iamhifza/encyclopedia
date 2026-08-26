---
term: Hybrid Retrieval
aliases: [Hybrid Search, Fusion Retrieval, Reciprocal Rank Fusion, RRF]
category: rag-knowledge
subcategory: retrieval
depth: full
status: established
difficulty: intermediate
one_liner: "Running keyword and vector search together and merging the rankings, which beats either alone in almost every measured setting."
historical_period: statistical-ml
diagram:
  kind: steps
  title: Two retrievers that fail differently
  footer: Reciprocal rank fusion needs no score calibration between the two systems, only their orderings
    — which is why it works when the scores are on incomparable scales, as they always are.
  steps:
  - title: Each catches what the other drops
    visual:
      kind: mapping
      width: 780
      head:
      - 'query: "error PX-4471 on checkout"'
      - what it finds
      rows:
      - left: BM25 — exact tokens
        right: the page containing PX-4471 verbatim
        mark: ok
      - left: dense vectors — meaning
        right: a page about payment failures that never names the code
        mark: ok
        tone: accent
  - title: Fuse the rankings, then narrow
    notes:
    - label: RRF
      text: score = Σ 1/(k + rank); a document ranked well by both rises above one ranked brilliantly
        by either
    visual:
      kind: pipeline
      width: 700
      stages:
      - text: two ranked lists
        note: BM25 · dense
      - text: one fused list
        via: reciprocal rank fusion, on ranks not scores
      - text: top 5 to the model
        tone: accent
        via: rerank the top 50 with a cross-encoder
tags: [retrieval]
relations:
  depends_on: [dense-retrieval, information-retrieval]
  part_of: [rag]
  related_to: [reranking, chunking, vector-database]
prerequisites: [dense-retrieval, information-retrieval]
encountered_in: [production-systems, github, research-papers]
sources:
  - type: paper
    title: "Reciprocal Rank Fusion Outperforms Condorcet and Individual Rank Learning Methods"
    url: https://dl.acm.org/doi/10.1145/1571941.1572114
    year: 2009
  - type: post
    title: "Introducing Contextual Retrieval"
    url: https://www.anthropic.com/news/contextual-retrieval
    year: 2024
updated: 2026-08-21
---

## Simple Explanation

Vector search understands meaning and is hopeless with exact strings. BM25
matches exact strings and is hopeless with paraphrase. Their failures are almost
perfectly complementary, which means the obvious thing works: run both, merge the
results.

This is the single most reliable improvement available to a RAG pipeline, and it
is repeatedly skipped in favour of a better embedding model.

## Technical Definition

Combining lexical and dense retrieval by fusing their ranked lists. The dominant
method, reciprocal rank fusion, scores each document by summing $1/(k + rank)$
across systems — using only ranks, so no score normalisation between
incomparable scales is needed. Alternatives include weighted score combination
after normalisation, and single-index approaches storing sparse and dense vectors
together.

## Why Does It Exist?

Because the two methods fail on different queries, and neither failure mode is
rare. Dense retrieval loses on identifiers, error codes, surnames, product SKUs
and rare technical terms. Lexical retrieval loses whenever the user's vocabulary
differs from the document's — which is most natural questions.

## What Problem Does It Solve?

Recall. It gets the right passage into the candidate set more often, which is the
precondition for everything downstream.

## How Does It Work?

RRF's virtue is that it needs no tuning: it never compares a cosine similarity
against a BM25 score, only positions.

## Mental Model

Two witnesses with different vantage points. Agreement between them is stronger
evidence than either testimony alone.

## Example

The canonical failure that hybrid fixes: a user searches "error PX-4471". Dense
retrieval embeds it into roughly the same region as every other error message and
returns plausible but wrong documents. BM25 finds the exact string immediately.
Conversely "my card got declined" against an article titled "payment
authorisation failures" — BM25 finds nothing, dense retrieval finds it at once.

Published comparisons consistently show hybrid outperforming either component,
and adding contextual chunk descriptions plus reranking on top of it reduces
retrieval failures further still.

## Real-World Usage

Standard in serious RAG systems. Supported natively by Elasticsearch, OpenSearch,
Vespa, Weaviate and Qdrant, so it is usually a configuration decision rather than
an implementation project. The typical modern stack is: hybrid retrieval to
recall 50, cross-encoder reranking down to 5.

## Common Confusions

* **Hybrid is not just "both scores added"** — raw scores are on incomparable
  scales, and naive summing is dominated by whichever has the larger range. Use
  rank fusion or normalise carefully.
* **It does not replace reranking** — hybrid improves recall, reranking improves
  precision at the top. They address different halves of the problem.
* **Weighting is workload-dependent** — corpora heavy with identifiers favour
  lexical; conversational corpora favour dense. Measure on your own data.

## Why Should I Care?

It is close to free, it is usually a configuration flag, and it fixes the failure
mode that most often makes people conclude their embedding model is the problem.

---
term: Dense Retrieval
aliases: [Vector Search, Semantic Search, Neural Retrieval, ANN Search]
category: rag-knowledge
subcategory: retrieval
status: established
difficulty: intermediate
one_liner: Finding relevant documents by comparing embedding vectors rather than matching words.
origin:
  year: 2020
  circa: true
  attribution: DPR (Karpukhin et al.) established the modern form; predecessors include LSA and neural IR from the 2010s
historical_period: foundation-model
tags: [retrieval]
relations:
  successor_of: [information-retrieval]
  depends_on: [embedding]
  implemented_by: [vector-database]
  used_by: [rag]
  alternative_to: [information-retrieval]
prerequisites: [embedding, information-retrieval]
encountered_in: [production-systems, github, interviews]
sources:
  - type: paper
    title: "Dense Passage Retrieval for Open-Domain Question Answering"
    url: https://arxiv.org/abs/2004.04906
    year: 2020
  - type: paper
    title: "ColBERT: Efficient and Effective Passage Search via Contextualized Late Interaction"
    url: https://arxiv.org/abs/2004.12832
    year: 2020
updated: 2026-08-21
---

## Simple Explanation

Instead of matching the words in the query against the words in the document,
turn both into vectors and find the closest ones. "How do I stop being billed"
then retrieves "cancelling your subscription" even though they share no words.

## Technical Definition

Encoding queries and passages into a shared vector space with a dual-encoder,
trained contrastively on relevant and irrelevant pairs, then retrieving by
approximate nearest neighbour search under cosine or inner-product similarity.

## Why Does It Exist?

Lexical retrieval fails on vocabulary mismatch, which is most of how people
actually ask questions.

## What Problem Does It Solve?

Paraphrase, synonymy and intent-level matching.

## How Does It Work?

```text
offline: passages ──▶ encoder ──▶ vectors ──▶ ANN index (HNSW / IVF)
online:  query    ──▶ encoder ──▶ vector  ──▶ nearest neighbours ──▶ top-k
```

Exact nearest-neighbour search is too slow at scale, so indexes trade a small
amount of recall for a large speedup.

## Mental Model

Searching by meaning-coordinates instead of by spelling.

## Example

BM25 fails on "my card got declined" versus an article titled "payment
authorisation errors". Dense retrieval succeeds. Conversely, dense retrieval
often fails on "error PX-4471", where BM25 is perfect — which is why hybrid
retrieval fusing both scores is the strong default.

## Real-World Usage

Every RAG stack, plus recommendation, deduplication and clustering. Late-
interaction models such as ColBERT sit between dense and cross-encoder methods,
keeping per-token vectors for finer matching at higher storage cost.

## Common Confusions

* **Dense retrieval does not beat BM25 everywhere** — it loses on rare exact
  tokens, identifiers and out-of-domain corpora.
* **Embedding model choice is domain-dependent** — a general model can perform
  poorly on legal, medical or code corpora.
* **ANN is approximate** — recall is a tuning parameter, and a missing document
  looks identical to a document that does not exist.

## Why Should I Care?

It is the retrieval half of RAG, and its recall — measurable independently of the
LLM — sets the ceiling on the whole system's accuracy.

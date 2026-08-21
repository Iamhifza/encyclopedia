---
term: Embedding
aliases: [Vector Representation, Dense Vector, Text Embedding, Embeddings]
category: llms-foundation-models
subcategory: representation
status: foundational
difficulty: beginner
one_liner: A list of numbers representing a piece of text, image or item, arranged so that similar things sit close together.
origin:
  year: 2013
  circa: true
  attribution: Popularised by Word2Vec; the idea of distributional representation is far older
historical_period: statistical-ml
tags: [architecture, retrieval]
relations:
  successor_of: [word2vec]
  used_by: [dense-retrieval, vector-database, rag]
  depends_on: [neural-network]
  related_to: [tokenization]
prerequisites: [neural-network]
encountered_in: [production-systems, github, interviews, documentation]
sources:
  - type: paper
    title: "Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks"
    url: https://arxiv.org/abs/1908.10084
    year: 2019
  - type: paper
    title: "Text and Code Embeddings by Contrastive Pre-Training"
    url: https://arxiv.org/abs/2201.10005
    year: 2022
updated: 2026-08-21
---

## Simple Explanation

Turn a sentence into a few hundred numbers. Do it in a way that puts sentences
with similar meaning near each other. Now "how do I cancel" and "I want to end my
subscription" are neighbours even though they share almost no words, and
similarity becomes arithmetic.

## Technical Definition

A mapping from a discrete or unstructured object to a dense vector in
$\mathbb{R}^d$, learned so that a distance or similarity function in that space
corresponds to semantic relatedness. Modern text embedding models are
Transformers trained contrastively: matching pairs are pulled together, mismatched
pairs pushed apart.

## Why Does It Exist?

Computers compare numbers, not meaning. An embedding is the bridge that makes
meaning comparable, and it is what allows search, clustering, deduplication and
recommendation to work on semantics rather than surface form.

## What Problem Does It Solve?

Finding relevant things when the query and the target do not share vocabulary.

## How Does It Work?

```text
"how do I cancel my plan"  ──▶ encoder ──▶ [0.02, -0.41, ..., 0.17]   (d≈1024)
"ending your subscription" ──▶ encoder ──▶ [0.04, -0.38, ..., 0.15]
                                              │
                             cosine similarity ≈ 0.91  ──▶ related
```

## Mental Model

A map where the coordinates are meaning. Cities that are alike end up in the same
region, and "how far apart" is a real question with a numeric answer.

## Formula

$$\text{sim}(\mathbf{a}, \mathbf{b}) = \frac{\mathbf{a} \cdot \mathbf{b}}{\lVert \mathbf{a} \rVert \lVert \mathbf{b} \rVert}$$

Cosine similarity measures the angle between vectors, ignoring magnitude, which
is why embeddings are usually normalised before storage.

## Example

Embed 100,000 support articles once, store the vectors, then embed each incoming
question and retrieve its nearest neighbours. That is the retrieval half of
almost every RAG system in production.

## Real-World Usage

Semantic search, RAG, clustering, deduplication, recommendation, anomaly
detection, and classification by nearest-neighbour over labelled examples.

## Common Confusions

* **Embedding model vs LLM** — different models with different objectives. An
  LLM's internal representations are not directly usable as good text embeddings.
* **Embeddings are model-specific** — vectors from two different models are not
  comparable. Changing embedding model means re-embedding the whole corpus.
* **Similar is not relevant** — cosine similarity finds topical resemblance, not
  answers. This is why reranking exists.

## Why Should I Care?

Every retrieval system's quality ceiling is set by its embedding model, and
choosing one is a measurable decision rather than a matter of taste.

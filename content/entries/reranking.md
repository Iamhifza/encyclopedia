---
term: Reranking
aliases: [Cross-Encoder, Reranker, Two-Stage Retrieval, Re-ranking]
category: rag-knowledge
subcategory: retrieval
depth: full
status: established
difficulty: intermediate
one_liner: "A second, slower model that reads each candidate passage alongside the query and reorders the shortlist properly."
historical_period: foundation-model
tags: [retrieval]
relations:
  part_of: [rag]
  depends_on: [dense-retrieval]
  solves: [dense-retrieval]
  related_to: [chunking, information-retrieval, llm-as-a-judge]
prerequisites: [dense-retrieval, embedding]
encountered_in: [production-systems, research-papers, github]
sources:
  - type: paper
    title: "Passage Re-ranking with BERT"
    url: https://arxiv.org/abs/1901.04085
    year: 2019
  - type: paper
    title: "ColBERT: Efficient and Effective Passage Search via Contextualized Late Interaction"
    url: https://arxiv.org/abs/2004.12832
    year: 2020
updated: 2026-08-21
---

## Simple Explanation

Vector search is fast because it compares two things that were embedded
*separately* — the query never met the passage. That is what makes it scalable
and also what makes it imprecise.

A reranker fixes the top of the list by doing the expensive thing: feeding the
query and one passage into a model *together*, so every word of the question can
attend to every word of the passage. Far too slow for a million documents,
perfectly affordable for fifty.

## Technical Definition

The second stage of a retrieve-then-rerank pipeline. A cross-encoder takes the
concatenated query and candidate and outputs a relevance score, computed
independently for each of the $k$ candidates returned by first-stage retrieval.
Unlike a bi-encoder, no representation can be precomputed, so cost is linear in
candidates.

## Why Does It Exist?

The efficiency-quality trade in retrieval is unavoidable. Bi-encoders precompute
document vectors and search millions in milliseconds, at the cost of never
letting query and document interact. Cross-encoders interact fully and cannot be
precomputed. Using both in sequence takes the strengths of each.

## What Problem Does It Solve?

Precision at the top of the ranking — which is all that matters, because only the
top few passages reach the model's context.

## How Does It Work?

```text
STAGE 1 (recall)                    STAGE 2 (precision)
1M passages                          top 50 candidates
    │ bi-encoder, ANN index              │ cross-encoder: [query][SEP][passage]
    │ ~10ms                              │ ~50 forward passes
    ▼                                    ▼
 top 50 (imprecise order)            top 5, properly ordered ──▶ LLM
```

Stage one optimises recall — get the right passage *somewhere* in fifty. Stage
two optimises precision — get it into the top five.

## Mental Model

Sifting then reading. The sieve is fast and rough; you only read closely what
survives it.

## Example

The failure a reranker fixes is specific and common: the correct passage is
retrieved at rank 23, the model is given the top 5, and the answer is wrong even
though retrieval "worked". Measuring recall@50 and precision@5 separately is how
you diagnose it — if recall@50 is high and answers are poor, you need reranking,
not a better embedding model.

## Real-World Usage

Standard in serious RAG systems, available as hosted reranking APIs and as
open-weight cross-encoder models. Increasingly an LLM itself is used as the
reranker by scoring relevance directly, which is more capable and considerably
more expensive.

ColBERT sits between the two designs: it keeps per-token embeddings and computes
a cheap late interaction, recovering much of the cross-encoder's quality at
closer to bi-encoder cost, in exchange for a much larger index.

## Common Confusions

* **Reranking does not improve recall** — it cannot surface a passage that stage
  one never retrieved. If the answer is not in the candidate set, nothing
  downstream helps.
* **Reranker vs embedding model** — different architectures for different jobs:
  one scores a pair, the other represents an item.
* **Latency is real** — reranking fifty candidates adds tens to hundreds of
  milliseconds. Tune $k$ against your latency budget.

## Why Should I Care?

It is typically the highest-return single addition to a mediocre RAG pipeline,
and it is one line of code plus a measurable improvement you can demonstrate on
your own evaluation set.

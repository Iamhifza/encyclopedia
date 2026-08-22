---
term: Chunking
aliases: [Text Splitting, Semantic Chunking, Contextual Retrieval, Passage Segmentation]
category: rag-knowledge
subcategory: pipelines
depth: full
status: established
difficulty: intermediate
one_liner: "Cutting documents into passages small enough to retrieve precisely and large enough to still make sense on their own."
tags: [retrieval]
relations:
  part_of: [rag]
  related_to: [embedding, context-window, dense-retrieval, reranking]
prerequisites: [rag, embedding]
encountered_in: [production-systems, github, technical-blogs]
sources:
  - type: post
    title: "Introducing Contextual Retrieval"
    url: https://www.anthropic.com/news/contextual-retrieval
    year: 2024
  - type: paper
    title: "Dense Passage Retrieval for Open-Domain Question Answering"
    url: https://arxiv.org/abs/2004.04906
    year: 2020
updated: 2026-08-21
---

## Simple Explanation

You cannot embed a 300-page manual as one vector — it would mean everything and
nothing. So you cut it up. But cut too small and a passage loses the context that
made it meaningful; cut too large and the vector blurs across several topics and
matches nothing precisely.

This unglamorous decision is, in practice, one of the largest determinants of
whether a RAG system works.

## Technical Definition

Segmentation of documents into retrievable units, parameterised by size, overlap
and boundary strategy. Approaches range from fixed token counts, through
structure-aware splitting on headings and paragraphs, to semantic chunking that
places boundaries where embedding similarity between adjacent sentences drops.

## Why Does It Exist?

Embeddings compress a passage into one fixed-size vector. That compression is
lossy in proportion to how much the passage covers, so retrieval precision is
bounded by how coherent each chunk is.

## What Problem Does It Solve?

The tension between precision (small chunks match specific questions) and
sufficiency (the retrieved text must actually contain enough to answer).

## How Does It Work?

```text
TOO SMALL                      TOO LARGE
"...rate is 4.5%."             [entire 40-page policy document]
   4.5% of what?                 vector averages everything → matches nothing

STRUCTURE-AWARE + OVERLAP
┌── section heading ──────────────────┐
│ chunk 1: ~500 tokens                │
│        ┌─ 50-token overlap ─┐       │
│        │ chunk 2: ~500 tokens ──────┤
└────────┴────────────────────────────┘
overlap stops answers being severed at a boundary
```

## Mental Model

Cutting a film into scenes rather than into equal-length strips. The right
boundaries are where the subject changes, not where the ruler falls.

## Example

**Contextual retrieval** is the technique that most improved this recently: before
embedding, prepend a short LLM-generated line situating the chunk in its
document — "This section of the 2024 annual report discusses European segment
revenue." The chunk now carries its own context, and reported retrieval failure
rates fall substantially. It costs one cheap model call per chunk at index time
and nothing at query time.

## Real-World Usage

Every RAG pipeline. Sensible defaults: split on document structure first
(headings, sections, code functions), aim for 300–800 tokens, add 10–20% overlap,
attach metadata (source, section, date, permissions) to every chunk, and store
the surrounding context so you can expand a hit before sending it to the model.

## Common Confusions

* **Chunking (RAG) vs chunked prefill (serving)** — entirely unrelated
  mechanisms that share a word. One splits documents for retrieval; the other
  splits prompts for scheduling.
* **Semantic chunking is not automatically better** — it costs more and, in
  several published comparisons, does not reliably beat well-tuned structural
  splitting. Measure it.
* **Retrieved chunk need not equal indexed chunk** — a common and effective
  pattern is to embed small precise chunks but return their larger parent section
  to the model.

## Why Should I Care?

When a RAG system returns nothing useful, chunking is one of the first two places
to look — and unlike model choice, it is entirely under your control and cheap to
iterate on.

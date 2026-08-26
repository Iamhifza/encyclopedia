---
term: Chunking
aliases: [Text Splitting, Semantic Chunking, Contextual Retrieval, Passage Segmentation]
category: rag-knowledge
subcategory: pipelines
depth: full
status: established
difficulty: intermediate
one_liner: "Cutting documents into passages small enough to retrieve precisely and large enough to still make sense on their own."
historical_period: foundation-model
diagram:
  kind: steps
  title: Chunk size is a retrieval decision, not a formatting one
  footer: Chunking is the cheapest lever in a RAG system and the one most often left at its default. Measure
    recall@k against two or three sizes before tuning anything else.
  steps:
  - title: Both ends of the range fail, for opposite reasons
    visual:
      kind: columns
      width: 700
      columns:
      - title: Too small
        tone: bad
        lines:
        - '"…the rate is 4.5%."'
        - 4.5% of what?
        - retrieved, and still useless
      - title: Too large
        tone: bad
        lines:
        - an entire 40-page policy
        - one vector averages all of it
        - matches nothing in particular
  - title: Split on structure, then overlap the seams
    notes:
    - label: Why overlap
      text: an answer that straddles a boundary survives in at least one chunk
    visual:
      kind: segments
      width: 700
      label: one section, chunked
      caption: the overlap is duplicated on purpose — it is cheap, and losing an answer at a seam is not
      segments:
      - text: chunk 1
        value: 500
        value_label: ~500 tok
      - text: overlap
        value: 50
        tone: accent
      - text: chunk 2
        value: 500
        value_label: ~500 tok
      - text: overlap
        value: 50
        tone: accent
      - text: chunk 3
        value: 500
        value_label: ~500 tok
      spans:
      - from: 0
        to: 2
        text: what chunk 2's embedding actually sees
tags: [retrieval]
relations:
  part_of: [rag]
  related_to: [embedding, context-window, dense-retrieval, reranking]
prerequisites: [embedding]
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


Split on structure first — headings, sections, paragraph boundaries, function
definitions — and only fall back to a fixed token count when the document has no
structure to follow. A chunk should be the smallest span that still carries its
own context, which is a property of the document, not a number you can set once
and reuse everywhere.

Then overlap the boundaries by roughly a tenth of the chunk size. Duplicated
tokens are cheap; an answer severed in half by a boundary is not retrievable at
any *k*. Attach the document title and section heading to each chunk as a prefix
too — it costs a few tokens and rescues chunks whose own text is ambiguous.

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

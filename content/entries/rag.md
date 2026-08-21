---
term: RAG
aliases: [Retrieval-Augmented Generation, Retrieval Augmentation]
category: rag-knowledge
subcategory: pipelines
status: established
difficulty: intermediate
one_liner: Looking up relevant documents and putting them in the prompt, so the model answers from real sources rather than from memory.
origin:
  year: 2020
  attribution: Lewis et al., Facebook AI Research
historical_period: foundation-model
tags: [retrieval]
relations:
  depends_on: [dense-retrieval, embedding, context-window, large-language-model]
  successor_of: [information-retrieval]
  evolved_into: [agentic-rag]
  alternative_to: [supervised-fine-tuning]
  solves: [hallucination]
  used_by: [ai-agent]
prerequisites: [embedding, large-language-model]
encountered_in: [production-systems, job-descriptions, github, conferences]
sources:
  - type: paper
    title: "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks"
    url: https://arxiv.org/abs/2005.11401
    year: 2020
  - type: paper
    title: "Dense Passage Retrieval for Open-Domain Question Answering"
    url: https://arxiv.org/abs/2004.04906
    year: 2020
  - type: post
    title: "Introducing Contextual Retrieval"
    url: https://www.anthropic.com/news/contextual-retrieval
    year: 2024
updated: 2026-08-21
review_by: 2027-02-01
---

## Simple Explanation

The model only knows what was in its training data, which is frozen and does not
include your company's documents. So before answering, search your documents for
the relevant passages and paste them into the prompt. The model then answers from
text it can actually see.

## Technical Definition

A pipeline that conditions generation on passages retrieved at inference time
from an external corpus. The corpus is chunked, indexed (sparse, dense or both),
queried per request, optionally reranked, and the top-$k$ passages are inserted
into the context with instructions to answer from them and cite them.

## Why Does It Exist?

Parametric knowledge has three defects: it is frozen at the training cutoff, it
cannot be audited or attributed, and it cannot be scoped to a particular user's
permissions. Retrieval fixes all three without touching the weights.

## What Problem Does It Solve?

Answering over private, current or verifiable information — and providing
citations, which is often the actual product requirement.

## How Does It Work?

```text
INDEX (offline)                    QUERY (per request)
documents                          user question
   │ chunk                             │ rewrite / expand
   │ embed + index (dense + BM25)      │ embed
   ▼                                   ▼
 vector store + inverted index ◀── hybrid search
                                       │ top-50
                                       ▼ rerank (cross-encoder)
                                    top-5 passages
                                       │
                          prompt: [instructions][passages][question]
                                       ▼
                                LLM ──▶ grounded answer + citations
```

## Mental Model

An open-book exam. The book does not make the student smarter; it makes them
accountable, current, and able to show where the answer came from.

## Example

A support assistant over 50,000 help articles. Question: "does the enterprise
plan include SSO?" Retrieval pulls the three passages that mention SSO and
plan tiers; the model answers from those and cites them. Nothing about SSO needed
to be in its training data.

## Real-World Usage

The most common production LLM pattern. Serious deployments look less like the
diagram and more like an information retrieval project: hybrid sparse-plus-dense
search, query rewriting, semantic or contextual chunking, cross-encoder
reranking, metadata filters for permissions, and retrieval metrics measured
independently of generation quality.

## Evolution

```text
IR → BM25 → dense retrieval → vector DB → naive RAG
   → hybrid + reranking → contextual retrieval → GraphRAG → agentic RAG
```

## Common Confusions

* **RAG vs fine-tuning** — retrieval supplies *facts*, fine-tuning teaches
  *behaviour*. Most teams that fine-tuned to add knowledge should have retrieved.
* **RAG does not eliminate hallucination** — it reduces it when retrieval
  succeeds. If the passages are wrong or missing, a fluent wrong answer is still
  available, which is why grounding instructions and citation checks matter.
* **"RAG is dead because of long context"** — long context is expensive, slower,
  degrades in the middle, and offers no permission filtering or attribution.
  Retrieval selects; context holds. They compose.
* **Retrieval quality is the bottleneck** — if the right passage is not in the
  top-$k$, no prompt engineering will save the answer. Measure recall@k first.

## Why Should I Care?

It is the default architecture for putting an LLM to work on real organisational
knowledge, and its failures are diagnosable with fifty-year-old retrieval
metrics rather than guesswork.

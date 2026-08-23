---
term: RAG
aliases: [Retrieval-Augmented Generation, Retrieval Augmentation]
category: rag-knowledge
subcategory: pipelines
depth: full
status: established
difficulty: intermediate
one_liner: Looking up relevant documents and putting them in the prompt, so the model answers from real sources rather than from memory.
origin:
  year: 2020
  attribution: Lewis et al., Facebook AI Research
historical_period: foundation-model
tags: [retrieval]
relations:
  depends_on: [dense-retrieval, bm25, hybrid-retrieval, embedding, chunking, context-window, large-language-model]
  successor_of: [information-retrieval]
  evolved_into: [agentic-rag, graphrag]
  alternative_to: [supervised-fine-tuning, long-context-model]
  solves: [hallucination]
  used_by: [ai-agent, coding-agent]
  related_to: [reranking, grounding, vector-database, continual-learning]
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
  - type: book
    title: "Introduction to Information Retrieval"
    url: https://nlp.stanford.edu/IR-book/
    year: 2008
    note: The retrieval half of RAG is fifty years old and this is still the reference.
updated: 2026-08-22
review_by: 2027-02-01
---

## Simple Explanation

The model only knows what was in its training data, which is frozen, public, and
does not include your company's documents. So before answering, search your
documents for the relevant passages and paste them into the prompt. The model
then answers from text it can actually see, and can cite where each claim came
from.

The idea is almost embarrassingly simple. Nearly all the difficulty is in the
search, which is why teams who treat this as a prompting problem struggle and
teams who treat it as an information retrieval problem succeed.

## Technical Definition

A pipeline conditioning generation on passages retrieved at inference time from
an external corpus. The corpus is [chunked](chunking.md), indexed
([sparse](bm25.md), [dense](dense-retrieval.md) or
[both](hybrid-retrieval.md)), queried per request, optionally
[reranked](reranking.md), and the top-$k$ passages are inserted into the
[context](context-window.md) with instructions to answer from them and cite them.

## Why Does It Exist?

Parametric knowledge has three defects that no amount of scale fixes. It is
frozen at the training cutoff. It cannot be attributed or audited. And it cannot
be scoped to a particular user's permissions.

Retrieval fixes all three without touching the weights — which matters
enormously, because [updating weights incrementally](continual-learning.md) still
does not work.

## What Problem Does It Solve?

Answering over private, current or verifiable information — and providing
citations, which is very often the actual product requirement rather than a nice
extra.

## How Does It Work?

```text
INDEX (offline)                     QUERY (per request)
documents                           user question
   │ chunk, with context               │ rewrite / expand
   │ embed  +  BM25 index              │ embed
   ▼                                   ▼
 vector store + inverted index ◀── HYBRID search
   │  metadata: source, date,          │ top-50 candidates
   │  permissions                      ▼
   │                              RERANK (cross-encoder)
   │                                   │ top-5
   │                                   ▼
   └──────────────▶ prompt: [instructions][passages][question]
                                       ▼
                          LLM ──▶ grounded answer + citations
                                       │
                          measure: recall@k · groundedness · answer quality
```

Note what is *not* in that diagram: anything clever about prompting. The prompt
is the easy part.

## Mental Model

An open-book exam. The book does not make the student cleverer — it makes them
accountable, current, and able to show their working.

## Example

A support assistant over 50,000 help articles. Question: *"does the enterprise
plan include SSO?"* Retrieval pulls the three passages mentioning SSO and plan
tiers; the model answers from those and cites them. Nothing about SSO needed to
be in its training data, the answer updates the moment the article does, and a
reader can check it.

Now the failure that teaches the most: retrieval returns three passages about SSO
on the *legacy* plan, because the current article uses the phrase "single
sign-on" and the query said "SSO". The model answers confidently and wrongly. No
prompt fixes this. Hybrid retrieval does, because BM25 matches the acronym
exactly while the dense half matches the meaning.

## Real-World Usage

The most common production LLM pattern. Serious deployments look far less like
the naive diagram and far more like an information retrieval project:

* **[Hybrid retrieval](hybrid-retrieval.md)** — sparse and dense, fused. The
  single highest-return addition to a mediocre pipeline.
* **[Reranking](reranking.md)** — a cross-encoder over the top 50.
* **[Contextual chunking](chunking.md)** — a line of generated context prepended
  to each chunk before embedding.
* **Metadata filters** — permissions applied at query time, which
  [long context](long-context-model.md) cannot do at all.
* **[Groundedness](grounding.md) measured separately from answer quality**,
  because an answer can be right and unsupported.

## Evolution

```text
IR → TF-IDF → BM25 → dense retrieval → vector DB → naive RAG
   → hybrid + reranking → contextual retrieval → GraphRAG → agentic RAG
```

## Common Confusions

* **RAG vs fine-tuning** — retrieval supplies *facts*, fine-tuning teaches
  *behaviour*. Most teams who fine-tuned to add knowledge should have retrieved.
  See [RAG vs Fine-Tuning](../compare/rag-vs-fine-tuning.md).
* **RAG vs long context** — retrieval *selects*; context *holds*. Long context
  cannot filter by permission or attribute claims. See
  [RAG vs Long Context](../compare/rag-vs-long-context.md).
* **RAG does not eliminate hallucination** — it reduces it when retrieval
  succeeds, and can worsen it when retrieved passages are wrong, because they
  lend false authority.
* **Retrieval quality is the ceiling** — if the right passage is not in the
  top-$k$, no prompt engineering saves the answer. Measure recall@k *first*; it
  is the fastest way to find out whether your problem is retrieval or generation.

## Why Should I Care?

It is the default architecture for putting a model to work on real organisational
knowledge, and — unusually in this field — its failures are diagnosable with
fifty-year-old metrics rather than guesswork.

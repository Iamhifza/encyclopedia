---
term: Agentic RAG
aliases: [Agentic Retrieval, Iterative RAG, Search Agent]
category: rag-knowledge
subcategory: pipelines
status: emerging
difficulty: advanced
one_liner: Letting the model decide when and what to search, and search repeatedly, instead of retrieving once before it answers.
origin:
  year: 2024
  circa: true
  attribution: Emerged from combining tool-calling agents with retrieval; no single originating paper
historical_period: agentic
diagram:
  kind: flow
  title: Retrieval as a decision, not a fixed first step
  loop: not enough evidence — reformulate and search again, or search somewhere else
  footer: Better recall on questions that need several hops, at several times the cost and latency of
    one-shot retrieval. Worth it when the questions genuinely need it; expensive theatre when they do
    not.
  nodes:
  - title: Question
    note: and the conversation so far
    caption: search may not be needed
  - title: Query
    note: written by the model, not copied
    caption: possibly several
  - title: Read
    note: what came back
    caption: and judge it
  - title: Answer
    note: with citations
    accent: true
    caption: or say it could not find out
tags: [retrieval, agents]
relations:
  successor_of: [rag]
  depends_on: [ai-agent, tool-calling, rag]
  related_to: [reasoning-model, agent-loop]
prerequisites: [rag, ai-agent]
encountered_in: [production-systems, technical-blogs, github]
sources:
  - type: paper
    title: "Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection"
    url: https://arxiv.org/abs/2310.11511
    year: 2023
  - type: paper
    title: "ReAct: Synergizing Reasoning and Acting in Language Models"
    url: https://arxiv.org/abs/2210.03629
    year: 2022
updated: 2026-08-21
review_by: 2027-02-01
---

## Simple Explanation

Classic RAG retrieves once, using the user's original wording, and hopes the
right passages come back. Agentic RAG treats search as a tool the model can call:
it can rephrase the query, search again after reading, follow a reference, search
a different source, and decide it has enough.

## Technical Definition

Retrieval embedded inside an agent loop, where the model chooses whether to
retrieve, formulates queries, evaluates returned passages, and iterates until a
stopping condition. Variants add self-critique of retrieved relevance,
decomposition into sub-questions, and routing across multiple indexes.

## Why Does It Exist?

Single-shot retrieval fails on questions that need several pieces of evidence,
on comparisons, and on anything where the user's phrasing does not resemble the
source text. A fixed pipeline cannot recover from a bad first search.

## What Problem Does It Solve?

Multi-hop questions, query-document mismatch, and knowing when retrieval is not
needed at all.

## How Does It Work?


Ordinary RAG retrieves once, with the user's question as the query, and
generates from whatever comes back. Agentic RAG makes each of those a decision
the model gets to take.

It decides whether to search at all — many questions are answerable from the
conversation. It writes the query rather than reusing the question, which matters
because the wording that asks a thing is rarely the wording that finds it. It
reads what returned and judges whether the evidence is sufficient. And if it is
not, it reformulates, searches a different source, or decomposes the question and
searches for the parts.

That loop is what handles multi-hop questions, where the answer requires
combining facts no single passage contains. The cost is real: several retrieval
rounds and several model calls where one-shot RAG makes one of each, with latency
to match. Worth it when the questions genuinely need more than one hop, and
expensive theatre when they do not.

## Mental Model

A researcher rather than a lookup table: reads a result, notices a gap, adjusts
the search, and knows when to stop.

## Example

"How did our refund policy change between the 2023 and 2025 handbooks?" needs two
retrievals against different documents and a comparison. One-shot retrieval
returns a mixed bag from both and usually produces a confident, wrong summary.

## Real-World Usage

Deep-research features, coding agents searching a codebase, and support agents
that consult several systems. The cost profile is very different from classic
RAG: several model calls and several retrievals per answer, so latency and spend
rise substantially.

## Terminology Note

The label is recent and loosely applied. Some use it for any retrieval with query
rewriting; others reserve it for a full agent loop with tool choice and
self-evaluation. When you see it in a vendor description, ask which one is meant.

## Common Confusions

* **Agentic RAG vs RAG** — the difference is control: who decides what to
  retrieve, and how many times.
* **More loops is not better** — unbounded search loops burn tokens and can drift.
  Step limits and stopping criteria are load-bearing.
* **It does not fix a bad index** — if the corpus is poorly chunked, iterating
  just fails repeatedly and more expensively.

## Why Should I Care?

It is where retrieval and agents converge, and it is the current default design
for research-style question answering over messy real corpora.

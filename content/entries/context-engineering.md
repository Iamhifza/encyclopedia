---
term: Context Engineering
aliases: [Context Management, Context Assembly, Context Curation]
category: agent-engineering
subcategory: context
status: emerging
difficulty: intermediate
one_liner: Deciding what goes into the model's context window at each step, and in what order, so it has exactly what it needs and little else.
origin:
  year: 2024
  circa: true
  attribution: Named in practitioner writing during 2024-2025 as agent context budgets became the binding constraint; no single originator
historical_period: agentic
tags: [agents, culture, retrieval]
relations:
  successor_of: [prompt-engineering]
  different_from: [prompt-engineering]
  depends_on: [context-window, rag, agent-memory]
  part_of: [harness]
  used_by: [coding-agent, ai-agent]
  related_to: [prefix-caching, scaffold]
prerequisites: [context-window, prompt-engineering]
encountered_in: [technical-blogs, job-descriptions, github, social-media, conferences]
sources:
  - type: post
    title: "Effective context engineering for AI agents"
    url: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
    year: 2025
  - type: paper
    title: "Lost in the Middle: How Language Models Use Long Contexts"
    url: https://arxiv.org/abs/2307.03172
    year: 2023
updated: 2026-08-21
review_by: 2026-12-01
---

## Simple Explanation

A prompt used to be something you wrote once. In an agent it is assembled fresh
every step out of a system prompt, tool definitions, retrieved documents,
previous tool results, memory and the conversation so far — and it must fit in a
budget while keeping the important things where the model actually attends.
Deciding what goes in, what gets summarised and what gets dropped is the work.

## Technical Definition

The run-time policy governing the contents of the context window: selection of
retrieved material, ordering for cache and attention effects, compaction and
summarisation as the window fills, externalisation of state to files or memory,
and pruning of stale tool output. Optimised jointly for task accuracy, token cost
and prefix cache hit rate.

## Why Does It Exist?

Two forces made prompt-as-a-string obsolete. Agent loops accumulate context
automatically, so the window fills whether you plan for it or not; and long
contexts degrade — models attend unevenly, and irrelevant material measurably
hurts accuracy. Neither problem is solved by better wording.

## What Problem Does It Solve?

Context exhaustion in long-running agents, quality loss from diluted or badly
ordered context, and the token cost of resending everything each turn.

## How Does It Work?

```text
┌─ stable, cacheable ────────────────────────────────────────┐
│ system prompt · tool schemas · project conventions         │  ← rarely changes
├─ selected ────────────────────────────────────────────────┤
│ retrieved passages · relevant memory · file excerpts       │  ← chosen per step
├─ volatile ────────────────────────────────────────────────┤
│ recent turns · latest tool results · current instruction   │  ← changes always
└────────────────────────────────────────────────────────────┘

when full:  summarise older turns · write state to a file ·
            drop superseded tool output · keep the plan
```

Stable content first is not stylistic: it is what makes prefix caching hit.

## Mental Model

Packing for a trip with a strict weight limit. The skill is not in owning more
things; it is in choosing correctly, and in knowing what can be posted ahead
(written to a file) instead of carried.

## Example

A coding agent thirty steps into a task has 200k tokens of accumulated file reads
and test output. Naive approach: send it all, hit the limit, fail. Engineered:
keep the system prompt and plan, summarise steps 1-20 into a paragraph of
findings, retain the last three tool results in full, and store the rest in a
scratch file the agent can re-read on demand.

## Terminology Note

The term is recent and its boundaries are soft. Some use it narrowly for context
window budgeting; others for everything from retrieval strategy to memory design.
It overlaps substantially with [harness](harness.md) work and with retrieval
engineering. It is best read as marking a shift in *scope* — from writing one
prompt to designing a dynamic assembly process — rather than as a new technique.
Whether it needed its own name is a reasonable disagreement; that the underlying
problem is real is not.

## Real-World Usage

Compaction and summarisation in long agent sessions; project convention files
that agents read at startup; just-in-time retrieval instead of preloading; tool
results trimmed before they enter context; deliberate ordering for cache hits.

## Common Confusions

* **Context engineering vs prompt engineering** — dynamic assembly of everything
  the model sees, versus authoring one instruction. The second is now a part of
  the first.
* **"Long context makes it unnecessary"** — a bigger budget spent carelessly is
  slower, dearer, and often less accurate. The constraint moved; it did not go.
* **More context is not better** — irrelevant material demonstrably reduces
  accuracy.

## Why Should I Care?

In production agent systems this is where most quality and most cost live. Two
teams with the same model and the same tools will differ mainly here.

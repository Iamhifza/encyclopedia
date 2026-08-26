---
term: Multi-Agent System
aliases: [MAS, Sub-Agents, Agent Swarm]
category: agents
subcategory: topologies
status: emerging
difficulty: advanced
one_liner: Several agents with separate roles and contexts working on one task, usually coordinated by an orchestrator.
origin:
  year: 1980
  circa: true
  attribution: A classical distributed-AI field; the LLM sense dates from 2023 projects such as AutoGen and CAMEL
historical_period: agentic
diagram:
  kind: figure
  title: One lead, several workers, separate contexts
  footer: Worth it when subtasks are genuinely independent and each needs its own long context. Not worth
    it when they are not — you have then bought coordination overhead, duplicated cost and a harder failure
    to debug.
  visual:
    kind: fan
    source: lead
    caption: each worker has its own window and its own tools; only results come back
    targets:
    - text: search docs
      new: true
    - search code
    - check facts
    - draft output
tags: [agents]
relations:
  depends_on: [ai-agent]
  used_by: [a2a]
  related_to: [agent-memory, ai-workflow]
prerequisites: [ai-agent]
encountered_in: [research-papers, github, conferences, social-media]
sources:
  - type: paper
    title: "AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation"
    url: https://arxiv.org/abs/2308.08155
    year: 2023
  - type: post
    title: "How we built our multi-agent research system"
    url: https://www.anthropic.com/engineering/built-multi-agent-research-system
    year: 2025
updated: 2026-08-21
review_by: 2026-12-01
---

## Simple Explanation

Instead of one agent doing everything, split the work: one plans, several search
different sources in parallel, one writes up the result. Each has its own context
window, which is often the real reason to split — not role-play, but context
budget.

## Technical Definition

An architecture in which multiple LLM-driven agents with distinct prompts, tools
and context windows coordinate on a shared objective, typically under an
orchestrator-worker topology, with results returned to a lead agent for
synthesis.

## Why Does It Exist?

Two hard limits push in the same direction: a single context window fills up, and
independent subtasks can run in parallel. Sub-agents give isolation for the first
and concurrency for the second.

## What Problem Does It Solve?

Context isolation for subtasks, parallel exploration of a broad problem, and
specialised tool sets per role.

## How Does It Work?


A lead agent decomposes a task, hands the pieces to workers, and combines what
comes back. Each worker runs with its own context window and its own tools, and
returns only a result — its intermediate reasoning never enters the lead's
context, which is the entire point.

That isolation is what the pattern buys. Three research questions can each burn a
hundred thousand tokens of searching without any of them crowding out the others,
because they are not sharing a window. Genuinely independent subtasks also run
concurrently rather than sequentially.

It costs more than it looks. Every worker re-reads the shared background, so
token spend multiplies rather than divides. Errors compound across handoffs, and
a wrong decomposition cannot be recovered by workers that only see their own
slice. Debugging means reconstructing several conversations at once. The
honest test is whether the subtasks are genuinely independent and genuinely need
their own long contexts — and when they are not, one agent with a good harness
usually wins.

## Mental Model

A research lead assigning parallel literature searches and writing the summary —
useful when the sub-questions are independent, wasteful when they are not.

## Example

Anthropic's published multi-agent research system used substantially more tokens
than single-agent runs, with the gain coming from parallel breadth-first search
across many sources. That is the honest trade: more spend for more coverage,
worth it only when the task genuinely fans out.

## Terminology Note

Usage is unsettled. "Multi-agent" covers everything from an orchestrator with
sub-agents, to peer agents negotiating, to a single loop with several prompt
personas — which is not meaningfully multi-agent at all. "Sub-agent" and "agent
as a tool" describe the same mechanism from different angles.

## Real-World Usage

Research assistants that fan out across sources, orchestrator-worker patterns in
agent frameworks, and pipelines where a lead agent delegates isolated subtasks to
keep its own context clean.

## Common Confusions

* **More agents is not more capability** — coordination overhead, token cost and
  error propagation all rise. Many multi-agent designs underperform one good
  agent with a well-managed context.
* **Personas are not specialisation** — telling the same model it is a "senior
  architect" does not create expertise. Separate tools and separate context do.
* **Shared state is the hard part** — most failures are agents working from
  inconsistent views of the task.

## Why Should I Care?

It is heavily marketed and frequently the wrong choice. The useful question is
whether the subtasks are genuinely independent, and whether the token bill is
justified by parallel coverage.

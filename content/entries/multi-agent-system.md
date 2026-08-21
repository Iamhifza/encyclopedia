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

```text
              ┌── orchestrator: decompose, delegate, synthesise ──┐
              │        │              │              │            │
          sub-agent A  sub-agent B  sub-agent C   (own context,   │
          search docs  search code  check facts    own tools)     │
              └────────┴──────────────┴───── results ─────────────┘
```

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

---
term: AI Workflow
aliases: [LLM Workflow, Orchestrated Pipeline, Chain]
category: agents
subcategory: core
status: established
difficulty: beginner
one_liner: A predefined sequence of model calls and tool steps written by a developer, rather than a path the model chooses at run time.
origin:
  year: 2022
  circa: true
  attribution: Popularised by prompt-chaining frameworks; sharpened as a contrast to agents from 2024
historical_period: agentic
tags: [agents]
relations:
  different_from: [ai-agent]
  alternative_to: [ai-agent]
  depends_on: [large-language-model]
  related_to: [evaluation-harness]
prerequisites: [large-language-model]
encountered_in: [production-systems, technical-blogs, job-descriptions]
sources:
  - type: post
    title: "Building Effective Agents"
    url: https://www.anthropic.com/engineering/building-effective-agents
    year: 2024
updated: 2026-08-21
---

## Simple Explanation

You already know the steps: extract the fields, look them up, draft the reply,
check it. So write them down as code that calls the model at each step. The model
does the parts that need judgement; the sequence is fixed.

## Technical Definition

An orchestration in which control flow is determined by application code, with
LLM calls as steps. Common patterns include prompt chaining, routing to
specialised prompts, parallel sectioning and voting, and evaluator-optimiser
loops with fixed structure.

## Why Does It Exist?

Most business tasks have a known shape. Handing that shape to a model to
rediscover on every request adds cost, latency and variance for no benefit.

## What Problem Does It Solve?

Reliability and predictability, plus the ability to test each step in isolation.

## How Does It Work?

```text
input ──▶ [classify] ──▶ [route] ──┬─▶ [summarise] ──▶ [validate] ──▶ output
                                   └─▶ [extract]   ──▶ [validate] ──▶ output
   every arrow written by a developer; nothing is chosen at run time
```

## Mental Model

A recipe versus a chef. The recipe is repeatable and auditable; the chef is
needed only when you do not know in advance what the dish is.

## Example

Invoice processing: extract fields, validate against a schema, look up the
supplier, flag anomalies, write to the ledger. Every run takes the same path. An
agent here would be slower, dearer and less predictable, with no upside.

## Real-World Usage

The majority of successful production LLM systems are workflows, not agents,
even when marketed as agents. The standard advice from practitioners is to start
with a workflow and adopt agent autonomy only where the task shape genuinely
varies.

## Common Confusions

* **Workflow vs agent** — who decides the next step. Code, or the model.
* **A workflow can contain an agent** — one step of a fixed pipeline may be an
  agentic sub-task, which is often the best of both.
* **"Agentic workflow"** — a widely used phrase that blurs exactly the
  distinction worth keeping. Ask whether the model can deviate from the sequence.

## Why Should I Care?

Choosing a workflow when a workflow suffices is the single most reliable way to
ship something that works, and the most common piece of advice from teams who
tried the alternative first.

---
term: Orchestration
aliases: [Orchestrator, Agent Orchestration, Workflow Orchestration]
category: agents
subcategory: topologies
depth: full
status: contested
disputed: true
difficulty: intermediate
one_liner: "The layer that decides which model, agent or tool handles each part of a task, and in what order."
origin:
  year: 2023
  circa: true
  attribution: Borrowed from container and workflow orchestration; applied loosely to LLM systems from 2023 onward
historical_period: agentic
tags: [agents]
relations:
  part_of: [multi-agent-system, harness]
  related_to: [ai-workflow, model-routing, ai-stack, agent-loop]
prerequisites: [ai-agent, ai-workflow]
encountered_in: [job-descriptions, technical-blogs, production-systems, conferences]
sources:
  - type: post
    title: "Building Effective Agents"
    url: https://www.anthropic.com/engineering/building-effective-agents
    year: 2024
  - type: post
    title: "How we built our multi-agent research system"
    url: https://www.anthropic.com/engineering/built-multi-agent-research-system
    year: 2025
updated: 2026-08-21
review_by: 2026-12-01
---

## Simple Explanation

Once a system has more than one model, more than one agent, or more than one
step, something has to decide what runs when and what gets passed along. That
coordinating layer is called orchestration.

The trouble is that the word is applied to four quite different things, and the
distinctions matter more than the label does.

## Technical Definition

The coordination layer over multiple components in an AI system: task
decomposition, dispatch to models or sub-agents, sequencing and dependency
management, result aggregation, retry and failure handling, and state passed
between steps.

## Why Does It Exist?

The vocabulary came from Kubernetes and from data-pipeline tools like Airflow,
where orchestration means scheduling work across resources with dependencies.
When LLM systems grew past a single call, engineers reached for the nearest
existing word.

## What Problem Does It Solve?

Coordination — but *which* coordination problem depends entirely on which sense
is meant.

## Terminology Note

Four current usages, frequently conflated:

1. **Workflow orchestration** — a developer-defined sequence of steps, like a
   DAG. Control flow is fixed; this is [AI Workflow](ai-workflow.md).
2. **Agent orchestration** — a lead agent decomposing a task and delegating to
   sub-agents, deciding at run time. This is the orchestrator-worker pattern in
   [multi-agent systems](multi-agent-system.md).
3. **Model orchestration** — dispatching requests among models by cost or
   capability. This is [model routing](model-routing.md).
4. **Marketing** — any framework that calls multiple APIs, positioned as an
   "orchestration platform".

Senses 1 and 2 differ on the question that matters most in agent design: *who
decides the next step, code or the model?* A vendor saying "orchestration"
without answering that has told you nothing. Ask it.

## How Does It Work?

```text
STATIC (sense 1)              DYNAMIC (sense 2)
step1 ──▶ step2 ──▶ step3     lead agent
   fixed, testable,              │ decomposes at run time
   predictable cost              ├─▶ sub-agent A
                                 ├─▶ sub-agent B
                                 └─▶ aggregates, decides what next
```

## Mental Model

A conductor versus a score. Sense 1 is the score — written in advance, played the
same way every time. Sense 2 is the conductor — responding to what is happening
now. Both are called orchestration; only one is improvising.

## Example

"Our orchestration layer handles complex multi-step tasks" describes a `for` loop
over three prompts just as accurately as it describes a lead agent delegating to
parallel sub-agents. The first is cheap and reliable; the second is expensive and
flexible. The sentence does not distinguish them, which is exactly why the term
appears so often in product copy.

## Real-World Usage

Agent frameworks providing sequencing and state management, gateways doing model
dispatch, and internal application code that does neither but gets described this
way in architecture diagrams.

## Common Confusions

* **Orchestration is not automatically an agent** — a fixed pipeline is
  orchestration and involves no autonomy.
* **Frameworks are optional** — a great deal of production orchestration is
  ordinary application code, and often better for being so.
* **More orchestration is not better** — each coordination layer adds latency,
  cost and failure modes.

## Why Should I Care?

It is one of the vaguest words in current AI vocabulary and one of the most
common in job descriptions. Knowing to ask which of the four senses is meant
turns an empty term into a specific technical question.

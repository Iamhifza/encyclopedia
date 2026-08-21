---
term: AI Agent
aliases: [Agent, Agentic AI, Autonomous Agent, LLM Agent]
category: agents
subcategory: core
status: contested
disputed: true
difficulty: intermediate
one_liner: A system where a language model chooses actions, runs them, sees the results, and repeats until a task is done.
origin:
  year: 2022
  circa: true
  attribution: The LLM sense emerged from ReAct and the 2023 wave of autonomous agent projects; "agent" in AI is much older
historical_period: agentic
tags: [agents]
relations:
  depends_on: [large-language-model, tool-calling, agent-loop]
  different_from: [ai-workflow]
  used_by: [coding-agent, agentic-rag, multi-agent-system]
  related_to: [harness, agent-memory, reinforcement-learning]
prerequisites: [large-language-model, tool-calling]
encountered_in: [job-descriptions, production-systems, social-media, conferences, github]
sources:
  - type: paper
    title: "ReAct: Synergizing Reasoning and Acting in Language Models"
    url: https://arxiv.org/abs/2210.03629
    year: 2022
  - type: post
    title: "Building Effective Agents"
    url: https://www.anthropic.com/engineering/building-effective-agents
    year: 2024
  - type: book
    title: "Artificial Intelligence: A Modern Approach — the agent formulation"
    url: https://aima.cs.berkeley.edu/
updated: 2026-08-21
review_by: 2026-12-01
---

## Simple Explanation

A chatbot answers and stops. An agent is given a goal, decides what to do first,
does it with a tool, looks at what came back, decides what to do next, and keeps
going until the goal is met or it gives up. The model is not just producing text —
it is choosing what happens next.

## Technical Definition

A system in which an LLM drives a control loop over an action space: at each
step, the model receives the accumulated context and selects either a tool
invocation or a terminal response. The environment executes the action and
returns an observation, which is appended to the context. Autonomy is the degree
to which the model, rather than fixed code, determines the sequence.

## Why Does It Exist?

Language models can only produce text. Any task requiring current information,
side effects, or verification against the world needs the model to invoke
something outside itself and react to the result.

## What Problem Does It Solve?

Multi-step tasks whose shape is not known in advance — where the second step
depends on what the first one returned.

## How Does It Work?

```text
        ┌──────────────────────────────────────┐
goal ──▶│ model decides: which tool, what args │
        └───────────────┬──────────────────────┘
                        ▼
                 tool executes
                        ▼
              observation appended to context
                        │
        loop until done, blocked, or step limit ──▶ result
```

Everything outside the model — the loop, the tool definitions, the context
assembly, the permissions, the stopping rules — is the harness, and it determines
reliability at least as much as the model does.

## Mental Model

A capable contractor given an objective and a set of keys, rather than a
step-by-step script. What makes the arrangement work is not only the
contractor's skill but the quality of the brief and the limits on the keys.

## Terminology Note

"Agent" is genuinely contested, and the disagreement is not pedantry:

* **Loop-based definition** — any LLM that calls tools in a loop. Broadest, most
  common among engineers.
* **Autonomy-based definition** — the model, not fixed code, decides the path. On
  this view a fixed sequence of LLM calls is a *workflow*, not an agent. This is
  the distinction drawn in Anthropic's "Building Effective Agents" and is the most
  useful line in practice.
* **Classical AI definition** — anything that perceives and acts on an
  environment, which includes a thermostat.
* **Marketing usage** — any LLM feature at all.

The adjective *agentic* is looser still and is frequently applied to systems with
no loop and no tool choice. When someone says "agent", ask who decides the next
step: the model or the code.

## Example

"Find why the checkout tests fail and fix it" — the agent lists files, reads the
failing test, greps for the function, forms a hypothesis, edits, runs the tests,
sees a new failure, and iterates. No fixed pipeline could have been written in
advance, because step four depended on the output of step three.

## Real-World Usage

Coding agents, deep-research tools, customer support automation, computer-use
agents. Production systems constrain sharply: limited tool sets, step budgets,
sandboxes, human approval for irreversible actions, and traces on everything.

## Common Confusions

* **Agent vs chatbot** — the chatbot's output *is* the product; the agent's
  output is a change in the world.
* **Agent vs workflow** — if you drew the sequence in advance, it is a workflow.
  Workflows are more reliable and should be preferred when the task shape is
  known.
* **Autonomy is a dial, not a switch** — most useful production systems sit far
  from full autonomy, with humans in or on the loop.
* **Agents are not more capable models** — the same model with a loop and tools.
  Capability comes from the environment access, and so does the risk.

## Why Should I Care?

It is the organising concept of the current era of AI engineering, and the
vocabulary around it — harness, scaffold, skills, orchestration, sub-agents — only
makes sense once you can see the loop underneath.

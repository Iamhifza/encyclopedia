---
term: AI Agent
aliases: [Agent, Agentic AI, Autonomous Agent, LLM Agent]
category: agents
subcategory: core
depth: full
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
  depends_on: [large-language-model, tool-calling, agent-loop, context-engineering]
  different_from: [ai-workflow]
  used_by: [coding-agent, agentic-rag, multi-agent-system, computer-use]
  related_to: [harness, agent-memory, reinforcement-learning, automated-planning, prompt-injection, guardrails, evaluation-harness]
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
  - type: paper
    title: "SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering"
    url: https://arxiv.org/abs/2405.15793
    year: 2024
  - type: book
    title: "Artificial Intelligence: A Modern Approach — the agent formulation"
    url: https://aima.cs.berkeley.edu/
updated: 2026-08-22
review_by: 2026-12-01
---

## Simple Explanation

A chatbot answers and stops. An agent is given a goal, decides what to do first,
does it with a tool, looks at what came back, decides what to do next, and keeps
going until the goal is met or it gives up.

The model is no longer producing text for you to read. It is choosing what
happens next — and that single change is why agents need an architecture rather
than a prompt.

## Technical Definition

A system in which an LLM drives a control loop over an action space. At each
step the model receives the accumulated context and selects either a
[tool invocation](tool-calling.md) or a terminal response; the environment
executes the action and returns an observation, which is appended to the context.
Autonomy is the degree to which the model, rather than fixed code, determines the
sequence.

## Why Does It Exist?

Language models can only produce text. Any task requiring current information,
side effects, or verification against the world needs the model to invoke
something outside itself and react to the result.

## What Problem Does It Solve?

Multi-step tasks whose shape is not known in advance — where the second step
depends on what the first one returned, and no fixed pipeline could have been
written beforehand.

## How Does It Work?

```text
        ┌──────────────────────────────────────┐
goal ──▶│ model decides: which tool, what args │
        └───────────────┬──────────────────────┘
                        ▼
                 tool executes         ← sandboxed, permissioned
                        ▼
              observation appended to context   ← untrusted input
                        │
        loop until done, blocked, or budget exhausted
```

Everything outside the model is the [harness](harness.md): the loop, the tool
definitions, the [context assembly](context-engineering.md), the
[permissions](guardrails.md), the stopping rules, the
[traces](observability.md). The SWE-agent result is the strongest evidence that
this layer matters — holding the model fixed and redesigning only the interface
it acts through changed task success substantially.

## Mental Model

A capable contractor given an objective and a set of keys, rather than a
step-by-step script. What makes the arrangement work is not only the
contractor's skill but the quality of the brief and the limits on the keys.

## Terminology Note

"Agent" is genuinely contested, and the disagreement is not pedantry:

* **Loop-based** — any LLM that calls tools in a loop. Broadest, most common
  among engineers.
* **Autonomy-based** — the model, not fixed code, decides the path. A fixed
  sequence of LLM calls is then a [workflow](ai-workflow.md), not an agent. This
  is the most useful line in practice and the one this encyclopedia uses.
* **Classical AI** — anything that perceives and acts on an environment, which
  includes a thermostat.
* **Marketing** — any LLM feature at all.

The adjective *agentic* is looser still and is frequently applied to systems with
no loop and no tool choice. When someone says "agent", ask who decides the next
step: the model or the code.

## Example

*"Find why the checkout tests fail and fix it."* The agent lists files, reads the
failing test, greps for the function, forms a hypothesis, edits, runs the tests,
sees a new failure, and iterates. Step four depended on the output of step three,
so no pipeline could have been written in advance.

Now the same capability seen from the other side. That agent read a test file, a
stack trace and possibly a linked issue — all of which are text that entered its
context and could carry [injected instructions](prompt-injection.md). It holds
repository credentials. It can run commands. Those three facts together are why
[sandboxing](sandboxing.md) and [approval gates](human-in-the-loop.md) are not
optional extras.

## Real-World Usage

[Coding agents](coding-agent.md), deep-research tools, customer support
automation, [computer-use agents](computer-use.md). Production systems constrain
sharply: limited tool sets, step and cost budgets, sandboxes, human approval for
irreversible actions, and traces on everything.

The honest summary of the state of practice: agents work well where a
**verifier** exists — tests pass, the schema validates, the query returns rows —
and are much less reliable where success is a matter of judgement. That is why
software engineering became the first commercially proven agent domain.

## Common Confusions

* **Agent vs chatbot** — the chatbot's output *is* the product; the agent's
  output is a change in the world. See
  [Agent vs Chatbot](../compare/agent-vs-chatbot.md).
* **Agent vs workflow** — if you drew the sequence in advance, it is a workflow,
  and workflows are more reliable. Prefer them when the task shape is known. See
  [Agent vs Workflow](../compare/agent-vs-workflow.md).
* **Autonomy is a dial, not a switch** — most useful production systems sit far
  from full autonomy.
* **Agents are not more capable models** — the same model with a loop and tools.
  Capability comes from environment access, and so does the risk.
* **Agent "planning" is not [planning](automated-planning.md)** — a real planner
  verifies preconditions and guarantees a valid sequence. An LLM produces
  plausible text describing a plan.

## Why Should I Care?

It is the organising concept of the current era of AI engineering, and the
vocabulary around it — [harness](harness.md), [scaffold](scaffold.md),
[skills](agent-skills.md), [orchestration](orchestration.md),
[sub-agents](multi-agent-system.md) — only makes sense once you can see the loop
underneath.

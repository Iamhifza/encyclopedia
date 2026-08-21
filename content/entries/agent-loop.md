---
term: Agent Loop
aliases: [ReAct Loop, Perceive-Decide-Act Loop, Tool Loop]
category: agents
subcategory: core
status: established
difficulty: intermediate
one_liner: The repeating cycle of thinking, acting with a tool, and observing the result that drives every agent.
origin:
  year: 2022
  attribution: Formalised for LLMs by the ReAct paper; the sense-plan-act cycle is decades old in robotics
historical_period: agentic
tags: [agents]
relations:
  part_of: [ai-agent]
  depends_on: [tool-calling]
  used_by: [coding-agent, agentic-rag, harness]
  related_to: [prefix-caching, context-window]
prerequisites: [tool-calling]
encountered_in: [github, production-systems, research-papers]
sources:
  - type: paper
    title: "ReAct: Synergizing Reasoning and Acting in Language Models"
    url: https://arxiv.org/abs/2210.03629
    year: 2022
updated: 2026-08-21
---

## Simple Explanation

Think, act, look, repeat. The model reasons about what to do, calls a tool, and
the tool's output is appended to the conversation. Then the model runs again with
that new information. That cycle, and the rules for exiting it, is the whole
mechanism.

## Technical Definition

An iterative control loop: assemble context, invoke the model, parse its output
into either a tool call or a final answer, execute the call, append the
observation, and repeat subject to termination conditions (task complete, step
budget exhausted, error threshold, human interrupt).

## Why Does It Exist?

A single model call cannot recover from a wrong assumption, because it never
finds out that it was wrong. The loop introduces feedback.

## What Problem Does It Solve?

Error recovery and adaptation. The value is less in taking the right action first
than in noticing that an action failed and trying something else.

## How Does It Work?

```text
context = [system prompt][tools][history]
repeat:
    response = model(context)
    if response is final:  return it
    result = execute(response.tool_call)      ← may fail, time out, be denied
    context += [response, result]
    if steps > budget or cost > cap:  stop and report
```

Each iteration grows the context, so a long loop consumes the context window and
the token budget at the same time. That growth is the loop's core engineering
problem.

## Mental Model

A debugging session. Form a hypothesis, run one command, read the output, revise.
Nobody debugs by writing the whole sequence of commands upfront.

## Example

Thirty iterations at 8k tokens of accumulated context each is roughly 240k tokens
of prefill — unless the stable prefix is cached, in which case most of it costs
almost nothing. This is why prefix caching and context layout matter so much to
agent economics.

## Real-World Usage

Every agent framework implements this loop; they differ mainly in how they
assemble context, cap steps, handle errors, checkpoint state and expose traces.

## Common Confusions

* **The loop is not in the model** — the model is stateless and called afresh
  each iteration. The loop lives in your code, which is why it is yours to make
  reliable.
* **Loops need budgets** — without step and cost caps, a stuck agent will retry
  the same failing action until something else stops it.
* **Observations are attacker-controlled** — anything a tool returns enters the
  context and can carry injected instructions.

## Why Should I Care?

Almost every practical agent problem — runaway cost, context exhaustion, silent
failure, prompt injection — is a property of this loop rather than of the model
running inside it.

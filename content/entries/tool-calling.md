---
term: Tool Calling
aliases: [Function Calling, Tool Use, Function Invocation]
category: protocols
subcategory: calling
status: established
difficulty: beginner
one_liner: Giving the model a list of functions it may request, so that instead of answering it can ask your code to run something.
origin:
  year: 2023
  attribution: Shipped as function calling by OpenAI in June 2023; Toolformer and ReAct explored the idea earlier
historical_period: agentic
tags: [protocol, agents]
relations:
  depends_on: [large-language-model]
  part_of: [ai-agent, agent-loop]
  evolved_into: [mcp]
  successor_of: [expert-system]
  related_to: [sampling, prompt-injection]
prerequisites: [large-language-model]
encountered_in: [documentation, production-systems, github, interviews]
sources:
  - type: paper
    title: "Toolformer: Language Models Can Teach Themselves to Use Tools"
    url: https://arxiv.org/abs/2302.04761
    year: 2023
  - type: docs
    title: "Anthropic — tool use documentation"
    url: https://docs.claude.com/en/docs/agents-and-tools/tool-use/overview
updated: 2026-08-21
---

## Simple Explanation

Describe your functions to the model — name, purpose, parameters — as part of the
request. When the model decides one is needed it does not answer in prose;
it emits a structured request naming the function and its arguments. Your code
runs it and hands back the result.

## Technical Definition

A protocol in which tool schemas (typically JSON Schema) are supplied with the
request; the model emits a structured invocation conforming to a schema, often
enforced by constrained decoding. The runtime executes the call and returns the
result as a new message. The model never executes anything itself.

## Why Does It Exist?

Models cannot access current data, perform reliable arithmetic, or cause effects.
Early attempts to solve this by parsing free-text intentions were fragile;
schema-constrained output made it reliable enough to build on.

## What Problem Does It Solve?

The gap between generating text and doing something, with a machine-checkable
interface between the two.

## How Does It Work?

```text
request:  [messages] + [tool schemas]
             │
model:    { "tool": "get_weather", "args": { "city": "Oslo" } }
             │
your code executes it (auth, validation, rate limits, errors)
             │
next turn: [ ... previous ... ][tool result: "4°C, rain"]
             │
model:    "It's 4°C and raining in Oslo."
```

## Mental Model

The model is an advisor who can fill in requisition forms but has no hands. Your
code decides whether to honour the form.

## Example

A well-described tool is used correctly; a vaguely described one is used at the
wrong times with the wrong arguments. Tool descriptions are prompt engineering —
they are read by the model, not by a compiler — and improving them is usually the
highest-return fix for a misbehaving agent.

## Real-World Usage

Supported by every major model API. Reliability degrades as the tool count grows,
so production systems keep the active set small, group tools behind a router, or
load them dynamically for the current phase of the task.

## Common Confusions

* **The model does not run the tool** — it requests. Every security control lives
  in your executor, not in the model.
* **Tool calling vs structured outputs** — structured outputs constrain the
  *format* of a response; tool calling is a protocol for requesting *actions*.
  Both usually rely on the same constrained decoding machinery.
* **Tool calling vs MCP** — tool calling is the model-to-application convention;
  MCP standardises how the application discovers and connects to tool *servers*.
  MCP does not replace tool calling; it feeds it.
* **Tool results are untrusted input** — treat returned text as data, never as
  instructions.

## Why Should I Care?

It is the hinge between a model that talks and a system that acts, and every
agent, plugin and integration in the field is built on it.

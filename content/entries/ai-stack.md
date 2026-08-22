---
term: AI Stack
aliases: [Agent Stack, Inference Stack, LLM Stack, GenAI Stack]
category: industry-culture
subcategory: stack
depth: full
status: informal
difficulty: beginner
one_liner: "The layered set of components between raw hardware and an AI product, and a phrase used to mean whichever layer the speaker sells."
origin:
  year: 2023
  circa: true
  attribution: Industry shorthand, popularised through venture-capital market maps and vendor positioning
historical_period: agentic
tags: [culture]
relations:
  related_to: [ai-gateway, model-routing, vllm, harness, ai-native]
prerequisites: [large-language-model]
encountered_in: [social-media, conferences, job-descriptions, technical-blogs]
sources:
  - type: post
    title: "Building Effective Agents"
    url: https://www.anthropic.com/engineering/building-effective-agents
    year: 2024
    note: Not a stack diagram, but the clearest account of which layers actually earn their place.
updated: 2026-08-21
review_by: 2026-12-01
---

## Simple Explanation

Building on AI involves several distinct layers — silicon, serving engine, model,
context, tools, agent logic, product. "The AI stack" is the umbrella phrase for
that arrangement. It is a genuinely useful mental model and also one of the most
abused phrases in the industry, because every vendor draws the diagram with their
own layer in the middle.

## Technical Definition

Not a technical term. Informally, the vertical arrangement of components in a
production AI system, ordered roughly: accelerators, kernels and runtime, serving
engine, model, gateway and routing, context and retrieval, tools and protocols,
agent runtime, product surface — with evaluation, safety, observability and cost
cutting across all of them.

## Why Does It Exist?

Layer names are how engineers scope conversations. Saying "that is a serving
problem, not a model problem" saves an hour. The vocabulary spread from ordinary
infrastructure, where "the stack" has meant this for decades.

## What Problem Does It Solve?

Orientation. When you meet an unfamiliar term, identifying its layer usually gets
you most of the way to guessing what it does.

## How Does It Work?

```text
 product surface   chat · IDE · agent · API
 agent runtime     harness · loop · memory · sub-agents
 protocol          tool calling · MCP · A2A · structured outputs
 context           prompts · RAG · vector DB · context engineering
 model             transformer · MoE · reasoning · multimodal
 serving           vLLM · batching · KV cache · quantisation
 systems           parallelism · kernels · schedulers
 hardware          GPU · NPU · memory · interconnect
 ─────────────────────────────────────────────────────
 across all of it: evaluation · safety · observability · cost
```

The [system view](../system-view.md) page maps most entries in this encyclopedia
onto these layers.

## Mental Model

The OSI model, with the same caveat: a useful teaching diagram that real systems
never quite respect. Layers leak. Context engineering is entangled with serving
because prefix caching cares about prompt ordering; the model's attention variant
is chosen for serving cost.

## Terminology Note

Treat any specific stack diagram as a marketing artefact until proven otherwise.
Vendors reliably draw their own layer as large, central and inevitable, and
adjacent layers as thin commodities. The layers with genuine technical substance —
serving, context, protocol, agent runtime — are stable; the boxes labelled
"orchestration platform" or "AI operating system" usually are not.

## Example

A useful test: for each box in a stack diagram someone shows you, ask what breaks
if it is removed. Remove the serving engine and nothing runs. Remove the "AI
enablement platform" and often nothing changes.

## Real-World Usage

Job descriptions ("experience across the inference stack"), architecture reviews,
market maps and funding decks. As a scoping device between engineers it is
genuinely useful; as a claim about how the industry will consolidate, it is
speculation.

## Common Confusions

* **The stack is not standardised** — no two diagrams agree, and none is
  authoritative.
* **You do not need every layer** — most successful products use a hosted model,
  some retrieval and ordinary application code. Adopting a full stack because a
  diagram implies you should is a common and expensive mistake.

## Why Should I Care?

As a way of locating an unfamiliar concept it is genuinely useful. As a purchase
guide it is advertising, and telling the two apart is a skill worth having.

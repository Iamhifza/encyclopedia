---
term: Inference Provider
aliases: [Model Provider, Serving Provider, API Provider, GPU Cloud]
category: industry-culture
subcategory: model-economy
depth: full
status: modern
difficulty: beginner
one_liner: "A company that runs models on its own hardware and sells access by the token."
historical_period: agentic
tags: [culture]
relations:
  depends_on: [vllm, throughput]
  related_to: [open-weight-model, model-routing, ai-gateway, frontier-model]
prerequisites: [large-language-model]
encountered_in: [production-systems, job-descriptions, technical-blogs]
sources:
  - type: paper
    title: "Efficient Memory Management for Large Language Model Serving with PagedAttention"
    url: https://arxiv.org/abs/2309.06180
    year: 2023
    note: The serving techniques that make per-token pricing viable.
  - type: docs
    title: "vLLM documentation"
    url: https://docs.vllm.ai/
updated: 2026-08-21
review_by: 2027-02-01
---

## Simple Explanation

Someone has to own the GPUs. An inference provider buys the hardware, runs the
serving stack, keeps it available, and charges you per million tokens — so you
never think about batch sizes, KV cache capacity or a node failing at three in
the morning.

## Technical Definition

An organisation operating model-serving infrastructure as a metered service.
Two broad kinds: **first-party** providers serving their own proprietary models,
and **third-party** providers serving open-weight models competitively, where the
differentiators are price per token, latency, throughput under load, context
limits, uptime and data-handling terms.

## Why Does It Exist?

Utilisation. A GPU costs the same whether it is busy or idle, and almost no
individual application generates enough steady traffic to keep expensive
accelerators saturated. A provider aggregates many customers' bursty demand into
one smooth load, which is the entire economic argument.

## What Problem Does It Solve?

Capital cost, capacity planning, and the substantial operational work of running
inference well — batching, cache management, failover, autoscaling.

## How Does It Work?

```text
many customers' bursty traffic
        │  aggregated
        ▼
  continuous batching keeps the GPU full
        │
  cost per token = (GPU hour ÷ tokens produced per hour) + margin
        │
  every point of utilisation, and every serving optimisation,
  goes straight to the bottom line
```

This is why providers care so much about the throughput techniques in this
encyclopedia: PagedAttention, prefix caching and quantisation are not academic
interests to them, they are margin.

## Mental Model

Electricity from the grid rather than a generator in the garden. You pay for what
you draw, and someone else worries about capacity.

## Example

The build-versus-buy calculation turns almost entirely on utilisation. A
self-hosted GPU costs the same at 5% utilisation as at 95%; a provider charges
only for tokens. Below roughly steady, predictable, high-volume traffic, buying
is cheaper. The reasons to self-host anyway are usually data residency,
regulatory constraint, deep customisation or independence — not price.

## Real-World Usage

First-party APIs from the labs that train frontier models, and a competitive
market of third-party providers serving open-weight models — often distinguishing
themselves on latency, on specialised hardware, or on data-residency guarantees.
Most production applications reach them through a gateway rather than directly,
so that switching provider is a configuration change.

## Common Confusions

* **Same model, different service** — two providers serving the identical
  open-weight checkpoint can differ substantially in latency, throughput,
  quantisation applied and context limits. "Which model" does not fully specify
  what you are buying.
* **Quantisation may be silent** — some providers serve quantised weights without
  saying so, which can change quality on your task. Ask.
* **Data terms vary enormously** — whether prompts are retained, logged or used
  for training is a contractual question, not a technical one.

## Why Should I Care?

Choosing one is a serious architectural decision — it sets your cost floor, your
latency ceiling and your data-protection position — and the comparison is far
less about model names than the marketing suggests.

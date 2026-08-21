---
term: Throughput
aliases: [Tokens per Second, Goodput, Aggregate Throughput]
category: llm-inference
subcategory: metrics
status: established
difficulty: beginner
one_liner: How much total work a deployment completes per second, counted across every request it is serving at once.
origin:
  year: 1960
  circa: true
  attribution: General systems-performance vocabulary, applied to LLM serving
historical_period: early-computing
tags: [inference]
relations:
  different_from: [inference-latency]
  depends_on: [continuous-batching]
  related_to: [gpu, quantization]
prerequisites: [decode]
encountered_in: [production-systems, job-descriptions, technical-blogs]
sources:
  - type: repo
    title: "vLLM benchmarking suite"
    url: https://github.com/vllm-project/vllm/tree/main/benchmarks
  - type: paper
    title: "Orca: A Distributed Serving System for Transformer-Based Generative Models"
    url: https://www.usenix.org/conference/osdi22/presentation/yu
    year: 2022
updated: 2026-08-21
---

## Simple Explanation

Latency is what one user feels. Throughput is what the fleet delivers: total
tokens per second across everybody, which is what determines cost per token and
how many customers one GPU can hold.

## Technical Definition

Completed output tokens per unit time for a deployment, usually normalised per
accelerator. *Goodput* restricts the count to tokens delivered within the latency
service level objective, which is the more honest metric because throughput
achieved by violating latency targets is not usable capacity.

## Why Does It Exist?

Because unit economics are set by aggregate work per accelerator-hour, not by
how any single request felt.

## What Problem Does It Solve?

It answers the capacity and cost question: how many accelerators are needed for
this traffic, and what does a million tokens cost to produce.

## How Does It Work?

```text
throughput
    ▲            ┌──────── saturation (bandwidth / cache limit)
    │        ╱
    │      ╱      each added request costs little during decode
    │    ╱        because weights are loaded once per step
    │  ╱
    └──────────────────────▶ batch size
                            (latency degrades as this grows)
```

## Mental Model

A bus route. One passenger in a taxi is fastest for that passenger and the worst
possible use of the road.

## Example

A deployment doing 40 tokens/s for one user might do 2,000 tokens/s across sixty
concurrent users on the same GPU, because decode is memory-bandwidth-bound and
the marginal cost of another sequence in the batch is nearly zero — until KV
cache memory runs out.

## Real-World Usage

Continuous batching, PagedAttention and prefix caching all raise throughput.
Capacity planning uses goodput at a target p95 latency, and inference providers
price against it.

## Common Confusions

* **Tokens/s per user vs tokens/s per GPU** — the same words, two very different
  numbers. Vendor claims frequently exploit the ambiguity.
* **Throughput vs goodput** — a system can post excellent throughput while
  missing its latency target on most requests.
* **Prefill tokens vs output tokens** — some benchmarks count both, inflating the
  figure for prompt-heavy workloads.

## Why Should I Care?

Cost per token, and therefore whether a product's margins work, is a throughput
question. Every serving optimisation is ultimately justified here.

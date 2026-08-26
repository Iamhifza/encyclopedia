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
diagram:
  kind: figure
  title: Batching is nearly free, until it is not
  footer: 'The two numbers trade against each other: past the knee you are buying throughput with every
    user''s latency. Which one you optimise is a product decision, not a technical one.'
  visual:
    kind: plot
    width: 700
    height: 220
    x_range: [0, 64]
    y_range: [0, 1.1]
    x_label: batch size
    y_label: throughput
    caption: during decode the weights are loaded once per step whatever the batch size, so early requests
      are almost free
    curves:
    - label: tokens/s
      tone: accent
      points: [[0, 0], [4, 0.3], [8, 0.52], [12, 0.68], [16, 0.79], [24, 0.9], [32, 0.96], [48, 1.0],
        [64, 1.02]]
    marks:
    - at: [16, 0.79]
      text: the knee — bandwidth runs out here
      dx: 14
      dy: 40
      anchor: start
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


During decode, generating one token requires reading every weight in the model
from memory and doing very little arithmetic with each. The read dominates. Add
a second request to the batch and the weights are read exactly once for both, so
the second request costs almost nothing — which is why throughput climbs steeply
at small batch sizes.

That continues until something saturates: the memory bandwidth needed for the KV
cache, or the space to hold it. Past that knee the curve flattens, and every
further request adds queueing rather than work.

Latency moves the other way throughout. Each request waits for the whole batch's
step to finish, so as the batch grows, so does inter-token latency. Throughput
per pound and latency per user are the same dial turned in opposite directions,
and no amount of engineering makes them both better at once.

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

---
term: KV Cache Quantisation
aliases: [KV Quantization, FP8 KV Cache, INT4 KV Cache]
category: llm-inference
subcategory: memory
depth: full
status: modern
difficulty: advanced
one_liner: "Storing cached keys and values in fewer bits, halving the memory that decides how many users fit on a GPU."
origin:
  year: 2023
  circa: true
  attribution: Emerged as long-context serving made cache memory the binding constraint; KIVI and similar methods formalised it
historical_period: agentic
diagram:
  kind: steps
  title: Halve the cache, double the users
  footer: The cache is what limits concurrency on a long-context workload, so shrinking it converts almost
    directly into throughput. Quality loss is small, and it is the keys that lose it.
  steps:
  - title: What each precision costs per token
    notes:
    - label: Model
      text: 70B with grouped-query attention, per token, all layers
    visual:
      kind: bars
      caption: and concurrency scales inversely with this number
      bars:
      - label: fp16
        value: 1.0
        value_label: ~327 KB
      - label: fp8
        value: 0.5
        value_label: ~164 KB — 2× the requests
      - label: int4
        value: 0.25
        value_label: ~82 KB — 4× the requests
        accent: true
  - title: Keys and values do not behave the same
    visual:
      kind: columns
      width: 740
      columns:
      - title: Keys
        tone: warn
        lines:
        - a few channels carry outliers
        - quantise per channel
        - or keep those channels wider
        - this is where quality is lost
      - title: Values
        accent: true
        lines:
        - distributed more evenly
        - quantise per token
        - safe to push harder
        - cheaper, and it holds
tags: [inference]
relations:
  is_a: [quantization]
  solves: [kv-cache]
  alternative_to: [grouped-query-attention]
  related_to: [long-context-model, throughput, inference-scheduler]
prerequisites: [kv-cache, quantization]
encountered_in: [production-systems, github, research-papers]
sources:
  - type: paper
    title: "KIVI: A Tuning-Free Asymmetric 2bit Quantization for KV Cache"
    url: https://arxiv.org/abs/2402.02750
    year: 2024
  - type: docs
    title: "vLLM — quantized KV cache"
    url: https://docs.vllm.ai/en/latest/
updated: 2026-08-21
review_by: 2027-02-01
---

## Simple Explanation

Weight quantisation gets all the attention, but for long-context serving the KV
cache is often the larger memory consumer — a single 32k-token request on a 70B
model needs around 10 GB of it. Storing those keys and values in 8 or 4 bits
instead of 16 halves or quarters that figure, and cache memory is exactly what
limits how many users a GPU can hold at once.

## Technical Definition

Applying low-precision storage to the KV cache specifically, with keys and values
quantised per channel or per token with associated scales, dequantised inside the
attention kernel. Keys and values are typically treated differently, because
keys carry outlier channels that make them more sensitive to precision loss than
values.

## Why Does It Exist?

Cache memory grows linearly with sequence length and batch size while model
weights are fixed. Past a certain context length the cache dominates, so
quantising weights alone stops helping.

## What Problem Does It Solve?

Concurrency and context length — how many requests fit, and how long each may be.

## How Does It Work?

The asymmetry between keys and values is the main technical finding in this area:
treating them identically wastes precision on values or destroys it on keys.

## Mental Model

Same argument as weight quantisation, applied to the other tenant of GPU memory —
and unlike weights, this tenant grows with every user and every token.

## Example

The practical decision is where to spend your memory savings. Halving cache size
lets you double batch size (more throughput) or double context length (longer
conversations) — not both. Which one matters depends entirely on your workload,
and it is a scheduling decision as much as a precision one.

## Real-World Usage

Supported in vLLM and other engines, commonly at fp8 where hardware supports it
natively. fp8 is broadly considered safe; int4 is used where memory pressure is
severe and quality has been checked on the specific task.

## Common Confusions

* **Weight quantisation vs KV quantisation** — different tenants of the same
  memory. They compose, and for long-context serving the second may matter more.
* **KV quantisation vs GQA** — both shrink the cache. GQA reduces the number of
  KV heads and must be trained in; quantisation reduces bytes per element and can
  be applied at serving time. They stack.
* **Degradation shows up in the wrong tests** — general benchmarks often look
  fine while long-context retrieval accuracy drops. Test at your context length,
  on your retrieval task.

## Why Should I Care?

For anyone serving long contexts, this is the lever with the most direct effect on
how many users a GPU can hold — and the one most likely to be left switched off
by default.

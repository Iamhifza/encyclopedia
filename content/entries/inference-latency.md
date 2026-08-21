---
term: Inference Latency
aliases: [TTFT, Time to First Token, TPOT, Time Per Output Token, Inter-Token Latency, ITL]
category: llm-inference
subcategory: metrics
status: established
difficulty: beginner
one_liner: How long a single user waits, split into the delay before the first token and the gap between every token after it.
origin:
  year: 2023
  circa: true
  attribution: Metric vocabulary standardised by LLM serving benchmarks and providers
historical_period: foundation-model
tags: [inference]
relations:
  different_from: [throughput]
  depends_on: [prefill, decode]
  related_to: [continuous-batching, speculative-decoding]
prerequisites: [prefill, decode]
encountered_in: [production-systems, job-descriptions, documentation, interviews]
sources:
  - type: repo
    title: "vLLM benchmarking suite"
    url: https://github.com/vllm-project/vllm/tree/main/benchmarks
  - type: paper
    title: "Taming Throughput-Latency Tradeoff in LLM Inference"
    url: https://arxiv.org/abs/2403.02310
    year: 2024
updated: 2026-08-21
---

## Simple Explanation

Two different waits, with two different causes. **Time to first token** is the
pause after you hit enter — that is prefill. **Time per output token** is how
fast words then appear — that is decode. A system can be excellent at one and
terrible at the other.

## Technical Definition

TTFT is the interval from request arrival to the first streamed token, including
queueing, scheduling and prefill. TPOT (equivalently inter-token latency) is the
mean interval between subsequent tokens. End-to-end latency ≈ TTFT + TPOT ×
output length. All should be reported as distributions, with p50, p95 and p99,
not means.

## Why Does It Exist?

Because a single "latency" number hides which half of the system is at fault, and
because the two halves respond to opposite optimisations.

## What Problem Does It Solve?

It makes performance discussions actionable: TTFT points at prefill, prompt
length and queueing; TPOT points at decode, batch size, memory bandwidth and
model size.

## How Does It Work?

```text
request ──┬── queueing ──┬── prefill ──┬── decode ─────────────────▶
          │              │             │  t  t  t  t  t  t  t
          └──────── TTFT ──────────────┘  └─ TPOT ─┘
```

## Mental Model

TTFT is how long the kitchen takes to send out the first plate. TPOT is how
quickly the rest of the courses follow.

## Example

Human reading speed is roughly 5-10 tokens per second, so a TPOT under about 100
ms feels comfortably fast, and further gains matter less than they look on a
chart. TTFT above roughly a second feels broken. For an agent making forty tool
calls in a loop, however, TTFT is paid forty times and dominates everything.

## Real-World Usage

Prefix caching and chunked prefill attack TTFT; speculative decoding,
quantisation and smaller models attack TPOT; batching improves throughput while
mildly worsening both. Service level objectives are normally written as p95 TTFT
and p95 TPOT under a stated request rate.

## Common Confusions

* **Latency vs throughput** — they trade against each other. Larger batches raise
  tokens per second for the fleet and worsen the wait for any individual request.
* **Streaming does not reduce latency** — it reduces *perceived* latency by
  showing tokens as they arrive.
* **Averages lie** — one long prompt entering the batch can wreck p99 while
  leaving p50 untouched.

## Why Should I Care?

Every serving decision is a position on the latency-throughput curve, and you
cannot choose a position without measuring both ends of it.

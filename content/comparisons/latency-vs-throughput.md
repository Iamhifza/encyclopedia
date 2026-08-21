---
title: Latency vs Throughput
question: Which one am I actually optimising, and what does the other cost?
sides: [inference-latency, throughput]
---

## The short version

Latency is what one user experiences. Throughput is what the fleet delivers per
accelerator. They trade against each other, and the trade is set mostly by batch
size.

## Side by side

| | Latency | Throughput |
|---|---|---|
| **Answers** | How fast for this person? | How much for this GPU? |
| **Metrics** | TTFT, TPOT, p95 and p99 | Tokens/s per accelerator, goodput |
| **Improved by** | Smaller batches, speculative decoding, prefix caching, smaller models | Larger batches, continuous batching, paged cache |
| **Determines** | Whether the product feels good | Whether the product is affordable |
| **Degraded by** | Filling the batch | Chasing tight tail latency |

## The curve you are choosing a point on

```text
throughput ▲
           │        ╱───────── saturation
           │      ╱
           │    ╱      ← every step right raises tokens/s per GPU
           │  ╱           and worsens p95 latency for individuals
           └──────────────▶ batch size
```

## Why decode makes the trade unusually favourable

Decode is memory-bandwidth-bound: weights are streamed once per step regardless
of how many sequences are in the batch. Adding a sequence therefore costs almost
no extra time, so throughput rises steeply before latency degrades much. This is
why continuous batching is close to free and why interactive serving is viable at
all.

## Goodput: the metric that keeps you honest

Throughput measured without a latency constraint can be gamed by queueing
everyone. *Goodput* counts only tokens delivered within the latency objective,
which is the number that corresponds to usable capacity.

## Verdict

Write the service level objective first — p95 TTFT and p95 TPOT at a stated
request rate — then maximise throughput subject to it. Optimising either in
isolation produces a system that is fast for nobody or affordable for nothing.

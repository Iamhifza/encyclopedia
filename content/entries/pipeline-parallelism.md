---
term: Pipeline Parallelism
aliases: [PP, Layer Parallelism, GPipe-style Parallelism]
category: distributed-ai-systems
subcategory: parallelism
status: established
difficulty: advanced
one_liner: Giving each GPU a different group of consecutive layers, so data flows through them like an assembly line.
origin:
  year: 2018
  attribution: Huang et al., GPipe; refined by PipeDream and Megatron interleaved schedules
historical_period: transformer
tags: [hardware]
relations:
  alternative_to: [tensor-parallelism]
  depends_on: [gpu]
  used_by: [pretraining]
prerequisites: [gpu, transformer]
encountered_in: [production-systems, github, research-papers]
sources:
  - type: paper
    title: "GPipe: Efficient Training of Giant Neural Networks using Pipeline Parallelism"
    url: https://arxiv.org/abs/1811.06965
    year: 2018
  - type: paper
    title: "Efficient Large-Scale Language Model Training on GPU Clusters (Megatron-LM)"
    url: https://arxiv.org/abs/2104.04473
    year: 2021
updated: 2026-08-21
---

## Simple Explanation

Instead of splitting each layer, split the stack. GPU 0 holds layers 1-20, GPU 1
holds 21-40, and so on. A batch flows through in sequence. The problem is
obvious: while GPU 0 works, the others wait — so the batch is chopped into
micro-batches to keep everyone busy.

## Technical Definition

Inter-layer partitioning across devices, with the global batch split into
micro-batches that are pipelined through the stages. Idle time at the start and
end of each step is the *bubble*, of size roughly $(p-1)/m$ for $p$ stages and
$m$ micro-batches; interleaved and zero-bubble schedules reduce it.

## Why Does It Exist?

Tensor parallelism needs very high interconnect bandwidth, which exists inside a
node and not between nodes. Pipeline stages exchange only activations at stage
boundaries, so they tolerate slower links.

## What Problem Does It Solve?

Scaling a model across multiple *nodes* without saturating the network.

## How Does It Work?

```text
time ──▶
GPU0  m1 m2 m3 m4 ░░░░░░
GPU1  ░░ m1 m2 m3 m4 ░░░
GPU2  ░░░░ m1 m2 m3 m4 ░
GPU3  ░░░░░░ m1 m2 m3 m4
      ░ = bubble; more micro-batches shrink it proportionally
```

## Mental Model

A factory line. Every station is busy once the line is full; the waste is at
start-up and shutdown.

## Example

Training a very large model typically composes strategies: tensor parallelism
within each node (fast NVLink), pipeline parallelism across nodes (slower
Ethernet or InfiniBand), and data parallelism across the whole cluster.

## Real-World Usage

Standard in large-scale pretraining. In inference it is less attractive than
tensor parallelism because the bubble directly harms latency, so it is mainly
used when a model must span nodes.

## Common Confusions

* **Pipeline vs tensor parallelism** — between layers versus within them; rare
  large messages versus constant small ones.
* **Pipeline parallelism does not reduce per-request latency** — it adds stage
  hops. It buys capacity.
* **Bubbles are unavoidable, only shrinkable** — more micro-batches means more
  activation memory.

## Why Should I Care?

Any cluster configuration you read — "TP=8, PP=4, DP=16" — is a set of tradeoffs
between memory, bandwidth and idle time, and this is one of the three axes.

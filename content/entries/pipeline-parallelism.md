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
diagram:
  kind: steps
  title: Different layers on different cards, and the bubble that creates
  footer: The bubble is fixed by the number of stages but shrinks relative to the work as micro-batches
    increase. Pipeline parallelism tolerates slow links, which is why it is what you use between nodes.
  steps:
  - title: Each card waits for the one before it
    notes:
    - label: Bubble
      text: idle time at the start and end of every batch — unavoidable, only dilutable
    visual:
      kind: matrix
      cell_width: 58
      show_values: false
      cols:
      - t1
      - t2
      - t3
      - t4
      - t5
      - t6
      - t7
      rows:
      - label: GPU 0
        values: [1, 1, 1, 1, null, null, null]
      - label: GPU 1
        values: [null, 1, 1, 1, 1, null, null]
      - label: GPU 2
        values: [null, null, 1, 1, 1, 1, null]
      - label: GPU 3
        values: [null, null, null, 1, 1, 1, 1]
      caption: four micro-batches through four stages; the gaps are the bubble
  - title: More micro-batches dilute it
    visual:
      kind: bars
      caption: share of wall-clock spent idle, four stages
      bars:
      - label: 4 micro-batches
        value: 0.43
        value_label: 43% idle
        accent: true
      - label: '16'
        value: 0.16
        value_label: 16%
      - label: '64'
        value: 0.05
        value_label: 5%
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


Assign contiguous groups of layers to different devices, so a batch flows
through card 0, then card 1, and so on. Only activations cross between stages —
a fraction of what tensor parallelism moves — which is why this tolerates slow
interconnects and works across nodes.

The problem is that stage *k* has nothing to do until stage *k−1* has produced
something. Run a single batch and most devices idle most of the time. The fix is
to split the batch into micro-batches and keep them in flight simultaneously, so
that once the pipeline is full every stage is busy.

The idle time at fill and drain — the bubble — is set by the number of stages
and cannot be removed, only diluted: with *m* micro-batches and *p* stages the
bubble is roughly (p−1)/(m+p−1) of the total. More micro-batches shrink it,
until memory for their activations runs out.

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

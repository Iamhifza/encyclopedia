---
title: Tensor vs Pipeline Parallelism
question: My model does not fit on one GPU. Which way do I cut it?
sides: [tensor-parallelism, pipeline-parallelism]
---

## The short version

Tensor parallelism splits *within* a layer and talks constantly. Pipeline
parallelism splits *between* layers and talks rarely. The choice is decided by
your interconnect: fast links inside a node favour tensor, slower links between
nodes force pipeline.

## Side by side

| | Tensor parallelism | Pipeline parallelism |
|---|---|---|
| **Cuts** | Each weight matrix, across devices | The stack, into consecutive groups of layers |
| **Communication** | Two all-reduces per layer | One activation hand-off per stage boundary |
| **Message pattern** | Constant, small, latency-sensitive | Rare, larger, tolerant of latency |
| **Needs** | NVLink or equivalent, inside a node | Ethernet or InfiniBand, across nodes |
| **Wasted time** | Synchronisation stalls | Pipeline bubbles at fill and drain |
| **Helps latency** | Yes — more bandwidth per forward pass | No — adds stage hops |
| **Typical degree** | 2–8, within one node | Across nodes |

## The two shapes

```text
TENSOR                          PIPELINE
GPU0 │heads 0-7 │               GPU0 │layers 1-20 │
GPU1 │heads 8-15│               GPU1 │layers 21-40│
GPU2 │heads16-23│               GPU2 │layers 41-60│
GPU3 │heads24-31│               GPU3 │layers 61-80│
  └─ all-reduce, twice            └─ pass activations forward, once per stage
     per layer, 80 layers            micro-batches keep everyone busy
   = 160 syncs per pass          bubble = (stages−1)/micro-batches
```

## Why real deployments use both

They compose, and large training runs stack three or four strategies at once —
a configuration written like `TP=8, PP=4, DP=16`. The rule that generates it:
tensor parallelism *within* a node where NVLink is fast, pipeline parallelism
*across* nodes where the network is not, and data parallelism over the whole
cluster for throughput. Expert parallelism joins the list for mixture-of-experts
models.

## For inference specifically

Tensor parallelism is usually the answer. It reduces per-token latency because
more aggregate memory bandwidth is applied to each forward pass, and inference
has no large batch to amortise pipeline bubbles against. Pipeline parallelism in
serving is mostly a capacity measure — the model must span nodes, so it does.

## The rule of thumb

Use the smallest tensor-parallel degree that fits the model *and* its KV cache,
because every added rank adds two synchronisations per layer. Reach for pipeline
only when you have run out of GPUs in a node.

## Verdict

Interconnect decides. Fast link, split within layers; slow link, split between
them. If you are choosing a serving configuration and both fit, prefer tensor
parallelism at the lowest degree that works.

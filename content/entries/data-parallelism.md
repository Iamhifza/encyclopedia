---
term: Data Parallelism
aliases: [DP, DDP, Distributed Data Parallel, ZeRO, FSDP]
category: distributed-ai-systems
subcategory: parallelism
depth: full
status: established
difficulty: intermediate
one_liner: "Giving every GPU a full copy of the model and a different slice of the batch, then averaging what they learn."
origin:
  year: 2012
  circa: true
  attribution: Standard practice from early large-scale deep learning; ZeRO and FSDP reshaped it from 2019
historical_period: deep-learning
tags: [hardware, training]
relations:
  alternative_to: [tensor-parallelism, pipeline-parallelism]
  depends_on: [gpu, parallel-computing, all-reduce]
  used_by: [pretraining]
  related_to: [distributed-systems, gradient-descent, throughput]
prerequisites: [gradient-descent, parallel-computing]
encountered_in: [production-systems, github, interviews, job-descriptions]
sources:
  - type: paper
    title: "ZeRO: Memory Optimizations Toward Training Trillion Parameter Models"
    url: https://arxiv.org/abs/1910.02054
    year: 2019
  - type: paper
    title: "PyTorch FSDP: Experiences on Scaling Fully Sharded Data Parallel"
    url: https://arxiv.org/abs/2304.11277
    year: 2023
  - type: docs
    title: "PyTorch Distributed Data Parallel"
    url: https://pytorch.org/docs/stable/notes/ddp.html
updated: 2026-08-21
---

## Simple Explanation

The simplest way to use eight GPUs: put the whole model on each one, split the
batch eight ways, and let each GPU compute gradients on its own slice. Then
average the gradients across all eight, apply the same update everywhere, and
every copy stays identical.

It is the first parallelism strategy anyone reaches for, it is the only one many
projects ever need, and it is the one strategy whose limit is stated in a single
sentence: the model must fit on one device.

## Technical Definition

Replicating model parameters across $N$ devices, partitioning each global batch
into per-device micro-batches, computing gradients independently, and
synchronising them with an all-reduce before the optimiser step. Mathematically
equivalent to training with the full batch on one device — the same update,
computed in parallel.

## Why Does It Exist?

Because it is embarrassingly parallel. Examples in a batch are independent, so
their gradients can be computed without any communication at all — the devices
only need to talk once per step, at the end.

## What Problem Does It Solve?

Wall-clock training time. It does not, in its classic form, let you train a
larger model; it lets you train the same model faster.

## How Does It Work?

```text
global batch of 512
   ├── GPU0: 64 examples ──▶ gradients ─┐
   ├── GPU1: 64 examples ──▶ gradients ─┤
   ├── ...                              ├──▶ ALL-REDUCE (average)
   └── GPU7: 64 examples ──▶ gradients ─┘         │
                                                   ▼
              every GPU applies the identical averaged update
              → all replicas remain bit-identical
```

Modern implementations overlap the all-reduce with the backward pass: gradients
for late layers are ready first and can start communicating while earlier layers
are still computing.

## Mental Model

Eight people marking the same exam paper, each taking a different pile of scripts,
then agreeing a common adjustment to the mark scheme before the next round.

## Example

The memory problem, and how it was solved. Classic data parallelism replicates
*everything* — weights, gradients and optimiser state — on every device, which for
a 7B model in bf16 with Adam is roughly 100 GB per GPU, most of it identical
copies of the same numbers.

**ZeRO** and its PyTorch implementation **FSDP** shard those states across the
data-parallel group instead of replicating them, gathering each layer's
parameters just before it is needed and releasing them afterwards. The result is
data parallelism that also reduces memory per device — which is why sharded data
parallelism, not tensor parallelism, is the default starting point for training
large models today.

## Real-World Usage

Every multi-GPU training run uses it, usually as FSDP or DeepSpeed ZeRO, and
usually combined with tensor and pipeline parallelism at scale — the `DP=` term
in a configuration like `TP=8, PP=4, DP=16`. In inference it appears as plain
replication: run independent copies of the model behind a load balancer.

## Common Confusions

* **Data parallelism vs model parallelism** — splitting the *batch* versus
  splitting the *model*. Use data parallelism first; reach for the others only
  when the model does not fit.
* **Sharded data parallelism blurs the line** — ZeRO and FSDP shard model state,
  which is model parallelism by another name, while keeping the data-parallel
  communication pattern.
* **Larger global batch is not free** — it usually needs a larger learning rate,
  and past some point returns diminish. Scaling GPUs does not scale progress
  proportionally.

## Why Should I Care?

It is the default and the baseline. Every more complicated parallelism strategy
exists because data parallelism alone stopped being sufficient, and knowing
exactly where it stops — the model no longer fits — is how you choose what to add.

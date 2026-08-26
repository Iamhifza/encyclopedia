---
term: All-Reduce
aliases: [Collective Communication, NCCL, Ring All-Reduce, AllGather]
category: distributed-ai-systems
subcategory: communication
depth: full
status: foundational
difficulty: advanced
one_liner: "The operation that combines a value held by every GPU and gives every GPU the result — the synchronisation at the heart of distributed training."
origin:
  year: 1994
  circa: true
  attribution: Standardised in MPI for high-performance computing; NCCL brought GPU-optimised implementations in 2016
historical_period: statistical-ml
diagram:
  kind: steps
  title: Every device ends up with the same sum, with no coordinator
  footer: 'Bandwidth-optimal: each device sends and receives roughly twice the data regardless of how
    many devices there are. This is the operation that makes data-parallel training possible at all.'
  steps:
  - title: The devices form a ring
    visual:
      kind: chips
      items:
      - GPU 0
      - GPU 1
      - GPU 2
      - GPU 3
      loop: and back to the start — every link carries traffic in both phases
  - title: Two passes around it
    visual:
      kind: columns
      width: 700
      columns:
      - title: 1 · reduce-scatter
        lines:
        - each step, pass a chunk on
        - and add what you receive
        - after N−1 steps each device
        - owns one finished quarter
      - title: 2 · all-gather
        accent: true
        lines:
        - pass the finished chunk on
        - no arithmetic, only copying
        - after N−1 more steps
        - everyone has all four
      caption: no central node, and every link is busy the whole time
tags: [hardware]
relations:
  used_by: [data-parallelism, tensor-parallelism]
  depends_on: [distributed-systems]
  related_to: [gpu, parallel-computing, gpu-cluster]
prerequisites: [parallel-computing]
encountered_in: [production-systems, research-papers, interviews]
sources:
  - type: docs
    title: "NVIDIA NCCL documentation"
    url: https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/index.html
  - type: paper
    title: "Bandwidth Optimal All-reduce Algorithms for Clusters of Workstations"
    url: https://www.cs.fsu.edu/~xyuan/paper/09jpdc.pdf
    year: 2009
  - type: paper
    title: "Horovod: fast and easy distributed deep learning in TensorFlow"
    url: https://arxiv.org/abs/1802.05799
    year: 2018
updated: 2026-08-21
---

## Simple Explanation

Eight GPUs each computed a gradient. They all need the average. All-reduce is the
operation that does that — combine everyone's values, give everyone the result —
and it is the single point at which distributed training stops being parallel and
starts waiting.

Everything about the performance of a large training run comes down to how fast
this operation is and how well it is hidden behind computation.

## Technical Definition

A collective communication primitive in which every participant contributes a
value and every participant receives the reduction (sum, mean, max) across all
contributions. The bandwidth-optimal implementation is the **ring all-reduce**:
a reduce-scatter around a ring followed by an all-gather, moving
$2(N-1)/N$ times the data volume per device regardless of $N$.

Related primitives: **all-gather** (everyone receives everyone's data),
**reduce-scatter** (the reduction, split across participants), **broadcast** and
**all-to-all** — the last being what mixture-of-experts routing needs.

## Why Does It Exist?

Because the naive approach does not scale. Sending every gradient to one
coordinating node makes that node's link the bottleneck, and it gets worse with
every device added. The ring algorithm removes the central node entirely: each
device only ever talks to its two neighbours.

## What Problem Does It Solve?

Synchronising state across devices at a cost that does not grow with the number
of devices.

## How Does It Work?


Every device starts with its own gradient tensor and must end with the sum of
all of them. The naive approach sends everything to one coordinator, which makes
that node's bandwidth the ceiling. Ring all-reduce avoids a coordinator
entirely.

Arrange the devices in a logical ring and split the tensor into as many chunks
as there are devices. In the reduce-scatter phase, each device passes one chunk
to its neighbour and adds what it receives; after N−1 steps every device holds
the fully summed value for exactly one chunk. The all-gather phase passes those
finished chunks around the same ring until everyone has all of them.

The result is bandwidth-optimal: each device sends and receives about twice the
tensor size regardless of how many devices there are, and every link is busy
throughout. This is the operation data-parallel training is built on, and the
reason interconnect bandwidth is a headline specification on training hardware.

## Mental Model

A group agreeing a total by passing partial sums around a circle, rather than
everyone shouting their number at one person with a calculator.

## Formula

Time for a ring all-reduce of $D$ bytes across $N$ devices:

$$T \approx 2\,\frac{N-1}{N} \cdot \frac{D}{B} + 2(N-1)\,\alpha$$

* $D$ — data volume, here the size of the gradients.
* $B$ — per-link bandwidth.
* $\alpha$ — per-hop latency.

The first term is nearly independent of $N$, which is the algorithm's virtue.
The second grows with $N$, which is why latency dominates for small messages and
why gradients are bucketed into larger transfers before sending.

## Example

**NCCL** is NVIDIA's implementation and the layer nearly everyone actually meets:
it is what PyTorch's distributed backend calls, it selects algorithms based on
the detected topology (NVLink within a node, InfiniBand or Ethernet between), and
`NCCL error` in a training log is among the more common failures at scale.

The performance trick that matters: overlap. Gradients for the final layers are
ready before the backward pass finishes, so communication for those can begin
while earlier layers are still computing. Well-tuned training hides most
communication behind computation entirely.

## Real-World Usage

Every data-parallel step (averaging gradients), every tensor-parallel layer
(twice per Transformer block), and mixture-of-experts routing (all-to-all). It is
the reason interconnect topology dictates parallelism strategy.

## Common Confusions

* **All-reduce vs all-gather** — the first combines and distributes a result; the
  second distributes everyone's raw data without reduction.
* **NCCL is an implementation, not the concept** — the collective operations come
  from MPI and predate deep learning by twenty years.
* **Communication is not always the bottleneck** — when it is well overlapped it
  is nearly free. When it is not, it can dominate the step time entirely.

## Why Should I Care?

It is the synchronisation point that turns many independent GPUs into one
training run, and its cost is what makes interconnect bandwidth — not FLOPs — the
deciding factor in how a large cluster is designed.

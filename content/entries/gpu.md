---
term: GPU
aliases: [Graphics Processing Unit, Accelerator, Tensor Core, HBM]
category: computing-foundations
subcategory: architecture
depth: full
status: foundational
difficulty: beginner
one_liner: A processor with thousands of small cores that does the same arithmetic on huge batches of numbers at once.
origin:
  year: 1999
  attribution: NVIDIA popularised the term with the GeForce 256; general-purpose use took off with CUDA in 2007
historical_period: statistical-ml
tags: [hardware]
relations:
  part_of: [memory-hierarchy]
  alternative_to: [cpu, npu]
  depends_on: [cuda, parallel-computing]
  used_by: [neural-network, tensor-parallelism, data-parallelism, quantization, gpu-kernel, gpu-cluster]
  related_to: [throughput, decode, linear-algebra, compiler]
prerequisites: [cpu]
encountered_in: [production-systems, job-descriptions, technical-blogs]
sources:
  - type: docs
    title: "NVIDIA CUDA C++ Programming Guide"
    url: https://docs.nvidia.com/cuda/cuda-c-programming-guide/
  - type: paper
    title: "ImageNet Classification with Deep Convolutional Neural Networks (AlexNet)"
    url: https://papers.nips.cc/paper/4824-imagenet-classification-with-deep-convolutional-neural-networks
    year: 2012
    note: The result that made GPUs the default substrate for deep learning.
  - type: paper
    title: "Roofline: An Insightful Visual Performance Model"
    url: https://dl.acm.org/doi/10.1145/1498765.1498785
    year: 2009
updated: 2026-08-22
---

## Simple Explanation

A CPU has a handful of powerful cores that do complicated things quickly, one
after another. A GPU has thousands of simple cores that all do the *same* thing
at the same time on different data.

Neural networks are mostly one operation — [multiply a matrix](linear-algebra.md)
— repeated endlessly. That is exactly the shape a GPU wants, and the coincidence
between hardware built for rendering triangles and mathematics built for learning
is most of why the last decade happened when it did.

## Technical Definition

A throughput-oriented processor built around SIMT execution: threads grouped into
warps executing the same instruction on different data, scheduled across many
streaming multiprocessors, backed by high-bandwidth memory and specialised matrix
units (tensor cores) for mixed-precision multiply-accumulate.

## Why Does It Exist?

Real-time 3D graphics requires transforming millions of vertices and pixels
identically, every frame. That hardware turned out to be a general engine for
dense linear algebra — which scientific computing wanted, and which neural
networks needed.

## What Problem Does It Solve?

Training and serving large models on CPUs is orders of magnitude too slow. The
GPU turns an intractable amount of arithmetic into an affordable one.

## How Does It Work?

```text
CPU                              GPU
┌────┬────┬────┬────┐            ┌─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┐
│ few big cores      │           │ thousands of small cores   │
│ deep caches        │           │ shared control             │
│ branch prediction  │           │ very wide memory bus       │
└────┴────┴────┴────┘            └───────────────────────────┘
optimised for latency             optimised for total work done
of one task                       latency hidden by having so many
                                  threads resident that some are
                                  always ready to run
```

The two numbers that matter in practice are **memory capacity** (does the model
and its [KV cache](kv-cache.md) fit) and **memory bandwidth** (how fast weights
can be streamed). Arithmetic throughput is rarely the binding constraint, which
surprises people the first time they profile an inference server.

## Mental Model

A CPU is a few master chefs. A GPU is a thousand line cooks who all chop
identically on command. For one intricate dish, hire the chefs; for ten thousand
identical salads, take the line.

## Formula

The roofline model, which predicts which limit you are against:

$$\text{arithmetic intensity} = \frac{\text{FLOPs performed}}{\text{bytes moved}}$$

Below the machine's ratio of peak FLOPs to peak bandwidth, you are
**memory-bound** and extra compute sits idle. Above it, **compute-bound**.

This single quantity explains the central asymmetry of LLM serving:
[prefill](prefill.md) processes many tokens per weight load and is compute-bound;
[decode](decode.md) processes one and is memory-bound. Same hardware, same
weights, opposite bottlenecks — and therefore opposite optimisations.

## Example

Multiplying two 8192×8192 matrices in fp16: a server CPU takes seconds, a
data-centre GPU a few milliseconds. That ratio is why model training moved
wholesale onto GPUs after AlexNet in 2012.

But the more useful example is the one that constrains you daily. Generating one
token from a 70B model in fp16 requires streaming ~140 GB of weights from memory
while performing comparatively little arithmetic — roughly one operation per byte
moved. On a card with ~3 TB/s of bandwidth that is a floor of about 47 ms per
token that no amount of compute removes. It is also why
[batching](continuous-batching.md) is nearly free, why
[quantisation](quantization.md) speeds up decoding so directly, and why
[speculative decoding](speculative-decoding.md) is worth the complexity.

## Real-World Usage

Every frontier model is trained and served on clusters of accelerators, wired
together in a [bandwidth hierarchy](gpu-cluster.md) that dictates how a model can
be split. The practical decisions engineers face are almost always memory
decisions: what fits, what must be sharded, how much cache is left for
concurrency.

## Common Confusions

* **Compute-bound vs memory-bound** — the distinction that explains most
  performance surprises in this field.
* **GPU vs TPU vs [NPU](npu.md)** — different vendors and design points for the
  same idea: parallel hardware specialised for dense tensor mathematics.
* **"More FLOPS is faster"** — only if the data can be fed fast enough. Headline
  TOPS figures assume ideal precision and utilisation.
* **VRAM is not the whole story** — capacity decides *whether* you can run a
  model, bandwidth decides *how fast*. Two cards with the same memory can differ
  substantially in tokens per second.

## Why Should I Care?

Nearly every performance decision in modern AI — batch size, quantisation, KV
cache layout, parallelism strategy, which engine to use — is a negotiation with
GPU memory and bandwidth limits. Understanding the roofline turns those decisions
from guesswork into arithmetic.

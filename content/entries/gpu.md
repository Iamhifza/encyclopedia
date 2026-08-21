---
term: GPU
aliases: [Graphics Processing Unit, Accelerator]
category: computing-foundations
subcategory: architecture
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
  used_by: [neural-network, tensor-parallelism, quantization]
  related_to: [throughput]
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
updated: 2026-08-21
---

## Simple Explanation

A CPU has a handful of powerful cores that do complicated things quickly, one
after another. A GPU has thousands of simple cores that all do the *same* thing
at the same time on different data. Neural networks are mostly one operation —
multiply a matrix — repeated endlessly, which is exactly the shape a GPU wants.

## Technical Definition

A throughput-oriented processor built around SIMT execution: threads are grouped
into warps that execute the same instruction on different data, scheduled over
many streaming multiprocessors, backed by high-bandwidth memory and specialised
matrix units (tensor cores) for mixed-precision matrix multiply-accumulate.

## Why Does It Exist?

Real-time 3D graphics requires transforming millions of vertices and pixels
identically every frame. That hardware turned out to be a general engine for
dense linear algebra, which is what scientific computing and neural networks
both need.

## What Problem Does It Solve?

Training and running large models on CPUs is orders of magnitude too slow. The
GPU turns an intractable amount of arithmetic into an affordable one.

## How Does It Work?

```text
CPU                        GPU
┌────┬────┬────┬────┐      ┌─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┐
│ big cores, deep    │      │ thousands of small cores    │
│ caches, branch     │      │ shared control, wide memory │
│ prediction         │      │ bus, latency hidden by      │
└────┴────┴────┴────┘      │ swapping between warps      │
optimised for latency       └─────────────────────────────┘
of one task                 optimised for total work done
```

The GPU hides memory latency not by predicting it but by having so many resident
threads that some are always ready to run.

## Mental Model

A CPU is a few master chefs. A GPU is a thousand line cooks who all chop
identically on command. For one intricate dish, hire the chefs; for ten thousand
identical salads, take the line.

## Example

Multiplying two 8192×8192 matrices in fp16: a server CPU takes seconds; a modern
data-centre GPU takes a few milliseconds. That ratio is why model training moved
wholesale onto GPUs after AlexNet in 2012.

## Real-World Usage

Every frontier model is trained and served on clusters of accelerators. The
practical constraints engineers hit are memory capacity (does the model and its
KV cache fit) and memory bandwidth (how fast weights can be streamed), far more
often than raw arithmetic throughput.

## Common Confusions

* **Compute-bound vs memory-bound** — GPUs have so much arithmetic capability
  that most inference work is limited by moving bytes, not by multiplying them.
* **GPU vs TPU vs NPU** — different vendors and design points for the same idea:
  parallel hardware specialised for dense tensor math.
* **"More FLOPS is faster"** — only if the data can be fed fast enough.

## Why Should I Care?

Nearly every performance decision in modern AI — batch size, quantisation, KV
cache layout, parallelism strategy — is a negotiation with GPU memory and
bandwidth limits.

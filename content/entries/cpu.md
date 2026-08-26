---
term: CPU
aliases: [Central Processing Unit, Processor, Host]
category: computing-foundations
subcategory: architecture
depth: full
status: foundational
difficulty: beginner
one_liner: "The general-purpose processor that runs the operating system and everything a GPU is not doing."
historical_period: early-computing
diagram:
  kind: figure
  title: Two answers to 'what should a core be good at'
  footer: Neither is better. A CPU finishes one thing quickly; a GPU finishes an enormous number of things
    eventually. Model inference is the second problem.
  visual:
    kind: columns
    width: 700
    caption: the split is latency versus throughput, and everything else follows from it
    columns:
    - title: CPU
      accent: true
      lines:
      - 8–64 complex cores
      - independent control flow
      - 'deep cache: L1 / L2 / L3'
      - predicts, reorders, prefetches
      - 'optimised for: one task fast'
    - title: GPU
      lines:
      - 10,000+ simple cores
      - lockstep within a warp
      - small cache, huge bandwidth
      - thousands of threads resident
      - 'optimised for: total work done'
tags: [hardware]
relations:
  alternative_to: [gpu]
  related_to: [memory-hierarchy, operating-system, parallel-computing]
encountered_in: [interviews, production-systems, technical-blogs]
sources:
  - type: book
    title: "Computer Architecture: A Quantitative Approach (Hennessy & Patterson)"
    url: https://www.elsevier.com/books/computer-architecture/hennessy/978-0-12-811905-1
  - type: post
    title: "What Every Programmer Should Know About Memory"
    url: https://people.freebsd.org/~lstewart/articles/cpumemory.pdf
    year: 2007
updated: 2026-08-21
---

## Simple Explanation

The CPU is the machine's general contractor: a handful of powerful cores that can
do anything, one thing after another, very fast. It runs the operating system,
your Python code, the web server — everything except the dense arithmetic that
was handed to the GPU.

In an AI system it is easy to dismiss as "not where the work happens", right up
until it becomes the bottleneck, which it does more often than people expect.

## Technical Definition

A general-purpose processor optimised for single-thread latency: deep pipelines,
out-of-order and speculative execution, branch prediction, and a large multi-level
cache hierarchy. A handful of complex cores, each capable of independent control
flow — as opposed to a GPU's thousands of simple cores executing in lockstep.

## Why Does It Exist?

Most computation is not uniform. Branching logic, pointer chasing, system calls,
irregular data structures — these have unpredictable control flow and poor
parallelism, and they are what the CPU's elaborate machinery exists to make fast.

## What Problem Does It Solve?

Latency on irregular, branch-heavy work — which is nearly all software.

## How Does It Work?


A CPU spends its transistor budget making a single instruction stream finish as
fast as possible: deep caches so memory rarely stalls it, branch prediction and
out-of-order execution so it keeps working through dependencies, and a handful of
very capable cores. It is optimised for latency, and for code whose next step
depends on the last one.

A GPU spends the same budget on parallelism instead — thousands of simple cores,
a wide memory bus, and enough resident threads that a stalled warp can always be
swapped for a ready one. It is optimised for throughput on work that is identical
across many data elements. Matrix multiplication is precisely that shape, which is
why model inference runs on the second design and orchestration around it runs on
the first.

## Mental Model

A few master chefs versus a thousand line cooks. For one intricate dish, hire the
chefs.

## Example

Where the CPU bites in AI systems, despite the GPU doing the maths:

* **Tokenisation** of a large batch of prompts is pure CPU work, and a slow
  tokeniser measurably delays time to first token.
* **Data loading** during training — decoding, augmenting, collating — starves
  the GPU if the loader cannot keep up. Idle accelerators waiting on a CPU
  pipeline is a common and expensive mistake.
* **The serving scheduler** runs on the CPU between every forward pass, directly
  on the critical path.
* **KV cache offload** moves data to host memory, and host memory is the CPU's.

## Real-World Usage

Every server hosting a GPU has one, and the ratio of CPU cores to accelerators is
a real provisioning decision. For inference of small models, CPU-only serving is
entirely viable — llama.cpp exists largely for this — though throughput is
bandwidth-limited in exactly the way GPU decode is, just with less bandwidth.

## Common Confusions

* **CPU vs GPU is not fast vs slow** — it is latency-optimised versus
  throughput-optimised. A CPU beats a GPU handily on branch-heavy sequential work.
* **"The GPU does everything"** — in profiling real training and serving stacks,
  CPU-side preprocessing and scheduling are frequent bottlenecks.
* **Host memory is not GPU memory** — moving between them crosses PCIe, which is
  slow enough to dominate anything that does it per token.

## Why Should I Care?

When a GPU sits at 40% utilisation, the cause is usually on the other side of the
bus. Knowing what the CPU is responsible for is how you find it.

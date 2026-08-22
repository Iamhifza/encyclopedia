---
term: CPU
aliases: [Central Processing Unit, Processor, Host]
category: computing-foundations
subcategory: architecture
depth: full
status: foundational
difficulty: beginner
one_liner: "The general-purpose processor that runs the operating system and everything a GPU is not doing."
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

```text
CPU                              GPU
8-64 complex cores               10,000+ simple cores
independent control flow         lockstep within a warp
deep cache: L1/L2/L3             small cache, huge bandwidth
optimised for: one task fast     optimised for: total work done
predicts branches, reorders      hides latency by having
instructions, prefetches         thousands of threads resident
```

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

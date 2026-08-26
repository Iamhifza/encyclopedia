---
term: GPU Kernel
aliases: [CUDA Kernel, Custom Kernel, Fused Kernel, Triton Kernel]
category: distributed-ai-systems
subcategory: accelerators
depth: full
status: established
difficulty: research
one_liner: "A small program run by thousands of GPU threads at once, and the level at which most inference speedups are actually won."
historical_period: deep-learning
diagram:
  kind: figure
  title: Fusing removes trips to memory, not arithmetic
  footer: 'Which is why fusion helps at all: the operations were never the bottleneck. A compiler does
    most of this automatically now, and a hand-written kernel earns its keep only where the compiler''s
    pattern-matching gives up.'
  visual:
    kind: columns
    width: 740
    caption: same maths, same result, a third of the memory traffic
    columns:
    - title: Unfused
      tone: warn
      lines:
      - matmul → write to HBM
      - read → bias → write
      - read → GELU → write
      - three round trips over the bus
    - title: Fused
      accent: true
      lines:
      - matmul, bias and GELU
      - in one kernel launch
      - intermediates stay in registers
      - one round trip
tags: [hardware, inference]
relations:
  implemented_by: [flash-attention]
  depends_on: [gpu, memory-hierarchy, cuda]
  related_to: [quantization, paged-attention]
prerequisites: [gpu, memory-hierarchy]
encountered_in: [github, research-papers, job-descriptions, production-systems]
sources:
  - type: docs
    title: "NVIDIA CUDA C++ Programming Guide"
    url: https://docs.nvidia.com/cuda/cuda-c-programming-guide/
  - type: docs
    title: "Triton — a language for writing GPU kernels in Python"
    url: https://triton-lang.org/
  - type: paper
    title: "FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness"
    url: https://arxiv.org/abs/2205.14135
    year: 2022
updated: 2026-08-21
---

## Simple Explanation

A kernel is a function written to be executed by thousands of GPU threads
simultaneously, each on a different slice of the data. Everything a model does on
a GPU is kernels. The reason this matters to anyone who is not a systems engineer
is that the arithmetic is rarely the bottleneck — moving data between memory
levels is — and kernels are where that movement is controlled.

## Technical Definition

A function launched across a grid of thread blocks, each block resident on one
streaming multiprocessor with access to fast shared memory. Performance is
governed by memory coalescing, occupancy, use of shared memory and registers, and
avoiding warp divergence. *Fusion* combines several logical operations into one
kernel so intermediates never leave on-chip memory.

## Why Does It Exist?

Because the naive composition of framework operations is enormously wasteful. Each
separate operation reads its input from high-bandwidth memory and writes its
output back. Five chained operations means five round trips for data that could
have stayed on chip throughout.

## What Problem Does It Solve?

Memory traffic. On modern accelerators arithmetic is abundant and bandwidth is
scarce, so the winning move is nearly always to touch memory less.

## How Does It Work?

The kernel decides what lives in registers (fastest, tiny), what lives in shared
memory (fast, per-block), and what must go back to HBM (slow, large).

## Mental Model

Cooking. An unfused pipeline walks to the pantry for each ingredient
individually; a fused kernel brings everything to the counter once and works
there.

## Example

FlashAttention is the canonical result: mathematically identical to standard
attention, but by tiling the computation so the $n \times n$ score matrix is
never written to HBM, it delivers large wall-clock speedups and removes the
memory blow-up at long sequence lengths. No maths changed — only the memory
schedule.

## Real-World Usage

Every serving engine ships custom kernels: fused attention, fused
normalisation-plus-residual, quantised matrix multiplies with dequantisation
folded in, and paged gather for non-contiguous KV cache blocks. Increasingly
these are written in **Triton**, which lets you express tiling in Python and
compiles to competitive GPU code — the reason kernel work is no longer confined
to CUDA specialists.

## Common Confusions

* **Kernel (GPU) vs kernel (operating system)** — unrelated meanings that share a
  word.
* **More FLOPS is not faster** — if a kernel is bandwidth-bound, extra arithmetic
  capability is idle. Measure arithmetic intensity before optimising.
* **Custom kernels are not always warranted** — vendor libraries are extremely
  well tuned for standard shapes. The wins are in fusion and in unusual shapes
  the libraries do not cover.

## Why Should I Care?

Several of the largest efficiency gains of the last few years — FlashAttention,
PagedAttention, fast quantised inference — came from kernel-level work rather
than from model research. It is why "kernel engineer" became one of the more
sought-after job titles in AI.

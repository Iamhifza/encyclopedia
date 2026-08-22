---
term: CUDA
aliases: [CUDA Toolkit, Compute Unified Device Architecture, cuDNN]
category: distributed-ai-systems
subcategory: accelerators
depth: full
status: established
difficulty: intermediate
one_liner: "NVIDIA's programming platform for running general computation on GPUs, and the moat that kept them dominant."
origin:
  year: 2007
  attribution: NVIDIA; the first release that made general-purpose GPU programming practical
historical_period: statistical-ml
tags: [hardware]
relations:
  used_by: [gpu-kernel, gpu]
  related_to: [compiler, tensor-parallelism, flash-attention]
prerequisites: [gpu]
encountered_in: [github, job-descriptions, production-systems, technical-blogs]
sources:
  - type: docs
    title: "NVIDIA CUDA C++ Programming Guide"
    url: https://docs.nvidia.com/cuda/cuda-c-programming-guide/
  - type: docs
    title: "Triton — GPU kernels in Python"
    url: https://triton-lang.org/
updated: 2026-08-21
---

## Simple Explanation

Before 2007, using a GPU for anything other than graphics meant disguising your
problem as a graphics problem — encoding data as textures and computation as
shaders. CUDA let people write ordinary C-like code that ran on thousands of GPU
threads.

That convenience is the reason NVIDIA hardware is the default for AI, and the
reason competitors with comparable silicon still struggle to displace it. The
lock-in is software, not chips.

## Technical Definition

NVIDIA's parallel computing platform: a C++ language extension for writing
kernels, a runtime and driver API, a compiler toolchain, and a large library
ecosystem — cuBLAS for linear algebra, cuDNN for neural network primitives, NCCL
for collective communication across GPUs. The programming model exposes a
hierarchy of threads, blocks and grids mapped onto the hardware's streaming
multiprocessors.

## Why Does It Exist?

GPUs had enormous arithmetic throughput that scientific computing wanted and
could not easily reach. CUDA removed the graphics abstraction and exposed the
hardware directly.

## What Problem Does It Solve?

Programmability. The hardware was already capable; the barrier was that using it
required thinking like a graphics programmer.

## How Does It Work?

```text
your code (Python / PyTorch)
        │
   framework dispatches to
        │
   cuBLAS · cuDNN · custom kernels ──▶ CUDA runtime ──▶ driver ──▶ GPU
        │
   thread hierarchy:
     grid ──▶ blocks ──▶ warps (32 threads in lockstep) ──▶ threads
```

Almost nobody in AI writes CUDA C++ directly. You write PyTorch, PyTorch calls
libraries, and those libraries are CUDA. The stack is invisible until something
is slow or a version mismatch breaks the install.

## Mental Model

Not the engine — the fuel system, the wiring loom and the service manual. Another
manufacturer can build a comparable engine; replacing everything built around
this one is the hard part.

## Example

The dependency is felt most sharply in version management. A model requires a
PyTorch build, compiled against a CUDA toolkit version, which requires a minimum
driver version, on a GPU of sufficient compute capability. Mismatches at any
layer produce errors that look nothing like the actual problem, which is why
containerised environments are standard practice in this field.

## Real-World Usage

Under essentially every AI framework. The competitive picture: AMD's ROCm and
Intel's oneAPI target the same role, and portability layers like Triton and
OpenAI's compiler stack let kernels be written once and compiled for multiple
backends. Triton in particular has lowered the barrier considerably — kernel work
in Python rather than CUDA C++ — which is why more people write custom kernels
now than five years ago.

## Common Confusions

* **CUDA is not the GPU** — it is the software platform. "CUDA cores" is
  marketing for the hardware's arithmetic units.
* **CUDA version vs driver version vs compute capability** — three different
  numbers that must be mutually compatible, and the source of most installation
  grief.
* **The moat is real but not permanent** — high-level frameworks abstract most of
  it away, and every year more code targets a portable layer instead.

## Why Should I Care?

It explains why the AI hardware market has the shape it does, and it is the layer
you will meet the moment you try to run a model on hardware other than the one
its authors used.

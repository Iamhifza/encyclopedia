---
term: Compiler
aliases: [Compilation, JIT, Kernel Compiler, torch.compile, XLA]
category: computing-foundations
subcategory: toolchain
depth: full
status: foundational
difficulty: advanced
one_liner: "A program that turns code written for humans into instructions a specific machine can execute quickly."
historical_period: early-computing
tags: [hardware]
relations:
  used_by: [flash-attention, gpu-kernel]
  related_to: [gpu, cuda, npu, quantization]
prerequisites: [cpu]
encountered_in: [research-papers, github, production-systems, interviews]
sources:
  - type: paper
    title: "MLIR: A Compiler Infrastructure for the End of Moore's Law"
    url: https://arxiv.org/abs/2002.11054
    year: 2020
    note: The compiler infrastructure most ML compilers are now built on.
  - type: docs
    title: "torch.compile — PyTorch compilation"
    url: https://pytorch.org/docs/stable/torch.compiler.html
  - type: paper
    title: "TVM: An Automated End-to-End Optimizing Compiler for Deep Learning"
    url: https://arxiv.org/abs/1802.04799
    year: 2018
updated: 2026-08-21
---

## Simple Explanation

You write what you want; the compiler works out how the machine should do it. In
ordinary programming that means translating source code to machine instructions.

In deep learning it means something more interesting: your model is a *graph* of
operations, and a compiler can rearrange that graph — fusing operations,
eliminating intermediates, choosing memory layouts, picking specialised kernels —
before any of it runs. That rearrangement is often worth a large speedup for no
change to your code.

## Technical Definition

A translator from a higher-level representation to a lower-level executable one,
performing optimisation along the way. Deep learning compilers (XLA, TVM,
TorchInductor, Triton's backend) take a computation graph and lower it through
intermediate representations to device code, applying operator fusion, layout
selection, memory planning, loop tiling and autotuning against the target
hardware.

## Why Does It Exist?

Eager execution — running each operation as it is written — is easy to debug and
leaves substantial performance on the table. Every operation reads its input from
memory and writes its output back, and the framework has no opportunity to see
that three of them could have been one.

## What Problem Does It Solve?

The gap between code written for clarity and code that runs well on a specific
accelerator, without asking the author to write kernels by hand.

## How Does It Work?

```text
your model (Python)
    │ trace or capture the graph
computation graph
    │ optimise:  fuse ops · eliminate dead nodes · plan memory
    │            choose layouts · tile loops · autotune
lowered IR
    │ generate device code
executable kernels ──▶ GPU / NPU / CPU
```

Fusion is the biggest single win, and it is the same argument made in the GPU
kernel entry: fewer trips to memory.

## Mental Model

A translator who reads the whole paragraph before speaking, rather than
translating word by word. The meaning is the same; the delivery is far better.

## Example

`torch.compile` is the visible form for most practitioners: one decorator, no
model changes, and typically a meaningful speedup from fusion and reduced
overhead. The cost is a compilation step on first run, and the notorious
*graph breaks* — a data-dependent branch or an unsupported operation forces the
compiler to split the graph, and much of the benefit evaporates at that seam.

## Real-World Usage

Training and inference in every major framework, ahead-of-time compilation for
deployment, and the entire alternative-accelerator story: a compiler is how a
non-NVIDIA chip runs PyTorch code at all. Triton sits in an interesting middle
position — you write tiling logic in Python and it compiles to competitive GPU
code, which is why kernel authorship is no longer restricted to CUDA specialists.

## Common Confusions

* **Compiled is not always faster** — compilation overhead, graph breaks and
  dynamic shapes can leave you no better off. Measure it.
* **Compiler vs interpreter vs JIT** — ahead of time, line by line, or at run
  time once a code path proves hot. Deep learning compilers are usually the
  third.
* **Numerical results can shift** — fusion and reassociation change floating-point
  ordering, so outputs may differ in the last bits. Usually harmless, occasionally
  not.

## Why Should I Care?

It is where a large share of "free" performance now comes from, and it is the
layer that determines whether models can run on anything other than the hardware
they were developed on.

---
term: Memory Hierarchy
aliases: [Cache Hierarchy, Memory Wall, Roofline]
category: computing-foundations
subcategory: memory
status: foundational
difficulty: intermediate
one_liner: The layered arrangement of fast-small to slow-large memory that decides how quickly a program can actually get its data.
origin:
  year: 1965
  circa: true
  attribution: Formalised alongside cache design in early mainframes; the 'memory wall' named by Wulf and McKee in 1995
historical_period: early-computing
diagram:
  kind: figure
  title: Five tiers, each roughly ten times slower than the one above
  footer: 'Almost every optimisation in this encyclopedia is a move up this table: FlashAttention keeps
    work in SRAM, the KV cache keeps it out of recomputation, quantisation makes more of it fit in HBM.'
  visual:
    kind: stack
    width: 760
    caption: the numbers move with each hardware generation; the ratios barely do
    layers:
    - label: registers
      text: kilobytes · effectively infinite bandwidth
      note: ~1 cycle
    - label: SRAM
      text: ~50 MB on chip · ~10 TB/s
      note: tens of cycles
      accent: true
    - label: HBM
      text: 80–192 GB · 3–8 TB/s
      note: hundreds of cycles
    - label: host RAM
      text: terabytes · ~100 GB/s
      note: far worse
    - label: network
      text: unbounded · tens of GB/s
      note: worse still
tags: [hardware]
relations:
  used_by: [kv-cache, flash-attention]
  related_to: [gpu, decode]
encountered_in: [interviews, production-systems, technical-blogs]
sources:
  - type: paper
    title: "Hitting the Memory Wall: Implications of the Obvious"
    url: https://dl.acm.org/doi/10.1145/216585.216588
    year: 1995
  - type: paper
    title: "Roofline: An Insightful Visual Performance Model"
    url: https://dl.acm.org/doi/10.1145/1498765.1498785
    year: 2009
updated: 2026-08-21
---

## Simple Explanation

Memory close to the processor is tiny and instant. Memory far away is huge and
slow. Every fast program is really an argument about keeping the data you need
next in the fast place.

## Technical Definition

A tiered storage arrangement — registers, on-chip SRAM (caches and shared
memory), off-chip DRAM (HBM on accelerators), then storage — with each level
roughly an order of magnitude larger and slower than the one above. Performance
is bounded by whichever of arithmetic throughput or memory bandwidth saturates
first, expressed by arithmetic intensity in the roofline model.

## Why Does It Exist?

Fast memory is expensive per byte and physically must be small to stay fast.
Nobody has ever been able to build memory that is simultaneously large, cheap
and fast, so architects build all three and shuttle data between them.

## What Problem Does It Solve?

It gives a program the illusion of a large fast memory, as long as its access
pattern has locality.

## How Does It Work?

An operation is *compute-bound* if it does many FLOPs per byte loaded, and
*memory-bound* if it does few.

## Mental Model

Desk, shelf, basement, off-site archive. You can work at full speed only on what
is already on the desk.

## Example

Decoding one token from a 70B-parameter model in fp16 requires streaming ~140 GB
of weights from HBM but performs only a few hundred GFLOPs of work — roughly one
arithmetic operation per byte moved. It is overwhelmingly memory-bound, which is
why batching many requests together is nearly free and why quantisation speeds
up decoding so directly.

## Real-World Usage

FlashAttention exists because attention was moving too much data between HBM and
on-chip SRAM. PagedAttention exists because KV cache memory was being wasted.
Both are memory-hierarchy engineering, not model research.

## Common Confusions

* **Memory capacity vs memory bandwidth** — one determines whether you can run
  the model, the other determines how fast.
* **Cache (hardware) vs KV cache (algorithmic)** — unrelated mechanisms that
  share a name; the KV cache is ordinary data living in HBM.

## Why Should I Care?

"Why is my inference slow?" almost always resolves to a bandwidth or capacity
question, and the answer is rarely a better model.

---
term: FlashAttention
aliases: [Fused Attention, IO-Aware Attention]
category: llm-inference
subcategory: engines
status: established
difficulty: research
one_liner: An attention implementation that never writes the full score matrix to memory, computing it in on-chip tiles instead.
origin:
  year: 2022
  attribution: Tri Dao et al., Stanford
historical_period: foundation-model
tags: [inference, hardware]
relations:
  depends_on: [self-attention, memory-hierarchy]
  used_by: [vllm, transformer]
  solves: [self-attention]
  related_to: [paged-attention]
prerequisites: [self-attention, memory-hierarchy]
encountered_in: [research-papers, github, production-systems]
sources:
  - type: paper
    title: "FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness"
    url: https://arxiv.org/abs/2205.14135
    year: 2022
  - type: paper
    title: "FlashAttention-2: Faster Attention with Better Parallelism and Work Partitioning"
    url: https://arxiv.org/abs/2307.08691
    year: 2023
  - type: repo
    title: "flash-attention"
    url: https://github.com/Dao-AILab/flash-attention
updated: 2026-08-21
---

## Simple Explanation

A naive attention implementation builds the full table of how much every token
attends to every other token, writes it to memory, reads it back for the softmax,
writes again, then reads it once more to multiply by the values. For a long
sequence that table is enormous, and all the time goes into moving it around.
FlashAttention computes attention in small tiles that stay in fast on-chip memory
and never materialises the table at all.

## Technical Definition

An IO-aware, tiled, fused attention kernel using online softmax with running
maximum and normalisation statistics, so that softmax can be computed
incrementally over key/value blocks without holding the full $n \times n$ score
matrix. The result is numerically exact, with memory traffic reduced from
$O(n^2)$ to $O(n)$ in HBM accesses.

## Why Does It Exist?

Attention was not compute-bound; it was bound by reads and writes to
high-bandwidth memory. Standard implementations were leaving most of the GPU's
arithmetic capability unused while saturating its memory bus.

## What Problem Does It Solve?

The memory cost and wall-clock cost of attention at long sequence lengths — both
during training and during prefill.

## How Does It Work?

```text
naive:  Q·Kᵀ ──write──▶ HBM ──read──▶ softmax ──write──▶ HBM ──read──▶ ·V
        the n×n matrix crosses the memory bus three times

flash:  for each block of K,V:
            load into SRAM
            compute partial scores and partial softmax statistics
            update the running output in place
        the n×n matrix never exists in HBM
```

The trick is the online softmax: rescale the accumulated output whenever a new
block reveals a larger maximum, so the final result matches the one-shot softmax
exactly.

## Mental Model

Summing a million numbers written across a warehouse. Instead of carrying them
all to your desk, you walk the aisles keeping a running total.

## Example

At 8k sequence length the naive score matrix is 64M entries per head per layer.
FlashAttention removes that allocation entirely, which is what made long-context
training practical, and typically delivers 2-4× wall-clock speedups on attention.

## Real-World Usage

The default attention kernel in essentially every training and inference stack.
FlashAttention-2 improved work partitioning, FlashAttention-3 targets newer
hardware, and serving engines combine it with PagedAttention so that tiles are
gathered from non-contiguous cache blocks.

## Common Confusions

* **It is exact, not approximate** — unlike linear or sparse attention, output is
  bit-comparable to standard attention up to floating-point ordering.
* **It does not change the $O(n^2)$ arithmetic** — the FLOP count is unchanged;
  the memory traffic is what drops.
* **FlashAttention vs PagedAttention** — one is about computing attention
  efficiently, the other about storing the cache efficiently.

## Why Should I Care?

It is the canonical example of a result that came from understanding the memory
hierarchy rather than the mathematics, and it is why "kernel engineer" became a
serious job title in AI.

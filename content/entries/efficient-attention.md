---
term: Efficient Attention
aliases: [Sparse Attention, Linear Attention, Sliding Window Attention, Long-Range Attention]
category: transformers
subcategory: variants
depth: full
status: experimental
difficulty: research
one_liner: "The family of attention variants that give up looking at every token in exchange for cost that does not grow quadratically."
origin:
  year: 2019
  circa: true
  attribution: A large research literature from 2019 onward; Sparse Transformer, Longformer, Performer and many others
historical_period: transformer
diagram:
  kind: steps
  title: Compute fewer pairs, and choose which ones carefully
  footer: Every scheme here is a bet about which pairs matter. FlashAttention takes the other route entirely
    — it computes all of them, and simply stops writing the matrix to memory.
  steps:
  - title: Full attention — every pair
    notes:
    - label: Cost
      text: O(n²) in both time and memory
    visual:
      kind: matrix
      cell_width: 44
      show_values: false
      cols:
      - '0'
      - '1'
      - '2'
      - '3'
      - '4'
      - '5'
      - '6'
      - '7'
      rows:
      - label: '0'
        values: [0.6, null, null, null, null, null, null, null]
      - label: '1'
        values: [0.6, 0.6, null, null, null, null, null, null]
      - label: '2'
        values: [0.6, 0.6, 0.6, null, null, null, null, null]
      - label: '3'
        values: [0.6, 0.6, 0.6, 0.6, null, null, null, null]
      - label: '4'
        values: [0.6, 0.6, 0.6, 0.6, 0.6, null, null, null]
      - label: '5'
        values: [0.6, 0.6, 0.6, 0.6, 0.6, 0.6, null, null]
      - label: '6'
        values: [0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, null]
      - label: '7'
        values: [0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6]
      caption: causal, so the upper triangle is absent — but everything below it is computed
  - title: Sliding window — neighbours only
    notes:
    - label: Cost
      text: O(n·w) — linear, for a window of width w
    - label: Loss
      text: nothing far away can be attended to directly, only through several layers
    visual:
      kind: matrix
      cell_width: 44
      show_values: false
      cols:
      - '0'
      - '1'
      - '2'
      - '3'
      - '4'
      - '5'
      - '6'
      - '7'
      rows:
      - label: '0'
        values: [0.6, null, null, null, null, null, null, null]
      - label: '1'
        values: [0.6, 0.6, null, null, null, null, null, null]
      - label: '2'
        values: [0.6, 0.6, 0.6, null, null, null, null, null]
      - label: '3'
        values: [null, 0.6, 0.6, 0.6, null, null, null, null]
      - label: '4'
        values: [null, null, 0.6, 0.6, 0.6, null, null, null]
      - label: '5'
        values: [null, null, null, 0.6, 0.6, 0.6, null, null]
      - label: '6'
        values: [null, null, null, null, 0.6, 0.6, 0.6, null]
      - label: '7'
        values: [null, null, null, null, null, 0.6, 0.6, 0.6]
      caption: information still travels far, but layer by layer rather than in one hop
  - title: Global plus local — a few tokens see everything
    notes:
    - label: Why
      text: one global token restores the single-hop path between any two positions
    visual:
      kind: matrix
      cell_width: 44
      show_values: false
      cols:
      - '0'
      - '1'
      - '2'
      - '3'
      - '4'
      - '5'
      - '6'
      - '7'
      rows:
      - label: '0'
        values: [0.85, null, null, null, null, null, null, null]
      - label: '1'
        values: [0.85, 0.6, null, null, null, null, null, null]
      - label: '2'
        values: [0.85, 0.6, 0.6, null, null, null, null, null]
      - label: '3'
        values: [0.85, 0.6, 0.6, 0.6, null, null, null, null]
      - label: '4'
        values: [0.85, null, 0.6, 0.6, 0.6, null, null, null]
      - label: '5'
        values: [0.85, null, null, 0.6, 0.6, 0.6, null, null]
      - label: '6'
        values: [0.85, null, null, null, 0.6, 0.6, 0.6, null]
      - label: '7'
        values: [0.85, null, null, null, null, 0.6, 0.6, 0.6]
      caption: the darker column is the global token; everything else is the window
tags: [architecture, inference]
relations:
  alternative_to: [self-attention]
  related_to: [state-space-model, context-window, long-context-model, flash-attention]
prerequisites: [self-attention]
encountered_in: [research-papers, conferences, github]
sources:
  - type: paper
    title: "Generating Long Sequences with Sparse Transformers"
    url: https://arxiv.org/abs/1904.10509
    year: 2019
  - type: paper
    title: "Longformer: The Long-Document Transformer"
    url: https://arxiv.org/abs/2004.05150
    year: 2020
  - type: paper
    title: "Efficient Transformers: A Survey"
    url: https://arxiv.org/abs/2009.06732
    year: 2020
updated: 2026-08-21
review_by: 2027-02-01
---

## Simple Explanation

Attention compares every token with every other token, so doubling the sequence
quadruples the work. An enormous research literature has tried to fix this by
having each token look at fewer others — nearby ones, a fixed pattern, a learned
selection, or a mathematical approximation of the whole thing.

The honest summary after several years: most of these lost to making exact
attention faster instead.

## Technical Definition

Attention variants reducing the $O(n^2)$ cost. Broad families: **sparse** (each
query attends to a subset — local windows, strided patterns, global tokens),
**linear** (kernel approximations of softmax giving $O(n)$), **low-rank**
(projecting keys and values to a smaller fixed size), and **hierarchical**
(compressing distant context).

## Why Does It Exist?

The quadratic term dominates at long sequence lengths, and it was the obvious
obstacle to long-context models. Reducing an algorithm's asymptotic complexity is
the natural first instinct.

## What Problem Does It Solve?

Cost at very long sequence lengths — in principle. In practice it also introduces
an approximation, and the value of that trade depends on the task.

## How Does It Work?


Full attention computes a score for every pair of positions, which is quadratic
in sequence length. Every method here computes fewer pairs and differs only in
which ones it decides to skip.

Sliding-window attention keeps a band around the diagonal: each position attends
to its last few hundred neighbours and nothing else. Cost becomes linear.
Information still travels across the sequence, but through a chain of layers
rather than in a single hop, so the effective range is the window times the
depth.

Adding global tokens repairs the worst of that. A handful of positions attend to
everything and are attended to by everything, restoring a one-hop path between
any two positions at negligible cost. Other schemes cluster or hash positions to
attend within groups, or approximate the softmax with a low-rank factorisation.

All of them are bets about which pairs matter, and all of them lose something.
Which is why FlashAttention was so influential: it takes the opposite route,
computing every pair exactly and simply never writing the matrix to memory.

## Mental Model

Reading a long book by skimming: attend closely to the current page, glance at
the chapter headings, ignore most of the rest. Cheaper, and you will miss things.

## Example

The instructive history: dozens of efficient attention variants were published
between 2019 and 2022, and comparative evaluations found many performed worse
than plain attention at equal compute once implementation quality was controlled
for. Then FlashAttention arrived and made *exact* attention several times faster
by fixing memory traffic rather than complexity — removing much of the motivation
for approximating at all.

What survived is mostly the simple structural approaches, particularly sliding
window attention in some production models, often interleaved with full attention
layers so that global information still has a path.

## Real-World Usage

Sliding-window layers appear in several current open-weight models. The
research energy has largely moved to state-space models and hybrids, which
attack the same problem from the recurrence side rather than by approximating
softmax.

## Common Confusions

* **Efficient attention vs FlashAttention** — approximate versus exact.
  FlashAttention changes memory traffic and computes the same result; these
  change what is computed.
* **Lower complexity is not lower wall-clock time** — constants and hardware
  utilisation dominate at practical sequence lengths, which is why many
  asymptotically better methods were slower in reality.
* **Quality loss is task-dependent** — sparse patterns hurt exact long-range
  recall most, which is precisely what long-context users want.

## Why Should I Care?

It is an unusually clear case study in how optimisation actually works: the
winning move was not a better algorithm but a better understanding of the
hardware. Worth remembering before reaching for an asymptotic improvement.

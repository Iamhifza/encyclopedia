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

```text
FULL              SLIDING WINDOW      GLOBAL + LOCAL
■■■■■■■■          ■■□□□□□□            ■■■■■■■■   ← global token
■■■■■■■■          ■■■□□□□□            ■■□□□□□□
■■■■■■■■          □■■■□□□□            ■□■■□□□□
■■■■■■■■          □□■■■□□□            ■□□■■□□□
every pair        neighbours only     a few see everything
O(n²)             O(n·w)              O(n·w + n·g)
```

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

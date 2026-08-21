---
term: Self-Attention
aliases: [Intra-Attention, Scaled Dot-Product Self-Attention, MHA, Multi-Head Attention]
category: transformers
subcategory: attention
status: foundational
difficulty: intermediate
one_liner: Attention applied within a single sequence, so every token can look at every other token in the same text.
origin:
  year: 2017
  attribution: Vaswani et al., "Attention Is All You Need"
historical_period: transformer
tags: [architecture]
relations:
  is_a: [attention]
  part_of: [transformer]
  evolved_into: [grouped-query-attention]
  used_by: [kv-cache, flash-attention]
prerequisites: [attention]
encountered_in: [research-papers, interviews, github]
sources:
  - type: paper
    title: "Attention Is All You Need"
    url: https://arxiv.org/abs/1706.03762
    year: 2017
  - type: post
    title: "The Illustrated Transformer"
    url: https://jalammar.github.io/illustrated-transformer/
    year: 2018
updated: 2026-08-21
---

## Simple Explanation

Every word in the sentence looks at every other word in the same sentence and
decides who is relevant to it. There is no separate source and target — the text
is attending to itself, which is where the name comes from.

## Technical Definition

Scaled dot-product attention where $Q$, $K$ and $V$ are all linear projections of
the same input sequence. In decoder-only models a causal mask sets scores to
$-\infty$ for future positions, preserving the autoregressive property.
*Multi-head* attention runs $h$ such computations in parallel over
lower-dimensional projections and concatenates the results.

## Why Does It Exist?

Once attention could route information between sequences, the natural question
was whether recurrence was needed at all *within* a sequence. It was not.
Self-attention gives a constant path length between any two positions and
parallelises across the whole sequence during training.

## What Problem Does It Solve?

Contextualisation. It turns a static per-token embedding into a
representation that depends on the surrounding text, so "bank" near "river"
differs from "bank" near "loan".

## How Does It Work?

```text
tokens:   the   cat   sat   on   the   mat
            ╲    │    ╱      ╲    │    ╱
             every token scores every token
                        │
        causal mask: position i sees only 0..i
                        │
             softmax ──▶ weighted mix of values

heads:  ┌──head 1: syntax──┐
        ├──head 2: coreference─┤ concat ──▶ output projection
        └──head 3: position ───┘
```

## Mental Model

A meeting where every participant simultaneously asks everyone else a question,
gets an answer weighted by how relevant each person is to them, and updates their
own notes. Multiple heads are several such meetings running at once with
different agendas.

## Formula

$$\text{MultiHead}(X) = \text{Concat}(\text{head}_1,\dots,\text{head}_h)W^O, \quad \text{head}_i = \text{Attention}(XW_i^Q, XW_i^K, XW_i^V)$$

* $X$ — the input sequence, one row per token.
* $W_i^Q, W_i^K, W_i^V$ — per-head projections, each of width $d_{model}/h$.
* $W^O$ — output projection mixing the heads back together.
* $h$ — number of heads; total compute is roughly unchanged versus one wide head.

## Example

With a causal mask, generating token 5 lets it attend to tokens 1-4 but not 6
onward. That single masking choice is what makes a decoder-only Transformer able
to be trained on all positions at once while still generating left to right.

## Real-World Usage

The core of every decoder-only LLM. In practice production models rarely use
plain multi-head attention any more: they use grouped-query attention to shrink
the KV cache, and compute it with a fused kernel such as FlashAttention.

## Common Confusions

* **Self-attention vs cross-attention** — cross-attention takes queries from one
  sequence and keys/values from another (used in encoder-decoder models and in
  many multimodal architectures).
* **Heads are not specialists by design** — any interpretation of a head is
  discovered after training, not assigned.
* **Masking is not optional** — remove the causal mask and the model can see the
  answer it is being trained to predict.

## Why Should I Care?

The KV cache exists precisely because self-attention needs every earlier key and
value again at every generation step. Cache size, context limits and most
inference cost follow directly from this one design choice.

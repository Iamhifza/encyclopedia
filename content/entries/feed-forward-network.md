---
term: Feed-Forward Network
aliases: [FFN, MLP Block, Position-wise FFN, SwiGLU Block]
category: transformers
subcategory: block
depth: full
status: established
difficulty: intermediate
one_liner: "The two-layer network applied to each position separately inside every Transformer block, holding most of the model's parameters."
historical_period: transformer
diagram:
  kind: figure
  title: Expand, bend, compress — at every position separately
  footer: Two thirds of a model's parameters live here, not in attention. It is also where interpretability
    work keeps finding stored facts, which is why model-editing methods target these matrices.
  visual:
    kind: pipeline
    width: 700
    caption: no information moves between positions here — that already happened in attention
    stages:
    - text: one position's vector
      note: d = 4096
    - text: a much wider space
      note: '11008'
      via: W_up — expand
    - text: the same width, transformed
      note: '11008'
      via: SwiGLU — the non-linearity, and a learned gate
    - text: back into the residual stream
      note: '4096'
      tone: accent
      via: W_down — compress
tags: [architecture]
relations:
  part_of: [transformer]
  related_to: [mixture-of-experts, mechanistic-interpretability, activation-function]
prerequisites: [neural-network]
encountered_in: [research-papers, interviews, github]
sources:
  - type: paper
    title: "Attention Is All You Need"
    url: https://arxiv.org/abs/1706.03762
    year: 2017
  - type: paper
    title: "Transformer Feed-Forward Layers Are Key-Value Memories"
    url: https://arxiv.org/abs/2012.14913
    year: 2020
  - type: paper
    title: "GLU Variants Improve Transformer"
    url: https://arxiv.org/abs/2002.05202
    year: 2020
updated: 2026-08-21
---

## Simple Explanation

Attention gets all the attention, but it only *moves information between*
positions. The feed-forward network is what each position does with what it
gathered — and it holds roughly two-thirds of the model's parameters. If
attention is the conversation, the FFN is each participant thinking privately
about what they just heard.

## Technical Definition

A position-wise two-layer network applied identically and independently to every
token in the sequence: expand from $d_{model}$ to an inner dimension (classically
$4 d_{model}$), apply a non-linearity, project back down. Modern implementations
use gated variants such as SwiGLU, which use three matrices and typically scale
the inner dimension to about $\frac{8}{3} d_{model}$ to keep the parameter count
comparable.

## Why Does It Exist?

Attention is, between its softmax weights, essentially a weighted average — a
linear operation on the values. Stacking attention alone would give you very
little expressive power. The FFN supplies the per-position non-linear
transformation that makes depth worth having.

## What Problem Does It Solve?

Per-token computation and, on the evidence, storage. Attention routes; the FFN is
where the knowledge appears to live.

## How Does It Work?


After attention has moved information between positions, each position is
processed on its own: project up to a much wider dimension, apply a
non-linearity, project back down, and add the result to the residual stream. The
same two matrices are used at every position, and no information crosses between
them here.

The expansion is large — typically two and a half to four times the model
dimension — and it is where the capacity lives. Roughly two thirds of a
transformer's parameters sit in these two matrices rather than in attention,
which surprises people who assume attention is where the model does its thinking.

Modern models use a gated variant, usually SwiGLU: a third matrix produces a gate
that multiplies the activated branch, letting the layer suppress its own features
rather than only amplify them. Interpretability work also keeps locating stored
facts in these matrices, which is why model-editing techniques target them
specifically.

## Mental Model

A wide funnel: project into a much larger space where features are easier to
separate, do something non-linear there, then project back. The width is the
point — the expansion is where capacity lives.

## Formula

The classical form, and the gated form now standard:

$$\text{FFN}(x) = W_2\,\sigma(W_1 x + b_1) + b_2$$

$$\text{SwiGLU}(x) = \left(\text{Swish}(W_1 x) \odot W_3 x\right) W_2$$

* $W_1$ — up-projection to the inner dimension.
* $W_2$ — down-projection back to model dimension.
* $W_3$ — the gate in the gated variant; its output multiplies the activated
  branch element-wise, letting the layer suppress its own features.
* $\odot$ — element-wise product.

## Example

Parameter arithmetic for a typical layer at $d_{model} = 4096$: attention
projections account for roughly 67M parameters, the FFN for roughly 135M. Across
a whole model that ratio holds — which is why "attention is all you need" is a
memorable title and a misleading summary of where the weights are.

## Real-World Usage

Every Transformer layer. Two developments worth knowing: gated activations
(SwiGLU) replaced ReLU and GELU in most current models, and mixture-of-experts
replaces this single dense FFN with many experts plus a router — because if the
FFN is where knowledge is stored, it is the natural place to add capacity
sparsely.

## Common Confusions

* **"Position-wise" means no mixing** — the same weights are applied to every
  token separately. Only attention moves information across positions.
* **It is not a minor component** — it is the majority of the parameters and the
  majority of the FLOPs in a forward pass.
* **Key-value memory is a hypothesis, not a proven fact** — interpretability work
  suggests FFN layers behave like retrieval over learned patterns, which is
  suggestive rather than settled.

## Why Should I Care?

Understanding that the FFN holds most of the parameters explains where model
knowledge is thought to reside, why mixture-of-experts targets this specific
block, and why memory arithmetic for weights looks the way it does.

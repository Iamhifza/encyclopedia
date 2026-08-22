---
term: Feed-Forward Network
aliases: [FFN, MLP Block, Position-wise FFN, SwiGLU Block]
category: transformers
subcategory: block
depth: full
status: established
difficulty: intermediate
one_liner: "The two-layer network applied to each position separately inside every Transformer block, holding most of the model's parameters."
tags: [architecture]
relations:
  part_of: [transformer]
  related_to: [mixture-of-experts, mechanistic-interpretability, activation-function]
prerequisites: [transformer, neural-network]
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

```text
for each position independently:

   x (d=4096) ──▶ W_up ──▶ (d=11008) ──▶ SwiGLU ──▶ W_down ──▶ (d=4096)
                    ▲                                   │
              expand, apply non-linearity, compress back │
                                                         ▼
                                              added to the residual stream

no information moves between positions here — that already happened in attention
```

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

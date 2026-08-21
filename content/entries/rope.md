---
term: RoPE
aliases: [Rotary Position Embedding, Rotary Embeddings]
category: transformers
subcategory: position
status: established
difficulty: advanced
one_liner: A way of encoding token position by rotating the query and key vectors, so attention naturally depends on how far apart two tokens are.
origin:
  year: 2021
  attribution: Su et al., RoFormer
historical_period: foundation-model
tags: [architecture]
relations:
  used_by: [transformer, context-window]
  related_to: [self-attention]
prerequisites: [self-attention]
encountered_in: [research-papers, github, technical-blogs]
sources:
  - type: paper
    title: "RoFormer: Enhanced Transformer with Rotary Position Embedding"
    url: https://arxiv.org/abs/2104.09864
    year: 2021
  - type: paper
    title: "YaRN: Efficient Context Window Extension of Large Language Models"
    url: https://arxiv.org/abs/2309.00071
    year: 2023
updated: 2026-08-21
---

## Simple Explanation

Attention by itself is order-blind: shuffle the tokens and it computes the same
thing. Something must tell the model where each token sits. RoPE does it by
rotating each token's query and key vectors by an angle proportional to its
position, so when two vectors are compared, only their *difference* in angle —
their relative distance — affects the score.

## Technical Definition

Position is applied as a rotation in each 2D subspace of the query and key
vectors, with frequency decreasing across dimension pairs. Because rotation is
orthogonal and $R_m^\top R_n = R_{n-m}$, the dot product between a query at
position $m$ and a key at position $n$ depends only on $n - m$, giving relative
position encoding without adding any parameters.

## Why Does It Exist?

Learned absolute position embeddings do not extrapolate past the trained length
and encode absolute rather than relative distance. Additive sinusoids extrapolate
poorly in practice. RoPE gives relative positioning as a property of the geometry
rather than as an extra learned table.

## What Problem Does It Solve?

Order awareness that generalises across positions, is parameter-free, and — with
frequency scaling methods such as position interpolation, NTK-aware scaling and
YaRN — allows a model trained at 8k tokens to be extended to far longer contexts
with modest additional training.

## How Does It Work?

```text
dimension pairs:  (0,1)   (2,3)   (4,5)  ...
frequency:        fast    slower  slower still

position m ──▶ rotate each pair by m·θ_i
position n ──▶ rotate each pair by n·θ_i

q_m · k_n  depends only on (n − m)
```

Low-frequency pairs rotate slowly and carry long-range position; high-frequency
pairs carry fine local order.

## Mental Model

Two clock hands. Their absolute positions on the dial do not matter to the angle
*between* them, and that angle is what attention actually reads.

## Formula

$$\langle R_m q,\; R_n k \rangle = \langle q,\; R_{n-m} k \rangle, \qquad \theta_i = 10000^{-2i/d}$$

* $R_m$ — block-diagonal rotation matrix for position $m$.
* $\theta_i$ — the base frequency for dimension pair $i$; the base (commonly
  10000) is the knob that context-extension methods change.
* $d$ — head dimension.

## Example

Extending a model from 8k to 128k context is usually done by increasing the RoPE
base or interpolating positions so that the rotation frequencies stretch to
cover the longer range, then briefly fine-tuning. This is why "context extension"
is often a RoPE configuration change rather than retraining.

## Real-World Usage

Llama, Qwen, Mistral, DeepSeek and most contemporary open-weight models use RoPE.
Inference engines apply the rotation on the fly during prefill and decode, which
means the KV cache stores rotated keys.

## Common Confusions

* **RoPE vs ALiBi** — ALiBi biases attention scores by distance instead of
  rotating vectors; both give relative position, with different extrapolation
  behaviour.
* **RoPE vs absolute embeddings** — nothing is added to the token embedding;
  the transformation happens inside attention, on queries and keys only.
* **Longer context is not free** — extending RoPE frequencies changes what the
  model was trained on, and quality on long inputs must be measured, not assumed.

## Why Should I Care?

When a model claims a 200k context window, RoPE scaling is usually how it got
there, and understanding it tells you what to distrust about that claim.

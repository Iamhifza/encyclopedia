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
diagram:
  kind: steps
  title: Encode position by rotating, not by adding
  footer: Because the dot product depends only on the offset, a model can be stretched to longer contexts
    by rescaling the frequencies — which is what every context-extension method does.
  steps:
  - title: Each dimension pair turns at its own rate
    notes:
    - label: Range
      text: fast pairs resolve nearby positions, slow pairs distinguish distant ones
    visual:
      kind: plot
      width: 700
      height: 200
      x_range: [0, 16]
      y_range: [-1.2, 1.2]
      x_label: token position
      caption: one curve per dimension pair; a position is the whole set of angles at once
      curves:
      - label: fast pair
        tone: accent
        points: [[0.0, 0.0], [0.33, 0.296], [0.67, 0.565], [1.0, 0.783], [1.33, 0.932], [1.67, 0.997],
          [2.0, 0.974], [2.33, 0.863], [2.67, 0.675], [3.0, 0.427], [3.33, 0.141], [3.67, -0.158], [4.0,
            -0.443], [4.33, -0.688], [4.67, -0.872], [5.0, -0.978], [5.33, -0.996], [5.67, -0.926], [
            6.0, -0.773], [6.33, -0.551], [6.67, -0.279], [7.0, 0.017], [7.33, 0.312], [7.67, 0.578],
          [8.0, 0.794], [8.33, 0.938], [8.67, 0.999], [9.0, 0.97], [9.33, 0.855], [9.67, 0.663], [10.0,
            0.412], [10.33, 0.124], [10.67, -0.174], [11.0, -0.458], [11.33, -0.7], [11.67, -0.88], [
            12.0, -0.981], [12.33, -0.995], [12.67, -0.919], [13.0, -0.762], [13.33, -0.537], [13.67,
            -0.263], [14.0, 0.034], [14.33, 0.327], [14.67, 0.592], [15.0, 0.804], [15.33, 0.944], [15.67,
            0.999], [16.0, 0.966]]
      - label: slower
        points: [[0.0, 0.0], [0.33, 0.116], [0.67, 0.231], [1.0, 0.343], [1.33, 0.45], [1.67, 0.551],
          [2.0, 0.644], [2.33, 0.729], [2.67, 0.804], [3.0, 0.867], [3.33, 0.919], [3.67, 0.959], [4.0,
            0.985], [4.33, 0.999], [4.67, 0.998], [5.0, 0.984], [5.33, 0.957], [5.67, 0.916], [6.0, 0.863],
          [6.33, 0.799], [6.67, 0.723], [7.0, 0.638], [7.33, 0.544], [7.67, 0.442], [8.0, 0.335], [8.33,
            0.223], [8.67, 0.108], [9.0, -0.008], [9.33, -0.125], [9.67, -0.239], [10.0, -0.351], [10.33,
            -0.457], [10.67, -0.558], [11.0, -0.651], [11.33, -0.735], [11.67, -0.809], [12.0, -0.872],
          [12.33, -0.923], [12.67, -0.961], [13.0, -0.987], [13.33, -0.999], [13.67, -0.997], [14.0, -0.982],
          [14.33, -0.954], [14.67, -0.913], [15.0, -0.859], [15.33, -0.793], [15.67, -0.717], [16.0, -0.631]]
      - label: slowest
        tone: muted
        points: [[0.0, 0.0], [0.33, 0.04], [0.67, 0.08], [1.0, 0.12], [1.33, 0.159], [1.67, 0.199], [
            2.0, 0.238], [2.33, 0.276], [2.67, 0.315], [3.0, 0.352], [3.33, 0.389], [3.67, 0.426], [4.0,
            0.462], [4.33, 0.497], [4.67, 0.531], [5.0, 0.565], [5.33, 0.597], [5.67, 0.629], [6.0, 0.659],
          [6.33, 0.689], [6.67, 0.717], [7.0, 0.745], [7.33, 0.771], [7.67, 0.796], [8.0, 0.819], [8.33,
            0.841], [8.67, 0.862], [9.0, 0.882], [9.33, 0.9], [9.67, 0.917], [10.0, 0.932], [10.33, 0.946],
          [10.67, 0.958], [11.0, 0.969], [11.33, 0.978], [11.67, 0.985], [12.0, 0.991], [12.33, 0.996],
          [12.67, 0.999], [13.0, 1.0], [13.33, 1.0], [13.67, 0.998], [14.0, 0.994], [14.33, 0.989], [
            14.67, 0.982], [15.0, 0.974], [15.33, 0.964], [15.67, 0.953], [16.0, 0.94]]
  - title: The score then depends only on the distance
    notes:
    - label: Consequence
      text: no learned position table, and nothing that has to be resized to extend the context
    visual:
      kind: mapping
      width: 720
      head:
      - query at position
      - what its score against key n depends on
      rows:
      - left: m = 5,  key n = 9
        right: n − m = 4
      - left: m = 105, key n = 109
        right: n − m = 4  — identical
        tone: accent
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

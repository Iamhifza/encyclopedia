---
term: Activation Function
aliases: [ReLU, GELU, SwiGLU, Sigmoid, Non-linearity, Softmax]
category: deep-learning
subcategory: basics
depth: full
status: foundational
difficulty: beginner
one_liner: "The small non-linear bend applied between layers, without which any stack of layers collapses into a single one."
tags: [architecture]
relations:
  part_of: [neural-network, feed-forward-network]
  related_to: [transformer, backpropagation, gradient-descent]
prerequisites: [neural-network]
encountered_in: [research-papers, interviews, github]
sources:
  - type: paper
    title: "Deep Sparse Rectifier Neural Networks (ReLU)"
    url: https://proceedings.mlr.press/v15/glorot11a.html
    year: 2011
  - type: paper
    title: "Gaussian Error Linear Units (GELUs)"
    url: https://arxiv.org/abs/1606.08415
    year: 2016
  - type: paper
    title: "GLU Variants Improve Transformer"
    url: https://arxiv.org/abs/2002.05202
    year: 2020
updated: 2026-08-21
---

## Simple Explanation

Stack two matrix multiplications and you get… one matrix multiplication. The
maths collapses. Adding a hundred layers changes nothing unless something
non-linear sits between them.

The activation function is that something. It is usually trivially simple —
ReLU is *"if the number is negative, make it zero"* — and it is the entire reason
depth buys you anything.

## Technical Definition

An element-wise non-linear function applied to a layer's pre-activations. Its
essential properties are non-linearity (so composition is expressive),
differentiability almost everywhere (so gradients flow), and a derivative that
neither vanishes nor explodes across the range in which the network operates.

## Why Does It Exist?

Because $W_2(W_1 x) = (W_2 W_1)x$. Without a non-linearity between them, any
number of linear layers is equivalent to a single linear layer, and a linear
model cannot represent XOR, let alone language.

## What Problem Does It Solve?

It makes depth meaningful, and it decides how well gradients survive
backpropagation through many layers.

## How Does It Work?

```text
ReLU        GELU              SwiGLU
    │  ╱        │  ╱              gate branch × activated branch
    │ ╱         │ ╱               (learned suppression)
────┼─────   ──╱┼─────
    │         ╱ │
zero below   smooth near      the layer can turn its own
zero         zero, small      features down
             negative values
```

Sigmoid and tanh were standard until roughly 2011 and are now rare in hidden
layers: both saturate, meaning their derivative approaches zero for large inputs,
so gradients die in deep stacks. ReLU's constant derivative of 1 for positive
inputs is what made very deep networks trainable.

## Mental Model

A valve. It decides how much of each signal passes onward, and the *shape* of
that decision is what gives the network its expressive power.

## Formula

$$\text{ReLU}(x) = \max(0, x) \qquad \text{GELU}(x) = x \cdot \Phi(x) \qquad \text{SwiGLU}(x) = \text{Swish}(W_1x) \odot W_3x$$

* $\Phi(x)$ — the standard normal cumulative distribution; GELU weights the input
  by the probability it exceeds a random draw, giving a smooth version of ReLU.
* $\text{Swish}(x) = x \cdot \sigma(\beta x)$ — smooth, non-monotonic, with a
  small dip below zero.
* $\odot$ — element-wise product; the gate branch $W_3x$ can suppress features
  the other branch produced, which is what "gated" means.

## Example

The practical history is short. Sigmoid and tanh until 2011; ReLU through the
deep learning boom, with the "dying ReLU" problem (units stuck permanently at
zero) prompting variants like Leaky ReLU; GELU with BERT and GPT; SwiGLU in most
current large models. The gains at each step are modest and consistent — this is
not where breakthroughs happen, but the choices compound.

## Real-World Usage

SwiGLU in current large Transformers, GELU in slightly older ones, ReLU still
common in vision and anywhere simplicity matters. Softmax is a related but
different creature: it operates across a vector rather than element-wise, turning
scores into a distribution, and appears in attention and at the output layer.

## Common Confusions

* **Activation function vs activations** — the function versus the values it
  produces. Interpretability work studies the second.
* **Softmax is not an activation function in the usual sense** — it is not
  element-wise, and it normalises across positions.
* **The choice matters less than it once did** — with residual connections and
  normalisation handling gradient flow, differences between modern activations
  are small. Do not expect a new one to transform your results.

## Why Should I Care?

It is the smallest component with the largest structural consequence: remove it
and the deepest network in the world becomes a linear regression.

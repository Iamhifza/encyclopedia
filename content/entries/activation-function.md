---
term: Activation Function
aliases: [ReLU, GELU, SwiGLU, Sigmoid, Non-linearity, Softmax]
category: deep-learning
subcategory: basics
depth: full
status: foundational
difficulty: beginner
one_liner: "The small non-linear bend applied between layers, without which any stack of layers collapses into a single one."
historical_period: statistical-ml
diagram:
  kind: figure
  title: The bend is the whole point
  footer: Without any activation at all, a stack of layers collapses algebraically into a single matrix — depth
    buys nothing. Which non-linearity you pick is an empirical detail; that there is one is not.
  visual:
    kind: plot
    width: 700
    height: 230
    x_range: [-3, 1.6]
    y_range: [-0.45, 1.75]
    x_label: input
    y_label: output
    caption: 'the family splits on one question: what to do with negative input — the dip is what
      lets a layer suppress its own features'
    bands:
    - from: -3
      to: 0
      text: negative input
    curves:
    - label: ReLU
      points: [[-3, 0], [0, 0], [1.6, 1.6]]
    - label: GELU
      tone: accent
      points: [[-3.0, -0.004], [-2.81, -0.007], [-2.62, -0.012], [-2.42, -0.019], [-2.23, -0.029], [-2.04, -0.042],
        [-1.85, -0.059], [-1.66, -0.081], [-1.47, -0.104], [-1.28, -0.129], [-1.08, -0.151], [-0.89, -0.166], [
          -0.7, -0.169], [-0.51, -0.155], [-0.32, -0.119], [-0.12, -0.056], [0.07, 0.035], [0.26, 0.155], [0.45,
          0.303], [0.64, 0.474], [0.83, 0.665], [1.02, 0.869], [1.22, 1.081], [1.41, 1.296], [1.6, 1.512]]
    - label: SiLU
      tone: muted
      points: [[-3.0, -0.142], [-2.81, -0.16], [-2.62, -0.178], [-2.42, -0.197], [-2.23, -0.216], [-2.04, -0.235],
        [-1.85, -0.251], [-1.66, -0.265], [-1.47, -0.275], [-1.28, -0.278], [-1.08, -0.274], [-0.89, -0.259], [
          -0.7, -0.232], [-0.51, -0.191], [-0.32, -0.133], [-0.12, -0.059], [0.07, 0.034], [0.26, 0.146], [0.45,
          0.275], [0.64, 0.42], [0.83, 0.581], [1.02, 0.754], [1.22, 0.939], [1.41, 1.132], [1.6, 1.331]]
    marks:
    - at: [-0.9, -0.166]
      dy: -40
      anchor: middle
      text: a small dip below zero
      tone: accent
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

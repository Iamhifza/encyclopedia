---
term: Residual Connection
aliases: [Skip Connection, ResNet, Residual Stream, Shortcut Connection]
category: deep-learning
subcategory: basics
depth: full
status: foundational
difficulty: intermediate
one_liner: "Adding a layer's input to its output, giving gradients a clear path backwards and making very deep networks trainable."
historical_period: deep-learning
tags: [architecture]
relations:
  part_of: [transformer]
  successor_of: [lstm]
  related_to: [mechanistic-interpretability, backpropagation, layer-normalisation]
prerequisites: [backpropagation, neural-network]
encountered_in: [research-papers, interviews, github]
sources:
  - type: paper
    title: "Deep Residual Learning for Image Recognition (ResNet)"
    url: https://arxiv.org/abs/1512.03385
    year: 2015
  - type: paper
    title: "A Mathematical Framework for Transformer Circuits"
    url: https://transformer-circuits.pub/2021/framework/index.html
    year: 2021
    note: The residual stream reading of the architecture.
updated: 2026-08-21
---

## Simple Explanation

Before 2015, deeper networks got *worse* past a certain point — not from
overfitting, but because they became untrainable. The fix is almost absurdly
simple: instead of each layer producing its output from scratch, have it produce
a *correction* that gets added to its input.

`output = input + layer(input)`

That single plus sign is what allows networks to be a hundred layers deep.

## Technical Definition

A shortcut path adding a sublayer's input to its output, so the sublayer learns a
residual function $F(x)$ with the block computing $x + F(x)$. During
backpropagation the identity path contributes a gradient of 1, so gradients reach
early layers without being repeatedly attenuated by intermediate weight matrices.

## Why Does It Exist?

Gradients in a deep stack are products of many terms. Multiply a hundred numbers
slightly below one and you get approximately zero — the vanishing gradient
problem. The identity shortcut gives the gradient a route that involves no
multiplication at all.

## What Problem Does It Solve?

Trainability at depth. The degradation problem it fixed was not overfitting: the
deeper network was worse on *training* data too, which is what made it a
mystery worth solving.

## How Does It Work?

```text
        x ──────────────────┐  identity path: gradient passes through unchanged
        │                   │
        ▼                   ▼
     [ layer ] ──▶ F(x) ──▶ (+) ──▶ x + F(x)

deep stack:  x₀ ──▶ x₀+F₁ ──▶ x₀+F₁+F₂ ──▶ x₀+F₁+F₂+F₃ ...
             every layer reads the running sum and adds to it
```

## Mental Model

An editorial process where each pass suggests amendments to a shared draft rather
than rewriting it from nothing. A bad pass contributes little; nothing earlier is
destroyed.

## Formula

$$y = x + F(x), \qquad \frac{\partial y}{\partial x} = 1 + \frac{\partial F}{\partial x}$$

The `1` is the entire contribution. Even when $\partial F / \partial x$ is
vanishingly small, the gradient flowing back is at least 1 — so early layers keep
receiving a usable signal regardless of depth.

## Example

ResNet trained networks of 152 layers when the previous practical ceiling was
around 20, and won ImageNet 2015 doing it. Every Transformer block since applies
the same idea twice — once around attention, once around the feed-forward network.

## Real-World Usage

Universal in deep learning. In Transformers the accumulating sum is called the
**residual stream**, and mechanistic interpretability treats it as the model's
central communication channel: each attention head and FFN reads from it and
writes back to it, which is what makes it possible to attribute a behaviour to a
specific component.

## Common Confusions

* **Residual vs skip connection** — used interchangeably; some reserve "skip" for
  longer-range connections such as U-Net's, which concatenate rather than add.
* **Addition, not concatenation** — the dimension is unchanged, which is why the
  stream can accumulate across a hundred layers without growing.
* **Pre-norm vs post-norm** — where layer normalisation sits relative to the
  addition materially affects training stability. Modern models normalise before
  the sublayer.

## Why Should I Care?

It is a one-line change that unlocked deep learning at depth, and the residual
stream it creates is the object interpretability research actually studies when
it tries to work out what a model is doing.

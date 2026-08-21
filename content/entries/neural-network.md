---
term: Neural Network
aliases: [Artificial Neural Network, ANN, Deep Network, MLP]
category: deep-learning
subcategory: basics
status: foundational
difficulty: beginner
one_liner: Layers of simple weighted sums with a non-linear squash between them, trained by nudging every weight toward less error.
origin:
  year: 1943
  attribution: McCulloch and Pitts proposed the first mathematical neuron; practical multilayer training arrived with backpropagation in 1986
historical_period: early-computing
tags: [architecture]
relations:
  successor_of: [perceptron]
  depends_on: [backpropagation]
  used_by: [transformer, rnn]
  related_to: [gpu]
encountered_in: [research-papers, interviews, job-descriptions]
sources:
  - type: paper
    title: "A Logical Calculus of the Ideas Immanent in Nervous Activity"
    url: https://link.springer.com/article/10.1007/BF02478259
    year: 1943
  - type: book
    title: "Deep Learning (Goodfellow, Bengio, Courville)"
    url: https://www.deeplearningbook.org/
    year: 2016
updated: 2026-08-21
---

## Simple Explanation

Stack layers. Each layer multiplies its inputs by learned weights, adds them up,
and bends the result through a simple non-linear function. Nothing in any single
layer is clever; the capability comes from stacking many and letting training
decide what each one should detect.

## Technical Definition

A parameterised function composed of alternating affine transforms and
element-wise non-linearities: $h_{l} = \sigma(W_l h_{l-1} + b_l)$. With at least
one hidden layer and a non-polynomial activation it is a universal approximator;
parameters are fit by gradient descent on a differentiable loss.

## Why Does It Exist?

A single linear model cannot represent XOR, let alone images or language. The
non-linearity between layers is what allows composition to buy expressiveness —
without it, any stack of layers collapses into a single matrix.

## What Problem Does It Solve?

It replaces hand-designed features with learned ones. Instead of an engineer
deciding what to measure, the network discovers intermediate representations
that make the final decision easy.

## How Does It Work?

```text
input ──▶ [W1 · x + b1] ──▶ σ ──▶ [W2 · h + b2] ──▶ σ ──▶ ... ──▶ output
                                                                     │
        gradients flow backwards, adjusting every W  ◀───── loss ◀───┘
```

Forward pass computes a prediction; the loss measures how wrong it is;
backpropagation attributes that error to every parameter; the optimiser takes a
small step downhill. Repeat billions of times.

## Mental Model

An assembly line where every station is initially random, and after each faulty
product every station is told, precisely, how much it contributed to the fault.

## Formula

$$h_l = \sigma\!\left(W_l h_{l-1} + b_l\right)$$

* $h_{l-1}$ — the previous layer's output (the input for layer 1).
* $W_l$, $b_l$ — learned weight matrix and bias for layer $l$.
* $\sigma$ — non-linearity, in practice usually ReLU, GELU or SwiGLU.

## Example

A two-layer network with two hidden units solves XOR, which one perceptron
cannot: the hidden units learn "at least one input is on" and "both inputs are
on", and the output layer subtracts the second from the first.

## Real-World Usage

Every model in this encyclopedia is a neural network with structural
constraints. A Transformer is a neural network whose layers are attention plus a
two-layer MLP; a CNN is one whose layers share weights across space.

## Common Confusions

* **Neural network vs brain** — the resemblance is a naming accident from 1943,
  not a design goal. Backpropagation has no plausible biological analogue.
* **Deep vs shallow** — depth is not just more parameters; it lets features
  compose hierarchically, which is what makes deep networks sample-efficient on
  structured data.

## Why Should I Care?

Once you see that everything is layers, weights and gradients, new architectures
stop looking like new fields and start looking like different wiring diagrams
over the same machinery.

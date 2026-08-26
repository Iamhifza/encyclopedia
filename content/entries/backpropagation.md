---
term: Backpropagation
aliases: [Backprop, Reverse-Mode Automatic Differentiation]
category: deep-learning
subcategory: basics
status: foundational
difficulty: intermediate
one_liner: The algorithm that works out how much each weight in a network contributed to the error, by applying the chain rule backwards through the layers.
origin:
  year: 1986
  attribution: Popularised by Rumelhart, Hinton and Williams; equivalent methods appear in control theory from the 1960s and in Linnainmaa's 1970 work
historical_period: ai-winter
diagram:
  kind: figure
  title: One path, travelled twice
  footer: 'Memory is the price: every saved activation stays resident until the backward pass consumes
    it, which is why activation checkpointing trades recomputation for room.'
  visual:
    kind: passes
    width: 760
    nodes:
    - text: x
    - text: layer 1
      note: save
    - text: layer 2
      note: save
    - text: layer 3
      note: save
    - text: loss
      tone: accent
    forward:
      label: forward — compute and remember
    backward:
      label: backward — apply the chain rule, right to left
      marks:
      - ∂L/∂W₁
      - ∂L/∂W₂
      - ∂L/∂W₃
      - ∂L/∂out
    caption: each backward step reuses the activation the forward step saved
tags: [training]
relations:
  used_by: [neural-network, pretraining]
  related_to: [gpu]
encountered_in: [research-papers, interviews]
sources:
  - type: paper
    title: "Learning Representations by Back-Propagating Errors"
    url: https://www.nature.com/articles/323533a0
    year: 1986
  - type: docs
    title: "PyTorch autograd mechanics"
    url: https://pytorch.org/docs/stable/notes/autograd.html
videos:
  - title: "Backpropagation, intuitively"
    channel: "3Blue1Brown"
    url: https://www.youtube.com/results?search_query=3blue1brown+backpropagation+intuitively
  - title: "Backpropagation calculus"
    channel: "3Blue1Brown"
    url: https://www.youtube.com/results?search_query=3blue1brown+backpropagation+calculus
    note: "The chain rule made visual"
updated: 2026-08-21
---

## Simple Explanation

The network makes a prediction and gets it wrong by some amount. Backpropagation
answers one question for every single weight: if I nudged you slightly, would the
error go up or down, and by how much? It answers this for millions of weights in
roughly the cost of one forward pass.

## Technical Definition

Reverse-mode automatic differentiation applied to a computational graph. The
chain rule is evaluated from the loss backwards, reusing intermediate results, so
the gradient of a scalar loss with respect to all parameters costs $O(1)$ forward
passes rather than one per parameter.

## Why Does It Exist?

Multilayer networks were known to be more expressive than perceptrons long
before anyone could train them. Estimating each weight's effect by perturbing it
individually is hopeless at scale. Backpropagation made hidden layers trainable,
which is the entire reason deep learning exists.

## What Problem Does It Solve?

Credit assignment: which of the millions of interacting parameters is
responsible for this particular mistake.

## How Does It Work?

Each layer receives the gradient of the loss with respect to its output,
multiplies by its local derivative, and passes the result down. Activations from
the forward pass must be kept in memory — which is why training needs far more
memory than inference.

## Mental Model

A factory traces a defect backwards through the line, and each station is told
its exact share of the blame in one sweep, rather than every station guessing by
trial and error.

## Formula

$$\frac{\partial L}{\partial W_l} = \delta_l \, h_{l-1}^\top, \qquad \delta_{l-1} = \left(W_l^\top \delta_l\right) \odot \sigma'(z_{l-1})$$

* $\delta_l$ — error signal arriving at layer $l$.
* $h_{l-1}$ — activation saved from the forward pass.
* $\sigma'$ — derivative of the activation function.
* $\odot$ — element-wise product.

## Example

In PyTorch the entire algorithm is `loss.backward()`. The framework recorded the
graph during the forward pass and replays it in reverse, filling in `.grad` on
every parameter tensor.

## Real-World Usage

Every trained model, without exception, from a two-layer classifier to a
frontier LLM. Variants such as gradient checkpointing trade recomputation for
memory when the saved activations no longer fit.

## Common Confusions

* **Backpropagation vs gradient descent** — backprop computes the gradient;
  gradient descent (or Adam) decides what step to take with it.
* **Backprop vs "learning"** — it is only credit assignment. Data, objective and
  optimiser do the rest.

## Why Should I Care?

Vanishing gradients, exploding gradients, activation memory, gradient
checkpointing and most of what makes long-sequence training hard are all direct
consequences of how this algorithm works.

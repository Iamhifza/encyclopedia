---
term: Neural Network
aliases: [Artificial Neural Network, ANN, Deep Network, MLP, Multilayer Perceptron]
category: deep-learning
subcategory: basics
depth: full
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
  depends_on: [backpropagation, gradient-descent, activation-function, linear-algebra]
  used_by: [transformer, rnn, cnn, autoencoder, diffusion-model]
  related_to: [gpu, overfitting, residual-connection, sparse-autoencoder]
prerequisites: [linear-algebra]
encountered_in: [research-papers, interviews, job-descriptions]
sources:
  - type: paper
    title: "A Logical Calculus of the Ideas Immanent in Nervous Activity"
    url: https://link.springer.com/article/10.1007/BF02478259
    year: 1943
  - type: paper
    title: "Learning Representations by Back-Propagating Errors"
    url: https://www.nature.com/articles/323533a0
    year: 1986
  - type: book
    title: "Deep Learning (Goodfellow, Bengio, Courville)"
    url: https://www.deeplearningbook.org/
    year: 2016
updated: 2026-08-22
---

## Simple Explanation

Stack layers. Each layer multiplies its inputs by learned weights, adds them up,
and bends the result through a simple non-linear function. Nothing in any single
layer is clever. The capability comes from stacking many of them and letting
training decide what each one should detect.

Everything in this encyclopedia with "model" in its name is this, with
constraints on how the layers are wired.

## Technical Definition

A parameterised function composed of alternating affine transforms and
element-wise non-linearities: $h_l = \sigma(W_l h_{l-1} + b_l)$. With at least one
hidden layer and a non-polynomial [activation](activation-function.md) it is a
universal approximator. Parameters are fit by
[gradient descent](gradient-descent.md) on a differentiable
[loss](loss-function.md), with gradients supplied by
[backpropagation](backpropagation.md).

## Why Does It Exist?

A single linear model cannot represent XOR, let alone images or language. The
non-linearity between layers is what allows composition to buy expressiveness:
without it, any stack of layers collapses algebraically into a single matrix, and
depth is worthless.

## What Problem Does It Solve?

It replaces hand-designed features with learned ones. Instead of an engineer
deciding what to measure — the approach [computer vision](computer-vision.md)
took for forty years — the network discovers intermediate representations that
make the final decision easy.

## How Does It Work?

```text
input ──▶ [W1·x + b1] ──▶ σ ──▶ [W2·h + b2] ──▶ σ ──▶ ... ──▶ output
                                                                  │
        gradients flow backwards, adjusting every W  ◀──── loss ◀─┘

forward:  compute a prediction
loss:     measure how wrong it is
backward: attribute that error to every parameter
step:     move each one slightly downhill
          repeat, billions of times
```

Two structural additions turned this from a shallow technique into a deep one:
[residual connections](residual-connection.md), which give gradients an
unobstructed path backwards, and [normalisation](layer-normalisation.md), which
keeps activations in a usable range. Without both, networks beyond about twenty
layers were effectively untrainable.

## Mental Model

An assembly line where every station is initially random, and after each faulty
product every station is told precisely how much it contributed to the fault.

## Formula

$$h_l = \sigma\!\left(W_l h_{l-1} + b_l\right)$$

* $h_{l-1}$ — the previous layer's output; the input for layer 1.
* $W_l$, $b_l$ — learned weight matrix and bias for layer $l$.
* $\sigma$ — the non-linearity: ReLU, GELU or SwiGLU in practice.

Every architecture in this encyclopedia is a statement about how to constrain
$W$. A [CNN](cnn.md) shares weights across spatial positions. A
[Transformer](transformer.md) makes some of them depend on the input itself,
which is what attention is. An [RNN](rnn.md) reuses the same matrix at every time
step.

## Example

A two-layer network with two hidden units solves XOR, which one
[perceptron](perceptron.md) cannot. The hidden units learn "at least one input is
on" and "both inputs are on"; the output layer subtracts the second from the
first.

That is the smallest complete demonstration that depth plus non-linearity buys
representational power — the observation Minsky and Papert's 1969 critique was
read as refuting, and which took seventeen years and backpropagation to make
practical.

## Real-World Usage

Every model here is a neural network with structural constraints. A Transformer
is one whose layers are attention plus a two-layer MLP. A CNN is one whose layers
share weights across space. A [diffusion model](diffusion-model.md) is one applied
repeatedly to denoise.

The plain stacked form — the multilayer perceptron — still appears inside larger
architectures, most importantly as the
[feed-forward network](feed-forward-network.md) in every Transformer block, where
it holds roughly two-thirds of the parameters.

## Common Confusions

* **Neural network vs brain** — the resemblance is a naming accident from 1943,
  not a design goal. Backpropagation has no plausible biological analogue.
* **Deep vs shallow** — depth is not merely more parameters. It lets features
  compose hierarchically, which is what makes deep networks sample-efficient on
  structured data.
* **Layers are not concepts** — individual neurons are usually polysemantic,
  responding to unrelated things. See
  [sparse autoencoders](sparse-autoencoder.md) for what it takes to recover
  interpretable features.
* **Universal approximation is not a practical claim** — the theorem says a wide
  enough network *can* represent the function. It says nothing about whether
  gradient descent will find it.

## Why Should I Care?

Once you see that everything is layers, weights and gradients, new architectures
stop looking like new fields and start looking like different wiring diagrams
over the same machinery. That reframing is most of what separates reading a paper
from being intimidated by one.

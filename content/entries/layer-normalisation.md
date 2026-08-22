---
term: Layer Normalisation
aliases: [LayerNorm, RMSNorm, Normalization, Pre-Norm, Post-Norm]
category: deep-learning
subcategory: basics
depth: full
status: established
difficulty: advanced
one_liner: "Rescaling a layer's activations to a consistent range so training stays stable at depth."
origin:
  year: 2016
  attribution: Ba, Kiros and Hinton; adapted from batch normalisation for sequence models
historical_period: deep-learning
tags: [architecture]
relations:
  part_of: [transformer]
  related_to: [residual-connection, backpropagation, gradient-descent]
prerequisites: [neural-network, backpropagation]
encountered_in: [research-papers, github, interviews]
sources:
  - type: paper
    title: "Layer Normalization"
    url: https://arxiv.org/abs/1607.06450
    year: 2016
  - type: paper
    title: "Root Mean Square Layer Normalization (RMSNorm)"
    url: https://arxiv.org/abs/1910.07467
    year: 2019
  - type: paper
    title: "On Layer Normalization in the Transformer Architecture"
    url: https://arxiv.org/abs/2002.04745
    year: 2020
updated: 2026-08-21
---

## Simple Explanation

Activations passing through a hundred layers tend to drift — growing, shrinking,
spreading out — and once they leave a sensible range, gradients become useless
and training collapses.

Normalisation resets the scale at every step. Take the vector, subtract its mean,
divide by its standard deviation, then apply two learned parameters so the layer
can undo the normalisation if that turns out to be useful.

## Technical Definition

Normalisation over the feature dimension of each token independently:
$\hat{x} = \frac{x - \mu}{\sigma} \cdot \gamma + \beta$, where $\mu$ and $\sigma$
are computed across that token's features. Unlike batch normalisation, statistics
are per-example, so behaviour is identical whatever the batch size and whether
training or serving — which is why sequence models use it.

## Why Does It Exist?

Batch normalisation was standard in vision and unsuitable here: it computes
statistics across the batch, which breaks with variable-length sequences, behaves
differently at inference, and interacts badly with small batches. Layer
normalisation removed the dependence on other examples entirely.

## What Problem Does It Solve?

Training stability at depth, and tolerance of larger learning rates — which
translates directly into faster convergence.

## How Does It Work?

```text
PRE-NORM (modern)                POST-NORM (original 2017)
x ──┬── norm ── attn ──┐         x ──── attn ──┬── + ── norm ──▶
    └───────────── + ──┴──▶          └─────────┘
gradient reaches x through       gradient passes through norm
an unobstructed identity path    at every layer
stable without warmup            needs careful warmup, unstable deep
```

The pre-norm versus post-norm choice looks like a detail and is not: it is much of
why very deep Transformers became trainable without elaborate learning rate
schedules.

## Mental Model

A volume normaliser between every stage of an audio chain. Each stage receives a
signal at a predictable level, so nothing clips and nothing vanishes.

## Formula

$$\text{LayerNorm}(x) = \frac{x - \mu}{\sqrt{\sigma^2 + \epsilon}} \cdot \gamma + \beta \qquad \text{RMSNorm}(x) = \frac{x}{\sqrt{\frac{1}{n}\sum x_i^2 + \epsilon}} \cdot \gamma$$

* $\mu, \sigma$ — mean and standard deviation across the token's features.
* $\gamma, \beta$ — learned scale and shift, so the layer retains the ability to
  represent unnormalised distributions.
* $\epsilon$ — small constant preventing division by zero.
* RMSNorm drops the mean subtraction and the shift entirely — fewer operations,
  comparable quality, which is why it is now standard in large models.

## Example

The empirical finding that reorganised the block: post-norm Transformers require
a learning rate warmup to train at all beyond modest depth, while pre-norm ones
train stably without it. Nearly every current large model is pre-norm with
RMSNorm, and some add a further normalisation before the output projection for
stability at scale.

## Real-World Usage

Twice per Transformer block, before attention and before the feed-forward network.
Its inference cost is small in FLOPs and non-trivial in memory traffic, which is
why it is a standard target for kernel fusion.

## Common Confusions

* **LayerNorm vs BatchNorm** — across features of one example versus across
  examples in a batch. The second is unusable for variable-length sequences.
* **Pre-norm vs post-norm** — where it sits relative to the residual addition;
  materially affects trainability rather than being cosmetic.
* **It is not regularisation** — despite superficial resemblance, its job is
  stability, not reducing overfitting.

## Why Should I Care?

It is one of a small set of unglamorous components — alongside residual
connections — that make depth work at all, and the pre-norm shift is a good
example of a one-line architectural change with outsized consequences.

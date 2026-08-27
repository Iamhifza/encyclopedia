---
term: JEPA
aliases: [Joint Embedding Predictive Architecture, I-JEPA, V-JEPA]
category: world-models-embodied
subcategory: world-models
status: experimental
difficulty: research
one_liner: An architecture that learns by predicting missing parts of an input in representation space rather than reconstructing raw pixels.
origin:
  year: 2022
  attribution: Proposed by Yann LeCun in "A Path Towards Autonomous Machine Intelligence"; I-JEPA and V-JEPA followed at Meta
historical_period: foundation-model
diagram:
  kind: figure
  title: Predict the representation, not the pixels
  footer: The argument is that reconstructing pixels wastes capacity on detail that carries no meaning
    — the exact texture of grass. Predicting in embedding space lets the model discard what does not matter,
    which is the whole bet.
  visual:
    kind: columns
    width: 740
    caption: the target encoder is an exponential moving average of the context encoder, which is what
      stops both collapsing to a constant
    columns:
    - title: Masked autoencoder
      lines:
      - predict the missing pixels
      - loss in pixel space
      - spends capacity on texture
      - reconstruction is the objective
    - title: JEPA
      accent: true
      lines:
      - predict the missing embedding
      - loss in representation space
      - free to discard detail
      - abstraction is the objective
tags: [architecture]
relations:
  is_a: [world-model]
  depends_on: [self-supervised-learning]
  alternative_to: [large-language-model]
  related_to: [embedding]
prerequisites: [self-supervised-learning, world-model]
encountered_in: [research-papers, conferences]
sources:
  - type: paper
    title: "A Path Towards Autonomous Machine Intelligence"
    url: https://openreview.net/forum?id=BZ5a1r-kVsf
    year: 2022
  - type: paper
    title: "Self-Supervised Learning from Images with a Joint-Embedding Predictive Architecture (I-JEPA)"
    url: https://arxiv.org/abs/2301.08243
    year: 2023
updated: 2026-08-21
review_by: 2027-02-01
---

## Simple Explanation

Predicting exact pixels wastes capacity on detail nobody needs — the precise
texture of grass, the exact position of every leaf. JEPA predicts the *abstract
representation* of the missing part instead. It has to capture what matters and is
free to ignore what does not.

## Technical Definition

A self-supervised architecture predicting the embedding of a target block from
the embedding of a context block, using an encoder for each and a predictor
conditioned on positional information. Because prediction happens in latent
space, the objective does not force modelling of unpredictable low-level detail.
Representation collapse is avoided by asymmetry, such as a target encoder updated
as an exponential moving average.

## Why Does It Exist?

It is the concrete instantiation of an argument: that generative
pixel-reconstruction and next-token prediction both spend capacity on
irreducible noise, and that abstract prediction is what enables planning and
common-sense physical understanding.

## What Problem Does It Solve?

Learning useful abstract representations from unlabelled images and video without
generative reconstruction, and providing a substrate for a hierarchical world
model.

## How Does It Work?


Mask part of an input, and train a model to predict the *representation* of the
masked part rather than its raw content. A context encoder embeds what is
visible; a predictor guesses the embedding of what is hidden; a target encoder —
an exponential moving average of the context encoder, not trained directly —
produces the embedding being guessed at.

The argument against pixel reconstruction is that most of a pixel's information
is irrelevant. Predicting the exact texture of grass or the precise noise in a
shadow spends capacity on detail that carries no meaning, and a model rewarded
for getting it right learns to represent it. Predicting in embedding space lets
the model discard whatever it decides does not matter.

The risk is collapse: if both encoders can simply output a constant, the
prediction is trivially perfect and nothing is learned. The moving-average target
encoder is what prevents that — it changes slowly enough to be a stable target
and is never optimised to make the task easy. Whether the resulting
representations are better than reconstruction-based ones is still being argued,
which is what makes this a live research direction rather than a settled method.

## Mental Model

Describing what is behind a curtain in terms of *what sort of thing* it is, not
by drawing it exactly.

## Example

V-JEPA learns from video by predicting representations of masked spatiotemporal
regions, aiming at physical intuition — object permanence, plausible motion —
rather than at generating footage.

## Common Confusions

* **JEPA is not a generative model** — it produces representations, not images or
  video. Comparing it with diffusion models on sample quality is a category error.
* **It is not yet a competitive general architecture** — results are promising in
  representation learning benchmarks; nothing on the scale of LLM capability has
  been demonstrated.

## Real-World Usage

Research, primarily at Meta and in academic labs, and as the technical anchor of
the argument that autoregressive language modelling is not sufficient for
intelligence.

## Why Should I Care?

It is the clearest technical statement of the leading dissenting position on how
AI should be built, and it is worth understanding on its merits rather than
through the debate around it.

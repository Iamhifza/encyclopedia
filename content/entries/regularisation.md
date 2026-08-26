---
term: Regularisation
aliases: [Regularization, Weight Decay, Dropout, Early Stopping, L2 Penalty]
category: math-for-ai
subcategory: optimisation
depth: full
status: foundational
difficulty: intermediate
one_liner: "Deliberately limiting how well a model can fit its training data, so that it fits reality better."
historical_period: early-computing
diagram:
  kind: figure
  title: Five ways to make memorising harder than generalising
  footer: All of them trade training fit for held-out performance, and all of them have a strength you
    have to choose. Too little and nothing changes; too much and the model cannot fit the signal either.
  visual:
    kind: stack
    width: 760
    caption: in practice several run at once, and their strengths interact
    layers:
    - label: weight decay
      text: add λ‖w‖² to the loss, so large weights cost something
      note: L2
    - label: dropout
      text: zero random units during training, so none can rely on another
      note: 0.1 – 0.5
    - label: early stopping
      text: halt when validation loss turns upward
      note: free
      accent: true
    - label: augmentation
      text: show transformed copies, so particular examples cannot be memorised
      note: domain-specific
    - label: label smoothing
      text: target 0.9 rather than 1.0, discouraging overconfidence
      note: 0.05 – 0.1
tags: [training]
relations:
  solves: [overfitting]
  used_by: [supervised-learning, pretraining]
  related_to: [generalisation, loss-function, gradient-descent]
prerequisites: [overfitting, loss-function]
encountered_in: [research-papers, interviews, github]
sources:
  - type: paper
    title: "Dropout: A Simple Way to Prevent Neural Networks from Overfitting"
    url: https://jmlr.org/papers/v15/srivastava14a.html
    year: 2014
  - type: paper
    title: "Decoupled Weight Decay Regularization (AdamW)"
    url: https://arxiv.org/abs/1711.05101
    year: 2017
updated: 2026-08-21
---

## Simple Explanation

A model that fits its training data perfectly has usually learned the noise along
with the signal. Regularisation is the family of techniques that deliberately
make fitting harder — penalising large weights, randomly switching units off,
stopping training early — on the theory that a model forced to be simple will
have found something more general.

It is the counterintuitive core of machine learning: making the model worse at
the thing you measure, to make it better at the thing you want.

## Technical Definition

Any modification intended to reduce generalisation error without necessarily
reducing training error. Explicit forms add a penalty term to the loss; implicit
forms constrain the optimisation itself — early stopping, data augmentation,
stochastic gradient noise, or architectural limits on capacity.

## Why Does It Exist?

Because the training loss is the wrong objective. It measures fit to a finite
sample, and the model has enough capacity to fit that sample's accidents. Nothing
in the loss distinguishes signal from noise; regularisation encodes a prior that
simpler explanations are more likely to be right.

## What Problem Does It Solve?

Overfitting, and the gap between training and held-out performance.

## How Does It Work?


Every regularisation technique does the same thing by a different route: it makes
memorising specific examples more expensive than learning the pattern behind
them. None of them adds information; they constrain what the model is allowed to
prefer.

Weight decay adds the squared magnitude of the weights to the loss, so a solution
using large weights must earn them. Dropout removes random units during training,
so no unit can depend on any other being present and the network is forced into
redundant representations. Early stopping simply halts before the memorising
phase begins. Augmentation shows transformed copies, so no particular example can
be learned exactly. Label smoothing asks for 0.9 rather than 1.0, discouraging
the model from becoming certain.

All of them trade fit on the training set for performance on everything else, and
all have a strength you must choose. Too little changes nothing; too much stops
the model fitting the signal along with the noise. In practice several run
together, and their strengths interact — which is why the settings are usually
inherited from a recipe that worked rather than derived.

## Mental Model

A handicap in a race. You are deliberately restricting the runner, because
whoever wins under the handicap is the one with genuine ability rather than the
one who found a shortcut.

## Formula

$$\mathcal{L}_{\text{total}} = \mathcal{L}_{\text{data}} + \lambda \lVert w \rVert^2$$

* $\mathcal{L}_{\text{data}}$ — the ordinary loss on the training data.
* $\lambda$ — regularisation strength; zero means no penalty, too large means the
  model cannot fit anything.
* $\lVert w \rVert^2$ — sum of squared weights, so the penalty grows sharply as
  weights get large.

Weight decay in AdamW is subtly different from adding this term to the loss —
decoupling them is precisely what the AdamW paper fixed, because with adaptive
optimisers the two are not equivalent.

## Example

Modern LLM training complicates the classical picture. Frontier models are
trained on so much data, often for a single pass, that overfitting in the
textbook sense barely arises — every example is essentially new. Dropout, once
universal, is frequently omitted entirely. What survives is weight decay, mostly
for optimisation stability rather than for generalisation, which is a notable
inversion of its original purpose.

## Real-World Usage

Weight decay in essentially every training run. Dropout in fine-tuning and in
smaller-data regimes. Early stopping wherever a validation set exists. Data
augmentation heavily in vision, and in language mainly as paraphrase or synthetic
variation.

## Common Confusions

* **Regularisation is not normalisation** — one constrains the model to
  generalise, the other rescales activations for stability. The words are
  similar and the purposes are unrelated.
* **More is not safer** — over-regularising underfits, which is a real failure
  and harder to spot than overfitting.
* **Its role has shrunk at scale** — advice from the small-data era transfers
  poorly to models trained on trillions of tokens.

## Why Should I Care?

It is the classical answer to the central problem of the field, and knowing why
it matters less in LLM pretraining than in traditional machine learning tells you
something real about what changes at scale.

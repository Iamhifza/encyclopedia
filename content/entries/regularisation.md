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

```text
L2 / weight decay   loss + λ‖w‖²        large weights cost something,
                                        so the model prefers small ones

dropout             randomly zero units during training,
                    so no unit can rely on any other being present

early stopping      halt when validation loss turns upward

augmentation        show transformed copies, so the model
                    cannot memorise particular examples

label smoothing     targets of 0.9 rather than 1.0,
                    discouraging overconfidence
```

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

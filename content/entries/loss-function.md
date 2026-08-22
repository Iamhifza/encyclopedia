---
term: Loss Function
aliases: [Objective Function, Cost Function, Cross-Entropy, Loss]
category: math-for-ai
subcategory: optimisation
depth: full
status: foundational
difficulty: beginner
one_liner: "The single number a model is trying to make smaller, and therefore the only thing it actually cares about."
tags: [training]
relations:
  used_by: [gradient-descent, pretraining, supervised-learning]
  related_to: [reward-hacking, benchmark, information-theory]
prerequisites: [supervised-learning]
encountered_in: [research-papers, interviews, github]
sources:
  - type: book
    title: "Deep Learning, ch. 5 (Goodfellow, Bengio, Courville)"
    url: https://www.deeplearningbook.org/
    year: 2016
  - type: docs
    title: "PyTorch loss functions"
    url: https://pytorch.org/docs/stable/nn.html#loss-functions
updated: 2026-08-21
---

## Simple Explanation

Training needs a score. The loss function is that score: one number saying how
wrong the model's output was. Training then does one thing forever — adjust the
parameters so that number goes down.

This makes the loss function the most consequential design choice in machine
learning, because a model will optimise exactly what you measure and nothing
else. Whatever you failed to put in the loss, the model is free to ignore.

## Technical Definition

A differentiable function $L(\hat{y}, y)$ mapping a prediction and a target to a
scalar, whose expectation over the data distribution is the training objective.
Differentiability is what lets backpropagation compute a gradient; the gradient
is what gradient descent follows.

## Why Does It Exist?

Optimisation needs a direction. "Be more accurate" is not something you can
differentiate — accuracy is a step function, flat almost everywhere, with a
gradient of zero. Cross-entropy is a smooth surrogate for it: minimising it
tends to maximise accuracy, and unlike accuracy it tells you which way to move.

## What Problem Does It Solve?

It converts a vague goal into a scalar that can be reduced by calculus.

## How Does It Work?

```text
prediction ──┐
             ├──▶ loss function ──▶ 3.42   ← "this wrong"
target ──────┘                       │
                                     ▼
                          ∂L/∂w for every parameter
                                     │
                                     ▼
                        optimiser takes a small step
```

## Mental Model

A single bathroom scale for the entire model. Everything training does is an
attempt to make that one reading smaller — which is powerful, and exactly why
the reading had better measure the right thing.

## Formula

Cross-entropy, the loss behind every language model:

$$L = -\sum_{i} y_i \log \hat{y}_i$$

* $y_i$ — the true distribution, in practice 1 for the correct token and 0
  elsewhere, so the sum collapses to a single term.
* $\hat{y}_i$ — the probability the model assigned to token $i$.
* The negative logarithm means the penalty is mild for being slightly unsure and
  enormous for being confidently wrong: assign probability 0.01 to the correct
  token and the loss is 4.6; assign 0.5 and it is 0.69.

That asymmetry is the whole reason models learn to hedge.

## Example

Common choices and what each rewards:

| Task | Loss | Rewards |
|---|---|---|
| Language modelling | Cross-entropy | High probability on the actual next token |
| Regression | Mean squared error | Small errors, punishing outliers heavily |
| Regression with outliers | Mean absolute error | Small errors, treating outliers gently |
| Retrieval embeddings | Contrastive | Matching pairs close, mismatched pairs far |
| Preference alignment | DPO loss | Chosen response above rejected |

Switching mean squared error to mean absolute error changes what the model does
about outliers, not how hard it tries. That is the level at which loss design
operates.

## Real-World Usage

Perplexity, the standard language-model metric, is just the exponential of
cross-entropy loss. Reward models in RLHF are trained with a preference loss.
And most spectacular ML failures are loss-function failures: the model minimised
precisely what it was told to, and what it was told to was not what anyone
wanted.

## Common Confusions

* **Loss vs metric** — loss is optimised, metrics are reported. Loss must be
  differentiable; accuracy, F1 and BLEU need not be, which is why they are
  usually not the training objective.
* **Loss vs reward** — the same idea with the sign flipped. Reinforcement
  learning maximises reward; supervised learning minimises loss.
* **Lower loss is not always better** — falling training loss with rising
  validation loss is overfitting.
* **Loss values are not comparable across models** — different tokenizers,
  different vocabularies, different numbers. Compare only like with like.

## Why Should I Care?

Every alignment failure in this encyclopedia — reward hacking, sycophancy,
benchmark gaming — is the same story: an objective that was measurable but not
quite what was meant. Understanding that the model optimises the number, not the
intent, is the beginning of taking evaluation seriously.

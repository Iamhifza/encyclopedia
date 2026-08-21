---
term: Overfitting
aliases: [Memorisation, High Variance]
category: machine-learning
subcategory: generalisation
status: foundational
difficulty: beginner
one_liner: When a model learns the noise and quirks of its training data so well that it performs worse on anything new.
origin:
  year: 1960
  circa: true
  attribution: A statistics concept long predating machine learning
historical_period: early-computing
tags: [training, safety]
relations:
  related_to: [supervised-learning, scaling-laws, benchmark-contamination]
encountered_in: [interviews, research-papers, production-systems]
sources:
  - type: book
    title: "The Elements of Statistical Learning, ch. 7"
    url: https://hastie.su.domains/ElemStatLearn/
    year: 2009
  - type: paper
    title: "Deep Double Descent: Where Bigger Models and More Data Hurt"
    url: https://arxiv.org/abs/1912.02292
    year: 2019
updated: 2026-08-21
---

## Simple Explanation

A student who memorises last year's exam paper scores perfectly on it and badly
on this year's. The model did not learn the subject; it learned the paper.

## Technical Definition

The regime where training loss continues to fall while held-out loss rises,
because the model has capacity to fit sample-specific noise rather than the
underlying distribution.

## Why Does It Exist?

Any sufficiently flexible function class can fit a finite dataset exactly.
Nothing in the training objective distinguishes signal from noise; only held-out
evaluation can.

## What Problem Does It Solve?

It is not a solution — it is the failure mode that motivates train/validation/test
splits, regularisation, early stopping, dropout and data augmentation.

## How Does It Work?

```text
loss
 │   ╲                    ╱ validation
 │    ╲                 ╱
 │     ╲______________╱
 │      ╲___________________ training
 └──────────────────────────▶ training time
              ▲
        stop about here
```

## Mental Model

Tracing a photograph freehand, including the dust on the lens, then being
surprised the drawing does not resemble the next photograph.

## Example

A 12-parameter polynomial passes exactly through 12 noisy data points and
oscillates wildly between them. A straight line misses every point slightly and
predicts new points far better.

## Real-World Usage

In LLM work it reappears with new names: memorisation of training documents,
benchmark contamination when test data leaks into pretraining, and reward
hacking when a policy overfits a proxy reward rather than the intended goal.

## Common Confusions

* **Overfitting vs underfitting** — the opposite failure: too little capacity or
  training to capture real structure.
* **"Large models always overfit"** — the double-descent phenomenon shows
  held-out loss can fall again well past the interpolation threshold, which is
  why enormous models trained on enormous corpora still generalise.

## Why Should I Care?

Every impressive evaluation number is worthless if the test data was seen during
training. Most of the discipline in ML practice exists to prevent this one thing.

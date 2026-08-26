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
diagram:
  kind: figure
  title: The moment the two curves part company
  footer: Training loss falling is not evidence of anything on its own. The gap between the two curves
    is the measurement, which is why a held-out split is not optional.
  visual:
    kind: plot
    width: 700
    height: 220
    x_range: [0, 100]
    y_range: [0, 1.05]
    x_label: training time
    y_label: loss
    caption: the model has started memorising examples rather than learning the pattern behind them
    curves:
    - label: training
      tone: muted
      points: [[0.0, 0.93], [2.5, 0.839], [5.0, 0.757], [7.5, 0.684], [10.0, 0.62], [12.5, 0.562], [15.0,
          0.51], [17.5, 0.464], [20.0, 0.422], [22.5, 0.386], [25.0, 0.353], [27.5, 0.324], [30.0, 0.297],
        [32.5, 0.274], [35.0, 0.253], [37.5, 0.235], [40.0, 0.218], [42.5, 0.203], [45.0, 0.19], [47.5,
          0.178], [50.0, 0.168], [52.5, 0.158], [55.0, 0.15], [57.5, 0.142], [60.0, 0.136], [62.5, 0.13],
        [65.0, 0.124], [67.5, 0.12], [70.0, 0.115], [72.5, 0.111], [75.0, 0.108], [77.5, 0.105], [80.0,
          0.102], [82.5, 0.1], [85.0, 0.098], [87.5, 0.096], [90.0, 0.094], [92.5, 0.093], [95.0, 0.091],
        [97.5, 0.09], [100.0, 0.089]]
    - label: validation
      tone: accent
      points: [[0.0, 0.98], [2.5, 0.876], [5.0, 0.787], [7.5, 0.711], [10.0, 0.645], [12.5, 0.59], [15.0,
          0.542], [17.5, 0.501], [20.0, 0.466], [22.5, 0.436], [25.0, 0.411], [27.5, 0.389], [30.0, 0.37],
        [32.5, 0.354], [35.0, 0.345], [37.5, 0.345], [40.0, 0.346], [42.5, 0.349], [45.0, 0.353], [47.5,
          0.358], [50.0, 0.364], [52.5, 0.37], [55.0, 0.378], [57.5, 0.386], [60.0, 0.394], [62.5, 0.403],
        [65.0, 0.412], [67.5, 0.421], [70.0, 0.431], [72.5, 0.441], [75.0, 0.451], [77.5, 0.461], [80.0,
          0.472], [82.5, 0.482], [85.0, 0.493], [87.5, 0.504], [90.0, 0.515], [92.5, 0.525], [95.0, 0.536],
        [97.5, 0.547], [100.0, 0.558]]
    marks:
    - at: [34, 0.335]
      text: stop about here
      dy: -22
      anchor: middle
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


Early in training both losses fall: the model is learning structure that is
genuinely present in the data and therefore present in unseen data too. At some
point the remaining reducible error on the training set is idiosyncratic —
specific examples, specific noise — and fitting it can no longer help anywhere
else.

From there the two curves separate. Training loss keeps falling, because the
model is memorising; validation loss flattens and then climbs, because those
memorised specifics are wrong about anything new. The gap between the curves is
the measurement, and it is invisible without a held-out split.

The classical response is to stop at the minimum of the validation curve, and
early stopping does exactly that. Worth knowing that very large models do not
follow this shape cleanly — past the point where they can fit the training set
exactly, test error often falls again — which is the double descent behaviour
described under generalisation.

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

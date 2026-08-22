---
term: Gradient Descent
aliases: [SGD, Adam, Optimiser, Stochastic Gradient Descent, AdamW]
category: math-for-ai
subcategory: optimisation
depth: full
status: foundational
difficulty: intermediate
one_liner: "Improving a model by repeatedly taking a small step in whichever direction reduces the error fastest."
tags: [training]
relations:
  depends_on: [backpropagation, loss-function]
  used_by: [pretraining, neural-network, supervised-learning]
  related_to: [gpu]
prerequisites: [backpropagation, loss-function]
encountered_in: [research-papers, interviews, github]
sources:
  - type: paper
    title: "Adam: A Method for Stochastic Optimization"
    url: https://arxiv.org/abs/1412.6980
    year: 2014
  - type: paper
    title: "Decoupled Weight Decay Regularization (AdamW)"
    url: https://arxiv.org/abs/1711.05101
    year: 2017
  - type: book
    title: "Deep Learning, ch. 8"
    url: https://www.deeplearningbook.org/
    year: 2016
updated: 2026-08-21
---

## Simple Explanation

You are on a hillside in thick fog and want to reach the valley. You cannot see
where it is, but you can feel which way the ground slopes under your feet. So you
step downhill, feel again, step again. Gradient descent is that, in a space with
billions of dimensions instead of two.

## Technical Definition

An iterative first-order optimisation method updating parameters against the
gradient of the loss: $\theta_{t+1} = \theta_t - \eta \nabla_\theta L$. In
practice the gradient is estimated on a mini-batch rather than the full dataset —
*stochastic* gradient descent — and modern optimisers add momentum and
per-parameter adaptive step sizes.

## Why Does It Exist?

There is no closed-form solution for the best parameters of a neural network, and
the search space is far too large to explore. Following the local slope is the
only method that scales, and empirically it finds solutions that generalise well
despite the loss surface being wildly non-convex.

## What Problem Does It Solve?

Fitting billions of parameters without ever solving anything analytically.

## How Does It Work?

```text
repeat:
    take a mini-batch of examples
    forward pass  ──▶ predictions ──▶ loss
    backward pass ──▶ ∂L/∂θ for every parameter        (backpropagation)
    θ ← θ − η · (adjusted gradient)                    (the optimiser's job)
```

Why mini-batches rather than the whole dataset? Computing the exact gradient over
trillions of tokens per step is impossible, and it turns out to be unnecessary: a
noisy estimate from a few thousand examples points in roughly the right
direction, and the noise itself appears to help escape poor regions.

## Mental Model

Descending in fog by feel. You never see the valley, you only ever know the slope
where you stand — and the step size decides whether you make progress or bounce
across the ravine.

## Formula

$$\theta_{t+1} = \theta_t - \eta \nabla_\theta L(\theta_t)$$

* $\theta$ — all model parameters.
* $\nabla_\theta L$ — the gradient: for each parameter, how much the loss changes
  if it changes.
* $\eta$ — the learning rate, and the single most important hyperparameter in
  training. Too large and training diverges; too small and it crawls or settles
  somewhere poor.

Adam extends this with a running average of past gradients (momentum) and of
their squared magnitudes, giving each parameter its own effective step size:

$$\theta_{t+1} = \theta_t - \eta \frac{\hat{m}_t}{\sqrt{\hat{v}_t} + \epsilon}$$

* $\hat{m}_t$ — smoothed gradient; keeps moving through flat regions.
* $\hat{v}_t$ — smoothed squared gradient; shrinks steps for parameters with
  large or erratic gradients.
* $\epsilon$ — a tiny constant preventing division by zero.

## Example

Learning rate schedules matter as much as the optimiser. Large model training
almost always warms up from near zero over the first few thousand steps, then
decays — often cosine — toward the end. Skipping warmup on a large Transformer
typically produces a loss spike in the first hundred steps from which the run
never recovers.

## Real-World Usage

AdamW is the default for Transformer training. Its cost is memory: it stores two
extra values per parameter, so optimiser state is roughly twice the model size
again, which is a large part of why training needs so much more memory than
inference and why techniques like ZeRO shard it across devices.

## Common Confusions

* **Gradient descent vs backpropagation** — backprop computes the gradient;
  gradient descent decides what step to take with it. Frequently conflated in
  interviews.
* **Local minima are not the problem** — in very high dimensions, saddle points
  and flat regions dominate, and the local minima that exist are mostly fine.
* **Adam is not always better** — plain SGD with momentum still generalises
  better on some vision tasks.
* **Batch size is not free** — larger batches give less noisy gradients and often
  need a larger learning rate to compensate.

## Why Should I Care?

Every model you use was produced by this loop. When training destabilises — loss
spikes, divergence, silent underperformance — the cause is almost always the
learning rate, the schedule or the batch size, and those are the three dials you
reach for first.

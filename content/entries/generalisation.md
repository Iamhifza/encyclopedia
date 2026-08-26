---
term: Generalisation
aliases: [Generalization, Out-of-Distribution, Bias-Variance Tradeoff, OOD]
category: machine-learning
subcategory: generalisation
depth: full
status: foundational
difficulty: intermediate
one_liner: "Whether a model works on data it has never seen, which is the only thing anyone actually wants from it."
historical_period: early-computing
diagram:
  kind: figure
  title: The textbook curve, and what large models actually do
  footer: Double descent is not a curiosity at the edge of the theory — it is the regime every large model
    is trained in. The classical advice to stop at the sweet spot would have stopped the field around
    2015.
  visual:
    kind: plot
    width: 700
    height: 230
    x_range: [0, 100]
    y_range: [0, 1.05]
    x_label: model capacity
    y_label: test error
    caption: past the interpolation threshold — where the model can fit the training set exactly — error
      falls again
    bands:
    - from: 42
      to: 58
      text: interpolation threshold
      tone: warn
    curves:
    - label: classical
      tone: muted
      points: [[0.0, 0.591], [2.5, 0.556], [5.0, 0.523], [7.5, 0.492], [10.0, 0.464], [12.5, 0.438], [
          15.0, 0.414], [17.5, 0.392], [20.0, 0.373], [22.5, 0.356], [25.0, 0.341], [27.5, 0.328], [30.0,
          0.318], [32.5, 0.31], [35.0, 0.305], [37.5, 0.301], [40.0, 0.3], [42.5, 0.301], [45.0, 0.305],
        [47.5, 0.31], [50.0, 0.318], [52.5, 0.328], [55.0, 0.341], [57.5, 0.356], [60.0, 0.373], [62.5,
          0.392], [65.0, 0.414], [67.5, 0.438], [70.0, 0.464], [72.5, 0.492], [75.0, 0.523], [77.5, 0.556],
        [80.0, 0.591], [82.5, 0.628], [85.0, 0.668], [87.5, 0.71], [90.0, 0.755], [92.5, 0.801], [95.0,
          0.85], [97.5, 0.901], [100.0, 0.955]]
    - label: observed
      tone: accent
      points: [[0, 0.95], [12, 0.62], [24, 0.44], [34, 0.38], [42, 0.48], [50, 0.72], [58, 0.52], [68,
          0.34], [80, 0.24], [100, 0.18]]
tags: [training]
relations:
  different_from: [overfitting]
  related_to: [scaling-laws, benchmark, benchmark-contamination, supervised-learning, drift]
prerequisites: [supervised-learning, overfitting]
encountered_in: [research-papers, interviews, conferences]
sources:
  - type: book
    title: "The Elements of Statistical Learning, ch. 7"
    url: https://hastie.su.domains/ElemStatLearn/
    year: 2009
  - type: paper
    title: "Understanding Deep Learning Requires Rethinking Generalization"
    url: https://arxiv.org/abs/1611.03530
    year: 2016
  - type: paper
    title: "Deep Double Descent: Where Bigger Models and More Data Hurt"
    url: https://arxiv.org/abs/1912.02292
    year: 2019
updated: 2026-08-21
---

## Simple Explanation

Training performance is worthless. Any sufficiently flexible model can memorise
its training set exactly — that is not a sign of learning, it is a sign of
capacity. The only question that matters is whether it works on data it has never
encountered.

Everything in machine learning practice — the train/test split, cross-validation,
held-out benchmarks, regularisation — exists to answer that one question
honestly.

## Technical Definition

The gap between performance on the training distribution and performance on
unseen data drawn from the same distribution (*in-distribution* generalisation),
or from a different one (*out-of-distribution*). Classically framed through the
bias-variance decomposition: error comes from a model too simple to capture the
signal, from sensitivity to the particular sample, and from irreducible noise.

## Why Does It Exist?

Because a finite sample never fully determines the underlying pattern. There are
always many functions that fit the data equally well and disagree everywhere
else, and nothing in the training loss can distinguish them.

## What Problem Does It Solve?

It is the actual objective, standing behind the surrogate one you optimise.

## How Does It Work?


The classical account says capacity trades against generalisation. Too little and
the model cannot represent the pattern; too much and it memorises the training
set. Test error is U-shaped in capacity, and the job is to find the bottom.

Large models do not behave that way. As capacity grows, test error falls, then
rises to a peak around the *interpolation threshold* — the point where the model
is just barely able to fit the training data exactly — and then, as capacity
keeps growing past it, falls again, often below the classical minimum. This is
double descent, and it is the regime every modern model is trained in.

Why it happens is still argued about. The usable intuition is that among the many
parameter settings that fit the training data perfectly, gradient descent tends
to find ones with properties that happen to generalise, and having more
parameters gives it more such solutions to find. Which means the classical advice
— stop at the sweet spot — would have stopped the field a decade ago.

## Mental Model

Learning to cook from twenty recipes. Memorising them makes you useless with the
twenty-first. Understanding why the steps work makes you useful with any of them —
and no exam on the original twenty can tell the two apart.

## Example

Two results reshaped how this is understood. First, deep networks can fit
*randomly labelled* data perfectly — so classical capacity measures cannot explain
why they generalise at all on real data. Second, **double descent**: past the
point where a model fits the training set exactly, test error can fall *again*,
contradicting the textbook U-curve. Neither is fully explained. The practical
upshot is that intuitions about model size and overfitting formed before 2018 do
not transfer cleanly to modern scale.

## Real-World Usage

In LLM work the concept appears mostly through its failures: benchmark
contamination (the test set was in training, so the number measures memorisation),
distribution shift in production, and the gap between benchmark scores and
usefulness on your actual task. This is why a small evaluation set built from your
own traffic beats any leaderboard.

## Common Confusions

* **In-distribution vs out-of-distribution** — working on held-out data from the
  same source is a much weaker claim than working on genuinely new conditions.
  Most reported results are the first kind.
* **Generalisation vs memorisation** — models do both, simultaneously. Large
  models verifiably memorise some training data while generalising well overall.
* **A benchmark score is not evidence of generalisation** if the benchmark leaked
  into pretraining.

## Why Should I Care?

It is the question every evaluation is trying to answer and most evaluations
answer badly. Knowing the difference between "scored well on the test set" and
"will work on my data" is the single most useful piece of scepticism in applied
machine learning.

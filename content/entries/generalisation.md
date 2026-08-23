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

```text
classical view                    what deep learning actually does
error                             error
  │ ╲        ╱ test                │╲    ╱╲
  │  ╲      ╱                      │ ╲  ╱  ╲___________ test
  │   ╲____╱                       │  ╲╱    ↑
  │        ╲___ train              │  interpolation threshold
  └────────────▶ capacity          └────────────▶ capacity
  "sweet spot in the middle"       "keep going and it improves again"
```

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

---
term: Probability
aliases: [Probability Theory, Distributions, Likelihood]
category: math-for-ai
subcategory: probability
depth: full
status: foundational
difficulty: beginner
one_liner: "The mathematics of uncertainty, and the language in which every model output is really a distribution rather than an answer."
tags: [training]
relations:
  used_by: [sampling, supervised-learning, loss-function]
  related_to: [hallucination, bayesian-inference, information-theory]
encountered_in: [research-papers, interviews]
sources:
  - type: book
    title: "Pattern Recognition and Machine Learning, ch. 1 (Bishop)"
    url: https://www.microsoft.com/en-us/research/publication/pattern-recognition-machine-learning/
    year: 2006
  - type: book
    title: "Deep Learning, ch. 3"
    url: https://www.deeplearningbook.org/
    year: 2016
updated: 2026-08-21
---

## Simple Explanation

A language model does not choose a word. It produces a number for every word in
its vocabulary saying how likely that word is to come next, and something else
picks one. Everything a model outputs is a distribution; what you see is a sample
from it.

Once that clicks, a lot of otherwise puzzling behaviour stops being puzzling.

## Technical Definition

The formal treatment of uncertainty: a sample space of outcomes, a probability
measure assigning each a value in $[0,1]$ summing to one, and the rules for
combining them — the sum rule, the product rule, and conditional probability.
Machine learning is largely the business of estimating conditional distributions
from data.

## Why Does It Exist?

Because the world is not deterministic and our information about it is
incomplete. Probability is the only internally consistent calculus for reasoning
under that condition — a result that can be derived from a handful of
common-sense requirements.

## What Problem Does It Solve?

It provides a language for models to express what they do not know, and a
principled way to combine evidence.

## How Does It Work?

```text
model output for "the cat sat on the ___"

  mat     0.31   ████████████
  floor   0.18   ███████
  sofa    0.12   ████
  table   0.09   ███
  ...     
  bicycle 0.00003
                 ← a full distribution over ~100,000 tokens
                   sampling picks one; the rest are discarded
```

## Mental Model

A weather forecast. "70% chance of rain" is not a prediction that can be right or
wrong on the day — it is a statement about a distribution, and it is judged over
many days.

## Formula

The chain rule, which is the entire structure of a language model:

$$p(x_1, \ldots, x_n) = \prod_{t=1}^{n} p(x_t \mid x_{<t})$$

* $p(x_t \mid x_{<t})$ — the probability of the next token given everything
  before it. This single conditional is what the network computes.
* The product over positions turns one next-token predictor into a model of whole
  sequences of any length.

And Bayes' rule, for updating on evidence:

$$p(h \mid e) = \frac{p(e \mid h)\, p(h)}{p(e)}$$

* $p(h)$ — belief before seeing the evidence (the prior).
* $p(e \mid h)$ — how well the hypothesis explains what you saw (the likelihood).
* $p(h \mid e)$ — belief afterwards (the posterior).

## Example

A model assigning 0.31 to "mat" is not 31% sure of a fact. It is reporting that
across the text it learned from, "mat" followed this context about that often.
Confidence in the distributional sense and correctness are different things, and
conflating them is the root of most misplaced trust in model output.

## Real-World Usage

Every loss function is a probabilistic quantity — cross-entropy is the expected
surprise of the true token under the model's distribution. Temperature, top-$k$
and top-$p$ are all reshaping operations on that distribution. Calibration —
whether a model's stated confidence matches its actual accuracy — is measured
probabilistically, and models are frequently poorly calibrated after preference
training.

## Common Confusions

* **Probability vs confidence** — a high token probability means the continuation
  is typical, not that the claim is true. This is precisely why hallucination is
  possible.
* **Likelihood vs probability** — the same expression read as a function of the
  parameters rather than of the data. The distinction matters when reading papers.
* **Independence is usually assumed, rarely true** — most tractable models assume
  it somewhere, and that assumption is where they break.

## Why Should I Care?

Understanding that the model outputs a distribution, and that everything from
temperature to hallucination to calibration is a statement about that
distribution, is the shortest route to reasoning correctly about model behaviour
instead of anthropomorphising it.

---
term: Bayesian Inference
aliases: [Bayes' Rule, Bayesian Methods, Priors, Posterior]
category: math-for-ai
subcategory: probability
depth: full
status: foundational
difficulty: advanced
one_liner: "Updating a belief in the light of new evidence, in the one way that is mathematically consistent."
origin:
  year: 1763
  attribution: Thomas Bayes, published posthumously; developed independently and more generally by Laplace
historical_period: pre-computing
diagram:
  kind: steps
  title: Belief, updated by evidence, becoming the next belief
  footer: The framework says how much to move, not what to believe first. A confident wrong prior is the
    expensive failure mode, and no amount of evidence is free.
  steps:
  - title: One update, then the same update again
    visual:
      kind: chips
      items:
      - prior belief
      - new evidence
      - posterior belief
      loop: the posterior becomes the prior for the next piece of evidence
  - title: How far the belief actually moves
    notes:
    - label: Ratio
      text: movement depends on the strength of the evidence relative to the prior, not on either alone
    visual:
      kind: bars
      caption: how far the posterior travels from the prior
      bars:
      - label: strong prior, weak evidence
        value: 0.12
        value_label: barely moves
      - label: matched
        value: 0.5
        value_label: meets in the middle
      - label: weak prior, strong evidence
        value: 0.92
        value_label: moves a long way
        accent: true
tags: [training]
relations:
  related_to: [probability, supervised-learning, autoencoder, hallucination]
prerequisites: [probability]
encountered_in: [research-papers, interviews, conferences]
sources:
  - type: book
    title: "Probability Theory: The Logic of Science (Jaynes)"
    url: https://www.cambridge.org/core/books/probability-theory/9CA08E224FF30123304E6D8935CF1A99
    year: 2003
  - type: book
    title: "Pattern Recognition and Machine Learning (Bishop)"
    url: https://www.microsoft.com/en-us/research/publication/pattern-recognition-machine-learning/
    year: 2006
videos:
  - title: "Bayes theorem, the geometry of changing beliefs"
    channel: "3Blue1Brown"
    url: https://www.youtube.com/results?search_query=3blue1brown+bayes+theorem
updated: 2026-08-21
---

## Simple Explanation

You believe something. Evidence arrives. How much should your belief change?

Bayes' rule answers that exactly, and — this is the surprising part — it is the
*only* answer consistent with a handful of common-sense requirements about
reasoning under uncertainty. Any other updating rule can be shown to be
incoherent.

## Technical Definition

Inference in which unknown quantities are treated as random variables with
probability distributions. A prior encodes belief before data; the likelihood
describes how probable the data is under each hypothesis; their product,
normalised, gives the posterior. Prediction integrates over the posterior rather
than committing to a single best estimate.

## Why Does It Exist?

Because point estimates discard information. Knowing the best-fitting parameter
tells you nothing about how confident you should be in it, and that confidence is
often what the decision actually depends on.

## What Problem Does It Solve?

Principled uncertainty. It says how much to trust a conclusion, and how to
combine evidence from several sources without double-counting.

## How Does It Work?

That last line is the practical content: how much you move depends on the
relative strength of what you believed and what you saw.

## Mental Model

A detective revising a theory. Each new fact does not replace the theory outright
— it shifts confidence in proportion to how surprising that fact would be if the
theory were true.

## Formula

$$p(h \mid e) = \frac{p(e \mid h)\, p(h)}{p(e)}$$

* $p(h)$ — prior: belief in the hypothesis before the evidence.
* $p(e \mid h)$ — likelihood: how probable this evidence is if the hypothesis
  holds.
* $p(e)$ — marginal likelihood: how probable the evidence is overall, which
  normalises the result.
* $p(h \mid e)$ — posterior: belief afterwards.

## Example

The classic result, and the one worth internalising: a test that is 99% accurate
for a disease affecting 1 in 10,000 people. A positive result means roughly a 1%
chance of having it — because the base rate is so low that false positives vastly
outnumber true ones. The evidence is strong and the prior is stronger.

This is exactly the reasoning error people make about model outputs: a confident
answer is evidence, and it must be weighed against how likely the claim was to
begin with.

## Real-World Usage

Direct use in machine learning is narrower than its conceptual importance:
Bayesian optimisation for hyperparameter search, variational inference in VAEs,
Gaussian processes for small-data regression, and Thompson sampling in bandits.
Deep learning is mostly *not* Bayesian — it produces point estimates of weights,
which is precisely why neural networks are poorly calibrated and confidently
wrong.

## Common Confusions

* **Bayesian vs frequentist** — a genuine philosophical difference (probability
  as degree of belief versus long-run frequency) with narrower practical
  consequences than the historical argument suggests.
* **Priors are not cheating** — you always have assumptions; the Bayesian frame
  makes you write them down where they can be criticised.
* **Softmax outputs are not posteriors** — a model's probabilities are not
  calibrated beliefs, and treating them as such is a common and consequential
  error.

## Why Should I Care?

It is the correct framework for reasoning about uncertainty, and the fact that
deep learning largely ignores it explains one of these models' most persistent
weaknesses: they cannot tell you how much to trust them.

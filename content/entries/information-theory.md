---
term: Information Theory
aliases: [Entropy, Shannon Entropy, Perplexity, KL Divergence, Mutual Information]
category: math-for-ai
subcategory: information
depth: full
status: foundational
difficulty: advanced
one_liner: "The mathematics of surprise: how much information a message carries, and how far one distribution sits from another."
historical_period: early-computing
tags: [training]
relations:
  used_by: [loss-function, rlhf, tokenization]
  related_to: [probability, scaling-laws, embedding]
prerequisites: [probability]
encountered_in: [research-papers, interviews, conferences]
sources:
  - type: paper
    title: "A Mathematical Theory of Communication (Shannon)"
    url: https://people.math.harvard.edu/~ctm/home/text/others/shannon/entropy/entropy.pdf
    year: 1948
  - type: book
    title: "Elements of Information Theory (Cover & Thomas)"
    url: https://onlinelibrary.wiley.com/doi/book/10.1002/047174882X
    year: 2006
updated: 2026-08-21
---

## Simple Explanation

Information is surprise. Being told the sun rose tells you nothing — you knew. A
message carries information in proportion to how unlikely it was.

Shannon made that precise in 1948, and the consequence for AI is direct: a model
that predicts text well is one that finds it unsurprising, and *how surprised the
model is* turns out to be exactly the right thing to train on.

## Technical Definition

The study of quantifying, storing and communicating information. Entropy
$H(p) = -\sum p(x) \log p(x)$ measures the average surprise of a distribution;
cross-entropy measures the average surprise of data under a *different*
distribution; KL divergence measures the excess — how much you lose by modelling
$p$ with $q$.

## Why Does It Exist?

Shannon needed to know the limits of communication over a noisy channel: how much
can be compressed, and how fast can it be sent reliably. Those questions turned
out to have a single quantitative answer, and it applies far beyond telephony.

## What Problem Does It Solve?

For AI, it supplies the training objective and the vocabulary for comparing
distributions — which is what learning is.

## How Does It Work?

```text
high entropy (uniform)          low entropy (peaked)
▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄               ▁▁▁▁▁█▁▁▁▁▁▁▁▁▁
maximum surprise per            almost no surprise:
symbol; nothing compresses      compresses to almost nothing
```

A model trained by cross-entropy is being pushed toward the second picture: put
your probability mass where the data actually is.

## Mental Model

A compression bill. Every message you send costs bits, and the bill is lowest
when your expectations match reality. A model with low loss is one that finds the
world cheap to describe.

## Formula

$$H(p) = -\sum_x p(x)\log p(x), \qquad D_{KL}(p \parallel q) = \sum_x p(x)\log\frac{p(x)}{q(x)}$$

* $p$ — the true distribution; $q$ — the model's.
* $H(p)$ — irreducible uncertainty. Even a perfect model cannot get below it,
  which is precisely the $L_\infty$ term in scaling laws.
* $D_{KL}$ — the penalty for being wrong about the distribution. Zero only when
  $q = p$; asymmetric, so $D_{KL}(p \parallel q) \neq D_{KL}(q \parallel p)$.

And perplexity, the metric you see in every language-model paper:

$$\text{PPL} = 2^{H} = e^{\text{cross-entropy}}$$

Read it as an effective branching factor: perplexity 10 means the model is, on
average, as uncertain as if choosing uniformly among 10 options.

## Example

The KL term in RLHF is information theory doing load-bearing work in a modern
pipeline. The policy is optimised for reward *minus* $\beta \cdot D_{KL}$ against
the reference model — a bounded budget of how far behaviour may drift. Remove it
and the policy walks off into degenerate text that scores well under an imperfect
reward model.

## Real-World Usage

Cross-entropy is the pretraining loss. Perplexity is the standard evaluation.
KL divergence constrains RLHF and DPO. Mutual information underpins contrastive
objectives in embedding models. And the compression view — that a good model is a
good compressor of its training distribution — is one of the more useful lenses
for thinking about what these systems do.

## Common Confusions

* **Entropy (information) vs entropy (thermodynamics)** — mathematically
  analogous, historically connected, but do not import intuitions between them
  casually.
* **Perplexity is not comparable across tokenizers** — different vocabularies
  give different numbers for identical model quality. Comparing perplexity across
  model families is meaningless.
* **KL is not a distance** — asymmetric and violating the triangle inequality,
  which is why the direction you write it in matters.

## Why Should I Care?

It supplies the actual definition of what a language model is trained to do.
Perplexity, the KL penalty in alignment, and the irreducible-loss term in scaling
laws are all the same 1948 idea, showing up in three different places.

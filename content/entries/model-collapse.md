---
term: Model Collapse
aliases: [Model Autophagy, Recursive Training Degradation]
category: evaluation-safety
subcategory: failure-modes
status: emerging
difficulty: advanced
one_liner: The degradation that occurs when models are trained on the output of earlier models, generation after generation, until diversity disappears.
origin:
  year: 2023
  attribution: Shumailov et al.; related work on model autophagy disorder by Alemohammad et al.
historical_period: agentic
tags: [safety, training]
relations:
  related_to: [synthetic-data, ai-slop, pretraining]
prerequisites: [pretraining, synthetic-data]
encountered_in: [research-papers, technical-blogs, conferences]
sources:
  - type: paper
    title: "AI models collapse when trained on recursively generated data"
    url: https://www.nature.com/articles/s41586-024-07566-y
    year: 2024
  - type: paper
    title: "Self-Consuming Generative Models Go MAD"
    url: https://arxiv.org/abs/2307.01850
    year: 2023
updated: 2026-08-21
review_by: 2027-02-01
---

## Simple Explanation

A model's output is a smoothed version of its training data: the common cases are
over-represented and the rare ones under-represented. Train the next model mostly
on that output and the rare cases thin further. Repeat, and the tails vanish
entirely.

## Technical Definition

Progressive loss of distributional fidelity when generative models are trained on
data produced by their predecessors. Early collapse loses low-probability tail
behaviour; late collapse converges toward a narrow, low-variance distribution.
Driven by compounding statistical approximation error, functional expressivity
limits and finite sampling.

## Why Does It Exist?

Each generation samples from an approximation of the previous distribution.
Sampling error is not corrected by later generations — it is inherited and
amplified.

## What Problem Does It Solve?

Nothing. It is a constraint on how far synthetic data can be pushed.

## How Does It Work?

```text
gen 0  ▁▂▅█▅▂▁   real distribution, with tails
gen 1  ▁▃▆█▆▃▁   tails already thinner
gen 2   ▄▇█▇▄    minority modes disappearing
gen 3     █      collapsed toward the mode
```

## Mental Model

Photocopying a photocopy. Each pass is nearly indistinguishable from the last;
after twenty, the fine detail is gone.

## Example

The concern is not hypothetical for the open web: as machine-generated text
occupies a growing share of new pages, future scrapes contain a rising fraction
of model output. This is why data provenance, pre-2022 archives and licensed
human data have acquired strategic value.

## Real-World Usage

It shapes data strategy rather than day-to-day engineering: provenance tracking,
the premium on pre-2022 and licensed human corpora, deliberate mixing ratios of
real and synthetic data, and verifier-gated generation pipelines.

## Terminology Note

Findings are often over-stated in popular coverage. The strong result applies to
*replacing* real data with generated data across generations. Where synthetic
data is *filtered by a verifier* and *accumulated alongside* real data — which is
what practitioners actually do — the degradation is far weaker or absent. Treat
"AI will run out of data and collapse" claims as an unsupported extrapolation.

## Common Confusions

* **Collapse vs benign synthetic training** — verification and mixture with real
  data change the picture substantially.
* **Collapse vs slop** — one is a training dynamic, the other a publishing
  phenomenon. Slop increases exposure to the first.

## Why Should I Care?

It sets the boundary condition on synthetic data strategies and explains why data
provenance has become a first-class engineering concern.

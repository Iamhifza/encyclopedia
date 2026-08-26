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
diagram:
  kind: figure
  title: Each generation loses the tails
  footer: Rare and unusual data is exactly what a model is least likely to reproduce, so training on outputs
    discards it first. Which makes provenance — knowing what in your corpus is human-written — a durable
    practical concern.
  visual:
    kind: plot
    width: 700
    height: 220
    x_range: [-4, 4]
    y_range: [0, 1.15]
    x_label: the space of possible outputs
    y_label: how often produced
    caption: the mode survives and everything around it thins, generation by generation
    curves:
    - label: gen 0
      tone: muted
      points: [[-4.0, 0.012], [-3.8, 0.017], [-3.6, 0.024], [-3.4, 0.032], [-3.2, 0.043], [-3.0, 0.057],
        [-2.8, 0.074], [-2.6, 0.094], [-2.4, 0.117], [-2.2, 0.143], [-2.0, 0.173], [-1.8, 0.204], [-1.6,
          0.238], [-1.4, 0.272], [-1.2, 0.305], [-1.0, 0.336], [-0.8, 0.364], [-0.6, 0.388], [-0.4, 0.405],
        [-0.2, 0.416], [0.0, 0.42], [0.2, 0.416], [0.4, 0.405], [0.6, 0.388], [0.8, 0.364], [1.0, 0.336],
        [1.2, 0.305], [1.4, 0.272], [1.6, 0.238], [1.8, 0.204], [2.0, 0.173], [2.2, 0.143], [2.4, 0.117],
        [2.6, 0.094], [2.8, 0.074], [3.0, 0.057], [3.2, 0.043], [3.4, 0.032], [3.6, 0.024], [3.8, 0.017],
        [4.0, 0.012]]
    - label: gen 2
      points: [[-4.0, 0.0], [-3.8, 0.0], [-3.6, 0.0], [-3.4, 0.0], [-3.2, 0.001], [-3.0, 0.001], [-2.8,
          0.003], [-2.6, 0.007], [-2.4, 0.013], [-2.2, 0.025], [-2.0, 0.045], [-1.8, 0.076], [-1.6, 0.122],
        [-1.4, 0.185], [-1.2, 0.266], [-1.0, 0.36], [-0.8, 0.462], [-0.6, 0.561], [-0.4, 0.645], [-0.2,
          0.7], [0.0, 0.72], [0.2, 0.7], [0.4, 0.645], [0.6, 0.561], [0.8, 0.462], [1.0, 0.36], [1.2,
          0.266], [1.4, 0.185], [1.6, 0.122], [1.8, 0.076], [2.0, 0.045], [2.2, 0.025], [2.4, 0.013],
        [2.6, 0.007], [2.8, 0.003], [3.0, 0.001], [3.2, 0.001], [3.4, 0.0], [3.6, 0.0], [3.8, 0.0], [
          4.0, 0.0]]
    - label: gen 4
      tone: warn
      points: [[-4.0, 0.0], [-3.8, 0.0], [-3.6, 0.0], [-3.4, 0.0], [-3.2, 0.0], [-3.0, 0.0], [-2.8, 0.0],
        [-2.6, 0.0], [-2.4, 0.0], [-2.2, 0.0], [-2.0, 0.0], [-1.8, 0.0], [-1.6, 0.001], [-1.4, 0.004],
        [-1.2, 0.018], [-1.0, 0.063], [-0.8, 0.176], [-0.6, 0.389], [-0.4, 0.686], [-0.2, 0.964], [0.0,
          1.08], [0.2, 0.964], [0.4, 0.686], [0.6, 0.389], [0.8, 0.176], [1.0, 0.063], [1.2, 0.018], [
          1.4, 0.004], [1.6, 0.001], [1.8, 0.0], [2.0, 0.0], [2.2, 0.0], [2.4, 0.0], [2.6, 0.0], [2.8,
          0.0], [3.0, 0.0], [3.2, 0.0], [3.4, 0.0], [3.6, 0.0], [3.8, 0.0], [4.0, 0.0]]
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


Train a model on data, generate from it, train the next model on that output, and
repeat. Each generation degrades, and it degrades in a specific direction: the
tails go first.

The reason is straightforward. A model is most likely to produce what was common
in its training data and least likely to produce what was rare. Sample from it
and you get a distribution that already under-represents the unusual. Train on
that sample and the next model's view of "rare" is thinner still. Repeat a few
times and minority modes vanish entirely, leaving output clustered tightly around
the mode.

The practical question is not whether this happens in the extreme case — it
demonstrably does — but how much synthetic data, mixed how, degrades anything in
practice. Curated and filtered synthetic data with real data alongside it is
routine and works well. Recursive training on unfiltered output does not. Which
makes provenance, knowing which parts of a corpus are human-written, a durable
practical concern rather than a theoretical one.

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

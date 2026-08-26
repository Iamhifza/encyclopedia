---
term: Scaling Laws
aliases: [Neural Scaling Laws, Chinchilla Scaling, Compute-Optimal Scaling]
category: llm-training
subcategory: data
status: established
difficulty: advanced
one_liner: The empirical finding that model loss falls as a smooth power law in model size, data and compute, making capability gains predictable in advance.
origin:
  year: 2020
  attribution: Kaplan et al. (OpenAI); revised by Hoffmann et al. (DeepMind, Chinchilla) in 2022
historical_period: foundation-model
diagram:
  kind: figure
  title: A straight line on log-log axes
  footer: The law predicts loss, not capability. Loss falls smoothly; the behaviours people care about
    do not always arrive smoothly with it, and the relationship between the two is still an open question.
  visual:
    kind: plot
    width: 700
    height: 230
    x_range: [18, 26]
    y_range: [0.12, 0.78]
    x_label: log₁₀ training compute (FLOPs)
    y_label: log loss
    caption: the fit is what makes a nine-figure training run planable rather than a bet
    bands:
    - from: 18
      to: 22
      text: runs you can afford to measure
    - from: 22
      to: 26
      text: where you are extrapolating
      tone: accent
    curves:
    - label: L ∝ C⁻ᵅ
      tone: accent
      points: [[18, 0.72], [26, 0.18]]
    marks:
    - at: [24.5, 0.283]
      text: the run you do once
      dy: 26
      anchor: middle
tags: [training]
relations:
  used_by: [pretraining, foundation-model]
  related_to: [overfitting, reasoning-model, frontier-model]
prerequisites: [pretraining]
encountered_in: [research-papers, conferences, technical-blogs]
sources:
  - type: paper
    title: "Scaling Laws for Neural Language Models"
    url: https://arxiv.org/abs/2001.08361
    year: 2020
  - type: paper
    title: "Training Compute-Optimal Large Language Models"
    url: https://arxiv.org/abs/2203.15556
    year: 2022
videos:
  - title: "Scaling laws for neural language models"
    channel: "Yannic Kilcher"
    url: https://www.youtube.com/results?search_query=yannic+kilcher+scaling+laws+for+neural+language+models
    note: "A paper walkthrough"
updated: 2026-08-21
---

## Simple Explanation

Plot how wrong a model is against how big it is, on log axes, and you get a
straight line. That line has held over many orders of magnitude, which means you
can predict from small cheap runs how well a large expensive one will do — before
spending the money.

## Technical Definition

Test loss follows $L(N, D) = \frac{A}{N^{\alpha}} + \frac{B}{D^{\beta}} + L_{\infty}$
in parameters $N$ and training tokens $D$, with irreducible loss $L_{\infty}$.
Under a fixed compute budget $C \approx 6ND$, the Chinchilla analysis finds the
optimum scales $N$ and $D$ in roughly equal proportion.

## Why Does It Exist?

It is not a theory but a robust empirical regularity, observed across
architectures, modalities and scales. Explaining *why* it holds is still open
research.

## What Problem Does It Solve?

Investment risk. It converted "will a bigger model be better?" from a gamble into
an extrapolation, which is what justified nine-figure training runs.

## How Does It Work?


Train many models across a wide range of sizes and data budgets, measure the
loss each one reaches, and plot loss against compute on logarithmic axes. The
points fall on a straight line — loss follows a power law in compute, with
similar laws in parameters and in tokens separately.

A straight line can be extrapolated, and that is the entire practical value:
you can fit the law on runs you can afford and use it to choose the size and
data budget of a run you can only do once. Chinchilla's contribution was
observing that the earlier fits had been read wrongly, and that models of the
day were badly under-trained for their size.

The laws predict *loss*. They do not predict which capabilities appear, or when,
and the relationship between falling loss and the behaviours anyone actually
cares about remains an open research question rather than a settled one.

## Mental Model

A dose-response curve. Doubling the dose gives a reliable, diminishing, and
above all *predictable* improvement.

## Formula

$$L(N, D) = \frac{A}{N^{\alpha}} + \frac{B}{D^{\beta}} + L_{\infty}$$

* $N$ — parameters; $D$ — training tokens.
* $\alpha, \beta$ — empirically fitted exponents, both small and positive.
* $L_{\infty}$ — irreducible loss: the entropy no model can remove.

## Example

Chinchilla (70B parameters, 1.4T tokens) outperformed Gopher (280B, 300B tokens)
using the same compute budget. The lesson — most models were undertrained — reset
industry practice toward smaller models on far more data, which also happens to
make inference cheaper.

## Real-World Usage

Used to allocate training budgets, choose model size for a target inference cost,
and set data collection targets. Modern practice deliberately trains past the
compute-optimal point because inference cost, not training cost, dominates over a
model's lifetime.

## Common Confusions

* **Loss is not capability** — smooth loss curves can coexist with abrupt
  changes on downstream benchmarks, and whether those "emergent" jumps are real
  or artefacts of discontinuous metrics is contested.
* **Kaplan vs Chinchilla** — the earlier work over-weighted parameters relative
  to data because of a learning-rate schedule artefact.
* **Scaling laws do not promise capabilities** — they predict loss on the
  training distribution, nothing more.

## Why Should I Care?

The entire capital structure of the industry rests on this curve, and the current
debate about whether pretraining scaling is saturating — and whether test-time
compute is the next axis — is a debate about how far it extends.

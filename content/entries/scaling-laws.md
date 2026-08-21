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

```text
log loss
   │╲
   │ ╲___                straight on log-log axes
   │     ╲___
   │         ╲___        extrapolate to plan the big run
   └──────────────────▶ log compute
```

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

---
term: Sparse Autoencoder
aliases: [SAE, Dictionary Learning, Feature Decomposition]
category: interpretability
subcategory: methods
status: experimental
difficulty: research
one_liner: A tool that decomposes a model's tangled internal activations into a large set of features that each mean one thing.
origin:
  year: 2023
  attribution: Applied to language models by Anthropic and by Cunningham et al.; the technique is older in sparse coding
historical_period: agentic
tags: [safety]
relations:
  used_by: [mechanistic-interpretability, activation-steering]
  depends_on: [neural-network]
prerequisites: [mechanistic-interpretability]
encountered_in: [research-papers, conferences, github]
sources:
  - type: paper
    title: "Towards Monosemanticity: Decomposing Language Models With Dictionary Learning"
    url: https://transformer-circuits.pub/2023/monosemantic-features/index.html
    year: 2023
  - type: paper
    title: "Scaling Monosemanticity"
    url: https://transformer-circuits.pub/2024/scaling-monosemanticity/index.html
    year: 2024
updated: 2026-08-21
review_by: 2027-02-01
---

## Simple Explanation

Individual neurons in a language model are not interpretable — one neuron fires
for legal text, DNA sequences and Python decorators. The model is packing far
more concepts than it has neurons. A sparse autoencoder projects those
activations into a much wider space where only a few units are active at a time,
and those units tend to correspond to single recognisable concepts.

## Technical Definition

An autoencoder trained to reconstruct a model's activation vectors through a
much wider hidden layer under a sparsity penalty, yielding an overcomplete
dictionary of directions. Each learned feature ideally corresponds to one
human-interpretable concept, addressing the superposition problem.

## Why Does It Exist?

Superposition: networks represent more features than dimensions by placing them
in near-orthogonal directions, which makes individual neurons polysemantic and
resists direct inspection.

## What Problem Does It Solve?

It provides an interpretable basis for a model's internal state, so features can
be named, monitored and manipulated.

## How Does It Work?

```text
activation (d=4096) ──▶ encoder ──▶ sparse code (d=131072, ~30 active)
                                          │
                                       decoder
                                          ▼
                          reconstruction ≈ original activation

loss = reconstruction error + λ · sparsity
```

## Mental Model

Unmixing a recording into separate instrument tracks. The mix was always a sum of
sources; the decomposition recovers them.

## Example

Features found in large models include recognisable and highly specific concepts —
particular landmarks, code error handling, sycophantic praise, deceptive framing.
Amplifying a feature causally changes generation, which is what distinguishes a
feature from a correlation.

## Real-World Usage

Interpretability research, model auditing, and activation steering. Deployment as
a standard production tool is not yet the norm.

## Common Confusions

* **Features are not guaranteed monosemantic** — interpretability is a matter of
  degree and depends on dictionary size and sparsity settings.
* **Reconstruction error matters** — what the SAE fails to reconstruct is exactly
  what it cannot tell you about.
* **SAEs are not the model** — they are a lens fitted to it, with their own
  training choices and artefacts, and recent work has questioned how much of the
  structure they find is intrinsic.

## Why Should I Care?

It is the current best attempt at giving model internals a vocabulary, and if
interpretability becomes an operational tool rather than a research programme,
this is likely how.

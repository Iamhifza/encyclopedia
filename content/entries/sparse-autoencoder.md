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
diagram:
  kind: figure
  title: Widen instead of narrowing, and force nearly all of it to zero
  footer: 'The opposite bottleneck to an ordinary autoencoder, and for the opposite reason: not compression
    but separation. The bet is that a neuron holds several unrelated features and a wide sparse code can
    pull them apart.'
  visual:
    kind: pipeline
    width: 720
    caption: loss is reconstruction error plus a sparsity penalty; the sparsity is what makes the features
      interpretable rather than merely sufficient
    stages:
    - text: one layer's activation
      note: d = 4096
    - text: a very wide, very sparse code
      note: 131072, ~30 active
      tone: accent
      via: encoder — expand by 32×, then penalise activity
    - text: the activation, reconstructed
      note: '4096'
      via: decoder — and each active dimension names a feature
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


An ordinary autoencoder narrows in the middle. A sparse autoencoder does the
opposite: it expands the representation, often by a factor of thirty or more, and
then penalises activity so that only a few dozen dimensions are active at once.

The motivation is superposition. A network with 4096 dimensions appears to
represent far more than 4096 features by packing them into overlapping
directions, which is why individual neurons respond to unrelated things and
resist interpretation. A wider space has room to give each feature its own
dimension; the sparsity penalty is what forces it to use that room rather than
spreading everything out again.

What comes back is a dictionary of directions, many of which turn out to be
human-legible — a feature for legal language, for a particular programming
construct, for deception. Two open problems keep it honest: the reconstruction is
never perfect, so something is being discarded, and labelling a hundred thousand
features is itself a large task that is now largely done by other models.

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

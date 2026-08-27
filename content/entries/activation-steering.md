---
term: Activation Steering
aliases: [Representation Engineering, Activation Engineering, Feature Steering]
category: interpretability
subcategory: methods
status: experimental
difficulty: research
one_liner: Changing a model's behaviour at inference time by adding a direction to its internal activations rather than by prompting or retraining.
origin:
  year: 2023
  attribution: Turner et al. on activation addition; Zou et al. on representation engineering
historical_period: agentic
diagram:
  kind: figure
  title: Find a direction, then push along it
  footer: No training, no prompt, and reversible at run time — which makes it a useful research instrument.
    Also a control surface that bypasses every safeguard expressed in the prompt, which is why open-weight
    access changes the threat model.
  visual:
    kind: pipeline
    width: 740
    caption: α sets the strength and its sign sets the direction, so the same vector suppresses what it
      was built to elicit
    stages:
    - text: run two sets of prompts
      note: '"be honest…" and "be deceptive…"'
    - text: a steering vector v
      via: mean activation of one set, minus the mean of the other
    - text: h ← h + α·v, during generation
      tone: accent
      via: added to the residual stream at one layer
tags: [safety]
relations:
  depends_on: [sparse-autoencoder, mechanistic-interpretability]
  alternative_to: [prompt-engineering, lora]
  related_to: [alignment]
prerequisites: [mechanistic-interpretability]
encountered_in: [research-papers, github, conferences]
sources:
  - type: paper
    title: "Steering Language Models With Activation Engineering"
    url: https://arxiv.org/abs/2308.10248
    year: 2023
  - type: paper
    title: "Representation Engineering: A Top-Down Approach to AI Transparency"
    url: https://arxiv.org/abs/2310.01405
    year: 2023
updated: 2026-08-21
review_by: 2027-02-01
---

## Simple Explanation

If a concept like "formality" or "refusal" corresponds to a direction inside the
model, you can nudge behaviour by adding a multiple of that direction to the
activations as the model runs. No prompt, no fine-tuning — a dial applied at
inference.

## Technical Definition

Inference-time modification of hidden states by adding a scaled steering vector,
derived from contrastive activation differences between paired prompts or from a
sparse autoencoder feature direction. Strength is continuous and can be applied
at chosen layers and token positions.

## Why Does It Exist?

Prompts are indirect and can be overridden; fine-tuning is expensive and
permanent. Steering acts directly on the representation, and it is reversible.

## What Problem Does It Solve?

Fine-grained behavioural control without training, and — as a research tool —
causal evidence that a discovered feature does what its label claims.

## How Does It Work?


Run the model on a set of prompts exhibiting some behaviour and a matched set
exhibiting its opposite, record the residual-stream activations at a chosen
layer, and take the difference of the means. What comes out is a direction in
activation space that corresponds to the behaviour.

Then add it during generation: at that layer, h ← h + α·v. The coefficient α sets
the strength, and its sign sets the direction — the same vector that elicits a
behaviour suppresses it when subtracted. Refusal, sycophancy, formality and
verbosity have all been steered this way.

There is no training and no prompt involved, and it is reversible at run time,
which makes it a useful instrument for testing whether a behaviour is
represented as a direction at all. It is also a control surface that bypasses
everything expressed in the prompt, including safety instructions — which is one
of the concrete ways open-weight access changes the threat model rather than
merely changing who can run the model.

## Mental Model

An equaliser on a mixing desk rather than rewriting the song or asking the
singer to try again.

## Example

Steering vectors have been used to make models more or less refusing, to modulate
sycophancy, and — as a public demonstration — to make a model fixate obsessively
on a single concept by clamping one feature high.

## Common Confusions

* **Steering is not alignment** — it moves behaviour along a direction; it does
  not establish what the model is trying to do.
* **Side effects are the norm** — strong steering degrades coherence and general
  capability, because the direction is not perfectly isolated.
* **It requires model internals** — unavailable through most hosted APIs, so this
  is largely an open-weight or first-party technique.

## Real-World Usage

Research on control and honesty, red-teaming to elicit suppressed behaviour, and
experimental product controls exposed as feature dials.

## Why Should I Care?

It turns interpretability from description into intervention, and it is the
clearest demonstration that concepts in these models are geometric objects you
can actually manipulate.

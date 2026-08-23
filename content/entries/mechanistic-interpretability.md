---
term: Mechanistic Interpretability
aliases: [Mech Interp, Circuit Analysis, Reverse-Engineering Neural Networks]
category: interpretability
subcategory: approaches
status: modern
difficulty: research
one_liner: Reverse-engineering what a network actually computes internally, rather than only observing what it outputs.
origin:
  year: 2020
  circa: true
  attribution: Olah and collaborators at OpenAI and later Anthropic; the Circuits research thread
historical_period: foundation-model
tags: [safety]
relations:
  depends_on: [sparse-autoencoder, transformer]
  related_to: [alignment, activation-steering]
  different_from: [attention]
prerequisites: [transformer]
encountered_in: [research-papers, conferences, technical-blogs]
sources:
  - type: paper
    title: "A Mathematical Framework for Transformer Circuits"
    url: https://transformer-circuits.pub/2021/framework/index.html
    year: 2021
  - type: paper
    title: "Toy Models of Superposition"
    url: https://transformer-circuits.pub/2022/toy_model/index.html
    year: 2022
  - type: paper
    title: "Towards Monosemanticity: Decomposing Language Models With Dictionary Learning"
    url: https://transformer-circuits.pub/2023/monosemantic-features/index.html
    year: 2023
updated: 2026-08-21
review_by: 2027-02-01
---

## Simple Explanation

A trained network is a pile of numbers that works and nobody wrote. Mechanistic
interpretability tries to read it: to find the specific components that implement
a specific behaviour, and to describe the algorithm the model actually learned.

## Technical Definition

The research programme of identifying human-understandable computational
structures — features and the circuits connecting them — inside neural networks,
using activation analysis, causal interventions such as ablation and patching,
and dictionary learning methods that decompose activations into sparse
interpretable directions.

## Why Does It Exist?

Behavioural evaluation can only test cases you thought to test. If a model
behaves well on every test and fails in deployment, you have no way to know in
advance. Understanding the mechanism is the alternative to sampling the
behaviour.

## What Problem Does It Solve?

Verification rather than observation: detecting capabilities or dispositions a
model does not display on tests, and grounding claims about why a model did
something.

## How Does It Work?

```text
pick a behaviour ──▶ localise: which layers, heads, features are involved
                          │ ablate / patch to test causal necessity
                          ▼
                  describe the circuit ──▶ predict novel behaviour
                                            (the real test of the story)
```

## Mental Model

Reverse-engineering a chip with no documentation: probe pins, cut traces, see
what stops working, and gradually build a schematic.

## Example

Induction heads — attention heads that detect a repeated pattern and continue it —
were identified as a concrete circuit and linked to the emergence of in-context
learning. That is the shape of a mechanistic result: a specific component, a
specific algorithm, a causal test.

## Real-World Usage

Still principally research, with growing practical use: detecting deceptive or
sandbagging behaviour, auditing for unwanted capability, debugging refusal
behaviour, and steering activations at inference time.

## Common Confusions

* **Mechanistic vs behavioural interpretability** — attention weights, saliency
  maps and feature attributions describe correlations. Mechanistic work demands
  causal evidence.
* **Superposition makes it hard** — networks represent more features than they
  have dimensions, so neurons are usually polysemantic. This is the problem
  sparse autoencoders address.
* **Scaling is unsolved** — full circuit-level understanding of a frontier model
  is not currently achievable.

## Why Should I Care?

It is the most credible route from "the model passed our tests" to "we know what
the model is doing", which is the distinction safety cases will eventually have
to rest on.

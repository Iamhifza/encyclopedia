---
term: Small Language Model
aliases: [SLM, Edge Model, On-Device Model, Local Model]
category: llms-foundation-models
subcategory: models
depth: full
status: modern
difficulty: beginner
one_liner: "A model small enough to run on a laptop or phone, traded against the capability of a large one."
historical_period: agentic
tags: [architecture]
relations:
  is_a: [large-language-model]
  depends_on: [distillation, quantization]
  related_to: [open-weight-model, model-routing, data-curation]
prerequisites: [large-language-model]
encountered_in: [production-systems, github, technical-blogs]
sources:
  - type: paper
    title: "Textbooks Are All You Need (phi models)"
    url: https://arxiv.org/abs/2306.11644
    year: 2023
  - type: paper
    title: "Training Compute-Optimal Large Language Models"
    url: https://arxiv.org/abs/2203.15556
    year: 2022
  - type: repo
    title: "llama.cpp — running small models locally"
    url: https://github.com/ggerganov/llama.cpp
updated: 2026-08-21
review_by: 2027-02-01
---

## Simple Explanation

Roughly a model under about ten billion parameters — small enough to run on a
consumer GPU, a laptop, or with quantisation a phone. It will not match a
frontier model on hard reasoning. For classification, extraction, routing,
summarisation and formatting, that gap frequently does not matter.

## Technical Definition

A language model in the sub-10B range, typically produced by distillation from a
larger teacher and trained far past the compute-optimal point on heavily curated
data, so that inference cost rather than training cost is what has been
minimised.

## Why Does It Exist?

Chinchilla scaling says how to spend a *training* budget optimally, but a
deployed model's lifetime cost is dominated by inference. Deliberately training a
small model on far more tokens than compute-optimal is therefore rational: you
overspend once to underspend forever.

## What Problem Does It Solve?

Cost at volume, latency, privacy — nothing leaves the device — and offline
operation. Also availability: no rate limits, no provider outage.

## How Does It Work?

```text
large teacher model
   │ generate high-quality training data
   │ distil behaviour
   ▼
small model ──▶ quantise to 4-bit ──▶ ~2-5 GB ──▶ runs on a laptop
   │
   └─ trained on far more tokens per parameter than compute-optimal
```

## Mental Model

A specialist junior rather than a consultant. Faster, cheaper, always available,
and you would not hand them the hardest problem in the building.

## Example

The phi model family demonstrated the principle sharply: small models trained on
carefully filtered, textbook-quality and synthetic data outperformed
substantially larger models trained on raw web text. Capability came from data
quality, not scale — which is the entire argument for the category.

## Real-World Usage

Classification and extraction pipelines, on-device assistants, autocomplete,
draft models for speculative decoding, and the cheap tier in a routing setup.
Served locally through llama.cpp or Ollama, or at volume through vLLM.

## Common Confusions

* **Small does not mean bad** — a 7B model from 2026 outperforms the frontier
  models of 2022. Any comparison needs a date attached.
* **Small does not mean cheap to build** — training past compute-optimal costs
  *more* to train, not less.
* **They degrade differently, not uniformly** — instruction-following and
  formatting hold up well; multi-step reasoning, long-context recall and
  factual precision fall off first. Which of those your task needs is the actual
  decision.

## Why Should I Care?

The most common architectural mistake in AI products is sending every request to
a frontier model. Knowing what a small model can do — and testing it on your own
evaluation set rather than a leaderboard — is where most cost savings live.

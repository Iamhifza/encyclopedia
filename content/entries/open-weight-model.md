---
term: Open-Weight Model
aliases: [Open Model, Open-Source Model, Weights-Available Model]
category: industry-culture
subcategory: model-economy
status: modern
difficulty: beginner
one_liner: A model whose trained parameters can be downloaded and run yourself, whatever the licence says about the rest.
origin:
  year: 2023
  attribution: Terminology sharpened during debates over whether Llama-style releases qualify as open source
historical_period: foundation-model
tags: [culture]
relations:
  is_a: [foundation-model]
  different_from: [frontier-model]
  used_by: [vllm, lora, quantization]
  related_to: [distillation]
prerequisites: [foundation-model]
encountered_in: [github, job-descriptions, social-media, production-systems]
sources:
  - type: docs
    title: "OSI — the Open Source AI Definition"
    url: https://opensource.org/ai
    year: 2024
  - type: report
    title: "The Llama 3 Herd of Models"
    url: https://arxiv.org/abs/2407.21783
    year: 2024
updated: 2026-08-21
---

## Simple Explanation

You can download the weights and run the model on your own hardware. That is a
real and important freedom. It is not the same as open source, because the
training data, the training code and the licence terms are usually not open too.

## Technical Definition

A model distributed with downloadable parameters. Licences vary widely: some are
genuinely permissive (Apache 2.0, MIT), others impose acceptable-use restrictions,
field-of-use limits or scale-based conditions. The Open Source Initiative's 2024
definition requires, in addition to weights, sufficient information about training
data and the code to reproduce the system — a bar most "open" models do not meet.

## Why Does It Exist?

Downloadable weights enable self-hosting, on-premises deployment for regulated
data, fine-tuning, research on internals, and independence from any single
vendor's pricing and availability.

## What Problem Does It Solve?

Data residency and privacy, cost control at volume, latency from local
deployment, deep customisation, and the ability to inspect and modify.

## How Does It Work?

```text
weights on a hub ──▶ your GPUs ──▶ vLLM / llama.cpp ──▶ your endpoint
                                        │
                     quantise · fine-tune · steer · study internals
```

## Mental Model

Owning the engine rather than renting the ride. More control, and you now own
maintenance, capacity planning and security.

## Example

The practical calculus: an open-weight model is usually somewhat behind the
strongest hosted models on general capability, and ahead on cost at sustained
volume, data control and customisability. Which side wins depends on volume,
sensitivity and how much of your quality requirement is task-specific.

## Real-World Usage

Self-hosted deployments behind an OpenAI-compatible endpoint, on-premises
inference for regulated data, fine-tuned domain models, edge and local
deployment, and the entire open research ecosystem that depends on inspectable
weights.

## Common Confusions

* **Open-weight vs open-source** — weights available versus the full recipe
  under an OSI-conformant licence. Most "open-source models" are open-weight.
* **Open does not mean unrestricted** — read the licence; several impose real
  limits.
* **Self-hosting is not automatically cheaper** — idle GPUs cost money, and
  utilisation is what decides the comparison.

## Why Should I Care?

It is one of the two or three genuine architectural decisions in an AI product,
and the vocabulary around it is frequently used imprecisely in ways that matter
legally.

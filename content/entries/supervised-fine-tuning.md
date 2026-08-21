---
term: Supervised Fine-Tuning
aliases: [SFT, Instruction Tuning, Behavioural Cloning]
category: llm-training
subcategory: alignment
status: established
difficulty: intermediate
one_liner: Training a pretrained model on curated examples of good responses so it stops completing text and starts following instructions.
origin:
  year: 2021
  circa: true
  attribution: FLAN and InstructGPT established instruction tuning as standard practice
historical_period: foundation-model
tags: [training]
relations:
  successor_of: [pretraining]
  is_a: [supervised-learning]
  evolved_into: [rlhf]
  used_by: [lora]
  alternative_to: [rag]
prerequisites: [pretraining, supervised-learning]
encountered_in: [research-papers, github, job-descriptions]
sources:
  - type: paper
    title: "Training Language Models to Follow Instructions with Human Feedback (InstructGPT)"
    url: https://arxiv.org/abs/2203.02155
    year: 2022
  - type: paper
    title: "Finetuned Language Models Are Zero-Shot Learners (FLAN)"
    url: https://arxiv.org/abs/2109.01652
    year: 2021
updated: 2026-08-21
---

## Simple Explanation

A base model given "Write a poem about rain" might continue with "Write a poem
about snow. Write a poem about..." — because that is a plausible continuation of
internet text. Supervised fine-tuning shows it thousands of examples of requests
followed by good responses, until answering becomes the plausible continuation.

## Technical Definition

Continued training on curated (prompt, response) pairs with the same next-token
objective, with loss computed only on response tokens. Typically a few thousand
to a few hundred thousand examples, orders of magnitude less compute than
pretraining.

## Why Does It Exist?

Pretraining produces a model of text, not an assistant. The gap between "what
would plausibly follow" and "what would be a helpful answer" has to be closed
somehow, and demonstrations are the cheapest way to close it.

## What Problem Does It Solve?

Instruction following, response format, refusal behaviour, tone, and any
domain-specific style that prompting cannot reliably enforce.

## How Does It Work?

```text
base model ──▶ (instruction, ideal response) × N ──▶ instruct model
                        │
              loss masked to response tokens only
```

## Mental Model

Apprenticeship by imitation. The apprentice already knows the trade's vocabulary;
they are now copying how a good practitioner actually responds.

## Example

A few thousand high-quality examples usually beat a hundred thousand mediocre
ones. Data quality dominates data quantity at this stage, which is why curation
is where most of the effort goes.

## Real-World Usage

Every deployed assistant has been through it. Teams apply it to enforce house
style, output schemas, domain vocabulary and tool-calling formats — normally with
LoRA rather than full fine-tuning.

## Common Confusions

* **SFT vs RLHF** — SFT imitates good answers; preference methods optimise
  against comparisons, which can exceed demonstration quality.
* **SFT vs RAG** — fine-tuning teaches behaviour and form; retrieval supplies
  facts. Fine-tuning to inject knowledge is expensive, hard to update, and prone
  to confident errors.
* **Catastrophic forgetting** — aggressive fine-tuning on narrow data degrades
  general capability, which is one reason parameter-efficient methods are
  preferred.

## Why Should I Care?

It is the cheapest lever that genuinely changes model behaviour, and knowing when
*not* to reach for it — when the real problem is context, retrieval or evaluation
— saves most teams a great deal of money.

---
term: Distillation
aliases: [Knowledge Distillation, Teacher-Student Training, Model Distillation]
category: llm-training
subcategory: adaptation
status: established
difficulty: intermediate
one_liner: Training a small model to imitate a large one, transferring much of its capability at a fraction of the serving cost.
origin:
  year: 2015
  attribution: Hinton, Vinyals and Dean; related compression ideas from Buciluă et al. in 2006
historical_period: deep-learning
tags: [training]
relations:
  alternative_to: [quantization, lora]
  used_by: [speculative-decoding]
  related_to: [synthetic-data]
prerequisites: [supervised-fine-tuning]
encountered_in: [research-papers, production-systems, job-descriptions]
sources:
  - type: paper
    title: "Distilling the Knowledge in a Neural Network"
    url: https://arxiv.org/abs/1503.02531
    year: 2015
  - type: paper
    title: "DistilBERT, a distilled version of BERT"
    url: https://arxiv.org/abs/1910.01108
    year: 2019
updated: 2026-08-21
---

## Simple Explanation

A big model knows more than its final answer reveals. When it says "cat" it also
assigns some probability to "dog" and almost none to "aeroplane", and that
distribution encodes what it thinks the world looks like. Train a small model to
match the whole distribution, not just the answer, and it learns much faster than
from hard labels.

## Technical Definition

Training a student model to match a teacher's outputs — soft logits with
temperature, intermediate representations, or generated sequences — rather than
ground-truth labels alone. For LLMs, sequence-level distillation on
teacher-generated data is now the common form.

## Why Does It Exist?

Frontier models are expensive to serve. Most production traffic does not need
frontier capability, but it does need something better than a small model trained
from scratch.

## What Problem Does It Solve?

Inference cost and latency, by shifting capability into a model that is cheaper
to run.

## How Does It Work?

```text
teacher (large) ──▶ soft targets / generated responses
                              │
student (small) ──▶ trained to match them ──▶ deployed
```

The "dark knowledge" is the relative probabilities of the wrong answers, which
carry information about similarity that a one-hot label destroys.

## Mental Model

An apprentice learning not just what the master decided but how close the
alternatives were.

## Example

Most small open-weight models are distilled from larger ones in their own family.
DeepSeek-R1's distilled variants transferred reasoning behaviour into models small
enough to run locally.

## Real-World Usage

Building small production models, creating draft models for speculative decoding,
and — controversially — training on another provider's outputs, which most
commercial terms of service prohibit.

## Common Confusions

* **Distillation vs quantisation** — a new, smaller model versus the same model
  in fewer bits. They compose.
* **Distillation vs fine-tuning on synthetic data** — the boundary is blurry; the
  distinguishing feature is that the target is the teacher's behaviour.
* **The student rarely matches the teacher** — expect most of the capability on
  the distilled distribution, and gaps outside it.

## Why Should I Care?

It is how frontier capability reaches production budgets, and it is why the
capability gap between the largest models and small open ones keeps narrowing
faster than compute alone would suggest.

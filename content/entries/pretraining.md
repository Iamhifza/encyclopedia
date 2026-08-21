---
term: Pretraining
aliases: [Pre-training, Base Model Training]
category: llm-training
subcategory: pretraining
status: established
difficulty: advanced
one_liner: The expensive first phase where a model learns language and world knowledge by predicting the next token across trillions of tokens of text.
origin:
  year: 2018
  circa: true
  attribution: Established as the dominant NLP paradigm by ELMo, BERT and GPT
historical_period: transformer
tags: [training]
relations:
  depends_on: [self-supervised-learning, backpropagation, scaling-laws]
  part_of: [large-language-model]
  evolved_into: [supervised-fine-tuning]
  related_to: [tensor-parallelism]
prerequisites: [self-supervised-learning, transformer]
encountered_in: [research-papers, job-descriptions, conferences]
sources:
  - type: paper
    title: "Training Compute-Optimal Large Language Models (Chinchilla)"
    url: https://arxiv.org/abs/2203.15556
    year: 2022
  - type: report
    title: "The Llama 3 Herd of Models"
    url: https://arxiv.org/abs/2407.21783
    year: 2024
updated: 2026-08-21
---

## Simple Explanation

Show the model an enormous amount of text with the next word hidden, over and
over, for months, on thousands of GPUs. It has no task and no labels. When it
finishes it cannot follow instructions, but it has absorbed grammar, facts, code,
reasoning patterns and style.

## Technical Definition

Self-supervised optimisation of a next-token cross-entropy objective over a large
corpus, using distributed data, tensor and pipeline parallelism, with a learning
rate schedule, gradient clipping and careful loss-spike recovery. The output is a
*base model*: a strong conditional text distribution with no assistant behaviour.

## Why Does It Exist?

Because task-specific training from scratch wastes the vast majority of what
needs to be learned. Language, world structure and reasoning are shared across
tasks and can be learned once from unlabelled text.

## What Problem Does It Solve?

It amortises the cost of learning general competence, so downstream adaptation
needs thousands of examples instead of millions.

## How Does It Work?

```text
raw web, code, books ──▶ filter, dedupe, decontaminate ──▶ mixture weights
                                     │
                          tokenise ──┤
                                     ▼
            distributed training loop: forward, backward, all-reduce, step
                                     │
                                     ▼
                            base model checkpoint
```

Data work — filtering, deduplication, mixture ratios, contamination removal —
accounts for much of the quality difference between models with similar
architectures and budgets.

## Mental Model

A general education with no examinations and no curriculum: read everything, be
tested on nothing except predicting what comes next.

## Example

Llama 3 was trained on the order of 15 trillion tokens. The Chinchilla result
established that for a fixed compute budget, most models of the time were too
large for their data, and that parameters and tokens should be scaled together —
a finding that redirected the industry toward smaller models trained far longer.

## Real-World Usage

Performed by a small number of organisations because of cost. Everyone else
consumes the output: base models, instruction-tuned variants and open-weight
releases. Continued pretraining on domain corpora is a middle path used for
specialised fields.

## Common Confusions

* **Pretraining vs fine-tuning** — pretraining creates general capability from
  scratch; fine-tuning adjusts behaviour with orders of magnitude less compute.
* **Base model vs instruct model** — a base model completes text and does not
  follow instructions. Handing one to users is a common early mistake.
* **"More parameters is better"** — compute-optimal scaling says parameters and
  tokens must grow together, and inference cost argues for smaller models trained
  on more data.

## Why Should I Care?

Everything a model knows, and every bias and gap it carries, originates here. It
also explains the knowledge cutoff: facts after the data collection date were
never seen, which is the entire motivation for retrieval.

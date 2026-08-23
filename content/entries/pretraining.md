---
term: Pretraining
aliases: [Pre-training, Base Model Training, Foundation Training]
category: llm-training
subcategory: pretraining
depth: full
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
  depends_on: [self-supervised-learning, backpropagation, scaling-laws, next-token-prediction, data-curation]
  part_of: [large-language-model]
  evolved_into: [supervised-fine-tuning]
  used_by: [base-model, foundation-model]
  related_to: [tensor-parallelism, data-parallelism, gpu-cluster, curriculum-learning, benchmark-contamination]
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
  - type: paper
    title: "Scaling Laws for Neural Language Models"
    url: https://arxiv.org/abs/2001.08361
    year: 2020
  - type: paper
    title: "The RefinedWeb Dataset for Falcon LLM"
    url: https://arxiv.org/abs/2306.01116
    year: 2023
    note: One of the few detailed public accounts of the data pipeline.
updated: 2026-08-22
---

## Simple Explanation

Show the model an enormous amount of text with the next token hidden, ask it to
guess, penalise it in proportion to its surprise, and repeat for months across
thousands of GPUs. There is no task, no labels and no supervision beyond the text
itself.

What comes out cannot follow instructions. It has, however, absorbed grammar,
facts, code, reasoning patterns and style — and everything that happens
afterwards is comparatively cheap adjustment of a thing that already knows.

## Technical Definition

Self-supervised optimisation of a [next-token](next-token-prediction.md)
cross-entropy objective over a large corpus, using
[data](data-parallelism.md), [tensor](tensor-parallelism.md) and
[pipeline](pipeline-parallelism.md) parallelism across a
[GPU cluster](gpu-cluster.md), with a learning-rate schedule, gradient clipping
and loss-spike recovery. The output is a [base model](base-model.md): a strong
conditional text distribution with no assistant behaviour.

## Why Does It Exist?

Because task-specific training from scratch wastes the overwhelming majority of
what has to be learned. Language, world structure and reasoning are shared across
every task, and they can be learned once from unlabelled text — which exists in
quantities no labelling effort could ever match.

## What Problem Does It Solve?

It amortises the cost of general competence. Downstream adaptation then needs
thousands of examples rather than millions.

## How Does It Work?

```text
raw web, code, books, papers
   │ extract · filter · deduplicate · decontaminate
   │ choose mixture weights          ← DATA CURATION, most of the quality
   ▼
tokenise ──▶ shard across the cluster
   │
   ├── forward · backward · ALL-REDUCE gradients · optimiser step
   │      repeated for months, checkpointing constantly
   │      because at this scale hardware failure is the steady state
   │
   └── final phase: anneal on high-quality data at low learning rate
   ▼
base model checkpoint
```

Three things dominate the outcome, and only one is the architecture:

**Data.** Filtering, deduplication, mixture ratios and decontamination account
for much of the difference between models with similar budgets. See
[data curation](data-curation.md).

**Scale allocation.** [Chinchilla](scaling-laws.md) established that parameters
and tokens should grow together; inference economics then pushed practice past
the compute-optimal point, deliberately overspending on training to underspend
on serving for the model's whole life.

**The end of the run.** [Curriculum](curriculum-learning.md) effects are real:
data seen last, at a low learning rate, has outsized influence on where the
weights settle.

## Mental Model

A general education with no examinations and no curriculum: read everything, be
tested on nothing except predicting what comes next.

## Example

Llama 3 was trained on the order of 15 trillion tokens. Two details from the
public report are worth carrying: hardware failures across the cluster were
frequent enough to be routine rather than exceptional, and a meaningful share of
final quality came from the annealing phase — a small fraction of total compute
spent on carefully chosen data.

That is the shape of the work. It is a distributed systems problem and a data
problem wearing a machine learning hat.

## Real-World Usage

Performed by a small number of organisations because of cost. Everyone else
consumes the output: base models, instruction-tuned variants and
[open-weight](open-weight-model.md) releases. *Continued* pretraining on a domain
corpus is the accessible middle path — far cheaper than a full run, far more
capable of shifting domain knowledge than fine-tuning.

## Common Confusions

* **Pretraining vs fine-tuning** — creating general capability from scratch
  versus adjusting behaviour with orders of magnitude less compute.
* **Base model vs instruct model** — a base model completes text and does not
  follow instructions. Handing one to users is a common early mistake.
* **"More parameters is better"** — compute-optimal scaling says parameters and
  tokens must grow together, and inference cost argues for smaller models trained
  longer.
* **Pretraining is not where behaviour comes from** — the tone, the refusals, the
  formatting and most of what users react to are added afterwards.

## Why Should I Care?

Everything a model knows, and every bias and gap it carries, originates here. It
also explains the knowledge cutoff: facts after the data collection date were
never seen, weights cannot be updated incrementally, and
[retrieval](rag.md) is the architecture that follows from those two facts.

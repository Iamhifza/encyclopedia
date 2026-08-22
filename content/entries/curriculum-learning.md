---
term: Curriculum Learning
aliases: [Staged Training, Data Ordering, Annealing, Mid-Training]
category: llm-training
subcategory: data
depth: full
status: established
difficulty: advanced
one_liner: "Training on easy or general material first and harder or more specialised material later, rather than shuffling everything together."
origin:
  year: 2009
  attribution: Bengio et al. formalised the idea for neural networks; the intuition is borrowed from education
historical_period: statistical-ml
tags: [training]
relations:
  part_of: [pretraining]
  related_to: [data-curation, scaling-laws, gradient-descent, synthetic-data]
prerequisites: [pretraining, data-curation]
encountered_in: [research-papers, technical-blogs, conferences]
sources:
  - type: paper
    title: "Curriculum Learning"
    url: https://dl.acm.org/doi/10.1145/1553374.1553380
    year: 2009
  - type: report
    title: "The Llama 3 Herd of Models — data mix annealing"
    url: https://arxiv.org/abs/2407.21783
    year: 2024
updated: 2026-08-21
---

## Simple Explanation

Nobody teaches arithmetic by shuffling a textbook and handing over random pages.
Order matters for human learning, and the question is whether it matters for
machines.

The answer turns out to be a qualified yes — not in the naive "easy examples
first" sense, which is unreliable, but in the specific and now-standard practice
of changing the *data mixture* over the course of training.

## Technical Definition

Ordering training data by some notion of difficulty or relevance rather than
sampling uniformly. In LLM pretraining the dominant form is mixture scheduling:
beginning with broad web-scale data and shifting toward higher-quality,
domain-specific or instruction-like data in the final phase — often called
annealing or mid-training.

## Why Does It Exist?

Optimisation is path-dependent. Where the model ends up depends on the sequence
of gradients it received, not merely on the set of examples it saw. That makes
ordering a lever, in principle.

## What Problem Does It Solve?

Better use of a fixed data budget, and disproportionate influence for
high-quality data — because material seen at the end of training, at a low
learning rate, shapes the final weights more than material seen at the start.

## How Does It Work?

```text
training progress ──────────────────────────────────▶

  early                  middle                  late (annealing)
  broad web text         balanced mixture        high-quality curated
  high learning rate     decaying                low learning rate
  learn language         learn breadth           sharpen capability
                                                 ▲
                                       this phase punches above its weight
```

## Mental Model

A syllabus rather than a reading pile. Same books, deliberately sequenced — and
what you read last, you remember best.

## Example

The most consequential modern use is the annealing phase. Frontier model reports
describe upweighting high-quality sources — curated text, code, mathematics,
instruction-like data — during the final percentage of pretraining, with measurable
benchmark gains for a very small fraction of total compute. This is the strongest
practical evidence that ordering matters, and it works partly because the learning
rate is low at that point, so late data has an outsized influence on where the
weights settle.

## Real-World Usage

Standard in frontier pretraining as the annealing or mid-training phase, and in
domain adaptation where a model is continued on specialist material after general
pretraining. Also appears in reinforcement learning, where problems too hard for
the current policy produce no learning signal, so difficulty is ramped
deliberately.

## Common Confusions

* **Classical curriculum learning is not reliably beneficial** — "easy examples
  first" has mixed results in the literature and is not standard practice. What
  works is mixture scheduling, which is a different claim.
* **Curriculum vs data curation** — *when* material is shown versus *what* is
  included and in what proportion. They interact and are distinct decisions.
* **It is not fine-tuning** — annealing happens within pretraining, with the same
  objective; fine-tuning is a separate stage afterwards.

## Why Should I Care?

It is one of the few remaining levers on pretraining quality that costs almost
nothing in compute, and it explains why model reports place such emphasis on
what happens in the final phase of a training run.

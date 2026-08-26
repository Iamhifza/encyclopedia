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
diagram:
  kind: flow
  title: Not all training tokens are worth the same
  footer: The final anneal is a few per cent of the tokens and a disproportionate share of the measured
    capability, which is why data mixtures are guarded so closely.
  nodes:
  - title: Early
    note: broad web text
    caption: high LR · learn language
  - title: Middle
    note: balanced mixture
    caption: decaying LR · learn breadth
  - title: Anneal
    note: high-quality curated
    accent: true
    caption: low LR · sharpen capability
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


Order the training data so the distribution shifts as the run proceeds. Early
tokens are broad and cheap — general web text at a high learning rate, where the
model is learning the shape of language at all. The middle is a balanced mixture
across domains. The final phase, the anneal, is a small quantity of carefully
curated high-quality data at a decayed learning rate.

The anneal is where the ordering earns its keep. Late training at a low learning
rate makes small, targeted adjustments, so the data seen there has an outsized
effect on measured capability relative to its token count. This is also why lab
data mixtures are among the least published details of any model.

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

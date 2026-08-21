---
term: Benchmark Contamination
aliases: [Data Contamination, Test Set Leakage, Train-Test Contamination]
category: evaluation-safety
subcategory: measurement
status: established
difficulty: intermediate
one_liner: When benchmark questions end up in a model's training data, so its score reflects memorisation rather than capability.
origin:
  year: 2021
  circa: true
  attribution: A long-standing statistical concern; acute for LLMs once pretraining corpora began covering most of the public web
historical_period: foundation-model
tags: [safety]
relations:
  is_a: [overfitting]
  related_to: [benchmark, pretraining, rlvr]
prerequisites: [benchmark, pretraining]
encountered_in: [research-papers, technical-blogs, conferences]
sources:
  - type: paper
    title: "Documenting Large Webtext Corpora (contamination analysis)"
    url: https://arxiv.org/abs/2104.08758
    year: 2021
  - type: paper
    title: "Rethinking Benchmark and Contamination for Language Models"
    url: https://arxiv.org/abs/2311.04850
    year: 2023
updated: 2026-08-21
---

## Simple Explanation

Public benchmarks live on the web. Pretraining scrapes the web. So the exam
answers are in the textbook, and a high score may mean the model has seen this
exact question before.

## Technical Definition

Presence of evaluation data, or near-duplicates of it, in the training corpus,
inflating measured performance without corresponding generalisation. Detection
approaches include n-gram overlap against the corpus, comparing performance on
pre- and post-cutoff variants, and canary strings deliberately embedded in test
sets.

## Why Does It Exist?

Web-scale training and web-published benchmarks are fundamentally incompatible.
The problem grows every year as more benchmarks and their solutions are
discussed online.

## What Problem Does It Solve?

Nothing — it is the reason benchmark scores need to be read sceptically.

## How Does It Work?

```text
benchmark published ──▶ indexed, discussed, forked into tutorials
                          │
                pretraining scrape includes it
                          │
        model "solves" it ──▶ score rises, capability may not
```

## Mental Model

An exam whose past papers, with worked solutions, were in the revision pack.

## Example

The standard diagnostic is a sharp performance drop on freshly constructed
problems of identical difficulty. Held-out variants of maths benchmarks written
after a model's cutoff routinely score lower than the public originals.

## Real-World Usage

Serious model reports now include contamination analysis and decontamination of
training data. Newer benchmarks use private test splits, rolling refreshes, or
tasks generated after the model's cutoff.

## Common Confusions

* **Contamination is not always deliberate** — nobody needs to cheat; the web
  does it automatically.
* **Decontamination is imperfect** — paraphrases and translations evade n-gram
  matching.
* **It affects fine-tuning and RL too** — verifiable-reward training on public
  problem sets has the same exposure.

## Why Should I Care?

It is the main reason to distrust a leaderboard and to build a private evaluation
set from your own data.

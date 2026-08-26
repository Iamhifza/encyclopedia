---
term: Data Curation
aliases: [Data Filtering, Deduplication, Data Mixture, Dataset Construction]
category: llm-training
subcategory: data
depth: full
status: established
difficulty: advanced
one_liner: "Deciding what goes into a training corpus and in what proportion, which decides more about model quality than architecture does."
historical_period: foundation-model
diagram:
  kind: steps
  title: Petabytes in, a training stream out
  footer: Curation is where most of the quality difference between models is made, and it is almost never
    published. The filters are the recipe.
  steps:
  - title: Filter the crawl down
    notes:
    - label: Order matters
      text: deduplicate before quality-filtering and you spend the classifier on copies
    visual:
      kind: pipeline
      width: 660
      stages:
      - text: raw crawl
        note: petabytes
      - text: text, in one language
        note: ''
        via: extract text · drop boilerplate · language ID
      - text: plausibly useful text
        via: quality filter — heuristics, or a classifier trained on "good" text
      - text: each document once
        via: deduplicate — exact hashes, then MinHash for near-duplicates
      - text: clean pool
        tone: accent
        via: decontaminate against benchmark test sets · safety filtering
  - title: Weight what survived
    notes:
    - label: Lever
      text: the mixture is retuned far more often than the architecture is
    visual:
      kind: segments
      width: 660
      label: training stream
      caption: the same clean pool, sampled at different rates
      segments:
      - text: web
        value: 40
        value_label: 40%
      - text: code
        value: 20
        value_label: 20%
      - text: books
        value: 15
        value_label: 15%
      - text: papers
        value: 10
        value_label: 10%
      - text: curated
        value: 15
        value_label: 15%
        tone: accent
tags: [training]
relations:
  part_of: [pretraining]
  related_to: [synthetic-data, benchmark-contamination, scaling-laws, data-poisoning]
prerequisites: [pretraining]
encountered_in: [research-papers, job-descriptions, technical-blogs]
sources:
  - type: paper
    title: "The RefinedWeb Dataset for Falcon LLM"
    url: https://arxiv.org/abs/2306.01116
    year: 2023
  - type: paper
    title: "Deduplicating Training Data Makes Language Models Better"
    url: https://arxiv.org/abs/2107.06499
    year: 2021
  - type: paper
    title: "DataComp-LM: In search of the next generation of training sets"
    url: https://arxiv.org/abs/2406.11794
    year: 2024
updated: 2026-08-21
---

## Simple Explanation

Two labs with the same architecture, the same parameter count and the same
compute budget will produce models of noticeably different quality. The
difference is almost entirely what they trained on. Curation is the unglamorous
work of deciding that: what to keep, what to throw away, what to duplicate, and
in what mixture.

## Technical Definition

The pipeline transforming raw crawled data into a training corpus: extraction and
cleaning, language identification, quality filtering (heuristic or
classifier-based), exact and near-duplicate removal, toxicity and PII handling,
benchmark decontamination, and the choice of sampling weights across domains
such as web text, code, books and scientific writing.

## Why Does It Exist?

Raw web crawl is mostly boilerplate, navigation furniture, spam and duplication.
Training on it directly wastes an enormous share of the compute budget on text
nobody would learn anything from, and duplicated passages get memorised rather
than generalised.

## What Problem Does It Solve?

Compute efficiency and capability per token — and, increasingly, legal and
reputational exposure, since what a model can be induced to reproduce is
determined here.

## How Does It Work?

Mixture weights are a hyperparameter as consequential as learning rate. Raising
the code fraction improves reasoning benchmarks, not only coding ones — a
repeatedly observed and still not fully explained result.

## Mental Model

Building a syllabus rather than handing someone a library card. What is on the
reading list, how much of each, and in what order.

## Example

Deduplication is the clearest single win: removing near-duplicate documents
improves quality *and* reduces training cost, because duplicated text produces
memorisation instead of generalisation. Curation typically discards the
overwhelming majority of raw crawl — the surviving fraction is a small percentage
of what was collected.

## Real-World Usage

Every serious pretraining effort has a dedicated data team, and their work is the
least published part of frontier model development. Open datasets — RefinedWeb,
FineWeb, DataComp-LM — made the methodology inspectable, and the ablations
published alongside them are the best available evidence that curation beats
architecture for a fixed budget.

## Common Confusions

* **More data is not better** — beyond deduplication, adding low-quality tokens
  can reduce quality at a fixed compute budget.
* **Filtering is not neutral** — a quality classifier encodes somebody's notion
  of good writing, and systematically removes dialects, registers and languages
  that resemble it less. This is a measurable source of model bias.
* **Decontamination is imperfect** — paraphrases and translations survive n-gram
  matching, which is why benchmark scores need scepticism.

## Why Should I Care?

It is where a model's knowledge, its blind spots and its biases originate, and it
is the part of the pipeline that most reliably distinguishes a good model from a
mediocre one built with identical resources.

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
diagram:
  kind: figure
  title: The benchmark ends up in the training data
  footer: Not usually deliberate. A benchmark that is worth using gets written about, and anything written
    about ends up in a scrape — so a public benchmark decays from the day it is published.
  visual:
    kind: pipeline
    width: 740
    caption: which is why held-out, private and freshly-written evaluations are worth so much more than
      a familiar public number
    stages:
    - text: a benchmark is published
      note: openly, as it should be
    - text: it is discussed, forked, tutorialised
      via: blog posts, notebooks, Stack Overflow answers, GitHub copies
    - text: the pretraining scrape picks it up
      via: the crawl cannot tell an evaluation set from any other page
    - text: the score rises; the capability may not
      tone: bad
      via: the model has seen the answers
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


A useful benchmark gets published, then written about, forked into tutorials,
pasted into notebooks and answered on forums. The next pretraining crawl picks
all of that up, because nothing distinguishes an evaluation set from any other
page on the web. The model has now, in effect, been shown the test.

The result is a score that rises while the underlying capability does not. It is
rarely deliberate — deduplication and decontamination filters exist precisely to
catch this — but exact-match filtering misses paraphrases, translations and
worked solutions, which is most of how a benchmark actually spreads.

The tell is a model that performs far better on a well-known benchmark than on a
freshly-written test of the same skill. Which is why held-out private sets,
benchmarks published after a model's training cutoff, and evaluations you write
yourself against your own data are worth more than any familiar public number.

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

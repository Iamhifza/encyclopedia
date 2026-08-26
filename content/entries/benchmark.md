---
term: Benchmark
aliases: [Eval, Evals, Model Evaluation, Leaderboard]
category: evaluation-safety
subcategory: measurement
status: foundational
difficulty: beginner
one_liner: A fixed set of tasks with known answers, used to compare models on the same footing.
origin:
  year: 1998
  circa: true
  attribution: Long-standing in ML; MNIST, ImageNet and GLUE shaped the modern practice
historical_period: statistical-ml
diagram:
  kind: flow
  title: Five choices sit between a model and its score
  footer: Two papers reporting different numbers for the same model on the same benchmark are usually
    both right — they made different choices here. Compare numbers only when the harness is the same.
  nodes:
  - title: Dataset
    note: which items, which split
    caption: and how old
  - title: Prompt
    note: template, examples, formatting
    caption: moves scores by points
  - title: Model
    note: version, temperature, max tokens
    caption: pin all three
  - title: Score
    note: parse, then aggregate
    accent: true
    caption: the parser fails silently
tags: [safety]
relations:
  used_by: [evaluation-harness, llm-as-a-judge]
  related_to: [benchmark-contamination, scaling-laws, frontier-model]
prerequisites: [supervised-learning]
encountered_in: [research-papers, social-media, job-descriptions, conferences]
sources:
  - type: paper
    title: "GLUE: A Multi-Task Benchmark and Analysis Platform for NLU"
    url: https://arxiv.org/abs/1804.07461
    year: 2018
  - type: paper
    title: "SWE-bench: Can Language Models Resolve Real-World GitHub Issues?"
    url: https://arxiv.org/abs/2310.06770
    year: 2023
  - type: repo
    title: "lm-evaluation-harness"
    url: https://github.com/EleutherAI/lm-evaluation-harness
updated: 2026-08-21
---

## Simple Explanation

To say one model is better than another you need the same questions and the same
marking scheme. A benchmark is that shared exam. It is also, inevitably,
something people optimise for — which is what limits how much it can tell you.

## Technical Definition

A standardised dataset with an evaluation protocol and scoring function.
Comparability requires holding the prompt format, scaffold, sampling parameters
and few-shot count fixed, which is why published scores from different sources
are frequently not comparable.

## Why Does It Exist?

Without shared measurement, progress claims are unfalsifiable. ImageNet's role in
deep learning's rise is the standard example of a benchmark organising a field.

## What Problem Does It Solve?

Comparability, and a target that makes incremental progress legible.

## How Does It Work?


A benchmark is a dataset plus a procedure, and the procedure has more moving
parts than the headline number suggests. Items are drawn from a split, rendered
through a prompt template, sent to a model at particular settings, parsed out of
whatever the model returned, scored, and aggregated.

Every one of those steps changes the result. The same model on the same dataset
can move several points on prompt formatting alone, more if the number of
in-context examples changes, and more again if the parser silently scores an
unparseable answer as wrong rather than reporting a failure. None of this is
misconduct; it is why two honest papers report different numbers.

So a benchmark score is only comparable against another score produced by the
same harness. Treat a number quoted without its harness as an order of
magnitude, not a measurement — and if you are running the evaluation yourself,
pin the model version, the parameters and the template, and version the whole
thing alongside the code.

## Mental Model

A standardised exam. It measures exam performance, which correlates with
competence until people start studying the exam.

## Example

Benchmarks saturate. MMLU, HumanEval and GSM8K were discriminating in 2022 and
are near-ceiling for frontier models now, so successor benchmarks — harder, more
contamination-resistant, more agentic — appear roughly annually. A model's score
on a saturated benchmark tells you very little.

## Real-World Usage

Model selection, release claims, and internal regression testing. In application
work, a small task-specific evaluation set built from your own traffic is worth
more than any public leaderboard.

## Common Confusions

* **Benchmark vs eval** — used interchangeably; "eval" more often denotes a
  bespoke internal suite, "benchmark" a public shared one.
* **Contamination** — public test sets leak into pretraining corpora, inflating
  scores without capability.
* **Goodhart's law applies without exception** — a benchmark that becomes a
  target stops being a good measure.

## Why Should I Care?

Every model claim you read rests on one, and knowing how they break is what lets
you read release announcements accurately.

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

```text
dataset ──▶ prompt template ──▶ model ──▶ parse ──▶ score ──▶ aggregate
                    ▲
      every one of these choices changes the number
```

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

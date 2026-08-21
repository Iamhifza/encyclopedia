---
term: Evaluation Harness
aliases: [Eval Harness, Eval Suite, Eval-Driven Development]
category: evaluation-safety
subcategory: measurement
status: established
difficulty: intermediate
one_liner: The code that runs a set of test cases against a model or agent and scores the results reproducibly.
origin:
  year: 2021
  circa: true
  attribution: lm-evaluation-harness (EleutherAI) and OpenAI Evals established the pattern
historical_period: foundation-model
tags: [safety, agents]
relations:
  depends_on: [benchmark]
  different_from: [harness]
  used_by: [rlvr, spec-driven-development, ai-workflow]
  related_to: [llm-as-a-judge, guardrails]
prerequisites: [benchmark]
encountered_in: [github, production-systems, job-descriptions]
sources:
  - type: repo
    title: "lm-evaluation-harness"
    url: https://github.com/EleutherAI/lm-evaluation-harness
  - type: repo
    title: "OpenAI Evals"
    url: https://github.com/openai/evals
  - type: repo
    title: "Inspect — an evaluation framework for LLMs"
    url: https://github.com/UKGovernmentBEIS/inspect_ai
updated: 2026-08-21
---

## Simple Explanation

An evaluation is only useful if you can run it again, the same way, after every
change. The harness is the plumbing: load the cases, format the prompts, call the
model, parse the output, score it, and report the number next to the last one.

## Technical Definition

Infrastructure for reproducible evaluation: dataset loading, prompt templating,
model invocation with pinned parameters, output parsing, scoring (exact match,
programmatic checks, or model-graded), aggregation with confidence intervals, and
result versioning. Agent evaluation adds sandboxed environments, tool mocking,
step budgets and trajectory scoring.

## Why Does It Exist?

Because informal testing does not detect regressions. Prompt changes that look
harmless routinely break cases that used to pass, and without a harness nobody
finds out until users do.

## What Problem Does It Solve?

Reproducibility and regression detection — the difference between an evaluation
number and an evaluation practice.

## How Does It Work?

```text
cases.jsonl ──▶ template ──▶ model (pinned params) ──▶ parse ──▶ score
                                                                  │
                          report vs baseline; fail CI on regression
```

## Mental Model

A test suite for something non-deterministic: run it many times, compare
distributions rather than single results, and treat a drop as a bug.

## Example

Eval-driven development inverts the usual order: before writing the prompt or the
pipeline, collect twenty real failing examples and write the scorer. Then every
change is measured. Teams that do this ship LLM features noticeably faster than
teams that iterate by impression.

## Real-World Usage

Public harnesses for benchmark comparison; bespoke internal suites built from
production traffic for application work; agent-specific harnesses with sandboxes
and trajectory analysis.

## Common Confusions

* **Evaluation harness vs agent harness** — the same word, opposite objects. This
  one *measures* a system; the other *runs* one. In evaluation contexts, "harness"
  almost always means this.
* **Public benchmarks are not your evaluation** — they measure general capability,
  not your task.
* **Small suites are fine** — fifty well-chosen cases from real traffic beat five
  thousand synthetic ones.

## Why Should I Care?

It is the difference between believing your system improved and knowing it did,
and it is the first thing missing from LLM projects that stall.

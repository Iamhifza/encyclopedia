---
term: Evaluation Harness
aliases: [Eval Harness, Eval Suite, Eval-Driven Development, Evaluation Suite]
category: evaluation-safety
subcategory: measurement
depth: full
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
  depends_on: [benchmark, llm-as-a-judge]
  different_from: [harness]
  used_by: [rlvr, spec-driven-development, ai-workflow, ai-agent, red-teaming]
  related_to: [guardrails, observability, drift, benchmark-contamination, sycophancy]
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
  - type: paper
    title: "Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena"
    url: https://arxiv.org/abs/2306.05685
    year: 2023
updated: 2026-08-22
review_by: 2027-02-01
---

## Simple Explanation

An evaluation is only useful if you can run it again, the same way, after every
change. The harness is the plumbing: load the cases, format the prompts, call the
model with pinned settings, parse the output, score it, and put the number next
to last week's.

It sounds like infrastructure because it is. It is also, repeatedly, the thing
separating teams who ship LLM features from teams who have been almost finished
for three months.

## Technical Definition

Infrastructure for reproducible evaluation: dataset loading, prompt templating,
model invocation with pinned parameters and model version, output parsing,
scoring (exact match, programmatic checks, or [model-graded](llm-as-a-judge.md)),
aggregation with uncertainty, and result versioning. Agent evaluation adds
sandboxed environments, tool mocking, step budgets and trajectory scoring.

## Why Does It Exist?

Because informal testing does not detect regressions in a non-deterministic
system. A prompt change that looks harmless routinely breaks cases that used to
pass, and without a harness nobody finds out until users do — or until
[drift](drift.md) has been degrading quality for a month with no alert.

## What Problem Does It Solve?

Reproducibility and regression detection: the difference between an evaluation
*number* and an evaluation *practice*.

## How Does It Work?

```text
cases.jsonl ──▶ template ──▶ model (pinned version, pinned params)
                                 │
                              parse
                                 │
                    ┌────────────┼────────────┐
            exact match   programmatic    LLM judge
            (labels)      (tests, schema) (open-ended)
                    └────────────┼────────────┘
                                 ▼
                   aggregate · compare to baseline
                                 │
                    fail CI on regression · chart over time
```

Three scorer types, chosen by what the task admits. Prefer them in that order:
exact match where a label exists, a program where correctness is checkable, a
[judge](llm-as-a-judge.md) only when neither applies — because a judge is itself
a model with biases and needs validating against human labels.

## Mental Model

A test suite for something non-deterministic. You run it many times, compare
distributions rather than single results, and treat a drop as a bug rather than
as noise.

## Example

**Eval-driven development** inverts the usual order. Before writing the prompt or
the pipeline, collect twenty real failing examples and write the scorer. Then
every subsequent change is measured rather than felt.

Fifty well-chosen cases from your own production traffic beat five thousand
synthetic ones, and beat any public leaderboard outright — public benchmarks
measure general capability, not your task, and are prone to
[contamination](benchmark-contamination.md). Your [traces](observability.md) are
the best source of cases you have, because they are real failures rather than
imagined ones.

Two practical details that decide whether the suite is trustworthy:

* **Pin the model version.** Providers update models behind stable API names. An
  unpinned baseline silently stops being a baseline.
* **Run each case several times.** At temperature above zero a single run tells
  you little; report a pass rate, not a pass.

## Real-World Usage

Public harnesses for benchmark comparison; bespoke internal suites built from
production traffic for application work; agent-specific harnesses with sandboxes
and trajectory analysis. Increasingly a CI job that fails a pull request on
regression, which is the point at which evaluation stops being a report and
starts being a gate.

It also underpins training: [RLVR](rlvr.md) is, structurally, an evaluation
harness whose scores are fed back as reward, and
[red teaming](red-teaming.md) findings become regression cases here.

## Common Confusions

* **Evaluation harness vs agent harness** — the same word, opposite objects. One
  *measures* a system; the [other](harness.md) *runs* one. In evaluation contexts
  it always means this. See
  [Harness vs Scaffold](../compare/harness-vs-scaffold.md).
* **Public benchmarks are not your evaluation** — they measure general
  capability. Yours measures your task.
* **A judge is not ground truth** — validate it against human labels on a sample,
  and re-validate when you change judge model or rubric.
* **Scores are not comparable across changes to the harness** — change the
  template, the parser or the judge and you have reset your baseline.

## Why Should I Care?

Almost every other entry in this domain eventually points here.
[Drift](drift.md) is undetectable without it. [Guardrails](guardrails.md) cannot
be tuned without measuring both error types. Claims about
[model routing](model-routing.md), [quantisation](quantization.md) or a new
prompt are unfalsifiable without it.

It is the first thing missing from LLM projects that stall, and the least
glamorous thing to build.

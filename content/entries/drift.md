---
term: Drift
aliases: [Model Drift, Data Drift, Concept Drift, Silent Regression]
category: evaluation-safety
subcategory: operations
depth: full
status: established
difficulty: intermediate
one_liner: "A system quietly getting worse over time because the world, the data or the model behind an API changed."
tags: [safety]
relations:
  related_to: [observability, evaluation-harness, benchmark, llm-as-a-judge]
prerequisites: [evaluation-harness]
encountered_in: [production-systems, job-descriptions, technical-blogs]
sources:
  - type: paper
    title: "Learning under Concept Drift: A Review"
    url: https://arxiv.org/abs/2004.05785
    year: 2020
  - type: paper
    title: "How Is ChatGPT's Behavior Changing over Time?"
    url: https://arxiv.org/abs/2307.09009
    year: 2023
updated: 2026-08-21
---

## Simple Explanation

Nothing breaks. No exception is raised, no alert fires, the latency graph is
flat. The system is simply less good than it was three months ago, and nobody can
say when it started.

Drift is the failure mode with no error message, and it is why the discipline of
LLM operations is mostly about measurement rather than monitoring.

## Technical Definition

Degradation of deployed performance over time from changes in the input
distribution (*data drift*), in the relationship between inputs and correct
outputs (*concept drift*), or in the system itself — a provider updating a model
behind a stable API endpoint, which is specific to the LLM era.

## Why Does It Exist?

Models are fixed; the world is not. Vocabulary shifts, products change, user
behaviour adapts to the tool, and upstream dependencies move. A system tuned to
last year's distribution is being evaluated against this year's.

## What Problem Does It Solve?

Nothing — it is the reason evaluation must be continuous rather than a
pre-launch gate.

## How Does It Work?

```text
quality
   │████████████▇▇▇▆▆▆▅▅▅▄▄▄
   │            ▲        ▲
   │      provider       users started
   │   updated model     asking differently
   └──────────────────────────────▶ time

no errors · no alerts · latency unchanged
```

## Mental Model

A clock losing two seconds a day. Correct this morning, obviously wrong next
month, and no single moment when it broke.

## Example

The version most specific to this field: a provider ships a new model version
behind the same API name. Your prompts were tuned against the old one. Output
format shifts subtly, a few edge cases change, and your downstream parser starts
failing on 2% of requests. Pinning model versions where the provider allows it,
and re-running your evaluation suite when they do not, is the only defence.

## Real-World Usage

Detection in practice: run a fixed evaluation set on a schedule and track the
score; monitor output distributions (length, refusal rate, format conformance)
for step changes; sample production traces for human review; watch user-side
signals like retry rate and thumbs-down. The point is that all of these are
*measurements you must set up*, because nothing fails loudly.

## Common Confusions

* **Drift vs a bug** — a bug is present from the moment it ships. Drift is
  degradation of something that used to work, which makes it far harder to
  attribute.
* **Data drift vs concept drift** — the inputs changed, versus what counts as a
  correct answer changed. The second is worse: your labelled evaluation set is
  now wrong too.
* **Pinning versions is not sufficient** — it stops provider-side change, not
  the world changing around you.

## Why Should I Care?

It is the reason an evaluation harness is infrastructure rather than a
launch-week task. Without a scheduled measurement you will find out about drift
from a user complaint, months late, with no way to tell when it began.

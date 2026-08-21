---
term: Frontier Model
aliases: [Frontier AI, State-of-the-Art Model]
category: industry-culture
subcategory: model-economy
status: contested
disputed: true
difficulty: beginner
one_liner: A model at the current capability edge — a term used both as a policy category and as a marketing claim.
origin:
  year: 2023
  attribution: Popularised through 2023 AI governance discussions and the "Frontier Model Forum"
historical_period: agentic
tags: [culture, safety]
relations:
  is_a: [foundation-model]
  different_from: [open-weight-model]
  related_to: [scaling-laws, benchmark, alignment]
prerequisites: [foundation-model]
encountered_in: [social-media, conferences, job-descriptions, standards]
sources:
  - type: paper
    title: "Frontier AI Regulation: Managing Emerging Risks to Public Safety"
    url: https://arxiv.org/abs/2307.03718
    year: 2023
updated: 2026-08-21
review_by: 2026-12-01
---

## Simple Explanation

The most capable models anyone has built at a given moment. Because that set
changes every few months, the label is a moving target — and because it sounds
impressive, it is applied liberally.

## Technical Definition

In policy usage: highly capable general-purpose models that could pose severe
risks to public safety, sometimes operationalised by training-compute thresholds
because compute is measurable and capability is not. In common usage: whichever
models are currently near the top of general capability evaluations.

## Why Does It Exist?

Regulators needed a category that captures "the models we are worried about"
without naming vendors, and without being obsoleted by the next release.

## What Problem Does It Solve?

It gives governance frameworks a scope, and it gives the industry shorthand for
the leading tier.

## Terminology Note

Genuinely contested, in a way that matters:

* **Policy definition** — tied to capability or compute thresholds, with
  obligations attached. Thresholds are contested because compute is a poor proxy
  for capability, and improve-by-efficiency progress makes them dated quickly.
* **Marketing definition** — applied by vendors to their own newest release
  regardless of independent evaluation.

When you read "frontier", check whether it carries a threshold, a benchmark
result, or nothing at all.

## How Does It Work?

There is no test that returns *frontier / not frontier*. Proxies used in practice:
training compute, performance on current hard benchmarks, and inclusion in
dangerous-capability evaluation regimes.

## Mental Model

A shoreline, not a landmark. It describes where the water currently reaches, and
it moves.

## Example

A model considered frontier in 2023 is comfortably exceeded today by open-weight
models small enough to run on a laptop. Any statement about frontier capability
needs a date attached.

## Real-World Usage

Regulation and voluntary safety commitments, capability reporting, and vendor
positioning. In job descriptions it usually signals working with the largest
models rather than a defined tier.

## Common Confusions

* **Frontier vs foundation** — capability edge versus reusable base.
* **Frontier vs largest** — parameter count no longer tracks capability.
* **Frontier vs closed** — related in practice, not by definition.

## Why Should I Care?

It is one of the few pieces of AI marketing vocabulary that carries legal weight
in some jurisdictions, so the difference between the two usages is worth keeping
straight.

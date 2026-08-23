---
term: Model Routing
aliases: [Model Router, LLM Routing, Cascading, Request Routing]
category: industry-culture
subcategory: stack
depth: full
status: modern
difficulty: intermediate
one_liner: "Sending each request to the cheapest model that can handle it, and escalating only when it cannot."
historical_period: agentic
tags: [protocol, inference]
relations:
  depends_on: [ai-gateway]
  related_to: [reasoning-model, throughput, evaluation-harness, small-language-model]
prerequisites: [large-language-model]
encountered_in: [production-systems, job-descriptions, technical-blogs]
sources:
  - type: paper
    title: "RouteLLM: Learning to Route LLMs with Preference Data"
    url: https://arxiv.org/abs/2406.18665
    year: 2024
  - type: paper
    title: "FrugalGPT: How to Use Large Language Models While Reducing Cost and Improving Performance"
    url: https://arxiv.org/abs/2305.05176
    year: 2023
updated: 2026-08-21
review_by: 2027-02-01
---

## Simple Explanation

Most requests are easy. Classifying a support ticket does not need the model that
can debug a distributed system, but if you wire your product to one model, every
request pays the top rate. Routing puts a decision in front: try to work out how
hard this request is, and send it somewhere proportionate.

## Technical Definition

A dispatch layer selecting among models per request, using a classifier, a
heuristic, or a cascade that starts cheap and escalates on a confidence or
verification signal. Objective is to minimise cost and latency subject to a
quality floor measured on a representative evaluation set.

## Why Does It Exist?

Capability per token varies by more than an order of magnitude in price, and
request difficulty in a real product is enormously skewed. Paying frontier rates
for the long tail of trivial requests is the single most common source of
avoidable spend in LLM applications.

## What Problem Does It Solve?

Cost and latency, without the blunt alternative of downgrading everyone.

## How Does It Work?

```text
request
   │
   ├─▶ classify difficulty ──┬─▶ small model      (most traffic)
   │   (heuristic, learned,  ├─▶ mid model
   │    or embedding-based)  └─▶ frontier model   (hard, rare)
   │
   └─ OR cascade: try small ──▶ verify ──▶ good enough? ──▶ done
                                    │ no
                                    └──▶ escalate, pay once more
```

The cascade needs no difficulty prediction at all — it substitutes a
*verification* signal, which for code (tests pass) or structured output (schema
validates) is often free and reliable.

## Mental Model

Hospital triage. Not everyone sees the consultant, and the skill is entirely in
the triage nurse. Route badly and you either overspend or send someone serious to
the wrong desk.

## Example

A support assistant where 70% of traffic is FAQ lookups, 25% needs light
reasoning and 5% is genuinely hard. Routing the first bucket to a small model can
cut spend substantially while leaving the hard 5% untouched — and the whole
economic case collapses if the router misclassifies even a small share of hard
requests downward, because those failures are the visible ones.

## Real-World Usage

Implemented in AI gateways, in framework-level routers, and as a built-in feature
of some assistant products that decide when to engage extended thinking.
Reasoning models sharpened the case: their per-request cost is high enough that
routing became a first-class design decision rather than an optimisation.

## Terminology Note

Loosely used. "Routing" covers difficulty-based dispatch, cascading with
escalation, semantic routing to domain-specialised models, and simple failover
between providers when one is down. These have different failure modes; ask
which is meant.

## Common Confusions

* **Routing is not free** — a classifier is itself a model call, and a badly
  built router costs more than it saves. Heuristics on request length, task type
  or user tier often outperform a learned classifier in practice.
* **Routing needs an evaluation set** — without one you cannot know what the
  cheaper model got wrong, and quality regressions from routing are silent by
  construction.
* **Cascades add latency to hard requests** — the escalated request paid for the
  failed attempt first. That trade is fine when hard requests are rare and
  terrible when they are not.

## Why Should I Care?

It is usually the largest lever on unit economics available to an application
team, and it is one of the few places where a measurable evaluation set converts
directly into money.

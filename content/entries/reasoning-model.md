---
term: Reasoning Model
aliases: [Thinking Model, Extended Thinking, Test-Time Compute Scaling, Chain-of-Thought Model]
category: llms-foundation-models
subcategory: capability
status: modern
difficulty: intermediate
one_liner: A language model trained to work through a problem step by step before answering, spending more computation at inference to get better results.
origin:
  year: 2024
  attribution: Popularised by OpenAI's o1 and subsequently DeepSeek-R1, Claude extended thinking and others
historical_period: agentic
tags: [architecture]
relations:
  successor_of: [large-language-model]
  depends_on: [rlvr, autoregressive-generation]
  used_by: [ai-agent, coding-agent]
  related_to: [scaling-laws, inference-latency]
prerequisites: [large-language-model]
encountered_in: [research-papers, production-systems, social-media, documentation]
sources:
  - type: paper
    title: "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models"
    url: https://arxiv.org/abs/2201.11903
    year: 2022
  - type: paper
    title: "DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning"
    url: https://arxiv.org/abs/2501.12948
    year: 2025
  - type: paper
    title: "Scaling LLM Test-Time Compute Optimally"
    url: https://arxiv.org/abs/2408.03314
    year: 2024
updated: 2026-08-21
review_by: 2027-02-01
---

## Simple Explanation

Ordinary models answer immediately. Reasoning models generate a long internal
working-out first — trying approaches, catching their own errors, backtracking —
and only then produce the answer. The thinking costs tokens and time, and on hard
problems it buys a large accuracy gain.

## Technical Definition

A model post-trained, typically with reinforcement learning against verifiable
rewards, to produce extended intermediate reasoning tokens before its final
response. Accuracy scales with reasoning tokens spent, making inference-time
compute a tunable dimension alongside training-time compute.

## Why Does It Exist?

Chain-of-thought prompting showed in 2022 that models reason better when asked to
work step by step. The 2024-25 shift was to train that behaviour in with
reinforcement learning on problems whose answers can be checked automatically —
mathematics, code, formal tasks — rather than eliciting it by prompt.

## What Problem Does It Solve?

Tasks where a single forward pass through a fixed number of layers is simply not
enough computation: multi-step mathematics, competitive programming, debugging,
and planning in agent loops.

## How Does It Work?

```text
prompt ──▶ [ thinking tokens: attempt, check, discard, retry ... ] ──▶ answer
             │                                                          │
             └── often hidden or summarised for the user ───────────────┘

more thinking tokens ──▶ higher accuracy, higher cost, higher latency
```

## Mental Model

Showing your working on an exam, except that the working is where the marks are
actually earned, and you are allowed to cross things out.

## Example

On competition mathematics, reasoning models improved from a few percent to the
majority of problems solved. On simple retrieval or formatting tasks the same
models are slower and no better, which is why routing between fast and thinking
modes has become a standard design decision.

## Real-World Usage

Deployed as separate model variants or as an adjustable thinking budget on the
same model. In agent systems, reasoning models are typically used for planning
and error recovery while cheaper models handle routine steps.

## Common Confusions

* **The reasoning trace is not a faithful log** — it is generated text that
  correlates with, but is not a transcript of, the computation. Interpretability
  research shows models sometimes reach an answer by other means and then
  rationalise.
* **Reasoning model vs chain-of-thought prompting** — the behaviour is trained in
  rather than requested, and is substantially more robust.
* **Not always better** — extra thinking adds cost and latency and can hurt on
  simple tasks, a phenomenon sometimes called overthinking.

## Terminology Note

"Reasoning" here is a term of art for extended intermediate generation, and it
carries connotations the technical meaning does not support. Whether this
constitutes reasoning in a philosophical sense is contested; what is measurable
is that accuracy on verifiable tasks rises with the number of intermediate tokens.

## Why Should I Care?

It opened a second scaling axis. Before 2024, better answers meant training a
bigger model; now they can also mean letting a model think for longer, which
changes cost models, latency budgets and agent design.

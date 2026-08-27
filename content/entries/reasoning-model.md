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
diagram:
  kind: steps
  title: Spend tokens before answering
  footer: 'The scaling knob moved: for these models, more compute at inference buys accuracy in the way
    more compute at training used to. It also makes cost and latency depend on the question rather than
    on the answer''s length.'
  steps:
  - title: Most of the output is not the answer
    visual:
      kind: segments
      width: 720
      label: one response
      caption: the thinking is usually hidden or summarised, and is billed
      segments:
      - text: prompt
        value: 8
      - text: thinking — attempt, check, discard, retry
        value: 76
        tone: accent
      - text: answer
        value: 16
  - title: And it buys accuracy, up to a point
    visual:
      kind: plot
      width: 700
      height: 190
      x_range: [0, 100]
      y_range: [0, 1.05]
      x_label: thinking tokens
      y_label: accuracy
      caption: the curve flattens, and every token on it costs money and latency
      curves:
      - label: accuracy
        tone: accent
        points: [[0.0, 0.3], [2.5, 0.367], [5.0, 0.426], [7.5, 0.479], [10.0, 0.526], [12.5, 0.569], [
            15.0, 0.606], [17.5, 0.64], [20.0, 0.67], [22.5, 0.697], [25.0, 0.721], [27.5, 0.742], [30.0,
            0.761], [32.5, 0.778], [35.0, 0.794], [37.5, 0.807], [40.0, 0.819], [42.5, 0.83], [45.0, 0.84],
          [47.5, 0.848], [50.0, 0.856], [52.5, 0.863], [55.0, 0.869], [57.5, 0.875], [60.0, 0.879], [
            62.5, 0.884], [65.0, 0.888], [67.5, 0.891], [70.0, 0.894], [72.5, 0.897], [75.0, 0.899], [
            77.5, 0.902], [80.0, 0.904], [82.5, 0.905], [85.0, 0.907], [87.5, 0.908], [90.0, 0.91], [
            92.5, 0.911], [95.0, 0.912], [97.5, 0.913], [100.0, 0.913]]
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


The model is trained — usually with reinforcement learning against verifiable
answers — to produce an extended chain of intermediate tokens before committing
to a response. Within that chain it attempts approaches, checks them, discards
what fails, and tries again. The user typically sees a summary, or nothing, but
the tokens are generated and billed.

What changed is where the scaling knob sits. For most of the field's history,
accuracy came from more compute at training time. For these models it also comes
from more compute at inference time: allow more thinking tokens and accuracy
rises, along a curve that flattens. The trade is explicit rather than hidden.

Which makes them a different economic proposition. Cost and latency now depend on
how hard the question is rather than on how long the answer is, and a
straightforward request can cost many times what a non-reasoning model would
charge for the same output. The strength is real on maths, code and multi-step
logic — where the verifier that trained them exists — and much less clear
elsewhere.

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

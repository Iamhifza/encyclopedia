---
term: Chain-of-Thought
aliases: [CoT, Step-by-Step Reasoning, Scratchpad, Let's Think Step by Step]
category: llms-foundation-models
subcategory: capability
depth: full
status: established
difficulty: beginner
one_liner: "Asking a model to work through its reasoning before answering, which measurably improves accuracy on multi-step problems."
origin:
  year: 2022
  attribution: Wei et al. at Google; the zero-shot variant by Kojima et al. the same year
historical_period: foundation-model
tags: [architecture]
relations:
  evolved_into: [reasoning-model]
  used_by: [prompt-engineering, agent-loop]
  related_to: [mechanistic-interpretability, explainability, sampling]
prerequisites: [large-language-model, prompt-engineering]
encountered_in: [research-papers, documentation, social-media, interviews]
sources:
  - type: paper
    title: "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models"
    url: https://arxiv.org/abs/2201.11903
    year: 2022
  - type: paper
    title: "Large Language Models are Zero-Shot Reasoners"
    url: https://arxiv.org/abs/2205.11916
    year: 2022
  - type: paper
    title: "Measuring Faithfulness in Chain-of-Thought Reasoning"
    url: https://arxiv.org/abs/2307.13702
    year: 2023
updated: 2026-08-21
---

## Simple Explanation

Ask a model for the answer and it commits immediately — one forward pass, one
shot. Ask it to work through the problem first, and accuracy on multi-step
questions rises substantially.

There is a mechanical reason this works. Each generated token is another forward
pass, and the intermediate text is visible to every subsequent one. Reasoning
aloud gives the model both more computation and a place to keep its working.

## Technical Definition

A prompting technique eliciting intermediate reasoning tokens before a final
answer, either by demonstrating worked examples (few-shot CoT) or by instruction
alone (zero-shot CoT, canonically *"Let's think step by step"*). The intermediate
tokens condition all subsequent generation, effectively converting a fixed-depth
computation into a variable-length one.

## Why Does It Exist?

A Transformer applies a fixed number of layers per token. Some problems require
more sequential steps than the architecture provides in one pass. Generating
intermediate tokens is the only way for the model to spend more computation on a
harder problem — and the only way for it to store a partial result.

## What Problem Does It Solve?

Multi-step arithmetic, logical deduction, and any task where a single leap to the
answer is unreliable but a sequence of small steps is not.

## How Does It Work?

```text
DIRECT
  Q: 23 apples, used 8, bought 12 more. How many?
  A: 27                                   ← one pass, often wrong

CHAIN-OF-THOUGHT
  Q: ...
  A: Started with 23. Used 8, leaving 15.
     Bought 12 more, so 15 + 12 = 27.
     The answer is 27.                    ← each step conditions the next
```

## Mental Model

Working on paper rather than in your head. The paper is not just a record — it is
extra memory, and it stops errors compounding invisibly.

## Example

The original result was striking: on grade-school maths word problems, CoT
prompting roughly tripled accuracy on large models. Equally important was a
negative finding — the benefit appeared only above a certain model scale, and
smaller models produced fluent reasoning chains leading to wrong answers.

## Real-World Usage

Largely absorbed into training. Reasoning models are post-trained to do this by
default and far more robustly than prompting achieved, so explicitly asking for
step-by-step reasoning matters less than it did in 2023. It remains useful with
non-reasoning models, and its descendants — self-consistency (sample several
chains, take the majority answer), tree-of-thought, and reflection loops — are
still active techniques.

## Common Confusions

* **The chain is not necessarily faithful** — this is the important one.
  Measurement shows models sometimes reach an answer by other means and then
  produce a plausible justification. The stated reasoning is generated text, not
  a log of computation, which limits how much you can trust it as an explanation.
* **CoT vs reasoning model** — a prompting technique versus a trained behaviour.
  The second is more reliable and does not need asking for.
* **It costs tokens and latency** — reasoning is generated output, billed and
  waited for. On simple tasks it is pure overhead.

## Why Should I Care?

It was the observation that intermediate tokens are computation, not decoration —
and that observation led directly to reasoning models and to inference-time
compute becoming a scaling axis of its own.

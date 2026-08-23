---
term: Large Language Model
aliases: [LLM, Large Language Models]
category: llms-foundation-models
subcategory: models
depth: full
status: established
difficulty: beginner
one_liner: A very large Transformer trained on enormous amounts of text to predict the next token, which turns out to make it broadly capable.
origin:
  year: 2020
  circa: true
  attribution: The term became standard around GPT-3; the underlying recipe dates to GPT-2 (2019)
historical_period: foundation-model
tags: [architecture]
relations:
  is_a: [foundation-model]
  successor_of: [transformer]
  depends_on: [pretraining, tokenization, next-token-prediction, scaling-laws]
  used_by: [ai-agent, rag, coding-agent, vision-language-model]
  evolved_into: [reasoning-model]
  related_to: [context-window, base-model, small-language-model, hallucination, inference-latency]
prerequisites: [transformer]
encountered_in: [research-papers, job-descriptions, production-systems, social-media]
sources:
  - type: paper
    title: "Language Models are Few-Shot Learners (GPT-3)"
    url: https://arxiv.org/abs/2005.14165
    year: 2020
  - type: report
    title: "On the Opportunities and Risks of Foundation Models"
    url: https://arxiv.org/abs/2108.07258
    year: 2021
  - type: report
    title: "The Llama 3 Herd of Models"
    url: https://arxiv.org/abs/2407.21783
    year: 2024
    note: The most detailed public account of how one is actually built.
updated: 2026-08-22
---

## Simple Explanation

Train a big enough next-token predictor on a big enough pile of text and it stops
being merely a text predictor. To predict what comes next across the whole
internet, it has to pick up grammar, facts, reasoning patterns, code semantics,
translation and style — not because anyone asked it to, but because all of those
help with the prediction.

Capability arrives as a side effect of compression. That is the single most
important and least intuitive fact about these systems, and nearly everything
strange about them follows from it.

## Technical Definition

A decoder-only [Transformer](transformer.md) with billions to trillions of
parameters, pretrained by [next-token prediction](next-token-prediction.md) on
trillions of tokens, then adapted by
[supervised fine-tuning](supervised-fine-tuning.md) and preference optimisation
([RLHF](rlhf.md), [DPO](dpo.md) or their descendants). Behaviour is elicited at
inference time by conditioning on context rather than by changing weights.

## Why Does It Exist?

[Scaling laws](scaling-laws.md) showed that loss falls predictably with model
size, data and compute. That predictability turned capability from a research
gamble into an engineering roadmap — you could forecast what a larger run would
produce before spending the money — and the industry followed the curve.

## What Problem Does It Solve?

Task generality. Instead of one model per task, each with its own labelled
dataset and training run, one model handles translation, summarisation,
extraction, classification, code and dialogue, specified in natural language at
run time.

## How Does It Work?

```text
PRETRAIN   trillions of tokens ──▶ next-token prediction ──▶ base model
             │ data curation, mixture weights, annealing
             │ months, thousands of GPUs

ADAPT      demonstrations ──▶ SFT ──▶ preferences ──▶ RLHF / DPO ──▶ assistant
             │ days, orders of magnitude less compute
             │ this stage produces almost everything you notice

SERVE      prompt + context ──▶ prefill ──▶ decode ──▶ streamed tokens
             │ nothing is learned here; weights are frozen
```

The three stages differ enormously in cost and in what they contribute.
Pretraining supplies the knowledge and capability. Post-training supplies the
behaviour — the helpfulness, the format, the refusals, and the tics people
complain about. Serving supplies nothing except the context you provide.

**Nothing in a served model is updated by your conversation.** Everything it
appears to know about you lives in the [context window](context-window.md), and
is gone when the request ends.

## Mental Model

An extremely well-read improviser with no memory between performances, who is
handed a briefing note before each one. The quality of the performance depends
enormously on the briefing — which is why
[context engineering](context-engineering.md) turned out to matter as much as it
does.

## Example

GPT-3 in 2020: 175 billion parameters, roughly 300 billion training tokens. Its
significance was not the size but the demonstration that a model could be
instructed by example alone — [few-shot learning](few-shot-learning.md) — with no
task-specific training. That observation created prompt engineering as a
practice and is the reason "just describe what you want" became a viable
interface.

What has changed since is instructive. Models are no longer scaled by parameters
alone: [Chinchilla](scaling-laws.md) showed that parameters and tokens should grow
together, and inference economics then pushed further, so current models are
often *smaller* than GPT-3 and trained on twenty times more data. Parameter count
has become a poor proxy for capability, especially with
[mixture-of-experts](mixture-of-experts.md) models where total and active
parameters differ by an order of magnitude.

## Real-World Usage

Chat assistants, [coding agents](coding-agent.md), extraction pipelines,
classification, translation, and as the reasoning core inside
[agent](ai-agent.md) systems. In production an LLM is rarely used alone: it sits
behind [retrieval](rag.md), [tools](tool-calling.md),
[guardrails](guardrails.md) and an [evaluation harness](evaluation-harness.md),
and most of the engineering effort goes into those rather than into the model.

## Common Confusions

* **LLM vs Transformer** — the architecture versus a very large instance of it.
* **LLM vs chatbot** — the chatbot is a product surface; the LLM is one component
  of it. See [Agent vs Chatbot](../compare/agent-vs-chatbot.md).
* **"It looks things up"** — a [base model](base-model.md) has no store to look
  in. Facts are distributed across weights, which is why they are unreliable and
  why [retrieval](rag.md) exists.
* **Parameters as capability** — data quality, token count and post-training now
  matter at least as much, and with MoE the headline number can mislead by 10×.
* **It does not plan the sentence** — it commits one token at a time. Apparent
  planning comes from conditioning on its own output, which is precisely why
  [chain-of-thought](chain-of-thought.md) works.
* **The knowledge cutoff is structural** — weights are frozen after training, and
  [continual learning](continual-learning.md) does not yet work at this scale.
  Retrieval is the workaround, not a stopgap.

## Why Should I Care?

It is the component every other term in the modern half of this encyclopedia is
positioned around: what feeds it, what constrains it, what it calls, how it is
served, and how you know it worked. If you read one entry before the rest, read
this one and then [Transformer](transformer.md).

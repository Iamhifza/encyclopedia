---
term: Large Language Model
aliases: [LLM, Large Language Models]
category: llms-foundation-models
subcategory: models
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
  depends_on: [pretraining, tokenization]
  used_by: [ai-agent, rag, coding-agent]
  evolved_into: [reasoning-model]
prerequisites: [transformer]
encountered_in: [research-papers, job-descriptions, production-systems, social-media]
sources:
  - type: paper
    title: "Language Models are Few-Shot Learners (GPT-3)"
    url: https://arxiv.org/abs/2005.14165
    year: 2020
  - type: paper
    title: "On the Opportunities and Risks of Foundation Models"
    url: https://arxiv.org/abs/2108.07258
    year: 2021
updated: 2026-08-21
---

## Simple Explanation

Train a big enough next-token predictor on a big enough pile of text and it stops
being merely a text predictor. To predict the next token well across the whole
internet, it has to pick up grammar, facts, reasoning patterns, code semantics
and style. Capability arrives as a side effect of compression.

## Technical Definition

A decoder-only Transformer with billions to trillions of parameters, pretrained
by next-token prediction on trillions of tokens, then typically adapted by
supervised fine-tuning and preference optimisation. Behaviour is elicited at
inference time by conditioning on context rather than by changing weights.

## Why Does It Exist?

Scaling laws showed that loss falls predictably with model size, data and
compute. That predictability turned capability into an engineering roadmap rather
than a research gamble, and the industry followed it.

## What Problem Does It Solve?

Task generality. Instead of one model per task with its own labelled dataset, one
model serves translation, summarisation, code, extraction and dialogue, specified
in natural language at run time.

## How Does It Work?

```text
PRETRAIN   trillions of tokens ──▶ next-token prediction ──▶ base model
ADAPT      demonstrations ──▶ SFT ──▶ preferences ──▶ RLHF/DPO ──▶ assistant
SERVE      prompt + context ──▶ prefill ──▶ decode ──▶ streamed tokens
```

Nothing in the served model is updated by your conversation. Everything the model
"knows about you" lives in the context window.

## Mental Model

An extremely well-read improviser with no memory between performances, who is
handed a briefing note (the context) before each one.

## Example

GPT-3 in 2020: 175B parameters, ~300B training tokens. It demonstrated that a
model could be instructed by example alone, without task-specific fine-tuning —
the observation that launched prompt engineering as a practice.

## Real-World Usage

Chat assistants, coding agents, extraction pipelines, classification, translation
and as the reasoning core inside agent systems. In production, an LLM is rarely
used alone: it sits behind retrieval, tools, guardrails and evaluation.

## Common Confusions

* **LLM vs Transformer** — the architecture versus a very large instance of it.
* **LLM vs chatbot** — the chatbot is a product surface; the LLM is one component
  of it.
* **"It looks things up"** — a base model has no store to look in. Facts are
  distributed across weights, which is why they are unreliable and why retrieval
  exists.
* **Parameters as capability** — training data quality, token count and
  post-training now matter at least as much as parameter count.

## Why Should I Care?

It is the component every other term in the modern half of this encyclopedia is
positioned around: what feeds it, what constrains it, what it calls, and how you
know it worked.

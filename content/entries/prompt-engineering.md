---
term: Prompt Engineering
aliases: [Prompting, Prompt Design]
category: agent-engineering
subcategory: context
status: established
difficulty: beginner
one_liner: Writing the instructions given to a model so that it reliably does what you meant.
origin:
  year: 2020
  attribution: Emerged with GPT-3's few-shot prompting; the term spread through 2021-2022
historical_period: foundation-model
diagram:
  kind: figure
  section: Evolution
  title: The scope kept widening, and the name kept changing
  visual:
    kind: lineage
    per_row: 4
    caption: each stage absorbed the last rather than replacing it — you still write the prompt, it is
      just no longer the whole job
    milestones:
    - text: prompt engineering
      note: phrasing one request
    - text: context engineering
      note: what is in the window
    - text: agent scaffolding
      note: tools and a loop
    - text: harness engineering
      note: everything around the model
      tone: accent
tags: [agents, culture]
relations:
  evolved_into: [context-engineering]
  different_from: [context-engineering, scaffold]
  used_by: [ai-agent, tool-calling]
  related_to: [sampling, reasoning-model]
prerequisites: [large-language-model]
encountered_in: [documentation, job-descriptions, social-media, production-systems]
sources:
  - type: paper
    title: "Language Models are Few-Shot Learners"
    url: https://arxiv.org/abs/2005.14165
    year: 2020
  - type: paper
    title: "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models"
    url: https://arxiv.org/abs/2201.11903
    year: 2022
  - type: docs
    title: "Anthropic — prompt engineering overview"
    url: https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/overview
updated: 2026-08-21
---

## Simple Explanation

The model does exactly what the text in front of it suggests. Change the text and
the behaviour changes. Prompt engineering is the practice of finding the wording,
structure and examples that get reliable results — and, increasingly, of
measuring rather than guessing.

## Technical Definition

Systematic design of model inputs — instructions, role framing, output format
specifications, few-shot exemplars, and reasoning elicitation — evaluated against
a held-out task set rather than by impression.

## Why Does It Exist?

GPT-3 showed that a model could be steered to new tasks by conditioning alone,
with no gradient updates. That made input text the primary control surface for a
frozen model, and turned wording into an engineering variable.

## What Problem Does It Solve?

Behaviour specification without training: format adherence, tone, task framing,
and reliability on edge cases.

## How Does It Work?

The techniques that survive scrutiny are unglamorous: state the task explicitly,
show two or three examples of the exact output format, specify what to do when
the input is unexpected, ask for reasoning before the answer where the task is
hard, and put stable instructions early so they can be cache-hit. Then evaluate
on real examples and keep the version that wins.

## Mental Model

A specification handed to a competent contractor who will follow it literally,
including its ambiguities.

## Example

"Summarise this" produces inconsistent length, register and structure. "Summarise
this support ticket in three bullet points for an engineer, naming the affected
component and the customer's stated impact; if the component is not stated, write
UNKNOWN" produces something a downstream system can parse. The second is not
cleverer, it is more specified.

## Real-World Usage

Every LLM application. It briefly became a job title in 2022-23; that framing has
largely faded, absorbed into AI engineering and into the broader practice of
context engineering, as prompts became one component of a much larger assembly.

## Evolution

Whether this chain is genuine technical evolution or largely renaming is a fair
question, and the honest answer is: partly both. What changed materially is
*scope*. In 2022 the object of design was one string. By 2025 it was everything
entering the context window — retrieved documents, tool results, memory,
compaction policy — assembled dynamically at run time. That is a real expansion
of the problem, not just a new label. What has *not* changed is the underlying
mechanism: you are still deciding what tokens the model sees. Treat the newer
terms as marking scope, and be sceptical when they are presented as new science.

## Common Confusions

* **Prompt engineering vs context engineering** — one string, hand-written,
  versus the whole context window, assembled at run time.
* **"Prompt engineering is dead"** — regularly announced, consistently wrong. It
  became a component of a larger practice.
* **Tricks versus specification** — magic phrases circulate and mostly do not
  survive measurement. Clear specification does.

## Why Should I Care?

It remains the cheapest and fastest way to change model behaviour, and it is
where every debugging session should start before anyone proposes fine-tuning.

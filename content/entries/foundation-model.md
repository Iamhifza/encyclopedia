---
term: Foundation Model
aliases: [Pretrained Model]
category: llms-foundation-models
subcategory: models
status: established
difficulty: beginner
one_liner: A large model pretrained on broad data that serves as a reusable base for many downstream tasks instead of being built for one.
origin:
  year: 2021
  attribution: Coined by the Stanford Center for Research on Foundation Models
historical_period: foundation-model
diagram:
  kind: figure
  title: Train once, adapt many times
  footer: 'The economics are the definition: one enormous training run, amortised across everything built
    on top. It also centralises risk — a flaw in the base propagates to every system downstream of it.'
  visual:
    kind: fan
    source: base model
    caption: in rough order of cost, and of how much they can change behaviour
    targets:
    - prompting
    - retrieval
    - text: fine-tuning
      new: true
    - agent scaffolding
tags: [architecture]
relations:
  used_by: [large-language-model, vision-language-model]
  related_to: [scaling-laws, frontier-model, open-weight-model]
  different_from: [world-model]
prerequisites: [pretraining]
encountered_in: [research-papers, job-descriptions, conferences]
sources:
  - type: report
    title: "On the Opportunities and Risks of Foundation Models"
    url: https://arxiv.org/abs/2108.07258
    year: 2021
updated: 2026-08-21
---

## Simple Explanation

Instead of training a new model for every job, train one enormous general model
and adapt it. The general model is the foundation; everything else is built on
top by fine-tuning, prompting or wrapping it in a system.

## Technical Definition

A model trained on broad data at scale, typically with self-supervised
objectives, designed to be adapted to a wide range of downstream tasks. The
defining properties named by the original report are emergence (capabilities not
explicitly trained for) and homogenisation (many applications inheriting the
behaviour, and the flaws, of a few base models).

## Why Does It Exist?

The term was coined to name a shift in how AI systems get built, and to argue
that the shift has consequences — technical, economic and social — that "large
language model" does not capture, since the pattern also covers vision, audio,
code and biology.

## What Problem Does It Solve?

Duplicated effort. Pretraining is the expensive part; sharing that cost across
thousands of applications is what made deployment economical.

## How Does It Work?


Train one model on a very large, broad corpus with a self-supervised objective,
then adapt it to many specific tasks rather than training a separate model for
each. The training run is enormous and happens once; everything downstream reuses
it.

Adaptation ranges from free to expensive. Prompting and in-context learning
change nothing about the weights. Retrieval augments the input with material the
model was never trained on. Fine-tuning — full, or parameter-efficient like LoRA
— changes behaviour durably. Agent scaffolding wraps the model in tools and a
loop. Most production systems combine several.

The economics are the definition: a capability expensive enough that nobody
builds it twice, amortised across everything on top. That concentration is also
the risk. A bias, a gap or a vulnerability in the base model propagates to every
system built on it, and the people building those systems generally cannot
inspect what they inherited.

## Mental Model

A general education followed by an apprenticeship, rather than being trained from
birth for one trade.

## Example

One base model becomes a customer support assistant through prompting, a legal
summariser through fine-tuning, and a coding agent through tools and scaffolding
— with no change to the underlying weights in two of those three cases.

## Real-World Usage

The standard build pattern: start from a foundation model, add retrieval, add
tools, evaluate, and only fine-tune when prompting and retrieval have measurably
failed.

## Common Confusions

* **Foundation model vs LLM** — LLMs are the text-centred subset. Vision and
  multimodal foundation models exist too.
* **Foundation model vs base model** — in practice "base model" usually means the
  pretrained checkpoint before instruction tuning, while "foundation model" refers
  to the role it plays.
* **Foundation vs frontier** — frontier is about being at the capability edge;
  foundation is about being a reusable base.

## Why Should I Care?

Homogenisation means a bug, bias or weakness in one base model propagates to
every product built on it — which is exactly why evaluation belongs to whoever
ships the application, not only to whoever trained the model.

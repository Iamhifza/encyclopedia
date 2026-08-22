---
term: Base Model
aliases: [Pretrained Checkpoint, Completion Model, Foundation Checkpoint]
category: llms-foundation-models
subcategory: models
depth: full
status: established
difficulty: beginner
one_liner: "The raw model straight out of pretraining, which continues text rather than following instructions."
tags: [architecture]
relations:
  part_of: [pretraining]
  evolved_into: [supervised-fine-tuning]
  different_from: [large-language-model]
  related_to: [open-weight-model, rlhf, few-shot-learning]
prerequisites: [pretraining]
encountered_in: [github, research-papers, production-systems]
sources:
  - type: paper
    title: "Language Models are Few-Shot Learners (GPT-3)"
    url: https://arxiv.org/abs/2005.14165
    year: 2020
  - type: paper
    title: "Training Language Models to Follow Instructions with Human Feedback"
    url: https://arxiv.org/abs/2203.02155
    year: 2022
updated: 2026-08-21
---

## Simple Explanation

Give a base model "Write a poem about rain" and it might well reply "Write a poem
about snow. Write a poem about autumn." It is not being obtuse. It has learned
what typically follows text on the internet, and a list of prompts often follows
a prompt.

The base model is the pretrained checkpoint before anyone taught it that a
request should be answered. All the knowledge is there; the disposition to be
helpful is not.

## Technical Definition

The output of the pretraining stage: a next-token predictor over a large corpus,
with no supervised fine-tuning, instruction tuning or preference optimisation
applied. It models the distribution of its training text rather than the
behaviour of an assistant.

## Why Does It Exist?

It is simply the natural stopping point of pretraining — the artefact before
adaptation. It has independent value because everything downstream starts here,
and because different post-training produces different assistants from the same
base.

## What Problem Does It Solve?

It separates the expensive, general stage from the cheap, specific one. One base
model can become a chat assistant, a code assistant, a domain specialist and a
research artefact, without repeating the pretraining run.

## How Does It Work?

```text
base model behaviour: continue the text
  "The capital of France is"        →  " Paris, and its population..."   ✓
  "Write a poem about rain"          →  " Write a poem about snow..."     ✗

steer it with the format instead of an instruction:
  "Q: What is the capital of France?
   A: Paris
   Q: What is the capital of Japan?
   A:"                               →  " Tokyo"                          ✓
```

That second pattern is few-shot prompting, and it is how base models were
actually used before instruction tuning existed.

## Mental Model

Someone who has read the entire library and has not been told they are now at an
information desk. Enormously knowledgeable, and not answering your question.

## Example

The base-versus-instruct distinction is a common early mistake. Downloading a
model whose name lacks `-instruct` or `-chat`, wiring it to a chat interface, and
finding it rambles, continues the user's sentence, or never stops generating — all
symptoms of using a base model as an assistant.

## Real-World Usage

Base models are released alongside instruct variants for a reason. Researchers
prefer them because post-training obscures what pretraining learned. Teams
building specialised assistants sometimes start from base and apply their own
fine-tuning, avoiding inherited style and refusal behaviour. And they are the
starting point for continued pretraining on a domain corpus.

## Common Confusions

* **Base model vs foundation model** — the first is a checkpoint before
  post-training; the second describes the *role* of being a reusable base. An
  instruct model is still a foundation model.
* **Base models are not less capable** — the knowledge is the same. The interface
  is different, and they are less safe by default, since refusal behaviour is
  trained in later.
* **Naming is not standardised** — check the model card rather than the filename.

## Why Should I Care?

It clarifies what pretraining actually produces, and it explains why two
assistants built on the same base can behave completely differently: the base
supplies the knowledge, post-training supplies nearly everything you notice.

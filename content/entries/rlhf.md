---
term: RLHF
aliases: [Reinforcement Learning from Human Feedback, Preference Tuning]
category: llm-training
subcategory: alignment
status: established
difficulty: advanced
one_liner: Training a model to produce responses people prefer, by learning a reward model from human comparisons and optimising against it.
origin:
  year: 2017
  attribution: Christiano et al. for control tasks; applied to language models by OpenAI and Anthropic from 2020
historical_period: foundation-model
tags: [training, safety]
relations:
  successor_of: [supervised-fine-tuning]
  evolved_into: [dpo, rlvr]
  depends_on: [reinforcement-learning]
  related_to: [sycophancy, alignment]
prerequisites: [supervised-fine-tuning]
encountered_in: [research-papers, conferences, job-descriptions]
sources:
  - type: paper
    title: "Deep Reinforcement Learning from Human Preferences"
    url: https://arxiv.org/abs/1706.03741
    year: 2017
  - type: paper
    title: "Training Language Models to Follow Instructions with Human Feedback"
    url: https://arxiv.org/abs/2203.02155
    year: 2022
  - type: paper
    title: "Constitutional AI: Harmlessness from AI Feedback"
    url: https://arxiv.org/abs/2212.08073
    year: 2022
updated: 2026-08-21
---

## Simple Explanation

Nobody can write down what makes a response good, but almost anyone can pick the
better of two. So collect a lot of those choices, train a second model to predict
them, and then tune the language model to score well under that predictor.

## Technical Definition

A three-stage pipeline: (1) supervised fine-tuning; (2) train a reward model on
human preference comparisons, typically with a Bradley-Terry objective; (3)
optimise the policy against the reward model with PPO or a similar algorithm,
regularised by a KL penalty against the SFT reference model to prevent drift.

## Why Does It Exist?

Helpfulness, harmlessness and honesty have no loss function. Demonstrations cap
quality at what the demonstrator produced; preferences let the model be optimised
toward outputs better than any single demonstration.

## What Problem Does It Solve?

Aligning generation with fuzzy human judgements that are easy to recognise and
hard to specify.

## How Does It Work?

```text
prompt ──▶ model generates A and B
              │
        human picks the better ──▶ reward model learns to predict preference
              │
        policy optimisation: maximise reward − β·KL(policy ‖ reference)
```

The KL term is essential: without it the policy drifts into degenerate text that
scores highly under an imperfect reward model.

## Mental Model

Coaching by taste-testing. The coach cannot describe the perfect dish but can
always say which of two plates is better, and the cook optimises toward that
judgement — including, if unchecked, toward whatever the coach superficially
likes.

## Example

InstructGPT showed a 1.3B RLHF-tuned model preferred by human raters over the
175B base model. Capability was unchanged; usefulness changed completely.

## Real-World Usage

Standard in every major assistant, though increasingly through simpler variants:
DPO removes the separate reward model, RLAIF and Constitutional AI replace human
labels with model-generated ones against a written set of principles, and RLVR
replaces the reward model entirely with automatic verification for tasks that
have checkable answers.

## Common Confusions

* **RLHF is not "adding safety"** — it optimises for rated preference, and safety
  behaviour is one thing the ratings can express.
* **Reward hacking is the standard failure** — models learn to satisfy the proxy,
  which is a leading explanation for sycophancy: agreeable answers get rated
  higher.
* **RLHF does not add knowledge** — it reshapes behaviour over what pretraining
  already contains.

## Why Should I Care?

Nearly every stylistic tendency users complain about — hedging, over-apologising,
excessive agreement, verbose structure — is a fingerprint of preference
optimisation, not of pretraining.

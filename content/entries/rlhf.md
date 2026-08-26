---
term: RLHF
aliases: [Reinforcement Learning from Human Feedback, Preference Tuning, Post-Training]
category: llm-training
subcategory: alignment
depth: full
status: established
difficulty: advanced
one_liner: Training a model to produce responses people prefer, by learning a reward model from human comparisons and optimising against it.
origin:
  year: 2017
  attribution: Christiano et al. for control tasks; applied to language models by OpenAI and Anthropic from 2020
historical_period: foundation-model
diagram:
  kind: steps
  title: Preferences in, a policy out
  footer: The reward model is a learned proxy, and optimising hard against a proxy is how you get reward
    hacking. The KL term is the admission that the proxy is only trustworthy near where it was trained.
  steps:
  - title: People compare; they do not score
    notes:
    - label: Why
      text: '"which of these is better" is far more reliable from human labellers than "rate this out
        of ten"'
    visual:
      kind: mapping
      width: 760
      head:
      - one prompt, two completions
      - the label
      rows:
      - left: A — hedged, accurate, a little dull
        right: preferred
        mark: ok
        tone: accent
      - left: B — confident, fluent, slightly wrong
        right: rejected
        mark: bad
  - title: The comparisons become a reward, then a policy
    visual:
      kind: pipeline
      width: 700
      stages:
      - text: preference pairs
        note: tens of thousands
      - text: reward model
        note: predicts which wins
        via: train on the comparisons
      - text: updated policy
        tone: accent
        via: maximise reward − β · KL(policy ‖ reference)
      caption: drop the KL term and the policy drifts into degenerate text that scores well under an imperfect
        reward model
tags: [training, safety]
relations:
  successor_of: [supervised-fine-tuning]
  evolved_into: [dpo, rlvr, rlaif]
  depends_on: [reinforcement-learning, information-theory]
  related_to: [sycophancy, alignment, reward-hacking, llm-as-a-judge, grpo]
prerequisites: [supervised-fine-tuning]
encountered_in: [research-papers, conferences, job-descriptions]
sources:
  - type: paper
    title: "Deep Reinforcement Learning from Human Preferences"
    url: https://arxiv.org/abs/1706.03741
    year: 2017
  - type: paper
    title: "Training Language Models to Follow Instructions with Human Feedback (InstructGPT)"
    url: https://arxiv.org/abs/2203.02155
    year: 2022
  - type: paper
    title: "Constitutional AI: Harmlessness from AI Feedback"
    url: https://arxiv.org/abs/2212.08073
    year: 2022
  - type: paper
    title: "Towards Understanding Sycophancy in Language Models"
    url: https://arxiv.org/abs/2310.13548
    year: 2023
    note: The clearest documented instance of what optimising for rated preference produces.
videos:
  - title: "Reinforcement Learning from Human Feedback explained"
    channel: "IBM Technology"
    url: https://www.youtube.com/results?search_query=ibm+technology+reinforcement+learning+from+human+feedback+rlhf+explained
updated: 2026-08-22
---

## Simple Explanation

Nobody can write down what makes a response good. Almost anyone can pick the
better of two.

So collect a great many of those choices, train a second model to predict them,
and then tune the language model to score well under that predictor. It is the
step that turned a text predictor into something people wanted to talk to — and
it is also where several of the field's most-discussed pathologies come from.

## Technical Definition

A three-stage pipeline. First [supervised fine-tuning](supervised-fine-tuning.md)
on demonstrations. Second, a reward model trained on human preference
comparisons, typically with a Bradley-Terry objective. Third, optimisation of the
policy against that reward with PPO or similar, regularised by a
[KL penalty](information-theory.md) against the SFT reference model to prevent
drift.

## Why Does It Exist?

Helpfulness, harmlessness and honesty have no loss function. Demonstrations cap
quality at what the demonstrator produced; preferences let the model be optimised
toward outputs better than any single demonstration, because comparison is easier
than composition.

## What Problem Does It Solve?

Aligning generation with fuzzy human judgements that are easy to recognise and
impossible to specify.

## How Does It Work?

The KL term is the whole safety mechanism of the procedure, and it is worth
understanding why. The reward model is a *proxy*. Optimise any proxy hard enough
and you find its errors rather than its intent — this is
[reward hacking](reward-hacking.md), and the KL budget is a limit on how far the
policy may travel while looking for them.

## Mental Model

Coaching by taste-testing. The coach cannot describe the perfect dish but can
always say which of two plates is better, and the cook optimises toward that
judgement — including, if unchecked, toward whatever the coach superficially
likes.

## Example

InstructGPT is the result that made the case: a 1.3B model tuned with RLHF was
preferred by human raters over the 175B base model. Capability was unchanged.
Usefulness changed completely, and the difference was entirely post-training.

The other instructive result runs the opposite way.
[Sycophancy](sycophancy.md) — models folding when a user pushes back on a correct
answer — is a measured consequence of this procedure, because raters prefer being
agreed with and the reward model learned that. It is the clearest available
demonstration that the proxy and the goal diverge exactly where the user is
wrong.

## Real-World Usage

Standard in every major assistant, though increasingly through simpler
descendants:

* **[DPO](dpo.md)** removes the separate reward model, reaching the same
  objective with an ordinary training loop. Now the default outside frontier labs.
* **[RLAIF](rlaif.md) and Constitutional AI** replace human labels with model
  judgements against a written set of principles — cheaper, and legible, because
  the values become a document.
* **[RLVR](rlvr.md)** replaces the reward model entirely with automatic
  verification, for tasks where correctness is checkable. This is what produced
  [reasoning models](reasoning-model.md).
* **[GRPO](grpo.md)** removes the value network, making the reinforcement stage
  practical at scale.

Read that list as a sequence of removals. Each step took a component out of the
original pipeline, and the field got both cheaper and more reliable as a result.

## Common Confusions

* **RLHF is not "adding safety"** — it optimises for rated preference. Safety
  behaviour is one thing ratings can express, alongside tone, format and
  agreeableness.
* **RLHF does not add knowledge** — it reshapes behaviour over what
  [pretraining](pretraining.md) already contains.
* **RLHF is not classic RL** — the environment is a learned reward model and
  episodes are one step long.
* **Reward hacking is the default, not the exception** — expect it, measure for
  it, and treat the KL budget as a real constraint rather than a hyperparameter.

## Why Should I Care?

Nearly every stylistic tendency users complain about — hedging, over-apologising,
excessive agreement, verbose structure — is a fingerprint of preference
optimisation rather than of pretraining. Knowing that tells you which
complaints a prompt can fix and which are baked into the model you chose.

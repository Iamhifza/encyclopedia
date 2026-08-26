---
term: DPO
aliases: [Direct Preference Optimization, Direct Preference Optimisation]
category: llm-training
subcategory: alignment
status: established
difficulty: research
one_liner: A way to train on human preferences directly with a simple loss, skipping the separate reward model and reinforcement learning loop that RLHF requires.
origin:
  year: 2023
  attribution: Rafailov et al., Stanford
historical_period: foundation-model
diagram:
  kind: figure
  title: The same preference data, without the reward model
  footer: 'Simpler and cheaper than RLHF, and it gives up something: no reward model means no way to sample
    new responses and score them, so DPO learns only from the pairs it was given.'
  visual:
    kind: mapping
    width: 780
    head:
    - one prompt, two responses
    - what the loss does to it
    rows:
    - left: chosen
      right: log-probability pushed up
      mark: ok
      tone: accent
    - left: rejected
      right: log-probability pushed down
      mark: bad
    - left: the frozen reference model
      right: both are measured relative to it, which bounds the drift
    caption: one loss on a triple, computed directly — no reward model, no sampling loop, no separate
      RL stage
tags: [training]
relations:
  successor_of: [rlhf]
  alternative_to: [rlhf]
  related_to: [supervised-fine-tuning]
prerequisites: [rlhf]
encountered_in: [research-papers, github, job-descriptions]
sources:
  - type: paper
    title: "Direct Preference Optimization: Your Language Model is Secretly a Reward Model"
    url: https://arxiv.org/abs/2305.18290
    year: 2023
updated: 2026-08-21
---

## Simple Explanation

RLHF trains a reward model, then uses reinforcement learning against it — two
models, an unstable optimiser and a lot of tuning. DPO shows the same objective
can be reached with one ordinary training loop on preference pairs: raise the
probability of the chosen answer, lower the rejected one, relative to a frozen
reference model.

## Technical Definition

A closed-form reparameterisation of the KL-constrained reward maximisation
objective, expressing the optimal policy's implicit reward as a log-ratio against
a reference policy. This yields a supervised binary classification loss over
preference pairs, eliminating explicit reward modelling and policy-gradient
optimisation.

## Why Does It Exist?

PPO-based RLHF is expensive, sensitive to hyperparameters and hard to reproduce.
DPO delivers comparable alignment quality with roughly the complexity of ordinary
fine-tuning.

## What Problem Does It Solve?

The engineering burden of preference training, which put RLHF out of reach for
most teams.

## How Does It Work?


RLHF takes preference pairs, trains a reward model on them, then optimises the
policy against that reward with reinforcement learning. DPO observes that the
optimal policy under such a reward has a closed form, and that you can therefore
optimise the policy against the preferences directly.

Each training example is a triple: a prompt, a chosen response and a rejected
one. The loss compares the policy's log-probabilities for both against a frozen
reference copy of the model, and pushes the chosen response up relative to the
rejected one. The reference ratio does the job the explicit KL penalty does in
RLHF, keeping the policy from drifting far from where it started.

What this buys is simplicity: one loss, one training loop, no reward model to
train and no sampling to manage. What it gives up is the ability to generate new
responses and score them, since there is no reward model to score with. DPO
learns from exactly the pairs it was given, which makes data quality the whole
game.

## Mental Model

Instead of hiring a critic and then arguing with them, you learn directly from
the pairs of drafts the critic would have compared.

## Formula

$$\mathcal{L} = -\log \sigma\!\left(\beta \log \frac{\pi(y_w|x)}{\pi_{ref}(y_w|x)} - \beta \log \frac{\pi(y_l|x)}{\pi_{ref}(y_l|x)}\right)$$

* $y_w, y_l$ — the preferred and rejected responses.
* $\pi_{ref}$ — frozen reference policy, usually the SFT model.
* $\beta$ — how far the policy may drift from the reference.

## Example

Open-weight instruction-tuned models are now commonly aligned with DPO or one of
its descendants (IPO, KTO, ORPO, SimPO), because the whole procedure fits in a
single training script.

## Real-World Usage

The default preference method outside frontier labs. Some evidence suggests
online RL still edges it out at the top end, so several labs run hybrid pipelines.

## Common Confusions

* **DPO is not RL** — no environment, no rollouts, no policy gradient, despite
  optimising an RL-derived objective.
* **It still needs preference data** — the expensive part was never the algorithm.
* **The reference model matters** — a poor SFT starting point limits everything
  downstream.

## Why Should I Care?

It is the reason preference alignment became routine engineering rather than a
frontier-lab speciality.

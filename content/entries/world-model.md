---
term: World Model
aliases: [Learned Simulator, Predictive World Model]
category: world-models-embodied
subcategory: world-models
status: emerging
difficulty: advanced
one_liner: A learned internal simulator of how an environment behaves, which an agent can use to predict outcomes before acting.
origin:
  year: 2018
  circa: true
  attribution: Ha and Schmidhuber's "World Models"; roots in model-based control and Kalman filtering
historical_period: deep-learning
tags: [architecture]
relations:
  different_from: [foundation-model]
  depends_on: [self-supervised-learning, reinforcement-learning]
  used_by: [vision-language-action-model, sim-to-real]
  related_to: [jepa, state-space-model]
prerequisites: [reinforcement-learning, self-supervised-learning]
encountered_in: [research-papers, conferences, technical-blogs]
sources:
  - type: paper
    title: "World Models"
    url: https://arxiv.org/abs/1803.10122
    year: 2018
  - type: paper
    title: "Mastering Diverse Domains through World Models (DreamerV3)"
    url: https://arxiv.org/abs/2301.04104
    year: 2023
updated: 2026-08-21
review_by: 2027-02-01
---

## Simple Explanation

Before you move a full glass, you know roughly what happens if you tip it. That
predictive model of physical consequence is what a world model tries to learn: not
what text follows, but what *happens next* in an environment, given an action.

## Technical Definition

A learned generative or predictive model of environment dynamics,
$p(s_{t+1} \mid s_t, a_t)$, typically over a compact latent state. It enables
planning by rollout, model-based reinforcement learning, and training a policy
inside the model rather than in the environment.

## Why Does It Exist?

Model-free reinforcement learning needs enormous numbers of environment
interactions. In the physical world interactions are slow, expensive and
sometimes destructive. Learning dynamics lets an agent practise internally.

## What Problem Does It Solve?

Sample efficiency and planning: evaluating candidate actions without executing
them.

## How Does It Work?

```text
observation ──▶ encoder ──▶ latent state z
                              │
        (z, action) ──▶ dynamics model ──▶ predicted z′ ──▶ predicted reward
                              │
             plan by rolling forward candidate action sequences
```

## Mental Model

Mental rehearsal. Playing the move out in your head before committing your hand.

## Example

DreamerV3 learned to collect diamonds in Minecraft from scratch, training its
policy largely inside its learned model rather than in the game — a task requiring
long horizons and sparse rewards.

## Terminology Note

The term has drifted and is now used for at least three different things: (1) the
classical model-based RL sense above; (2) video generation models marketed as
"world models" because they produce physically plausible footage — which is
prediction of *pixels*, not necessarily of *dynamics* usable for control; and (3)
loosely, any claim that an LLM has an internal representation of the world. These
are not the same claim, and the third is actively contested. Ask whether the
model is used for control or only for generation.

## Real-World Usage

Robotics, autonomous driving simulation, game agents, and increasingly as a
research direction arguing that language-only training is insufficient for
physical understanding — the position associated with JEPA and with LeCun's
critique of the LLM-centred roadmap.

## Common Confusions

* **World model vs foundation model** — one predicts environment dynamics under
  actions; the other predicts tokens. A foundation model may contain implicit
  world knowledge without being usable as a simulator.
* **Video generation is not world modelling** — plausible video does not entail a
  causal, action-conditioned model.

## Why Should I Care?

It is the most serious research alternative to the assumption that scaling
language models is the whole path, and the vocabulary is entering products
faster than the underlying capability is.

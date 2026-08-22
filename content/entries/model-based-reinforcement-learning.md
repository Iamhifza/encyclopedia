---
term: Model-Based Reinforcement Learning
aliases: [Model-Based RL, Dyna, Planning with a Learned Model, MuZero]
category: world-models-embodied
subcategory: world-models
depth: full
status: established
difficulty: research
one_liner: "Learning how the environment behaves and then practising inside that learned model instead of in the real world."
origin:
  year: 1990
  circa: true
  attribution: Sutton's Dyna architecture; roots in optimal control and dynamic programming
historical_period: ai-winter
tags: [training]
relations:
  is_a: [reinforcement-learning]
  depends_on: [world-model]
  related_to: [sim-to-real, search-algorithm, embodied-ai, automated-planning]
prerequisites: [reinforcement-learning, world-model]
encountered_in: [research-papers, conferences]
sources:
  - type: paper
    title: "Integrated Architectures for Learning, Planning, and Reacting (Dyna)"
    url: https://dl.acm.org/doi/10.1145/122344.122377
    year: 1991
  - type: paper
    title: "Mastering Atari, Go, Chess and Shogi by Planning with a Learned Model (MuZero)"
    url: https://arxiv.org/abs/1911.08265
    year: 2019
  - type: paper
    title: "Mastering Diverse Domains through World Models (DreamerV3)"
    url: https://arxiv.org/abs/2301.04104
    year: 2023
updated: 2026-08-21
---

## Simple Explanation

Model-free reinforcement learning learns purely by doing: try something, see what
happens, adjust. That needs an enormous number of attempts, which is fine in a
simulator and impossible on real hardware.

Model-based RL learns the environment's dynamics as well, then practises inside
that learned model. Millions of imagined attempts, no broken robots.

## Technical Definition

Reinforcement learning that learns a model of environment dynamics
$p(s_{t+1}, r_t \mid s_t, a_t)$ and uses it for planning, for generating
synthetic experience, or both. Planning may be explicit search over imagined
rollouts, or implicit through training a policy on model-generated trajectories.

## Why Does It Exist?

Sample efficiency. Model-free methods can require millions of environment
interactions — acceptable in a game, prohibitive when each interaction takes
seconds of real time and risks damaging hardware.

## What Problem Does It Solve?

The cost of experience. It converts expensive real interactions into cheap
imagined ones, and it allows evaluating an action before committing to it.

## How Does It Work?

```text
real experience ──▶ learn dynamics model
                            │
                    ┌───────┴────────┐
                    │                │
            imagine rollouts     plan by search
            train policy on      over imagined
            synthetic data       futures
                    │                │
                    └───────┬────────┘
                       act in the real world
                            │
                   new experience improves the model
```

## Mental Model

Rehearsing in your head before performing. Cheap, repeatable, and only as useful
as your mental model is accurate.

## Example

MuZero is the striking result: it learned to play Go, chess, shogi and Atari at
superhuman level *without being told the rules*. It learned a model of dynamics
sufficient for planning — one that predicts value, policy and reward rather than
reconstructing the actual game state. That distinction matters: the model does not
need to be accurate about everything, only about what affects decisions.

DreamerV3 pushed the other direction, learning entirely inside an imagined latent
world and solving long-horizon sparse-reward tasks like collecting diamonds in
Minecraft from scratch.

## Real-World Usage

Robotics, where real interaction is expensive; control systems; game agents.
Largely absent from LLM training, though the framing is increasingly discussed for
agent planning — an agent that could predict the consequence of a tool call before
making it would be doing exactly this.

## Common Confusions

* **Model-based vs model-free** — whether the agent learns environment dynamics.
  Model-free is simpler and more robust to a bad model; model-based is far more
  sample-efficient when the model is good.
* **"Model" means dynamics, not neural network** — both are called models, which
  is a persistent source of confusion. Here it means a model *of the environment*.
* **Model errors compound** — planning over long horizons amplifies small
  inaccuracies, which is why imagined rollouts are usually kept short.

## Why Should I Care?

It is the technical core of the world-model research programme, and the clearest
statement of an alternative bet: that intelligence requires predicting
consequences, not just predicting text.

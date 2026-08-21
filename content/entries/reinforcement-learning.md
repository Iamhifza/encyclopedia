---
term: Reinforcement Learning
aliases: [RL, Reward-Based Learning]
category: machine-learning
subcategory: paradigms
status: foundational
difficulty: advanced
one_liner: Learning by acting, receiving a reward, and adjusting behaviour to earn more reward over time.
origin:
  year: 1988
  circa: true
  attribution: Sutton and Barto formalised temporal-difference learning; roots in optimal control and animal psychology
historical_period: ai-winter
tags: [training]
relations:
  used_by: [rlhf, rlvr, world-model]
  alternative_to: [supervised-learning]
  related_to: [ai-agent]
encountered_in: [research-papers, conferences, job-descriptions]
sources:
  - type: book
    title: "Reinforcement Learning: An Introduction (Sutton & Barto)"
    url: http://incompleteideas.net/book/the-book.html
    year: 2018
  - type: paper
    title: "Human-level control through deep reinforcement learning (DQN)"
    url: https://www.nature.com/articles/nature14236
    year: 2015
updated: 2026-08-21
---

## Simple Explanation

No one tells the learner the right answer. It tries something, gets a number back
saying how well that went, and gradually shifts toward actions that earn higher
numbers. The hard part is that the reward often arrives long after the decision
that caused it.

## Technical Definition

Learning a policy $\pi(a \mid s)$ that maximises expected discounted return in a
Markov decision process, given only reward signals from interaction. Central
issues are exploration versus exploitation, credit assignment over time, and
sample efficiency.

## Why Does It Exist?

Many problems have no labelled correct action — games, robotics, resource
allocation, dialogue — but do have a measurable outcome. RL learns from the
outcome.

## What Problem Does It Solve?

Sequential decision-making where actions have delayed consequences.

## How Does It Work?

```text
        ┌──────── action ────────┐
     agent                    environment
        └──── state, reward ◀────┘
   update the policy toward actions that preceded higher return
```

## Mental Model

Training an animal with treats, where the treat sometimes arrives ten minutes
after the behaviour that earned it.

## Example

AlphaGo combined RL with search to beat the strongest human Go players in 2016 —
the result that made RL famous outside research.

## Real-World Usage

Inside the LLM stack it appears as preference optimisation (RLHF), verifiable-
reward training for reasoning models (RLVR), and increasingly for training agents
end-to-end on multi-step tool-use tasks.

## Common Confusions

* **RL vs supervised learning** — supervised learning is told the right answer;
  RL is told only how good its answer was.
* **Reward is not the goal** — it is a proxy for the goal, and optimising a proxy
  hard enough is precisely how reward hacking happens.
* **RLHF is not classic RL** — the "environment" is a learned reward model, and
  episodes are one step long.

## Why Should I Care?

It is the framework behind every alignment method and every agent trained to act
rather than merely answer, and its central pathology — optimising the measure
rather than the intent — recurs throughout applied AI.

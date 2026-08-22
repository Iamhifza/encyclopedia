---
term: GRPO
aliases: [Group Relative Policy Optimization, Group Relative Policy Optimisation]
category: llm-training
subcategory: alignment
depth: full
status: emerging
difficulty: research
one_liner: "A reinforcement learning method that scores a batch of sampled answers against each other, removing the need for a separate value network."
origin:
  year: 2024
  attribution: Introduced by DeepSeek in the DeepSeekMath work and central to DeepSeek-R1
historical_period: agentic
tags: [training]
relations:
  used_by: [rlvr, reasoning-model]
  alternative_to: [dpo, rlhf]
  depends_on: [reinforcement-learning]
prerequisites: [rlhf, reinforcement-learning]
encountered_in: [research-papers, github, technical-blogs]
sources:
  - type: paper
    title: "DeepSeekMath: Pushing the Limits of Mathematical Reasoning in Open Language Models"
    url: https://arxiv.org/abs/2402.03300
    year: 2024
  - type: paper
    title: "DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning"
    url: https://arxiv.org/abs/2501.12948
    year: 2025
updated: 2026-08-21
review_by: 2027-02-01
---

## Simple Explanation

Standard policy-gradient RL needs a second model — a value network — to estimate
how good a situation is, so it can tell whether an answer was better or worse
than expected. That model is expensive to train and a common source of
instability.

GRPO removes it with a simple substitution: sample several answers to the same
question, and use the group's average score as the baseline. Better than your
peers means good; worse means bad. No value network required.

## Technical Definition

A policy-gradient method estimating advantage from the empirical distribution of
rewards within a sampled group. For each prompt, $G$ completions are drawn and
scored; each completion's advantage is its reward normalised against the group's
mean and standard deviation. The policy is updated with a clipped surrogate
objective and a KL penalty against a reference model.

## Why Does It Exist?

PPO's value network roughly doubles the memory and complexity of RL training on
large models, and estimating value accurately for long generated sequences is
genuinely hard. If you can sample multiple completions cheaply — which you can —
the group itself supplies a perfectly serviceable baseline.

## What Problem Does It Solve?

Cost and stability of reinforcement learning on language models, which is what
made RL post-training practical outside the largest labs.

## How Does It Work?

```text
prompt ──▶ sample G completions
             │
        score each      [0.9  0.2  0.7  0.1  0.8]   ← verifier or reward model
             │
        group mean = 0.54
             │
        advantage = (reward − mean) / std
             │       [+1.2 −1.1  +0.5 −1.4  +0.9]
             ▼
        push up the winners, push down the losers
        KL penalty keeps the policy near the reference
```

## Mental Model

Grading on a curve. You do not need an absolute standard of what a good answer
looks like — only which of these five was better than the others.

## Formula

$$A_i = \frac{r_i - \operatorname{mean}(r_{1..G})}{\operatorname{std}(r_{1..G})}$$

* $r_i$ — reward for completion $i$, from a verifier or reward model.
* $G$ — group size; larger gives a less noisy baseline at proportionally more
  sampling cost.
* $A_i$ — advantage, which replaces what a value network would have estimated.

## Example

GRPO is the algorithm behind DeepSeek-R1's reasoning training, paired with
verifiable rewards on mathematics and code. The combination is what made that
result reproducible by others: no reward model to train, no value network to
stabilise, just sampling and a checker.

## Real-World Usage

Widely adopted for reasoning and agent training since 2025, supported in the main
open-source RL training libraries. Variants adjusting the normalisation and the
clipping have followed quickly.

## Terminology Note

This is a fast-moving area and the algorithm zoo is crowded — GRPO, DAPO, GSPO,
RLOO and others differ in details of baseline estimation and clipping. Treat
specific claims of superiority cautiously; comparisons are often confounded by
data and reward design rather than the algorithm.

## Common Confusions

* **GRPO vs DPO** — both avoid PPO's machinery, differently. DPO needs
  *preference pairs* and no sampling; GRPO needs *sampled groups* and a reward
  signal, and is on-policy.
* **The group baseline needs variance** — if every sample scores identically, all
  advantages are zero and nothing is learned. Problems must be neither trivial
  nor impossible for the current policy.
* **Group size costs compute** — $G$ completions per prompt per step is the price
  of not having a value network.

## Why Should I Care?

It is the algorithm behind the 2025 jump in open reasoning models, and a neat
example of removing a component by exploiting something you were already doing —
sampling — rather than by adding sophistication.

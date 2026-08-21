---
term: RLVR
aliases: [Reinforcement Learning from Verifiable Rewards, Verifiable Rewards, RLVR Training]
category: llm-training
subcategory: alignment
status: emerging
difficulty: research
one_liner: Training a model with reinforcement learning where the reward comes from automatically checking the answer, not from human opinion.
origin:
  year: 2024
  circa: true
  attribution: Named in Tülu 3 work at AI2; the approach was central to DeepSeek-R1 and contemporaneous reasoning models
historical_period: agentic
tags: [training]
relations:
  successor_of: [rlhf]
  depends_on: [reinforcement-learning]
  used_by: [reasoning-model]
  related_to: [benchmark-contamination, evaluation-harness]
prerequisites: [rlhf]
encountered_in: [research-papers, github, technical-blogs]
sources:
  - type: paper
    title: "Tülu 3: Pushing Frontiers in Open Language Model Post-Training"
    url: https://arxiv.org/abs/2411.15124
    year: 2024
  - type: paper
    title: "DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning"
    url: https://arxiv.org/abs/2501.12948
    year: 2025
updated: 2026-08-21
review_by: 2027-02-01
---

## Simple Explanation

Human preference ratings are slow, expensive and gameable. But for maths, code
and formal tasks you do not need an opinion — you can just run the test. If the
answer is right, reward it. That single change removes the reward model and much
of its pathology.

## Technical Definition

Reinforcement learning where the reward is produced by a deterministic verifier —
unit tests, an exact-match checker, a proof assistant, a compiler — rather than a
learned preference model. Commonly optimised with GRPO, which estimates advantage
from a group of sampled completions and dispenses with a separate value network.

## Why Does It Exist?

Learned reward models can be hacked: the policy finds outputs that score well and
are not actually good. A verifier cannot be flattered.

## What Problem Does It Solve?

Reward hacking and the cost of human labelling, in the domains where correctness
is mechanically checkable.

## How Does It Work?

```text
problem ──▶ sample k solutions ──▶ run the verifier on each
                                        │
             advantage = how each scored relative to the group
                                        │
                          policy update toward the winners
```

## Mental Model

Training with an answer key rather than a panel of judges.

## Example

DeepSeek-R1 demonstrated that extended reasoning behaviour — self-checking,
backtracking, trying alternative approaches — emerges from RLVR on maths and code
without being demonstrated in supervised data.

## Real-World Usage

The dominant recipe for reasoning models, and increasingly for agent training,
where the verifier is "did the test suite pass" or "did the task complete".

## Terminology Note

The label is recent (late 2024) and not universally used; some labs describe the
same practice as outcome-supervised RL, execution feedback, or simply RL with
programmatic rewards. Expect the naming to keep shifting; the technique is what
to track.

## Common Confusions

* **Verifiable does not mean correct-by-construction** — passing unit tests is not
  the same as being right, and models learn to exploit weak tests.
* **It does not generalise everywhere** — most valuable tasks (writing, advice,
  design) have no verifier, so preference methods remain necessary.
* **RLVR vs RLHF** — the difference is only where the reward comes from.

## Why Should I Care?

It explains the sharp 2025 jump in mathematical and coding capability, and it
sets the boundary of that jump: capability grew fastest exactly where automatic
verification was possible.

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
diagram:
  kind: flow
  title: Let a program decide whether the answer was right
  footer: 'The constraint is the whole method: it only works where correctness is checkable. Maths, code
    and formal proofs qualify; essays, strategy and taste do not, and no amount of scale changes that.'
  nodes:
  - title: Problem
    note: with a checkable answer
    caption: maths, code, proofs
  - title: Sample k
    note: several attempts at once
    caption: diversity is the point
  - title: Verify
    note: run the tests, check the proof
    accent: true
    caption: no human, no reward model
  - title: Update
    note: toward whatever passed
    caption: scored against the group
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


Take a problem whose answer can be checked by a program, sample several attempts,
run the checker on each, and update the policy toward whatever passed. No reward
model, no human labels, and no learned proxy that can be gamed — the reward is a
test suite or a proof checker returning a verdict.

Sampling several attempts is essential rather than incidental. A single attempt
gives a reward with no baseline to compare it against; a group gives each attempt
a relative score, which is what the policy gradient needs. This is why RLVR and
GRPO are usually described together.

Everything rests on the verifier. Where correctness is mechanically checkable —
competition maths, unit-tested code, formal proofs — this is the cleanest reward
signal in machine learning, and it is where the recent jump in reasoning ability
came from. Where it is not, the method simply does not apply, and no amount of
scale supplies a verifier that does not exist.

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

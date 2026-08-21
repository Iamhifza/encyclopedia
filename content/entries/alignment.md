---
term: Alignment
aliases: [AI Alignment, Value Alignment]
category: evaluation-safety
subcategory: alignment
status: established
difficulty: advanced
one_liner: The problem of getting an AI system to pursue what people actually intend rather than what was literally specified.
origin:
  year: 1960
  circa: true
  attribution: Wiener articulated the specification problem in 1960; the modern research field formed in the 2010s
historical_period: statistical-ml
tags: [safety]
relations:
  used_by: [rlhf]
  related_to: [reward-hacking, sycophancy, mechanistic-interpretability, guardrails]
prerequisites: [reinforcement-learning]
encountered_in: [research-papers, conferences, job-descriptions, social-media]
sources:
  - type: paper
    title: "Concrete Problems in AI Safety"
    url: https://arxiv.org/abs/1606.06565
    year: 2016
  - type: paper
    title: "Constitutional AI: Harmlessness from AI Feedback"
    url: https://arxiv.org/abs/2212.08073
    year: 2022
updated: 2026-08-21
---

## Simple Explanation

You cannot write down everything you want, and any system optimising hard against
what you *did* write down will find the gap. Alignment is the study of closing
that gap — making systems that do what was meant, including in situations nobody
specified.

## Technical Definition

The problem of ensuring an AI system's objectives and behaviour correspond to
human intent. Usually decomposed into *outer alignment* (specifying the right
objective) and *inner alignment* (the system actually pursuing that objective
rather than a correlated proxy learned during training). Current practice
addresses it with preference learning, principle-based training, red teaming,
evaluations and interpretability.

## Why Does It Exist?

Wiener's 1960 formulation still holds: if we use a machine to achieve a purpose
with which we cannot efficiently interfere, we had better be sure the purpose put
into it is the one we really desire. Every optimiser exploits the difference
between the objective and the intent.

## What Problem Does It Solve?

Specification gaming, unintended behaviour in unanticipated situations, and — as
systems become more capable and more autonomous — behaviour that cannot be
corrected after the fact.

## How Does It Work?

```text
intent ──▶ specification ──▶ training signal ──▶ learned behaviour
        ▲                 ▲                   ▲
        │ hard to state   │ proxy, gameable   │ may differ from what was trained
        └──── outer alignment ────┘   └── inner alignment ──┘
```

## Mental Model

The three wishes problem. The genie grants exactly what you said, and the
interesting failures all live in the gap between that and what you meant.

## Example

Concrete, current instances: sycophancy from preference training, reward hacking
in RLVR where a model edits the test rather than fixing the code, and jailbreaks
that recover behaviour training was meant to suppress.

## Terminology Note

The word carries different weight in different communities: for some it is a
practical engineering agenda about deployed model behaviour; for others it refers
specifically to risks from highly capable future systems. Both usages are common
and are frequently talked past each other.

## Real-World Usage

RLHF and its descendants, Constitutional AI and principle-based training, red
teaming, dangerous-capability evaluations, and interpretability research aimed at
verifying rather than only observing behaviour.

## Common Confusions

* **Alignment is not content moderation** — refusing a request is one visible
  surface of a much broader problem.
* **Aligned to whom** — the specification problem includes deciding whose intent
  counts, which is a governance question, not a technical one.

## Why Should I Care?

It explains most odd model behaviours you will encounter in practice, and it is
the frame in which capability and control are discussed as the same problem.

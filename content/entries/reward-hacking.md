---
term: Reward Hacking
aliases: [Specification Gaming, Reward Gaming, Goodharting]
category: evaluation-safety
subcategory: failure-modes
status: established
difficulty: intermediate
one_liner: When a system finds a way to score highly on the measure without doing the thing the measure was meant to capture.
origin:
  year: 2016
  circa: true
  attribution: Named in "Concrete Problems in AI Safety"; the underlying idea is Goodhart's law (1975)
historical_period: statistical-ml
diagram:
  kind: figure
  title: The measure was satisfied; the intent was not
  footer: Not a malfunction. The model optimised exactly what it was given, and found that the cheapest
    route to a passing score did not pass through doing the work. Every proxy has one of these.
  visual:
    kind: mapping
    width: 780
    head:
    - what was asked for
    - what happened
    rows:
    - left: 'intended:  fix the bug so the tests pass'
      right: what a person meant
    - left: 'measured:  the tests pass'
      right: what the reward actually checked
      tone: warn
    - left: 'found:  delete the assertion'
      right: scores perfectly, achieves nothing
      mark: bad
    caption: the gap between the second and third rows is where every reward hack lives
tags: [safety]
relations:
  is_a: [alignment]
  depends_on: [reinforcement-learning]
  related_to: [sycophancy, benchmark, rlvr]
prerequisites: [reinforcement-learning]
encountered_in: [research-papers, production-systems, conferences]
sources:
  - type: paper
    title: "Concrete Problems in AI Safety"
    url: https://arxiv.org/abs/1606.06565
    year: 2016
  - type: post
    title: "Specification gaming: the flip side of AI ingenuity"
    url: https://deepmind.google/discover/blog/specification-gaming-the-flip-side-of-ai-ingenuity/
    year: 2020
updated: 2026-08-21
---

## Simple Explanation

You reward the number, and the system optimises the number. A cleaning robot
rewarded for seeing no mess learns to close its eyes. A coding agent rewarded for
passing tests learns to delete the failing test.

## Technical Definition

Optimisation of a proxy objective in ways that increase measured reward while
decreasing true utility. It is the expected consequence of Goodhart's law under
strong optimisation pressure, and it becomes more likely, not less, as the
optimiser gets more capable.

## Why Does It Exist?

Every measurable objective is a proxy. The set of high-scoring behaviours is
always larger than the set of intended ones, and optimisation searches the whole
set.

## What Problem Does It Solve?

Nothing — but studying it is how objectives get designed defensively.

## How Does It Work?


Specify a reward, optimise against it hard enough, and the model finds the
cheapest route to a high score. When the reward is a proxy — and it always is —
that route need not pass through doing the thing you wanted.

The canonical shape: the intent is *fix the bug so the tests pass*, the measure
is *the tests pass*, and the discovered solution is to delete the failing
assertion. The score is perfect. Nothing was fixed. The model did not
misunderstand; it optimised precisely what it was given.

This is Goodhart's law with a very fast optimiser attached, and it is why reward
design is treated as an adversarial exercise. The mitigations all limit how far
the policy can travel from known-good behaviour or make the proxy harder to
satisfy trivially: KL penalties against a reference model, verifiers that check
the work rather than the outcome, held-out evaluations the reward never sees, and
human review of the cases that score suspiciously well.

## Mental Model

Paying bounty per rat caught, and discovering someone has started farming rats.

## Example

In LLM systems it appears as: models weakening tests instead of fixing code,
padding answers because verbose responses are rated higher, exploiting judge
biases in model-graded evaluation, and sycophancy as a reward-model artefact.

## Real-World Usage

Mitigations are all about making the proxy harder to game: held-out verifiers,
adversarial evaluation, human spot-checks, multiple uncorrelated metrics, KL
penalties keeping a policy near a reference, and capping optimisation pressure
rather than maximising it.

## Common Confusions

* **Not a bug in the model** — the model did exactly what was rewarded. The
  defect is in the specification.
* **Not solvable by a better metric alone** — every metric has a gap; the
  question is how much pressure you apply to it.
* **Reward hacking vs cheating** — no intent is implied or required.

## Why Should I Care?

Every evaluation you build is a target someone will optimise, including the model
you are training. Designing metrics as if they were adversarial is the practical
lesson.

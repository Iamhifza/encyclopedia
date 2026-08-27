---
term: Automated Planning
aliases: [Planning, STRIPS, Task Planning, Task and Motion Planning]
category: ai-foundations
subcategory: search-planning
depth: full
status: established
difficulty: advanced
one_liner: "Working out an ordered sequence of actions that gets from the current state to a desired one."
historical_period: classical-ai
diagram:
  kind: steps
  title: Actions declare what they need and what they change
  footer: Explicit preconditions are what an LLM planner lacks. It will happily emit a step whose precondition
    does not hold — which is why the interesting systems let a model propose the plan and a planner verify
    it.
  steps:
  - title: Every action is a contract
    notes:
    - label: Goal
      text: at(cup, sink), from a world where the cup is on the table
    visual:
      kind: mapping
      width: 780
      head:
      - PICK-UP(x, loc) requires
      - and afterwards
      rows:
      - left: at(robot, loc)
        right: holding(x)
        tone: accent
      - left: at(x, loc)
        right: ¬at(x, loc)
      - left: holding(nothing)
        right: ¬holding(nothing)
  - title: A plan is a sequence whose contracts all hold
    visual:
      kind: chips
      items:
      - MOVE→table
      - PICK-UP cup
      - MOVE→sink
      - PUT-DOWN cup
      caption: each step's preconditions are checked against the state projected by every step before
        it — which is what makes the plan verifiable before anything moves
tags: [symbolic, agents]
relations:
  used_by: [ai-agent, agent-loop]
  related_to: [search-algorithm, world-model, reasoning-model, reinforcement-learning]
prerequisites: [search-algorithm]
encountered_in: [research-papers, conferences, production-systems]
sources:
  - type: paper
    title: "STRIPS: A New Approach to the Application of Theorem Proving to Problem Solving"
    url: https://www.sciencedirect.com/science/article/abs/pii/0004370271900105
    year: 1971
  - type: book
    title: "Artificial Intelligence: A Modern Approach, planning chapters"
    url: https://aima.cs.berkeley.edu/
  - type: paper
    title: "On the Planning Abilities of Large Language Models"
    url: https://arxiv.org/abs/2302.06706
    year: 2023
updated: 2026-08-21
---

## Simple Explanation

You know where you are and where you want to be. Planning is finding the sequence
of actions that connects them — and checking, before you start, that each step's
preconditions will actually hold when you get there.

## Technical Definition

Given an initial state, a goal condition, and a set of actions each with
preconditions and effects, find a sequence of actions transforming the initial
state into one satisfying the goal. Classical planning assumes a deterministic,
fully observable world; extensions handle uncertainty, partial observability,
time and continuous quantities.

## Why Does It Exist?

Search alone finds a path through states; planning adds structure by representing
*actions* with explicit preconditions and effects. That representation makes it
possible to reason about long sequences without enumerating every intermediate
state.

## What Problem Does It Solve?

Multi-step tasks where actions have dependencies and order matters, and where
discovering a problem halfway through is expensive.

## How Does It Work?


Describe the world as a set of facts, describe each action by what it requires
and what it changes, and give a goal. A planner then searches for a sequence of
actions whose preconditions all hold when they are reached and whose combined
effects satisfy the goal.

The representation is what does the work. PICK-UP requires that the robot is in
the same place as the object and is holding nothing; afterwards it is holding the
object and the object is no longer where it was. Because each action declares
this explicitly, a candidate plan can be verified against the state it projects,
step by step, before anything is executed.

That guarantee is precisely what a language model asked to plan does not offer.
It will produce a fluent sequence containing a step whose precondition does not
hold, and nothing in the process notices. Which is why the interesting current
systems combine the two: the model proposes, in natural language, and a planner
checks whether the proposal is actually executable.

## Mental Model

Writing a recipe rather than improvising. You establish in advance that the oven
will be hot when the dish is ready to go in.

## Example

The interesting current question is what LLMs do here. Given a planning problem,
a language model produces a plausible-looking plan quickly — and formal
evaluation shows it is frequently invalid, with unmet preconditions, on problems
a classical planner solves reliably. Reasoning models improved this substantially
but did not close the gap on longer horizons.

The productive pattern is hybrid: the LLM translates a messy natural-language
goal into a formal problem specification, a classical planner solves it with
guarantees, and the LLM explains the result. Each does what it is good at.

## Real-World Usage

Logistics and scheduling, spacecraft operations, manufacturing, game AI, and
robotics — where task and motion planning must produce a sequence that is both
logically valid and physically executable. In agent systems, "planning" usually
means something looser: the model proposing a sequence of steps in prose, with no
formal verification.

## Common Confusions

* **Classical planning vs agent planning** — one produces a verified sequence
  under an explicit model; the other produces text that looks like a plan. The
  word is the same, the guarantees are not.
* **Planning vs reinforcement learning** — planning reasons over a known model of
  actions; RL learns a policy from experience without needing one.
* **A plan is not a schedule** — planning determines order and dependency;
  scheduling assigns times and resources.

## Why Should I Care?

It is the half-century of prior art that agent design is currently rediscovering,
and knowing what a real planner guarantees makes it much easier to see what an
LLM's "plan" does not.

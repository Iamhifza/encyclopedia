---
term: Search Algorithm
aliases: [State Space Search, A-star, Tree Search, MCTS, Monte Carlo Tree Search]
category: ai-foundations
subcategory: search-planning
depth: full
status: foundational
difficulty: intermediate
one_liner: "Systematically exploring possible moves or states to find one that reaches a goal."
tags: [symbolic]
relations:
  used_by: [reasoning-model, automated-planning]
  related_to: [reinforcement-learning, world-model, sampling]
prerequisites: [symbolic-ai]
encountered_in: [research-papers, interviews, conferences]
sources:
  - type: book
    title: "Artificial Intelligence: A Modern Approach, search chapters"
    url: https://aima.cs.berkeley.edu/
  - type: paper
    title: "Mastering the Game of Go with Deep Neural Networks and Tree Search (AlphaGo)"
    url: https://www.nature.com/articles/nature16961
    year: 2016
  - type: paper
    title: "Tree of Thoughts: Deliberate Problem Solving with Large Language Models"
    url: https://arxiv.org/abs/2305.10601
    year: 2023
updated: 2026-08-21
---

## Simple Explanation

You are at a state, several moves are available, each leads to a new state. Search
is the systematic exploration of that branching structure looking for a state
that satisfies your goal.

It was what "AI" mostly meant for thirty years, and it is quietly returning:
letting a model generate several candidate reasoning paths and evaluating them is
tree search with a neural network supplying the moves.

## Technical Definition

Exploration of a state space defined by an initial state, a successor function
and a goal test. Uninformed strategies (breadth-first, depth-first, uniform-cost)
explore blindly; informed strategies use a heuristic estimating distance to the
goal, with A* guaranteeing optimality when that heuristic never overestimates.
Monte Carlo Tree Search handles enormous branching factors by sampling
trajectories and concentrating effort on promising branches.

## Why Does It Exist?

Many problems are naturally states and transitions — puzzles, games, routes,
plans, proofs — and for those, the question is not what to compute but which
possibilities to examine and in what order.

## What Problem Does It Solve?

Finding a solution in a space too large to enumerate, by ordering exploration
intelligently.

## How Does It Work?

```text
              start
            /   |   \
          A     B     C          expand promising nodes first
         / \        /   \
        D   E      F     G       heuristic estimates distance to goal
             \
             GOAL                A* = cost so far + estimated cost remaining
```

The heuristic is everything. A good one turns an intractable search into a
direct walk; a bad one degenerates to brute force.

## Mental Model

A maze explored with a compass. Without the compass you flood every corridor;
with it you walk toward the exit, checking corners only when the compass is
uncertain.

## Formula

$$f(n) = g(n) + h(n)$$

* $g(n)$ — actual cost of the path from the start to node $n$.
* $h(n)$ — heuristic estimate of the remaining cost from $n$ to a goal.
* If $h$ never overestimates (it is *admissible*), A* is guaranteed to find an
  optimal path. Overestimate and it becomes fast and possibly wrong.

## Example

AlphaGo is the landmark synthesis: Go's branching factor defeats classical
search, so MCTS supplied the exploration while neural networks supplied the
heuristic — a policy network proposing plausible moves and a value network
estimating position strength. Neither component would have sufficed alone.

## Real-World Usage

Route planning, logistics, compilers, theorem provers, game engines. In LLM
systems the ideas have returned under new names: self-consistency samples several
chains and votes, tree-of-thought branches and evaluates, and reasoning models
trained with RL learn something functionally similar internally — exploring,
backtracking, discarding.

## Common Confusions

* **Search (AI) vs search (retrieval)** — exploring a state space versus finding
  documents. Entirely different problems sharing a word, and this encyclopedia
  covers both.
* **Search vs learning** — search explores a space you already know how to
  describe; learning infers structure from data. AlphaGo is interesting precisely
  because it combined them.
* **A heuristic is not a guarantee** — its quality determines everything, and
  designing one is where the domain knowledge goes.

## Why Should I Care?

It is the oldest idea in AI and one of the most quietly relevant now. Every
argument about whether language models can plan is, underneath, an argument about
whether they are doing search — and if so, how well.

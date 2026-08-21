---
term: Coding Agent
aliases: [Software Engineering Agent, SWE Agent, Autonomous Coding Agent, Agentic Coding]
category: ai-coding-culture
subcategory: practice
status: modern
difficulty: intermediate
one_liner: An agent that reads a codebase, edits files, runs commands and iterates until the tests pass.
origin:
  year: 2023
  circa: true
  attribution: SWE-agent and Devin popularised the category; command-line and IDE agents followed
historical_period: agentic
tags: [agents, culture]
relations:
  is_a: [ai-agent]
  depends_on: [agent-loop, tool-calling, reasoning-model]
  related_to: [vibe-coding, spec-driven-development, harness, ai-slop]
prerequisites: [ai-agent]
encountered_in: [github, production-systems, job-descriptions, social-media]
sources:
  - type: paper
    title: "SWE-bench: Can Language Models Resolve Real-World GitHub Issues?"
    url: https://arxiv.org/abs/2310.06770
    year: 2023
  - type: paper
    title: "SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering"
    url: https://arxiv.org/abs/2405.15793
    year: 2024
updated: 2026-08-21
review_by: 2026-12-01
---

## Simple Explanation

Not autocomplete. You describe a task; the agent explores the repository, decides
which files matter, makes edits, runs the tests, reads the failures and tries
again. You review the result rather than the keystrokes.

## Technical Definition

An agent whose tool surface is a development environment — file read and write,
search, shell execution, version control, test runners, sometimes a browser —
operating in a loop against a repository, usually in a sandbox, with the test
suite or type checker as the verifier.

## Why Does It Exist?

Software work has an unusual property: correctness is partly machine-checkable.
Tests, compilers and type checkers give an agent a reliable feedback signal that
most other domains lack, which is why coding became the first area where agents
worked well enough to deploy.

## What Problem Does It Solve?

The long tail of mechanical engineering work — migrations, test writing, bug
reproduction, refactors, dependency upgrades — where the intent is clear and the
execution is tedious.

## How Does It Work?

```text
task ──▶ explore (grep, read) ──▶ hypothesis ──▶ edit ──▶ run tests
             ▲                                                │
             └────────── read failure, revise ◀───────────────┘
                     until green, or budget exhausted
```

The quality of the harness — how files are presented, how test output is fed
back, how much context is retained — often matters more than which model is used.

## Mental Model

A junior engineer with the whole repository open, infinite patience for running
the test suite, and no memory of yesterday unless you write it down for them.

## Example

SWE-bench measures resolution of real GitHub issues. Scores rose from a few
percent in 2023 to a substantial majority of the verified subset by 2025 — a
pace that reflects harness and tooling improvements as much as model gains.

## Real-World Usage

Command-line agents, IDE-integrated agents, and asynchronous agents that open
pull requests from an issue. Teams that get value from them invest in the things
agents depend on: a fast reliable test suite, clear project conventions in a file
the agent reads, small reviewable diffs, and sandboxed execution.

## Common Confusions

* **Coding agent vs autocomplete** — completion predicts the next few lines
  inside your editor; an agent takes multi-step action across a repository.
* **Passing tests is not correctness** — agents optimise the verifier, including
  by weakening it. Review the diff, not the green tick.
* **Coding agent vs vibe coding** — the tool versus a way of using it. Vibe coding
  is accepting output without reading it; using an agent while reviewing every
  diff is not vibe coding.

## Why Should I Care?

It is the most commercially proven agent category, and it is reshaping what
software teams spend their time on: less typing, considerably more reviewing,
specifying and verifying.

---
term: Coding Agent
aliases: [Software Engineering Agent, SWE Agent, Autonomous Coding Agent, Agentic Coding]
category: ai-coding-culture
subcategory: practice
depth: full
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
  successor_of: [ai-pair-programming]
  depends_on: [agent-loop, tool-calling, reasoning-model, context-engineering, sandboxing]
  used_by: [prompt-to-app]
  related_to: [vibe-coding, spec-driven-development, harness, ai-slop, human-in-the-loop, evaluation-harness]
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
  - type: post
    title: "Building Effective Agents"
    url: https://www.anthropic.com/engineering/building-effective-agents
    year: 2024
updated: 2026-08-22
review_by: 2026-12-01
---

## Simple Explanation

Not autocomplete. You describe a task; the agent explores the repository, decides
which files matter, makes edits, runs the tests, reads the failures and tries
again. You review the result rather than the keystrokes.

It is the first agent category that genuinely worked in production, and the
reason is worth stating: software has a verifier. Tests either pass or they do
not, and an agent with a reliable signal can iterate its way out of being wrong.

## Technical Definition

An [agent](ai-agent.md) whose tool surface is a development environment — file
read and write, search, shell execution, version control, test runners, sometimes
a browser — operating in a loop against a repository, usually inside a
[sandbox](sandboxing.md), with the test suite or type checker as the verifier.

## Why Does It Exist?

Because correctness is partly machine-checkable here. Most domains give an agent
no feedback: write a marketing email and nothing tells you it was wrong. Write
code and the compiler, the type checker and the tests all have opinions, in
seconds, for free.

That feedback loop is the entire reason this category advanced faster than any
other agent application.

## What Problem Does It Solve?

The long tail of mechanical engineering work — migrations, test writing, bug
reproduction, refactors, dependency upgrades — where the intent is clear and the
execution is tedious.

## How Does It Work?

```text
task ──▶ explore (grep, read) ──▶ hypothesis ──▶ edit ──▶ run tests
             ▲                                                │
             └────────── read the failure, revise ◀───────────┘
                     until green, or the budget is exhausted

what actually determines success:
   how files and diffs are presented to the model
   how test output is truncated and fed back
   what the agent is allowed to run, and where
   when it is made to stop
```

The SWE-agent finding is the important one: holding the model constant and
redesigning only the *interface* — how the agent sees files, how errors are
reported, what commands exist — changed task success substantially. The
[harness](harness.md) is not glue around the interesting part; it is a large
share of the interesting part.

## Mental Model

A junior engineer with the whole repository open, infinite patience for running
the test suite, and no memory of yesterday unless you write it down for them.

## Example

SWE-bench measures resolution of real GitHub issues. Scores rose from a few
percent in 2023 to a substantial majority of the verified subset by 2025 — a pace
driven by harness and tooling improvements at least as much as by model gains.

The failure mode to watch for is more instructive than the score. An agent
optimising for "tests pass" will sometimes weaken the test, delete the assertion,
or special-case the failing input. This is [reward hacking](reward-hacking.md)
appearing in ordinary engineering work, and it is why *review the diff, not the
green tick* is the operative rule.

## Real-World Usage

Command-line agents, IDE-integrated agents, and asynchronous agents that open pull
requests from an issue. Teams that get value from them invest in the things
agents depend on:

* a fast, reliable test suite — the verifier is the whole loop
* project conventions in a file the agent reads at startup
* small, reviewable diffs rather than sweeping changes
* [sandboxed](sandboxing.md) execution with scoped credentials
* [approval gates](human-in-the-loop.md) before anything irreversible

## Common Confusions

* **Coding agent vs [autocomplete](ai-pair-programming.md)** — completion
  predicts the next few lines in your editor; an agent takes multi-step action
  across a repository. Different units of work, different review burden.
* **Passing tests is not correctness** — agents optimise the verifier, including
  by weakening it.
* **Coding agent vs [vibe coding](vibe-coding.md)** — the tool versus a way of
  using it. Reviewing every diff is not vibe coding.
* **The security surface is real** — an agent reads issues, comments and web
  pages, all of which are [attacker-influenced text](prompt-injection.md), while
  holding repository credentials.

## Why Should I Care?

It is the most commercially proven agent category, and it is reshaping what
software teams spend their time on: less typing, considerably more reviewing,
specifying and verifying. Whether that trade is good depends almost entirely on
whether the reviewing actually happens.

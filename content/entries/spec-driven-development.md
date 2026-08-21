---
term: Spec-Driven Development
aliases: [Specification-Driven Development, SDD, Spec-First Development]
category: ai-coding-culture
subcategory: practice
status: emerging
difficulty: intermediate
one_liner: Writing a precise specification and acceptance checks first, then letting an agent implement against them.
origin:
  year: 2025
  circa: true
  attribution: Named in practitioner writing and agent tooling during 2025; the underlying idea is older than AI
historical_period: agentic
tags: [culture, agents]
relations:
  different_from: [vibe-coding]
  alternative_to: [vibe-coding]
  depends_on: [coding-agent, evaluation-harness]
  related_to: [context-engineering]
prerequisites: [coding-agent]
encountered_in: [technical-blogs, github, job-descriptions, conferences]
sources:
  - type: repo
    title: "GitHub spec-kit — tooling for specification-driven development with agents"
    url: https://github.com/github/spec-kit
    year: 2025
updated: 2026-08-21
review_by: 2026-12-01
---

## Simple Explanation

If the agent will write the code, the leverage moves upstream. Spend your effort
stating precisely what "done" means — behaviour, constraints, edge cases, tests —
and let the agent handle implementation. The specification becomes the artefact
you maintain.

## Technical Definition

A development practice in which an executable or checkable specification precedes
implementation, and agent output is validated against it automatically. In LLM
application work the analogous practice is *eval-driven development*: define the
evaluation set before building the prompt or pipeline, and treat evaluation
scores as the acceptance criterion.

## Why Does It Exist?

When generating code is cheap, the bottleneck becomes knowing whether it is
right. Ambiguous requirements produce confidently wrong implementations quickly,
which is worse than producing them slowly.

## What Problem Does It Solve?

Underspecification, and the reviewing burden that unreviewed generated code
creates.

## How Does It Work?

```text
intent ──▶ specification ──▶ acceptance checks ──▶ agent implements
              ▲                                          │
              └────── spec updated when checks reveal ────┘
                      ambiguity, not the code patched around it
```

## Mental Model

Test-driven development with the roles shifted: you write the contract, the agent
writes the code, and the contract is the thing under version control that matters.

## Example

Instead of "add rate limiting", the spec states the limit, the window, the
identity key, the response code and headers on rejection, the behaviour when the
store is unavailable, and the tests that must pass. The agent's implementation
either satisfies it or does not, and review becomes checking the spec rather than
reading every line.

## Real-World Usage

Agent tooling that generates an implementation plan for approval before editing,
project convention files that state constraints once, and evaluation suites
written before the prompt they will judge.

## Terminology Note

Recent, fashionable, and overlapping with several older practices — TDD,
behaviour-driven development, design-by-contract. Sceptics note that "write down
what you want first" is not new advice. The defensible claim is narrower: when
implementation is nearly free, the *relative* value of precise specification
rises sharply, so a practice that was often skipped becomes the main lever.

## Common Confusions

* **Spec-driven vs waterfall** — specifications here are small, iterative and
  executable, not a document phase before coding begins.
* **A spec is not a prompt** — a prompt asks for work; a spec defines acceptance.
* **It does not remove review** — it changes what you review from
  implementation to acceptance criteria.

## Why Should I Care?

It is the considered counterpart to vibe coding, and the practice most teams
converge on once generated code has to survive contact with production.

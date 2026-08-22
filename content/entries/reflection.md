---
term: Reflection
aliases: [Self-Critique, Self-Correction, Self-Refine, Self-Verification]
category: agents
subcategory: cognition
depth: full
status: emerging
difficulty: intermediate
one_liner: "Having a model review and criticise its own output before acting on it or returning it."
origin:
  year: 2023
  attribution: Formalised in Reflexion and Self-Refine; the pattern appeared informally in agent projects before that
historical_period: agentic
tags: [agents]
relations:
  part_of: [agent-loop]
  related_to: [llm-as-a-judge, reasoning-model, chain-of-thought, evaluation-harness]
prerequisites: [agent-loop, chain-of-thought]
encountered_in: [research-papers, github, production-systems]
sources:
  - type: paper
    title: "Reflexion: Language Agents with Verbal Reinforcement Learning"
    url: https://arxiv.org/abs/2303.11366
    year: 2023
  - type: paper
    title: "Self-Refine: Iterative Refinement with Self-Feedback"
    url: https://arxiv.org/abs/2303.17651
    year: 2023
  - type: paper
    title: "Large Language Models Cannot Self-Correct Reasoning Yet"
    url: https://arxiv.org/abs/2310.01798
    year: 2023
updated: 2026-08-21
review_by: 2026-12-01
---

## Simple Explanation

Generate an answer, then ask the model to criticise it, then revise. It is an
appealing idea and it works — but only under a condition that is easy to miss and
easy to get wrong.

## Technical Definition

An agent pattern inserting an evaluation step between generation and acceptance.
The model, or a separate critic, assesses the output against criteria and
produces feedback that conditions a revision. Iterated until a stopping condition
or a step budget.

## Why Does It Exist?

A single generation commits immediately and cannot notice its own error. Adding a
review step gives the system a chance to catch mistakes before they propagate —
particularly valuable inside agent loops, where an early error compounds across
every subsequent step.

## What Problem Does It Solve?

Error detection and recovery, provided the errors are detectable.

## How Does It Work?

```text
generate ──▶ critique ──▶ revise ──▶ accept?
                ▲                        │ no
                └────────────────────────┘

the critique step is only useful if it has
something the generation step did not:
   test results · compiler errors · retrieved evidence ·
   a rubric · a different model · the user
```

## Mental Model

Proofreading your own essay. You will catch typos. You will not catch the
misunderstanding that shaped the argument, because the same understanding
produced both.

## Example

The important negative result: on reasoning tasks, models asked to self-correct
*without external feedback* frequently make things worse — changing correct
answers to incorrect ones, because a request to revise implies something was
wrong. Reported gains from pure self-critique often vanish under careful
evaluation.

The same pattern with *grounded* feedback works well. A coding agent that runs
the tests and reads the failure is reflecting against reality, not against
itself. That distinction is the whole entry.

## Real-World Usage

Coding agents iterating against test output; retrieval systems checking whether
retrieved passages actually support a claim; draft-then-review pipelines with a
rubric; multi-agent designs using a separate critic model. Production systems
overwhelmingly pair reflection with an external signal.

## Terminology Note

Loosely used. "Reflection" covers everything from a second prompt saying "check
your work" to a structured loop with verifiers and persistent memory of past
failures. When a framework advertises reflection, ask what the critique step has
access to that the generation step did not.

## Common Confusions

* **Self-correction without grounding is unreliable** — the single most important
  caveat, and the most commonly ignored.
* **Reflection vs reasoning models** — reasoning models do something functionally
  similar *inside* a single generation, trained in rather than orchestrated. That
  reduced the value of external reflection loops considerably.
* **It costs a multiple** — every reflection round is another generation. Two
  rounds triples your token bill for the step.

## Why Should I Care?

It is one of the most widely recommended agent patterns and one of the most
frequently misapplied. The rule to remember: reflection is worth its cost exactly
when the critic knows something the generator did not.

---
title: Agent vs Workflow
question: Should the model decide the steps, or should I?
sides: [ai-agent, ai-workflow]
---

## The short version

If you can draw the sequence in advance, write it as a workflow. Use an agent
only when the path genuinely depends on what earlier steps returned. The
distinction is not tooling — it is who chooses the next step.

## Side by side

| | Workflow | Agent |
|---|---|---|
| **Control flow** | Written by a developer | Chosen by the model at run time |
| **Predictability** | High; same path every run | Low; varies per request |
| **Debuggability** | Step-by-step, testable in isolation | Trace analysis over a trajectory |
| **Cost** | Bounded and known | Variable; needs step and spend caps |
| **Latency** | Predictable | Unbounded without limits |
| **Handles novelty** | Poorly | Well |
| **Failure mode** | Wrong branch not anticipated | Loops, drift, runaway spend |

## The test

Ask what happens on step three. If the answer is always the same action, it is a
workflow. If it depends on what step two returned in a way you cannot enumerate,
it is an agent.

## The usual mistake

Building an agent for a task with a fixed shape, because agents are the
interesting thing to build. The result is slower, dearer and less reliable than
five lines of orchestration, and considerably harder to debug when it fails.

## The hybrid, which is usually right

A workflow whose steps are mostly deterministic, with one genuinely open-ended
step delegated to an agent — bounded by a step budget, a sandbox and an
evaluation. You get predictability where the task is known and adaptability where
it is not.

## Verdict

Default to a workflow. Adopt agent autonomy where you can name the specific
uncertainty that requires it, and pay for that autonomy with budgets, guardrails
and traces.

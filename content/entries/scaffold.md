---
term: Scaffold
aliases: [Agent Scaffolding, Scaffolding, LLM Scaffold]
category: agent-engineering
subcategory: structure
status: contested
disputed: true
difficulty: intermediate
one_liner: The prompt structure and control flow arranged around a model to shape how it approaches a task — a term used both for agent structure and, in evaluation, for the rig that elicits a model's capability.
origin:
  year: 2023
  circa: true
  attribution: Adopted from educational psychology (Wood, Bruner and Ross, 1976) via AI evaluation work on eliciting model capability
historical_period: agentic
tags: [agents, culture]
relations:
  similar_to: [harness]
  different_from: [harness, prompt-engineering]
  part_of: [ai-agent]
  related_to: [context-engineering, evaluation-harness]
prerequisites: [prompt-engineering, ai-agent]
encountered_in: [research-papers, technical-blogs, social-media, conferences]
sources:
  - type: paper
    title: "SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering"
    url: https://arxiv.org/abs/2405.15793
    year: 2024
  - type: paper
    title: "The Role of Tutoring in Problem Solving (origin of 'scaffolding')"
    url: https://acamh.onlinelibrary.wiley.com/doi/10.1111/j.1469-7610.1976.tb00381.x
    year: 1976
updated: 2026-08-21
review_by: 2026-12-01
---

## Simple Explanation

Give a model a hard task cold and it flounders. Give it structure — break the
problem into stages, require a plan first, force it to check its work, provide a
place to keep notes — and the same model does much better. That imposed structure
is the scaffold.

## Technical Definition

The externally imposed structure that shapes a model's approach to a task:
decomposition into phases, mandated intermediate artefacts (plans, checklists,
critiques), the format of the action space, and the control flow between steps.
In AI evaluation the term denotes the surrounding apparatus used to elicit a
model's capability, and results are reported as model-plus-scaffold because the
pair is what was measured.

## Why Does It Exist?

The educational metaphor is apt: temporary support that lets a learner complete
something beyond their unaided reach. In evaluation the concept became necessary
because the same model scores wildly differently under different scaffolds, so
reporting a bare model score is close to meaningless.

## What Problem Does It Solve?

The gap between what a model *can* do and what it does when simply asked.

## How Does It Work?

```text
unscaffolded:  task ──▶ model ──▶ attempt
scaffolded:    task ──▶ [understand] ──▶ [plan] ──▶ [execute step]
                              ▲                          │
                              └──── [verify, revise] ◀────┘
```

## Mental Model

Builder's scaffolding: structure erected around the work, not part of the
finished building, and removed when no longer needed. The metaphor carries a
prediction — as models improve, some scaffolding becomes unnecessary, which is
exactly what happened to elaborate chain-of-thought scaffolds after reasoning
models arrived.

## Terminology Note

Contested, and colliding with [harness](harness.md):

* In **agent engineering**, scaffold usually means the prompt-and-flow structure
  around the model, while harness leans toward the executing runtime. Many
  engineers use both words for the same thing.
* In **evaluation and safety research**, scaffolding specifically means the
  apparatus used to elicit capability, and the phrase "capability under
  scaffolding" is a term of art in dangerous-capability assessment.
* Some practitioners use **scaffold** pejoratively, for structure that
  compensates for a weak model and should disappear as models improve.

None of these is authoritative. Ask whether someone means prompt structure,
runtime, or evaluation apparatus.

## Example

Reported agent results on the same benchmark can differ by tens of percentage
points between scaffolds with the same underlying model. This is why credible
evaluations publish the scaffold, and why comparing two agent products tells you
little about the models inside them.

## Real-World Usage

Agent frameworks, benchmark submissions, and safety evaluations where the
question is what a model can be made to do with strong elicitation.

## Common Confusions

* **Scaffold vs prompt engineering** — prompt engineering optimises the wording
  of one request; scaffolding structures a multi-step process.
* **Scaffold vs harness** — see above. Treat them as overlapping, not distinct.
* **Scaffolding is not permanent** — much of it is a workaround for current model
  limitations, and reasoning models absorbed a good deal of it.

## Why Should I Care?

Any claim of the form "model X gets Y% on this task" is incomplete without the
scaffold, and knowing that lets you read agent benchmarks with appropriate
scepticism.

---
term: AI Engineer
aliases: [Agent Engineer, LLM Engineer, Applied AI Engineer, Forward Deployed Engineer]
category: ai-coding-culture
subcategory: roles
depth: full
status: emerging
difficulty: beginner
one_liner: "The role that builds products on top of existing models rather than training new ones, which is now most AI work."
origin:
  year: 2023
  attribution: Named in practitioner writing as a distinct role from ML engineer and research scientist
historical_period: agentic
tags: [culture]
relations:
  related_to: [context-engineering, evaluation-harness, harness, ai-pair-programming, ai-native]
prerequisites: [large-language-model]
encountered_in: [job-descriptions, conferences, social-media, technical-blogs]
sources:
  - type: post
    title: "The Rise of the AI Engineer"
    url: https://www.latent.space/p/ai-engineer
    year: 2023
  - type: post
    title: "Building Effective Agents"
    url: https://www.anthropic.com/engineering/building-effective-agents
    year: 2024
updated: 2026-08-21
review_by: 2026-12-01
---

## Simple Explanation

Before foundation models, using AI meant training a model, which meant knowing
statistics, GPUs and a great deal of maths. Now the model exists and is available
through an API, and the hard parts have moved: what goes in the context, which
tools it can call, how you know it works, what happens when it fails, and what it
costs per request.

The people doing that are mostly software engineers, not researchers. The term
names that shift.

## Technical Definition

A software engineering role specialising in building applications on pretrained
models: prompt and context design, retrieval systems, tool and agent
architecture, evaluation harnesses, guardrails and observability, and the
cost-latency-quality trade-offs of serving. Distinguished from the ML engineer
(who trains and deploys models) and the research scientist (who develops methods).

## Why Does It Exist?

Because the bottleneck moved. When capability lives in a model anyone can call,
competitive advantage comes from the system around it — the context, the tools,
the evaluation, the interface. That is engineering work, and it needed a name so
that job descriptions could stop demanding a PhD for it.

## What Problem Does It Solve?

A hiring and self-description problem, mostly. It let a large group of software
engineers recognise that the work was open to them.

## How Does It Work?

```text
what the role actually spends time on, roughly in order:

  evaluation      building and maintaining the suite that says if it works
  context         retrieval, prompts, memory, what the model sees
  integration     tools, protocols, APIs, the surrounding application
  reliability     guardrails, fallbacks, error handling, observability
  cost & latency  routing, caching, model selection
  the model       choosing one, occasionally fine-tuning
```

The ordering surprises people. Model selection is near the bottom.

## Mental Model

A backend engineer whose most unreliable dependency is also its most capable one,
and who therefore spends most of their time on the interface to it.

## Example

The most common failure in this role is reaching for the model when the problem
is elsewhere: fine-tuning to fix what was a retrieval failure, or switching model
to fix what was a context-ordering problem. The distinguishing skill is
diagnosis — knowing which layer a problem lives in — and that requires an
evaluation set, which is why evaluation sits at the top of the list.

## Real-World Usage

The title now appears widely in job listings, at conferences organised around the
role, and as the framing for a large body of practitioner writing. In
organisations it typically sits inside a product team rather than a research
group, which is itself the point: the work is shipping software, and the model is
a dependency rather than the subject.

## Terminology Note

Contested at the edges. Some treat it as a genuinely new discipline; others as
"backend engineer who has used an API", and argue the title inflates ordinary
application work. Both readings have merit. What is defensible: the *knowledge
set* is real and non-obvious — context budgeting, evaluation design, agent
failure modes, inference economics — and it is not covered by either traditional
ML or traditional backend training.

Adjacent titles in current use: **agent engineer** (narrower, agent systems),
**LLM engineer** (often includes fine-tuning), **forward deployed engineer**
(building on models directly with customers).

## Common Confusions

* **AI engineer vs ML engineer** — builds with models versus builds models. The
  ML engineer's job did not disappear; it became a different, smaller field.
* **It does not require a research background** — and job descriptions demanding
  one for this work are usually miscategorised.
* **Prompting is not the skill** — it is the entry point. Evaluation and system
  design are the job.

## Why Should I Care?

If you are reading this encyclopedia to work in AI, this is most likely the role
you are heading toward, and it tells you what to learn: the middle of the stack,
not the model.

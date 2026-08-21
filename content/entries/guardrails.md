---
term: Guardrails
aliases: [Safety Filters, Policy Enforcement, Content Filters, Output Validation]
category: agent-engineering
subcategory: control
status: established
difficulty: intermediate
one_liner: Checks and limits placed around a model so unacceptable inputs, outputs or actions are blocked by code rather than trusted to the model.
origin:
  year: 2023
  circa: true
  attribution: Practitioner term that spread with LLM application frameworks
historical_period: agentic
tags: [safety, agents]
relations:
  part_of: [harness]
  depends_on: [tool-calling]
  related_to: [prompt-injection, alignment, evaluation-harness]
prerequisites: [ai-agent]
encountered_in: [production-systems, job-descriptions, documentation]
sources:
  - type: docs
    title: "OWASP Top 10 for LLM Applications"
    url: https://owasp.org/www-project-top-10-for-large-language-model-applications/
  - type: docs
    title: "NIST AI Risk Management Framework"
    url: https://www.nist.gov/itl/ai-risk-management-framework
updated: 2026-08-21
---

## Simple Explanation

Do not ask the model nicely to avoid doing something dangerous — make it
impossible. Validate inputs, validate outputs, restrict what tools exist, require
approval for irreversible actions, and cap what a loop can spend.

## Technical Definition

Deterministic controls surrounding a probabilistic component: input classification
and filtering, output schema validation and content checks, tool allow-lists and
scoped credentials, human-in-the-loop approval gates, sandboxing, rate and cost
limits, and egress restrictions.

## Why Does It Exist?

Model behaviour is a distribution, not a guarantee. Anything that must never
happen cannot be enforced by a prompt, because prompts are advisory.

## What Problem Does It Solve?

The gap between "usually behaves correctly" and "cannot do this particular
thing".

## How Does It Work?

```text
input ──▶ [validate, classify] ──▶ model ──▶ [schema check, policy check]
                                       │
                              tool call ▼
                          [allow-list · permission · sandbox · approval]
                                       │
                                    execute, log, trace
```

## Mental Model

Guard rails on a mountain road. They do not steer; they bound the consequences of
steering badly.

## Example

An agent with database access should hold read-only credentials, not be
instructed not to write. The first is a guardrail; the second is a hope. The same
logic applies to network egress, file system scope and spend caps.

## Real-World Usage

Content classifiers on input and output, JSON schema validation, allow-listed
tools, scoped tokens, container sandboxes, approval gates on irreversible
actions, and full tracing for after-the-fact review.

## Common Confusions

* **Guardrails are not alignment** — they constrain a deployed system; alignment
  concerns what the model is trying to do.
* **Prompt instructions are not guardrails** — they can be overridden by
  injection or simply ignored.
* **Filters have both error types** — over-blocking degrades the product;
  under-blocking is the incident. Both need measuring.

## Why Should I Care?

The difference between a demo and a deployable system is almost entirely here,
and it is what a security review will ask about first.

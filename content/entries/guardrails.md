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
diagram:
  kind: figure
  title: Checks on the way in, on the way out, and around every tool call
  footer: The output checks catch what the model got wrong. The tool-call checks catch what an attacker
    got right — and those are the ones that stop an injected instruction becoming an action.
  visual:
    kind: pipeline
    width: 740
    caption: none of these depend on the model behaving; that is what makes them guardrails rather than
      instructions
    stages:
    - text: the request
      note: possibly hostile
    - text: accepted input
      via: validate shape · classify intent · rate-limit
    - text: a candidate response
      via: the model runs
    - text: a checked response
      via: schema check · policy check · citation check
    - text: an executed action
      tone: accent
      via: allow-list · permission · sandbox · human approval when irreversible
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


Guardrails are checks in the code path, not instructions in the prompt. The
distinction matters because a prompt is a request the model may decline, ignore,
or be argued out of, while a check in the harness runs whatever the model
decided.

They sit at three points. On the way in: validate the shape of the request,
classify intent, apply rate limits. On the way out: check the response against a
schema, against policy, against whether its citations resolve. And around every
tool call: an allow-list of what may be invoked, permissions on what each tool
may touch, a sandbox around execution, and a human before anything irreversible.

The output checks catch the model being wrong. The tool-call checks catch
something else — an attacker being right. When injected text has persuaded the
agent to do something, the model is functioning perfectly and the only thing
between the instruction and the action is the permission check. That is why the
tool boundary deserves the strictest guardrail in the system.

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

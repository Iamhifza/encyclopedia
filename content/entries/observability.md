---
term: Observability
aliases: [Tracing, LLM Observability, Monitoring, Spans, Telemetry]
category: evaluation-safety
subcategory: operations
depth: full
status: established
difficulty: intermediate
one_liner: "Recording every prompt, tool call and response so you can reconstruct what a system actually did when it went wrong."
historical_period: agentic
tags: [safety, agents]
relations:
  part_of: [harness]
  related_to: [evaluation-harness, drift, agent-loop, ai-gateway, guardrails]
prerequisites: [ai-agent]
encountered_in: [production-systems, job-descriptions, github]
sources:
  - type: spec
    title: "OpenTelemetry semantic conventions for generative AI"
    url: https://opentelemetry.io/docs/specs/semconv/gen-ai/
  - type: docs
    title: "OWASP Top 10 for LLM Applications"
    url: https://owasp.org/www-project-top-10-for-large-language-model-applications/
updated: 2026-08-21
---

## Simple Explanation

An agent took twenty steps and produced something wrong. Which step broke it? You
cannot rerun it — the model is stochastic and the world has moved on. Unless you
recorded the whole trajectory as it happened, the answer is unrecoverable.

That is the difference from ordinary software debugging, and it is why
observability is not optional here.

## Technical Definition

Structured capture of a system's execution: a trace per request, spans per model
call and tool invocation, each with inputs, outputs, token counts, latency,
model version, sampling parameters and errors. Aggregated, it supports cost
attribution, latency analysis, failure clustering and regression detection.

## Why Does It Exist?

Three properties make LLM systems opaquer than normal services: outputs are
non-deterministic, failures are semantic rather than exceptional (the code
returned 200 and the answer was wrong), and behaviour changes when a provider
updates a model underneath you without notice.

## What Problem Does It Solve?

Debuggability after the fact, and detection of the failure mode that has no
exception attached — quietly degrading quality.

## How Does It Work?

```text
trace: "user asked to reconcile invoices"
 ├─ span: LLM call        prompt, response, 4.1k tokens, 820ms, temp 0
 ├─ span: tool search     args, result, 120ms
 ├─ span: LLM call        ...
 ├─ span: tool write      DENIED by policy       ← the interesting line
 └─ span: LLM call        final answer

aggregate across traces:
   cost per user · p95 latency · failure clusters · eval scores over time
```

## Mental Model

A flight recorder. Nobody reads it when the flight is fine; when it is not, it is
the only thing that can tell you what happened.

## Example

An agent starts failing on Tuesdays. Traces show tool calls timing out only when
a particular upstream service is slow, and the model responding to the timeout by
inventing a plausible result rather than reporting failure. Without traces you
would see "the agent is unreliable"; with them you see a missing error path and a
prompt that never told the model what to do when a tool fails.

## Real-World Usage

Dedicated LLM observability platforms, tracing built into agent frameworks, and
OpenTelemetry's generative-AI semantic conventions for teams that want this
inside their existing monitoring. The AI gateway is a natural collection point,
since everything passes through it anyway.

Production traces have a second, larger use: they are the best source of
evaluation cases. Real failures beat invented ones.

## Common Confusions

* **Observability is not evaluation** — one records what happened, the other
  judges whether it was good. They compose: traces supply the cases, evals score
  them.
* **Logging prompts is a data-protection decision** — you are now storing
  everything users typed, potentially including personal or confidential
  information. Retention limits and redaction are part of the design, not an
  afterthought.
* **Sampling loses the tail** — recording 1% of traces is cheap and will miss
  exactly the rare failures you needed.

## Why Should I Care?

The gap between a demo and a system you can operate is mostly this. When someone
reports that the agent "did something strange last Thursday", either you can
answer or you cannot.

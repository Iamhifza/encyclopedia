---
term: AI Gateway
aliases: [LLM Gateway, Model Proxy, LLM Proxy]
category: protocols
subcategory: infrastructure
depth: full
status: modern
difficulty: intermediate
one_liner: "A single endpoint in front of many model providers that handles keys, quotas, retries, logging and cost tracking."
historical_period: agentic
tags: [protocol]
relations:
  used_by: [model-routing]
  related_to: [guardrails, throughput, observability, mcp]
prerequisites: [large-language-model]
encountered_in: [production-systems, job-descriptions, documentation]
sources:
  - type: repo
    title: "LiteLLM — an open-source LLM gateway"
    url: https://github.com/BerriAI/litellm
  - type: docs
    title: "OWASP Top 10 for LLM Applications"
    url: https://owasp.org/www-project-top-10-for-large-language-model-applications/
updated: 2026-08-21
review_by: 2027-02-01
---

## Simple Explanation

Once more than one team is calling more than one model provider, the same
problems appear everywhere at once: who holds the API keys, what happens when a
provider is down, which team spent what, and how do you swap models without
editing twelve services. A gateway is one endpoint in front of all of it.

## Technical Definition

A reverse proxy for model APIs, normalising provider-specific formats behind a
single interface — usually an OpenAI-compatible one — and centralising
authentication, key management, rate limiting, retries and failover, caching,
request and response logging, cost attribution, and policy enforcement.

## Why Does It Exist?

Because these concerns are identical for every application and nobody wants to
implement them twelve times. It is the same argument that produced API gateways
in ordinary service architecture, applied to a new backend.

## What Problem Does It Solve?

Key sprawl, unattributable spend, vendor lock-in, and the absence of any single
place to enforce policy or see what is actually being sent to models.

## How Does It Work?

```text
   your services
        │  one API, one credential
        ▼
┌────────────────── GATEWAY ──────────────────┐
│ auth · quotas · routing · retries/failover  │
│ caching · logging · cost attribution        │
│ guardrails: PII redaction, content policy   │
└──────┬──────────────┬──────────────┬────────┘
       ▼              ▼              ▼
  provider A     provider B     self-hosted vLLM
```

Because everything passes through one point, it is also the natural home for
model routing and for the observability that agent debugging depends on.

## Mental Model

A switchboard. Callers dial one number; the board knows who is available, who is
allowed to call whom, and it keeps the record of every call.

## Example

Swapping a workload from a hosted provider to a self-hosted open-weight model
behind vLLM is a configuration change at the gateway rather than a code change in
every service. That portability is often the reason to adopt one before the cost
tracking is.

## Real-World Usage

Open-source gateways (LiteLLM and others), commercial products, and internally
built proxies at most organisations of any size. They typically expose an
OpenAI-compatible interface because so much client tooling already speaks it.

## Common Confusions

* **Gateway vs router** — the gateway is the infrastructure; routing is one
  policy it can implement. A gateway with no routing is still useful.
* **Gateway vs MCP** — unrelated layers. The gateway sits between your code and
  *models*; MCP sits between your application and *tools and data*.
* **It adds a hop** — one more network round trip and one more thing that can
  fail. Worth it at scale, overhead for a single small service.
* **Logging is a liability as well as an asset** — the gateway now holds every
  prompt, which may include personal or confidential data. Retention and
  redaction policy is not optional.

## Why Should I Care?

The first serious question an infrastructure or security review asks about an AI
product is where the keys live and who can see the prompts. This is the answer,
and building it late is considerably more painful than building it early.

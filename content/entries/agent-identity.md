---
term: Agent Identity
aliases: [Agent Authentication, Agent Authorisation, Delegated Authority, Machine Identity]
category: protocols
subcategory: infrastructure
depth: full
status: emerging
difficulty: advanced
one_liner: "Establishing who an agent is acting for and what it is permitted to do on their behalf."
origin:
  year: 2025
  circa: true
  attribution: An open problem raised by agent deployment; drawing on OAuth delegation and workload identity practice
historical_period: agentic
tags: [protocol, safety]
relations:
  depends_on: [a2a]
  related_to: [guardrails, prompt-injection, mcp, sandboxing, human-in-the-loop]
prerequisites: [ai-agent, mcp]
encountered_in: [conferences, technical-blogs, standards, production-systems]
sources:
  - type: spec
    title: "OAuth 2.0 Authorization Framework"
    url: https://datatracker.ietf.org/doc/html/rfc6749
  - type: spec
    title: "Model Context Protocol — authorisation"
    url: https://modelcontextprotocol.io/
  - type: docs
    title: "OWASP Top 10 for LLM Applications"
    url: https://owasp.org/www-project-top-10-for-large-language-model-applications/
updated: 2026-08-21
review_by: 2026-12-01
---

## Simple Explanation

An agent books a flight. Whose credit card, whose authority, and how does the
airline know? Existing systems recognise two things: a human logging in, or a
service with an API key. An agent acting *on behalf of* a specific person, with a
subset of that person's authority, for a bounded task, fits neither.

This is largely unsolved, and it is the gap most likely to hold back agents doing
anything consequential.

## Technical Definition

The problem of authenticating an autonomous agent and scoping its authority.
Components: an identity for the agent distinct from its principal, a verifiable
delegation from that principal, scope constraints (what actions, what resources,
what limits), a time or task bound, an audit trail attributing actions to both
agent and principal, and revocation.

## Why Does It Exist?

Current practice is to hand the agent the user's credentials, or a service
account's. Both are wrong in the same way: the agent receives the *whole* of that
identity's authority, when the task required a sliver of it. Combine that with
prompt injection and the consequences are unbounded.

## What Problem Does It Solve?

Least privilege for non-human actors, and accountability — being able to say
afterwards which agent did what, for whom, under whose authority.

## How Does It Work?

```text
user ──delegates──▶ agent ──acts on──▶ resource

what the delegation should carry:
  principal   : who authorised this
  agent id    : which agent, which version
  scope       : read invoices · no writes · no external send
  limits      : £200 · 20 actions · expires in 1 hour
  audit       : every action attributable to both parties
  revocation  : the principal can withdraw it immediately
```

The building blocks exist — OAuth delegation, short-lived scoped tokens, workload
identity — but they were designed for services with fixed behaviour, not for
actors whose next action is decided by a model reading untrusted text.

## Mental Model

Power of attorney rather than handing over your wallet. Specific, bounded,
revocable, and documented — which is exactly what an API key is not.

## Example

The concrete danger: an agent given a personal access token to "check the repo"
now holds the ability to force-push, delete branches and read every private
repository that token can reach. If a poisoned issue comment convinces it to act,
the credential does not distinguish the agent's intent from the user's. Scoped,
short-lived, task-bound credentials are the mitigation — and issuing them per
task is operationally harder than it sounds.

## Real-World Usage

Emerging rather than settled. MCP has an authorisation specification, A2A carries
identity in its Agent Card, and enterprise deployments generally handle this with
existing machinery — scoped service accounts, short-lived tokens, per-agent
identities in an existing identity provider. Standards work is active and
unconsolidated.

## Terminology Note

Vocabulary is unsettled: *agent identity*, *machine identity*, *non-human
identity*, *workload identity* and *delegated authority* are used with
overlapping meanings by different vendors and standards bodies. Treat claims that
this is solved with scepticism — it is an area where the marketing is well ahead
of the practice.

## Common Confusions

* **Authentication is not authorisation** — knowing which agent this is does not
  settle what it may do.
* **An API key is not an identity** — it is a bearer token conveying whatever
  authority it was issued with, to whoever holds it.
* **This is not a model problem** — no amount of alignment fixes an
  over-privileged credential.

## Why Should I Care?

Every serious discussion about agents doing consequential work eventually arrives
here, and it is currently the weakest link between capable agents and
deployments anyone should be comfortable with.

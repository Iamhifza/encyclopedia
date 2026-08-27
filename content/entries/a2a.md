---
term: A2A
aliases: [Agent-to-Agent Protocol, Agent2Agent]
category: protocols
subcategory: agent-protocols
status: emerging
difficulty: advanced
one_liner: A protocol for agents built by different teams to discover each other and delegate tasks, rather than calling tools.
origin:
  year: 2025
  attribution: Announced by Google in April 2025 with partner organisations; subsequently placed under open governance
historical_period: agentic
diagram:
  kind: figure
  title: Agents as long-running peers, not as tools
  footer: The distinction from MCP is the unit of work. A tool call returns; an A2A task may run for hours,
    stream progress, and be checked on — which is why it needs its own protocol rather than a longer timeout.
  visual:
    kind: pipeline
    width: 740
    caption: neither agent sees the other's internals — only the card, the task and what comes back
    stages:
    - text: fetch the Agent Card
      note: capabilities, auth, endpoints
    - text: create a task
      via: a goal, not a function call
    - text: streaming status updates
      note: minutes to hours
      via: the remote agent works autonomously
    - text: artefacts and a result
      tone: accent
      via: returned when the task completes, or fails
tags: [protocol, agents]
relations:
  different_from: [mcp]
  depends_on: [multi-agent-system]
  related_to: [tool-calling]
prerequisites: [ai-agent, mcp]
encountered_in: [documentation, conferences, technical-blogs]
sources:
  - type: spec
    title: "A2A Protocol specification"
    url: https://a2a-protocol.org/
    year: 2025
  - type: repo
    title: "a2aproject/A2A"
    url: https://github.com/a2aproject/A2A
updated: 2026-08-21
review_by: 2026-12-01
---

## Simple Explanation

MCP lets an agent use tools. A2A lets an agent hand a task to *another agent* it
did not build and may not be able to inspect — one that has its own tools, its
own model and its own opinions about how to do the job.

## Technical Definition

An HTTP-based protocol in which agents publish an **Agent Card** describing
identity, capabilities and authentication requirements, and exchange **tasks**
with defined lifecycle states. Long-running work is supported through streaming
updates and push notifications; agents remain opaque to each other, exposing
capability rather than internal state.

## Why Does It Exist?

Enterprise deployments increasingly involve agents owned by different teams and
vendors. Wrapping every peer agent as a tool loses what matters about a peer:
that the task is delegated, may run for hours, and returns progress rather than a
single value.

## What Problem Does It Solve?

Cross-organisational delegation: discovery, identity, authentication and
long-running task lifecycle between independently built agents.

## How Does It Work?


An agent publishes an Agent Card — a document describing what it can do, how to
authenticate, and where to send work. Another agent fetches that card, creates a
task rather than calling a function, and receives streaming status updates while
the remote agent works.

The unit of work is what distinguishes this from MCP. A tool call is a request
and a response, usually in under a second. An A2A task is a goal handed to a peer
that may work on it for minutes or hours, report progress, ask a clarifying
question, and eventually return artefacts. Neither side sees the other's
internals, its model, or its own tools.

Whether this layer is needed is still open. Much of what gets described as
multi-agent collaboration is one system calling another over an ordinary API, and
a protocol earns its place only when agents genuinely need to discover each other
and coordinate long-running work across organisational boundaries. That case
exists; it is rarer than the enthusiasm suggests.

## Mental Model

MCP is hiring a tool; A2A is subcontracting to another firm. You care about their
credentials, what they can take on, and progress reports — not their internal
process.

## Example

A procurement agent delegates supplier risk assessment to a vendor's compliance
agent. It never sees that agent's prompts, model or tools; it receives a task
identifier, progress updates and a final artefact.

## Terminology Note

Agent interoperability is an unsettled area with several competing and
overlapping efforts, and adoption is far behind MCP as of mid-2026. Treat
specific claims about "the standard" for agent communication with caution, and
check current adoption rather than announcement-era coverage.

## Real-World Usage

Early enterprise pilots for cross-vendor agent delegation, and reference
implementations from the specification's maintainers. Production adoption remains
limited compared with MCP.

## Differences

* **A2A vs MCP** — peers versus tools. MCP servers expose typed capabilities to
  one agent; A2A counterparties are autonomous, opaque and long-running. They are
  complementary: an agent commonly uses MCP internally and A2A externally.
* **A2A vs a plain API call** — the protocol carries capability discovery,
  identity and task lifecycle, which a bare REST call does not.

## Common Confusions

* **It does not make agents interoperable by itself** — it standardises the
  envelope, not whether two agents understand the same task semantics.
* **Identity and authorisation are the hard part** — deciding what another
  organisation's agent may do on your behalf is a governance problem, not a
  protocol one.

## Why Should I Care?

If multi-agent systems cross organisational boundaries, something like this is
needed. Whether this particular protocol wins is genuinely open, so learn the
problem shape rather than the specific field names.

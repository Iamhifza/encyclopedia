---
term: MCP
aliases: [Model Context Protocol, MCP Server, MCP Client]
category: protocols
subcategory: mcp
status: modern
difficulty: intermediate
one_liner: An open protocol that lets any AI application connect to any tool or data source through one standard interface instead of a custom integration each time.
origin:
  year: 2024
  attribution: Introduced by Anthropic in November 2024; subsequently adopted across the industry and donated to open governance
historical_period: agentic
tags: [protocol, agents]
relations:
  successor_of: [tool-calling]
  depends_on: [tool-calling]
  different_from: [a2a]
  used_by: [ai-agent, coding-agent]
  related_to: [agent-skills, prompt-injection]
prerequisites: [tool-calling]
encountered_in: [documentation, github, production-systems, job-descriptions, conferences]
sources:
  - type: spec
    title: "Model Context Protocol specification"
    url: https://modelcontextprotocol.io/
    year: 2024
  - type: repo
    title: "modelcontextprotocol — reference implementations"
    url: https://github.com/modelcontextprotocol
updated: 2026-08-21
review_by: 2026-12-01
---

## Simple Explanation

Every AI application that wanted access to GitHub, Slack, a database or a file
system used to write its own integration for each one. With $M$ applications and
$N$ systems that is $M \times N$ integrations. MCP defines one protocol: a system
exposes an MCP server once, and every MCP-speaking application can use it.

## Technical Definition

A JSON-RPC 2.0 protocol between *hosts* (AI applications, containing clients) and
*servers* (processes exposing capabilities). Servers offer three primitives:
**tools** (model-invoked functions), **resources** (application-controlled
context, addressed by URI) and **prompts** (user-selected templates). Transports
are stdio for local servers and streamable HTTP for remote ones. Sessions
negotiate capabilities at initialisation.

## Why Does It Exist?

The integration problem is old and the solution shape is familiar: LSP did it for
editors and language tooling, ODBC for databases. Tool calling standardised how a
*model* requests an action, but not how an *application* discovers and connects
to the thing that performs it.

## What Problem Does It Solve?

Combinatorial integration cost, and the lock-in that follows from every AI
product having its own plugin ecosystem.

## How Does It Work?

```text
   AI application (host)              your systems
   ┌──────────────┐    JSON-RPC     ┌─────────────────┐
   │  MCP client  │◀───────────────▶│ MCP server: git │
   │  MCP client  │◀───────────────▶│ MCP server: db  │
   │  MCP client  │◀───────────────▶│ MCP server: crm │
   └──────────────┘                 └─────────────────┘
        │  initialise → list tools/resources → call
        ▼
      model sees the tools and asks for one
```

## Mental Model

USB-C for AI applications. The port is standard; what you plug in is up to you,
and neither side needs to know about the other in advance.

## Example

A local MCP server exposing a `query_database` tool works unchanged in any
MCP-compatible client — the same server, no rewrite per application. That
portability is the entire point.

## Real-World Usage

Widely adopted since 2025 across AI coding tools, desktop assistants and
enterprise platforms, with servers for source control, issue trackers,
databases, browsers, cloud consoles and internal systems.

## Differences

* **MCP vs an API** — MCP does not replace APIs; servers usually wrap them. It
  standardises *description and discovery* so a model can find and use a
  capability without bespoke integration code.
* **MCP vs tool calling** — tool calling is between the model and the
  application; MCP is between the application and external systems. A tool
  discovered over MCP is still invoked through ordinary tool calling.
* **MCP vs A2A** — MCP connects an agent to tools and data; A2A connects agents
  to each other as peers. Vertical versus horizontal.

## Common Confusions

* **MCP is not a model feature** — the model never speaks MCP. The host does.
* **Connecting a server is granting access** — an MCP server runs with whatever
  credentials you give it, and its returned content enters the context window.
  Untrusted servers are an indirect prompt injection vector, and the combination
  of private data, untrusted content and external communication is the dangerous
  one.
* **More servers is not better** — every connected server adds tools, and tool
  selection degrades as the list grows.

## Why Should I Care?

It is the closest thing the agent ecosystem has to a standard integration layer,
and it is now a common line item in job descriptions and platform requirements.

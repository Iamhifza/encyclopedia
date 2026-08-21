---
title: MCP vs A2A
question: Is the thing on the other end a tool or a peer?
sides: [mcp, a2a]
---

## The short version

MCP connects an agent **downward** to tools and data. A2A connects an agent
**sideways** to other agents. They are complementary, and an agent may well speak
both — MCP internally to reach its systems, A2A externally to delegate.

## Side by side

| | MCP | A2A |
|---|---|---|
| **Other end is** | A capability: tool, resource, prompt | An autonomous agent |
| **Interaction** | Call and return | Task delegation with a lifecycle |
| **Duration** | Typically a single request | Minutes to hours, with progress updates |
| **Counterparty state** | Stateless or session-scoped | Opaque; it has its own reasoning and tools |
| **Discovery** | Capability negotiation at initialisation | Agent Card describing skills and auth |
| **Transport** | stdio, streamable HTTP (JSON-RPC) | HTTP |
| **Introduced** | Late 2024 | Mid 2025 |
| **Adoption (mid-2026)** | Broad | Early |

## Where the line actually falls

Wrap a peer agent as an MCP tool and you lose what makes it a peer: it cannot
report progress on a two-hour task, it has no independent identity, and its
autonomy is hidden behind a function signature. Conversely, using an agent
protocol to fetch a database row is pure overhead.

```text
        ┌─────────────┐   A2A   ┌─────────────┐
        │   agent A   │◀───────▶│   agent B   │   peers, opaque, long-running
        └──────┬──────┘         └──────┬──────┘
           MCP │                       │ MCP
        ┌──────▼──────┐         ┌──────▼──────┐
        │ tools, data │         │ tools, data │   capabilities, typed, fast
        └─────────────┘         └─────────────┘
```

## Both are envelopes, not agreements

Neither protocol makes two systems understand each other. They standardise
discovery, transport and lifecycle. Whether agent B interprets your task the way
you meant is a semantics and governance problem that no wire format solves.

## Verdict

Use MCP now; it is widely adopted and solves an immediate problem. Treat
agent-to-agent protocols as an unsettled area: learn the shape of the problem —
identity, delegation, long-running tasks, authorisation across organisational
boundaries — rather than committing to specific field names.

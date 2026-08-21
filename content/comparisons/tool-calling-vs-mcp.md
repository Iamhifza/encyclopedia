---
title: Tool Calling vs MCP
question: Does MCP replace function calling?
sides: [tool-calling, mcp]
---

## The short version

No — MCP feeds it. Tool calling is the convention between the **model and your
application**. MCP is the protocol between **your application and external
systems**. A tool discovered over MCP is still invoked through ordinary tool
calling.

## Side by side

| | Tool calling | MCP |
|---|---|---|
| **Sits between** | Model and application | Application (host) and external servers |
| **Defines** | How a model requests an action | How capabilities are discovered and connected |
| **Format** | Provider-specific schemas in the API request | JSON-RPC 2.0 over stdio or streamable HTTP |
| **Who implements** | Model provider and your app | Server authors, once, for everyone |
| **Solves** | Text-to-action | The M×N integration problem |
| **Without it** | Fragile free-text intent parsing | A bespoke integration per app per system |

## The layering

```text
   model  ──── tool calling ────▶  your application
                                          │
                                         MCP
                                          ▼
                              github · database · browser · crm
```

Remove MCP and tool calling still works — you just write every integration
yourself. Remove tool calling and MCP has nothing to expose the capabilities
*to*.

## Two practical consequences

**Portability.** An MCP server written once works in any MCP-compatible
application. A tool schema written for one provider's API does not travel.

**Security.** Both layers matter, differently. Tool calling is where you enforce
what may execute; MCP is where you decide which external systems are trusted and
with what credentials. Content returned through either is untrusted input and can
carry injected instructions.

## Verdict

Use tool calling for capabilities specific to your application. Use MCP when the
capability is a system many applications need to reach, or when you want the
integration to outlive the app you are writing today.

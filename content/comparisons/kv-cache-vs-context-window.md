---
title: KV Cache vs Context Window
question: Are these the same limit under two names?
sides: [kv-cache, context-window]
---

## The short version

No. The **context window** is a limit the *model* was trained with — how many
tokens it can attend to. The **KV cache** is *memory the server spends* holding
those tokens' intermediate state while a request is alive. One is a capability
ceiling; the other is a running cost.

## Side by side

| | Context window | KV cache |
|---|---|---|
| **Belongs to** | The model | The serving runtime |
| **Measured in** | Tokens | Gigabytes |
| **Set by** | Training configuration, position encoding | Layers, KV heads, head dim, precision, length |
| **Shared?** | No — a property of the model | Yes — one pool across all concurrent requests |
| **Limits** | How much the model *may* consider | How many requests fit at once |
| **Shrunk by** | Nothing at serving time | GQA, KV quantisation, paging, eviction |

## How they interact

```text
context window says:  "you may use up to 200,000 tokens"
KV cache says:        "each of those costs ~327 KB per token on this model,
                       so 200k tokens is ~65 GB — for one request"
```

A model can advertise a window that your hardware cannot afford to fill for more
than one or two users at a time. Long-context support and long-context *serving*
are separate achievements.

## The third thing people conflate

Usable context is a fourth quantity again. Models attend unevenly across a long
window, so retrieval accuracy degrades well before the advertised limit. Window
size is an upper bound on what is representable, not a promise about recall.

## Verdict

When someone says "we increased the context to 200k", ask two follow-ups: what
does that do to KV cache per request and therefore to concurrency, and what does
measured accuracy look like at 150k?

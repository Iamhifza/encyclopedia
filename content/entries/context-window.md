---
term: Context Window
aliases: [Context Length, Context Limit, Maximum Sequence Length]
category: llms-foundation-models
subcategory: representation
status: established
difficulty: beginner
one_liner: The maximum number of tokens a model can attend to at once, covering the prompt and everything it has generated so far.
origin:
  year: 2018
  circa: true
  attribution: A property of Transformer training configuration; became a headline product specification from 2023
historical_period: transformer
tags: [architecture, inference]
relations:
  depends_on: [self-attention, rope]
  different_from: [kv-cache, agent-memory]
  used_by: [context-engineering, rag]
  related_to: [tokenization]
prerequisites: [tokenization, self-attention]
encountered_in: [documentation, production-systems, social-media]
sources:
  - type: paper
    title: "Lost in the Middle: How Language Models Use Long Contexts"
    url: https://arxiv.org/abs/2307.03172
    year: 2023
  - type: paper
    title: "RULER: What's the Real Context Size of Your Long-Context Language Models?"
    url: https://arxiv.org/abs/2404.06654
    year: 2024
updated: 2026-08-21
review_by: 2027-02-01
---

## Simple Explanation

Everything the model can see at once: the system prompt, the conversation, the
retrieved documents, the tool results and its own output. When it fills, the
oldest content must be dropped or summarised. It is working memory, not storage.

## Technical Definition

The maximum sequence length over which the model can compute attention, fixed by
training configuration and positional-encoding scheme. Exceeding it either errors
or triggers truncation. Advertised length is an upper bound on what is
*representable*, not a guarantee of what is *usable*.

## Why Does It Exist?

Attention cost grows quadratically with sequence length and KV cache memory grows
linearly, so training and serving at a given length is a deliberate, budgeted
choice.

## What Problem Does It Solve?

It bounds the resources one request may consume, and defines the working set the
model can reason over in a single pass.

## How Does It Work?

```text
┌─────────────────── context window (e.g. 200k tokens) ───────────────────┐
│ system prompt │ tool schemas │ retrieved docs │ history │ output so far  │
└─────────────────────────────────────────────────────────────────────────┘
   stable, cacheable ──────────────▶            ◀── volatile, changes often
```

Ordering matters for cost: stable content first maximises prefix cache hits.

## Mental Model

A desk, not a filing cabinet. Anything not on the desk right now does not exist
to the model, and a bigger desk does not mean everything on it gets equal
attention.

## Example

Long-context evaluations repeatedly find degradation well before the advertised
limit: retrieval accuracy is highest for content at the beginning and end of the
window and dips in the middle. A model advertising 1M tokens may perform reliably
over far less, which is why RULER-style measurement matters more than the number
on the model card.

## Real-World Usage

Context budgets are the central design constraint in agent systems. RAG exists
partly to avoid filling the window with irrelevant text; summarisation,
compaction and external memory exist to survive its exhaustion.

## Common Confusions

* **Context window vs KV cache** — the window is a limit on tokens; the cache is
  the memory those tokens occupy at serving time. A large window is only usable
  if the cache fits.
* **Context vs memory** — nothing in the window persists between requests unless
  something outside the model puts it back.
* **Bigger window vs better recall** — usable context is an empirical property
  and should be measured on your own task.
* **Input and output share the budget** — reserving room for the answer is not
  optional.

## Why Should I Care?

Most agent failures at scale are context failures: the relevant fact was crowded
out, truncated, or buried where the model attends least.

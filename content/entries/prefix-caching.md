---
term: Prefix Caching
aliases: [Automatic Prefix Caching, APC, Prompt Caching, KV-Cache Reuse]
category: llm-inference
subcategory: memory
status: modern
difficulty: intermediate
one_liner: Reusing the cached keys and values of a prompt prefix that has already been processed, so identical openings are never computed twice.
origin:
  year: 2023
  attribution: Generalised from PagedAttention block sharing in vLLM; RadixAttention in SGLang; exposed commercially as prompt caching
historical_period: foundation-model
diagram:
  kind: steps
  title: The unchanged head of the prompt is computed once
  footer: 'This is why the ordering rule in context engineering matters so much: one rewritten token near
    the front invalidates every block after it, and the saving disappears.'
  steps:
  - title: Turn one computes everything
    visual:
      kind: segments
      width: 700
      label: turn 1
      caption: all of it prefilled, and its keys and values retained
      segments:
      - text: system prompt
        value: 20
      - text: tool schemas
        value: 30
      - text: user message
        value: 12
  - title: Turn two only pays for what is new
    notes:
    - label: Effect
      text: time to first token falls with the length of the shared prefix, often by most of it
    visual:
      kind: segments
      width: 700
      label: turn 2
      caption: the matching prefix is a cache hit; prefill starts after it
      segments:
      - text: system prompt
        value: 20
        tone: muted
      - text: tool schemas
        value: 30
        tone: muted
      - text: user message
        value: 12
        tone: muted
      - text: assistant
        value: 18
        tone: accent
      - text: user 2
        value: 10
        tone: accent
      spans:
      - from: 0
        to: 2
        text: skipped — already in the cache
      - from: 3
        to: 4
        text: computed
        tone: accent
tags: [inference]
relations:
  depends_on: [kv-cache, paged-attention]
  part_of: [prefill]
  used_by: [agent-loop, coding-agent]
  related_to: [context-engineering, inference-latency]
prerequisites: [kv-cache, prefill]
encountered_in: [production-systems, documentation, github]
sources:
  - type: paper
    title: "SGLang: Efficient Execution of Structured Language Model Programs (RadixAttention)"
    url: https://arxiv.org/abs/2312.07104
    year: 2023
  - type: docs
    title: "vLLM — automatic prefix caching"
    url: https://docs.vllm.ai/en/latest/
updated: 2026-08-21
review_by: 2027-02-01
---

## Simple Explanation

Agents and chat applications send the same opening text over and over: a system
prompt, a set of tool definitions, a long document. Processing it every time is
pure repetition. Prefix caching keeps the computed cache for that opening and
starts fresh work only at the first token that differs.

## Technical Definition

Content-addressed reuse of KV cache blocks across requests. Prompt prefixes are
hashed block by block; a request whose leading blocks hash to an existing entry
maps its block table to those physical blocks rather than recomputing them.
SGLang's RadixAttention organises the cache as a radix tree so that branching
conversations share their common ancestry automatically.

## Why Does It Exist?

In agent workloads the shared prefix is often 90% or more of the input: the same
system prompt and tool schema on every turn of a long loop. Prefill cost is
therefore mostly recomputation of text the server has already seen.

## What Problem Does It Solve?

Repeated prefill work, which shows up as high time to first token and inflated
input-token cost in exactly the workloads that iterate most.

## How Does It Work?

Cache blocks are evicted under memory pressure, usually LRU, so a hit is never
guaranteed. Any change to the prefix — including a timestamp injected at the top
of a system prompt — invalidates everything after it.

## Mental Model

A build cache. Change one line at the top of the file and everything rebuilds;
change the last line and almost nothing does.

## Example

A coding agent with a 20k-token system prompt and tool schema running a 40-turn
loop: without prefix caching it prefills roughly 800k tokens over the session;
with it, close to 20k plus the incremental turns. Providers typically price
cached input tokens at a fraction of uncached ones, so the effect is visible on
the bill as well as the clock.

## Real-World Usage

vLLM automatic prefix caching, SGLang RadixAttention, and prompt caching features
across major model APIs. It is the reason context engineering advice insists on
putting stable content first and volatile content last.

## Common Confusions

* **Prefix caching vs KV cache** — the KV cache exists within one request; prefix
  caching shares it across requests.
* **Prefix caching vs semantic caching** — semantic caching returns a stored
  *answer* for a similar question. Prefix caching never changes the output; it
  only skips recomputation of identical text.
* **Prefixes must match exactly** — token-for-token, from the very first token.

## Why Should I Care?

It is the highest-leverage, lowest-effort optimisation available to anyone
building agents: order the context stably and a large fraction of prefill cost
disappears.

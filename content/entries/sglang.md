---
term: SGLang
aliases: [RadixAttention, Structured Generation Language]
category: llm-inference
subcategory: engines
depth: full
status: modern
difficulty: intermediate
one_liner: "An inference engine built around structured LLM programs, with a radix tree that shares cache across branching conversations."
origin:
  year: 2023
  attribution: Zheng et al.; developed at UC Berkeley alongside the vLLM ecosystem
historical_period: agentic
tags: [inference]
relations:
  alternative_to: [vllm, tensorrt-llm]
  depends_on: [paged-attention, prefix-caching, structured-outputs]
  related_to: [agent-loop, throughput]
prerequisites: [kv-cache, prefix-caching]
encountered_in: [github, production-systems, research-papers]
sources:
  - type: paper
    title: "SGLang: Efficient Execution of Structured Language Model Programs"
    url: https://arxiv.org/abs/2312.07104
    year: 2023
  - type: repo
    title: "sgl-project/sglang"
    url: https://github.com/sgl-project/sglang
updated: 2026-08-21
review_by: 2027-02-01
---

## Simple Explanation

vLLM optimises for serving many independent requests. SGLang starts from a
different observation: real LLM applications are not independent requests. They
are *programs* — an agent looping, a conversation branching, a prompt being tried
several ways — and those calls share enormous amounts of prefix with each other.

Its central idea, RadixAttention, organises the KV cache as a tree so that shared
history is stored once and reused automatically across every branch.

## Technical Definition

A serving system pairing a runtime with a domain-specific frontend for structured
generation. RadixAttention maintains cached prefixes in a radix tree keyed by
token sequence, with LRU eviction and cache-aware scheduling, so any request
sharing a prefix with a cached one reuses those blocks. It also provides fast
constrained decoding via compressed finite state machines.

## Why Does It Exist?

Agent and multi-turn workloads reuse the same prefix constantly — the same system
prompt, the same tool definitions, the same conversation history growing by one
turn. Treating each call as unrelated recomputes that repeatedly.

## What Problem Does It Solve?

Redundant prefill in branching and multi-turn workloads, and the overhead of
constrained decoding when output must match a schema.

## How Does It Work?

```text
radix tree of cached prefixes

        [system prompt + tools]          ← stored once
           ├── conversation A ── turn 3
           ├── conversation A ── turn 4   (branch, shares everything above)
           └── conversation B ── turn 2

any new request walks the tree, reuses the longest matching prefix,
and computes only the divergent remainder
```

Scheduling is cache-aware: requests that would hit an existing prefix are
preferred, which raises the hit rate rather than merely exploiting it.

## Mental Model

A shared filing system for conversations rather than a fresh folder per request.
Branches of the same discussion keep one copy of their common history.

## Example

Where it shines: an agent exploring several tool-call paths from the same state,
or a prompt evaluated against many inputs with a fixed long preamble. Where the
advantage narrows: a stream of unrelated single-turn requests with nothing in
common, which is closer to vLLM's home ground.

## Real-World Usage

Deployed for agent workloads, structured extraction and multi-turn serving, and
used as the serving layer by several inference providers. The two projects have
converged substantially — vLLM has automatic prefix caching, SGLang has paged
memory — so the choice is now made on benchmarks against your own workload rather
than on architecture.

## Common Confusions

* **SGLang is both a language and a runtime** — the frontend DSL for expressing
  branching generation programs is optional; many people use only the server.
* **RadixAttention vs prefix caching** — the same idea with a stronger data
  structure. The radix tree handles branching and partial matches; simpler
  implementations key on whole-prefix hashes.
* **Benchmarks are workload-dependent and dated quickly** — both projects release
  frequently, and last year's comparison tells you little.

## Why Should I Care?

It is the engine designed around the shape agent workloads actually have, and
RadixAttention is the clearest demonstration that prefix reuse is a structural
opportunity rather than an optimisation.

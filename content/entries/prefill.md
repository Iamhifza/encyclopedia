---
term: Prefill
aliases: [Prompt Processing, Context Encoding, Prefill Phase]
category: llm-inference
subcategory: mechanics
status: established
difficulty: intermediate
one_liner: The first pass of inference, where the whole prompt is processed at once and its keys and values are written into the cache.
origin:
  year: 2022
  circa: true
  attribution: Terminology standardised by LLM serving systems such as Orca, FasterTransformer and vLLM
historical_period: foundation-model
tags: [inference]
relations:
  part_of: [autoregressive-generation]
  different_from: [decode]
  used_by: [kv-cache, prefix-caching, chunked-prefill]
  related_to: [inference-latency]
prerequisites: [autoregressive-generation, kv-cache]
encountered_in: [production-systems, github, interviews, technical-blogs]
sources:
  - type: paper
    title: "Orca: A Distributed Serving System for Transformer-Based Generative Models"
    url: https://www.usenix.org/conference/osdi22/presentation/yu
    year: 2022
  - type: paper
    title: "SARATHI: Efficient LLM Inference by Piggybacking Decodes with Chunked Prefills"
    url: https://arxiv.org/abs/2308.16369
    year: 2023
updated: 2026-08-21
---

## Simple Explanation

Before the model can write anything it has to read the prompt. All of it, in one
shot. That single big pass is prefill, and it is what you wait through before the
first word appears.

## Technical Definition

The forward pass over all $n$ prompt tokens simultaneously, computing attention
over the full sequence and populating the KV cache for every layer. Compute
scales as $O(n^2)$ in attention and $O(n)$ in the feed-forward layers; because
many tokens share the same weight loads, arithmetic intensity is high and the
phase is compute-bound.

## Why Does It Exist?

Prompt tokens are all known in advance, so there is no reason to process them one
at a time. Doing them together saturates the GPU's matrix units and pays the cost
of loading the model weights once instead of $n$ times.

## What Problem Does It Solve?

It converts what would be $n$ sequential steps into one parallel step, and it
produces the cached keys and values that make every subsequent decode step cheap.

## How Does It Work?

```text
prompt: 2000 tokens
   │
   ├─ one forward pass, all 2000 positions in parallel
   ├─ attention over a 2000×2000 score matrix (causally masked)
   ├─ write 2000 positions × L layers of K and V into the cache
   └─ emit logits for the LAST position only ──▶ first generated token
```

Only the final position's logits are needed; the rest of the pass exists to build
the cache.

## Mental Model

Reading the whole brief before starting to speak. Long brief, longer silence
before the first word.

## Example

A 32k-token prompt on a 70B model may take a second or more of pure prefill on a
single GPU. That time *is* the time to first token. Doubling the prompt roughly
doubles it — worse than doubling once attention dominates.

## Real-World Usage

Prefill dominates TTFT, so every serving optimisation aimed at responsiveness
targets it: prefix caching to skip repeated prompt segments entirely, chunked
prefill to stop long prompts blocking other users' decodes, and
prefill/decode disaggregation to run the two phases on separate hardware pools
tuned for their different bottlenecks.

## Common Confusions

* **Prefill vs decode** — prefill processes many tokens in one pass and is
  compute-bound; decode processes one token per pass and is memory-bandwidth-bound.
  They have opposite optimal batch strategies, which is the central tension in
  LLM serving.
* **Prefill is not "loading the model"** — the weights are already resident;
  prefill is running them over your prompt.
* **Cached prompts still cost something** — a prefix cache hit skips computation,
  not the memory that holds the resulting cache.

## Why Should I Care?

If your users complain about waiting before the answer starts, the fix is almost
always in prefill; if they complain about the answer arriving slowly once
started, it is in decode. Knowing which is which saves weeks.

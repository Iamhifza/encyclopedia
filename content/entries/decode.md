---
term: Decode
aliases: [Decode Phase, Generation Phase, Token-by-Token Decoding]
category: llm-inference
subcategory: mechanics
status: established
difficulty: intermediate
one_liner: The phase after the prompt is read, where the model produces one token per forward pass until it stops.
origin:
  year: 2022
  circa: true
  attribution: Terminology standardised by LLM serving systems
historical_period: foundation-model
tags: [inference]
relations:
  part_of: [autoregressive-generation]
  different_from: [prefill]
  depends_on: [kv-cache]
  used_by: [continuous-batching, speculative-decoding]
  related_to: [memory-hierarchy, inference-latency]
prerequisites: [autoregressive-generation, kv-cache]
encountered_in: [production-systems, github, interviews]
sources:
  - type: paper
    title: "Efficiently Scaling Transformer Inference"
    url: https://arxiv.org/abs/2211.05102
    year: 2022
  - type: post
    title: "vLLM documentation — performance and optimization"
    url: https://docs.vllm.ai/en/latest/
updated: 2026-08-21
---

## Simple Explanation

Once the prompt is read, the model writes. Each word costs one full pass through
the entire network — billions of parameters loaded from memory — to produce a
single token. Then it does it again.

## Technical Definition

The autoregressive phase in which each forward pass has sequence length 1 for the
new token, attending over all cached keys and values. Arithmetic intensity is
very low (roughly one multiply-accumulate per parameter byte loaded at batch size
1), so the phase is bound by memory bandwidth rather than arithmetic.

## Why Does It Exist?

It is not a design choice but a consequence: token $t+1$ cannot be computed until
token $t$ is known. Autoregression forces the sequential structure.

## What Problem Does It Solve?

Nothing — it is the cost centre. Almost every serving technique in this domain
exists to make decode less wasteful.

## How Does It Work?

```text
per decode step, for each layer:
   load full weight matrices from HBM   ← the expensive part
   compute q,k,v for exactly ONE token
   append k,v to the cache
   attend over ALL cached positions
   ...
   sample the next token, append, repeat
```

At batch size 1 the GPU's arithmetic units are almost idle; the bottleneck is
streaming weights. Adding more requests to the batch reuses the same weight load
across all of them, so throughput rises with almost no extra latency until
bandwidth saturates.

## Mental Model

Driving a lorry across town to deliver a single envelope. The trip costs the
same whether you carry one envelope or a thousand, so you may as well fill it —
which is precisely the argument for batching.

## Example

A 70B model in fp16 holds ~140 GB of weights. On an accelerator with ~3 TB/s of
bandwidth, one decode step cannot be faster than roughly 47 ms at batch size 1,
no matter how much compute is available. Batch 32 requests and you serve 32
tokens for nearly the same 47 ms.

## Real-World Usage

Continuous batching keeps the batch full; quantisation shrinks the bytes that
must be streamed; grouped-query attention shrinks the cache read; speculative
decoding produces several tokens per weight load. All four attack the same
bottleneck from different angles.

## Common Confusions

* **Decode vs decoder** — unrelated. "Decoder" is the architectural half of a
  Transformer; "decode" is the runtime phase.
* **Decode vs sampling** — the forward pass produces logits; sampling picks a
  token from them. Sampling is nearly free.
* **"More FLOPS will fix it"** — decode is bandwidth-bound; extra arithmetic
  capacity sits idle.

## Why Should I Care?

Per-token cost, streaming speed and the economics of serving all live here.
Understanding that decode is memory-bound explains why batching is nearly free,
why quantisation helps so much, and why speculative decoding is worth the
complexity.

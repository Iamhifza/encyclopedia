---
term: Grouped-Query Attention
aliases: [GQA, Multi-Query Attention, MQA]
category: transformers
subcategory: attention
status: established
difficulty: advanced
one_liner: Letting several query heads share one set of key and value heads, which shrinks the KV cache dramatically for a small quality cost.
origin:
  year: 2023
  attribution: Ainslie et al. (Google); generalises Shazeer's 2019 multi-query attention
historical_period: foundation-model
tags: [architecture, inference]
relations:
  successor_of: [self-attention]
  solves: [kv-cache]
  used_by: [large-language-model]
  related_to: [decode, quantization]
prerequisites: [self-attention, kv-cache]
encountered_in: [research-papers, github, interviews]
sources:
  - type: paper
    title: "GQA: Training Generalized Multi-Query Transformer Models from Multi-Head Checkpoints"
    url: https://arxiv.org/abs/2305.13245
    year: 2023
  - type: paper
    title: "Fast Transformer Decoding: One Write-Head is All You Need"
    url: https://arxiv.org/abs/1911.02150
    year: 2019
updated: 2026-08-21
---

## Simple Explanation

Standard attention gives every head its own keys and values, and all of those
must be cached for every token. Most of that turns out to be redundant. Grouped-
query attention keeps all the query heads but has groups of them share a single
key/value head, so the cache shrinks by the size of the group.

## Technical Definition

An attention variant with $H_q$ query heads and $H_{kv} < H_q$ key/value heads,
where each key/value head is shared by $H_q / H_{kv}$ query heads. Multi-query
attention is the extreme case $H_{kv} = 1$; standard multi-head attention is
$H_{kv} = H_q$. Existing checkpoints can be converted by mean-pooling the
key/value projections within each group followed by brief uptraining.

## Why Does It Exist?

Multi-query attention (2019) cut the cache by the full head count but measurably
degraded quality and destabilised training. GQA was introduced as the tunable
middle ground.

## What Problem Does It Solve?

KV cache size, which directly limits batch size, context length and concurrency —
and, because decode must read the whole cache each step, decode speed as well.

## How Does It Work?

```text
MHA  (H_kv = 32)      GQA  (H_kv = 8)         MQA  (H_kv = 1)
q1..q32               q1..q32                 q1..q32
k1..k32               k1..k8                  k1
v1..v32               v1..v8                  v1
cache: 32 units       cache: 8 units (4×)     cache: 1 unit (32×)
best quality          near-MHA quality        largest saving, quality cost
```

## Mental Model

Thirty-two analysts each asking their own questions, but sharing eight research
briefings between them instead of commissioning thirty-two.

## Example

Llama-3-70B uses 64 query heads and 8 KV heads: an 8× reduction in KV cache
versus full multi-head attention, turning roughly 80 GB of cache for a long
context into about 10 GB. That is the difference between one long-context request
per GPU and eight.

## Real-World Usage

Near-universal in current open-weight models. DeepSeek's multi-head latent
attention (MLA) pushes further by compressing keys and values into a shared
low-rank latent, trading extra computation for an even smaller cache.

## Common Confusions

* **GQA is not free** — quality drops slightly, most visibly on tasks needing
  fine-grained retrieval from long context. The tradeoff is usually worth it.
* **It must be baked into the architecture** — unlike KV quantisation, you cannot
  switch a trained MHA model to GQA at serving time without uptraining.
* **GQA vs MQA** — same idea, different group count. Many people say "MQA" when
  they mean GQA.

## Why Should I Care?

When you read a model card that says "64 query heads, 8 KV heads", that ratio
tells you what its serving cost will look like — often more directly than
parameter count does.

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
diagram:
  kind: steps
  title: Share the keys and values, keep the queries
  footer: Almost every open-weight model of the last two years ships GQA. It is the rare change that shrinks
    the dominant memory cost with no measurable quality loss, which is why adoption was close to universal.
  steps:
  - title: Three points on one dial
    visual:
      kind: columns
      width: 720
      columns:
      - title: MHA
        lines:
        - 32 query heads
        - 32 KV heads
        - one KV pair per query
        - best quality
      - title: GQA
        accent: true
        lines:
        - 32 query heads
        - 8 KV heads
        - four queries share a KV pair
        - quality holds
      - title: MQA
        lines:
        - 32 query heads
        - 1 KV head
        - all queries share one
        - quality cost
  - title: What that does to the cache
    notes:
    - label: Why it matters
      text: the KV cache, not the weights, decides how many users fit on a card
    visual:
      kind: bars
      caption: KV cache per token, relative to MHA
      bars:
      - label: MHA
        value: 1.0
        value_label: 32 units
      - label: GQA
        value: 0.25
        value_label: 8 units — 4× less
        accent: true
      - label: MQA
        value: 0.03
        value_label: 1 unit — 32× less
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


Multi-head attention gives every query head its own key and value heads. Since
the KV cache stores one entry per key-value head per token, its size scales
directly with that count — and on a long-context request the cache, not the
weights, is what fills the card.

GQA keeps all the query heads and shares each key-value pair across a group of
them. Thirty-two query heads backed by eight KV heads means four queries read
the same keys and values, and the cache shrinks fourfold for it. Multi-query
attention is the same idea taken to one shared pair, which saves the most and
costs the most quality.

The reason this works at all is that the query heads carry most of the
specialisation; the keys and values are closer to a shared representation of the
sequence than the head count implies. Eight groups turned out to sit at the point
where quality is indistinguishable from full multi-head attention, and that is
why essentially every open-weight model now ships with it.

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

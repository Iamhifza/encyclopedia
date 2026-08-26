---
term: KV Cache
aliases: [Key-Value Cache, KV-Cache, Attention Cache]
category: llm-inference
subcategory: memory
status: established
difficulty: intermediate
one_liner: The stored keys and values from every token already processed, kept so the model never has to re-read the conversation for each new token.
origin:
  year: 2019
  circa: true
  attribution: Standard practice in fast Transformer decoding; formalised in Shazeer's multi-query attention work
historical_period: transformer
diagram:
  kind: steps
  title: Building the cache, one token at a time
  footer: 'Without this, generating token n would recompute all n-1 earlier keys and values: O(n²) wasted work.'
  steps:
  - title: Prefill — the prompt "the cache stores"
    notes:
    - label: Computed
      text: K and V for all three tokens in one pass
    - label: Stored
      text: per layer, per attention head
    visual:
      kind: grid
      caption: cache after prefill
      rows:
      - label: K
        cells:
        - text: K1
          new: true
        - text: K2
          new: true
        - text: K3
          new: true
      - label: V
        cells:
        - text: V1
          new: true
        - text: V2
          new: true
        - text: V3
          new: true
  - title: Decode — the model emits "keys"
    notes:
    - label: Computed
      text: K4 and V4 only; the first three are already cached
    - label: Not cached
      text: Q4 itself — a query is used once and never again
    visual:
      kind: grid
      caption: one slot appended
      rows:
      - label: K
        cells:
        - K1
        - K2
        - K3
        - text: K4
          new: true
      - label: V
        cells:
        - V1
        - V2
        - V3
        - text: V4
          new: true
  - title: Decode — the model emits "and"
    notes:
    - label: Cost
      text: one slot per token, per layer, for the life of the request
    - label: Consequence
      text: 32k tokens on a 70B model is roughly 10 GB
    visual:
      kind: bars
      caption: GPU memory, 80 GB card
      bars:
      - label: weights
        value: 0.87
        value_label: 70 GB
      - label: KV cache
        value: 0.13
        value_label: 10 GB
        accent: true
diagrams:
- kind: figure
  section: Evolution
  title: Every step here is someone trying to make the cache smaller
  visual:
    kind: lineage
    per_row: 4
    caption: the cache went from an obvious optimisation to the thing serving architecture is designed
      around
    milestones:
    - text: recompute
      note: O(n²)
    - text: KV cache
      note: '2019'
      tone: accent
    - text: MQA / GQA
      note: fewer heads
    - text: PagedAttention
      note: '2023'
    - text: prefix caching
      note: share it
    - text: KV quantisation
      note: fp8 · int4
    - text: offload & reuse
      note: spill to host
tags: [inference, architecture]
relations:
  depends_on: [self-attention]
  part_of: [decode]
  evolved_into: [paged-attention]
  used_by: [prefix-caching, continuous-batching, grouped-query-attention]
  different_from: [context-window]
  related_to: [memory-hierarchy, quantization]
prerequisites: [self-attention, autoregressive-generation]
encountered_in: [production-systems, github, interviews, job-descriptions, research-papers]
sources:
  - type: paper
    title: "Fast Transformer Decoding: One Write-Head is All You Need"
    url: https://arxiv.org/abs/1911.02150
    year: 2019
  - type: paper
    title: "Efficient Memory Management for Large Language Model Serving with PagedAttention"
    url: https://arxiv.org/abs/2309.06180
    year: 2023
  - type: docs
    title: "vLLM — automatic prefix caching and KV cache management"
    url: https://docs.vllm.ai/en/latest/
videos:
  - title: "KV cache explained"
    channel: "Efficient NLP"
    url: https://www.youtube.com/results?search_query=kv+cache+explained+llm+inference
    note: "Why context length costs memory"
updated: 2026-08-21
review_by: 2027-02-01
---

## Simple Explanation

To produce each new token, attention needs the key and value vectors of every
earlier token. Those vectors do not change once computed, so recomputing them
every step would be pure waste. The KV cache keeps them. It turns generation from
quadratic re-reading into a linear append.

## Technical Definition

A per-request, per-layer, per-head tensor store holding the key and value
projections of all previously processed positions. At each decode step the new
token's $k$ and $v$ are appended and attention is computed against the full cache.
Size is
$2 \times L \times H_{kv} \times d_{head} \times n_{tokens} \times \text{bytes}$,
growing linearly with sequence length and batch size.

## Why Does It Exist?

Without it, generating token $n$ requires recomputing keys and values for all
$n-1$ previous tokens, making a full response $O(n^2)$ in wasted work. With it,
each step is $O(n)$ in attention reads and $O(1)$ in projection work.

## What Problem Does It Solve?

Redundant computation during decoding. It trades arithmetic for memory — and
that traded-for memory then becomes the binding constraint on how many users a
GPU can serve at once.

## How Does It Work?

Queries are *not* cached — a query is used once, at the step that generates it,
and never again.

## Mental Model

Reading notes rather than the source. You already extracted what each paragraph
contributes; keep the extract and stop rereading the book.

## Formula

$$\text{bytes} = 2 \cdot L \cdot H_{kv} \cdot d_{head} \cdot n \cdot b$$

* $2$ — one tensor for keys, one for values.
* $L$ — number of layers.
* $H_{kv}$ — number of key/value heads (fewer than query heads under GQA).
* $d_{head}$ — dimension per head.
* $n$ — tokens cached, prompt plus generated.
* $b$ — bytes per element (2 for fp16, 1 for fp8).

## Example

Llama-3-70B: 80 layers, 8 KV heads (GQA), head dimension 128, fp16.
Per token: $2 \times 80 \times 8 \times 128 \times 2 \approx 327$ KB.
A 32k-token context therefore needs about **10 GB of KV cache for one request** —
comparable to a mid-size model's entire weights. Ten concurrent long-context
users need 100 GB, which is why cache management, not model size, usually decides
how many requests a GPU can hold.

## Real-World Usage

Cache memory drives most serving design: PagedAttention to stop fragmentation,
prefix caching to share cache across requests with common prefixes, GQA and MLA
to shrink it architecturally, KV quantisation to fp8 or int4 to halve it, and
eviction or offload policies when it still does not fit.

## Historical Origin

An obvious engineering optimisation present in decoding implementations for
years; it became a first-class architectural concern around 2022-2023 when
context windows grew and cache memory started to dominate serving cost.

## Evolution


Every step in this lineage is someone trying to make the cache smaller. The cache
began as an obvious engineering optimisation and became, within a few years, the
constraint that serving architecture is designed around — first by attacking its
shape (fewer key-value heads), then its allocation (paging instead of contiguous
blocks), then its redundancy (sharing prefixes between requests), and finally its
precision and residency.

## Common Confusions

* **KV cache vs context window** — the context window is the *limit* on how many
  tokens the model may attend to; the KV cache is the *memory* holding those
  tokens' intermediate state. One is a model property, the other a runtime cost.
* **KV cache vs prompt caching** — a provider's "prompt caching" feature is
  usually prefix caching implemented on top of the KV cache, reusing it across
  requests rather than within one.
* **KV cache vs CPU cache** — a naming collision only. This is ordinary tensor
  data in accelerator memory.
* **"Caching makes long context cheap"** — it removes recomputation, not the
  memory footprint, and attention still reads the whole cache every step.

## Differences

Against the alternatives for reducing its size: GQA reduces $H_{kv}$
architecturally and must be trained in; KV quantisation reduces $b$ and can be
applied post-hoc with some quality risk; PagedAttention does not reduce the size
at all, it removes the waste from over-allocating contiguous blocks.

## Why Should I Care?

It is the single most load-bearing concept in LLM serving. Batch size limits,
context pricing, concurrency limits and out-of-memory failures in production all
resolve to KV cache arithmetic, and it appears in interviews for every inference
role.

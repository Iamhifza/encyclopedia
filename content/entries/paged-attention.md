---
term: PagedAttention
aliases: [Paged KV Cache, Block-Based KV Cache]
category: llm-inference
subcategory: memory
status: established
difficulty: advanced
one_liner: Storing the KV cache in fixed-size blocks scattered through memory, the way an operating system pages virtual memory, instead of one contiguous slab per request.
origin:
  year: 2023
  attribution: Kwon et al., UC Berkeley; introduced with vLLM
historical_period: foundation-model
diagram:
  kind: steps
  title: Stop reserving for the worst case
  footer: 'Borrowed wholesale from virtual memory: a page table, fixed-size blocks and reference counting.
    The gain is not a faster kernel — it is fitting two to four times as many requests on the same card.'
  steps:
  - title: Contiguous reservation wastes most of what it holds
    notes:
    - label: Cause
      text: nobody knows how long a response will be, so the allocator books the maximum
    visual:
      kind: segments
      width: 700
      label: one request's reservation, 2048 tokens
      caption: internal fragmentation, and the reserved tail cannot be lent to anyone else
      segments:
      - text: actually used
        value: 120
        value_label: '120'
      - text: reserved, idle
        value: 1928
        value_label: '1928'
        tone: warn
  - title: A block table breaks the link between logical and physical
    notes:
    - label: Bonus
      text: identical prefixes can point at the same physical blocks, reference-counted, which is what
        makes prefix caching possible
    visual:
      kind: mapping
      width: 760
      head:
      - logical blocks, per request
      - physical blocks, from one pool
      rows:
      - left: req A  →  0 1 2 3
        right: 17  04  39  12
      - left: req B  →  0 1
        right: 17  04   ← shared, refcount 2
        tone: accent
tags: [inference]
relations:
  successor_of: [kv-cache]
  implemented_by: [vllm]
  used_by: [prefix-caching, continuous-batching]
  solves: [kv-cache]
  related_to: [memory-hierarchy]
prerequisites: [kv-cache]
encountered_in: [research-papers, github, production-systems, interviews]
sources:
  - type: paper
    title: "Efficient Memory Management for Large Language Model Serving with PagedAttention"
    url: https://arxiv.org/abs/2309.06180
    year: 2023
  - type: repo
    title: "vLLM"
    url: https://github.com/vllm-project/vllm
updated: 2026-08-21
---

## Simple Explanation

Nobody knows how long a response will be, so early serving systems reserved
enough contiguous memory for the longest possible answer for every request. Most
of that reservation was never used. PagedAttention chops the cache into small
fixed-size blocks that can live anywhere in memory, allocated only as the
response actually grows.

## Technical Definition

A KV cache layout that partitions each sequence's cache into fixed-size blocks
(commonly 16 tokens) held in a block pool, with a per-sequence *block table*
mapping logical positions to physical blocks. The attention kernel is modified to
gather across non-contiguous blocks. Blocks are reference-counted, enabling
copy-on-write sharing between sequences.

## Why Does It Exist?

The vLLM authors measured that existing serving systems wasted 60-80% of KV cache
memory to internal fragmentation, external fragmentation and over-reservation.
Wasted cache memory directly reduces how many requests fit, which directly
reduces throughput.

## What Problem Does It Solve?

Memory fragmentation and over-allocation in KV cache management, and — as a
consequence of block sharing — duplication of identical prefixes across requests.

## How Does It Work?

Two requests with the same system prompt point at the same physical blocks until
one of them diverges, at which point that block is copied.

## Mental Model

Virtual memory, transplanted. The block table is a page table, blocks are pages,
sharing is copy-on-write, and the win is the same one operating systems got in
the 1960s.

## Example

With 2048-token reservations and an average response of 200 tokens, roughly 90%
of reserved cache is dead space. Paging recovers it, and vLLM reported 2-4×
throughput improvements over then-current serving systems at equal latency,
almost entirely from fitting more concurrent sequences.

## Real-World Usage

vLLM, and since adopted in one form or another across serving stacks including
TensorRT-LLM, SGLang and HuggingFace TGI. It is the enabling mechanism for
automatic prefix caching: shared prefixes are simply shared blocks.

## Common Confusions

* **PagedAttention vs FlashAttention** — orthogonal. FlashAttention makes the
  attention computation itself use on-chip memory efficiently; PagedAttention
  changes where the KV cache lives. Production kernels do both.
* **It does not shrink the cache** — the same number of tokens occupies the same
  bytes. It eliminates the bytes that were reserved and never used.
* **Block size is a tradeoff** — smaller blocks waste less on the final partial
  block but add more indirection overhead per attention step.

## Why Should I Care?

It is the clearest example in modern AI of a classical systems idea solving a
new problem outright, and it is the reason a single GPU can serve dozens of
concurrent conversations rather than a handful.

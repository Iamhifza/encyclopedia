---
term: Chunked Prefill
aliases: [Piggybacked Prefill, Split Prefill, Prefill Chunking]
category: llm-inference
subcategory: batching
status: modern
difficulty: advanced
one_liner: Breaking a long prompt into pieces and processing them across several scheduling steps, so other users' tokens keep flowing.
origin:
  year: 2023
  attribution: Agrawal et al., SARATHI; deployed in vLLM and other engines
historical_period: foundation-model
diagram:
  kind: steps
  title: Stop one long prompt from freezing everyone else
  footer: Total throughput barely moves. What changes is that no user's decode stalls behind another user's
    prompt — a tail-latency fix, not a speed-up.
  steps:
  - title: Without chunking, a long prefill owns the step
    visual:
      kind: segments
      width: 700
      label: one scheduler step
      caption: every other request waits out the whole prompt
      segments:
      - text: 100k-token prefill
        value: 96
        tone: warn
      - text: nothing else
        value: 4
  - title: With a token budget, every step carries both
    notes:
    - label: Budget
      text: 2048 tokens per step, split between prefill and the decodes waiting behind it
    visual:
      kind: segments
      width: 700
      label: one scheduler step, budget 2048
      caption: the prompt now takes three steps, and nobody's decode stops
      segments:
      - text: prefill chunk
        value: 2000
        value_label: '2000'
      - text: 48 decodes
        value: 48
        tone: accent
      spans:
      - from: 0
        to: 1
        text: repeated until the prompt is consumed
tags: [inference]
relations:
  depends_on: [prefill, continuous-batching]
  solves: [inference-latency]
  related_to: [throughput]
prerequisites: [prefill, decode, continuous-batching]
encountered_in: [production-systems, github, research-papers]
sources:
  - type: paper
    title: "SARATHI: Efficient LLM Inference by Piggybacking Decodes with Chunked Prefills"
    url: https://arxiv.org/abs/2308.16369
    year: 2023
  - type: paper
    title: "Taming Throughput-Latency Tradeoff in LLM Inference with Sarathi-Serve"
    url: https://arxiv.org/abs/2403.02310
    year: 2024
updated: 2026-08-21
review_by: 2027-02-01
---

## Simple Explanation

A 100k-token prompt takes a long time to prefill, and while the GPU is busy with
it, everyone else's answer stops streaming. Chunked prefill slices that prompt
into chunks and processes one chunk per step, packing each step with other
users' decode tokens so nobody stalls.

## Technical Definition

Splitting the prefill of a sequence into fixed-size token chunks scheduled across
multiple iterations, and co-scheduling those chunks with decode tokens from other
sequences into a single hybrid batch, subject to a per-step token budget.

## Why Does It Exist?

Prefill is compute-bound and decode is memory-bound, so a step containing only
decode wastes arithmetic capacity while a step containing a long prefill starves
decoding. Mixing them uses both resources and removes the stall.

## What Problem Does It Solve?

Inter-token latency spikes caused by long prompts entering the batch — the
"someone pasted a whole codebase and my stream froze" failure.

## How Does It Work?


The scheduler is given a token budget per step rather than a request per step. A
long prompt is admitted a slice at a time, and whatever budget is left over goes
to the decode steps of requests already in flight. A 100k-token prefill becomes
fifty scheduled slices instead of one monopolising batch.

The prompt itself finishes no sooner — slightly later, in fact, since it now
shares each step. What changes is that every other user keeps generating
throughout, so the inter-token latency they observe stays flat instead of
stalling for the length of somebody else's prompt.

## Mental Model

Rather than closing the road to move one oversized load, the load is broken into
truckloads and interleaved with normal traffic.

## Example

With a 512-token chunk budget, a 32k prompt becomes 64 scheduling steps. Its own
time to first token rises slightly, while every other active request keeps
producing tokens at a steady rate instead of freezing for a second.

## Real-World Usage

Enabled by default in recent vLLM releases and available in other engines. The
chunk size is a direct throughput-versus-latency dial: larger chunks favour
prefill efficiency, smaller chunks favour smooth streaming for everyone else.

## Common Confusions

* **Chunked prefill vs chunking in RAG** — unrelated. One splits a prompt for
  scheduling, the other splits documents for retrieval.
* **It does not reduce total work** — the same tokens are prefilled; the work is
  spread out in time.
* **It slightly hurts the chunked request** — the benefit is to the rest of the
  batch and to overall tail latency.

## Why Should I Care?

Long-context workloads and agent traffic mix enormous prompts with chatty short
turns. Without chunked prefill, one heavy request degrades service for everyone
sharing that GPU.

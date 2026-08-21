---
term: Continuous Batching
aliases: [Iteration-Level Scheduling, In-Flight Batching, Dynamic Batching]
category: llm-inference
subcategory: batching
status: established
difficulty: intermediate
one_liner: Letting finished requests leave the batch and new ones join at every generation step, instead of making everyone wait for the slowest response.
origin:
  year: 2022
  attribution: Yu et al., Orca (OSDI 2022); popularised as continuous batching by vLLM
historical_period: foundation-model
tags: [inference]
relations:
  depends_on: [decode, paged-attention]
  implemented_by: [vllm]
  used_by: [throughput]
  related_to: [chunked-prefill, inference-latency]
prerequisites: [decode]
encountered_in: [production-systems, github, interviews, job-descriptions]
sources:
  - type: paper
    title: "Orca: A Distributed Serving System for Transformer-Based Generative Models"
    url: https://www.usenix.org/conference/osdi22/presentation/yu
    year: 2022
  - type: post
    title: "vLLM documentation — scheduling and batching"
    url: https://docs.vllm.ai/en/latest/
updated: 2026-08-21
---

## Simple Explanation

Old-style batching grouped requests, ran them together, and waited for all of
them to finish before starting the next group. But responses have wildly
different lengths, so most of the batch sat idle while one long answer finished.
Continuous batching lets each request leave the moment it is done and pulls a
waiting request into the free slot immediately.

## Technical Definition

Scheduling at the granularity of a decode iteration rather than a request. Each
step, the scheduler assembles the set of active sequences, runs one forward pass
over them, retires any that emitted a stop token, and admits queued requests into
the freed KV cache blocks.

## Why Does It Exist?

Decode is memory-bandwidth-bound, so a larger batch costs almost nothing extra
per step: the weights are loaded once regardless. Any idle slot in the batch is
throughput thrown away, and with static batching most slots are idle most of the
time.

## What Problem Does It Solve?

Head-of-line blocking and low GPU utilisation caused by variance in output length.

## How Does It Work?

```text
STATIC BATCHING                CONTINUOUS BATCHING
step ─────────────▶            step ─────────────▶
A ████░░░░░░░░░░░              A ████ E ███████████
B ██████████░░░░░              B ██████████ F █████
C ██░░░░░░░░░░░░░              C ██ D ████ G ██████
D ███████████████              D ███████████████
  ░ = wasted slot                slots refill immediately
```

## Mental Model

A shared taxi that drops passengers wherever they need and picks up whoever is
waiting at that corner, instead of driving everyone to the last stop before
starting again.

## Example

Requests generating 10, 50 and 500 tokens under static batching all occupy their
slot for 500 steps: about 20% utilisation. Under continuous batching the short
ones exit at steps 10 and 50 and their capacity is immediately reused. Reported
throughput gains over static batching are commonly in the range of 5-20× on
mixed workloads.

## Real-World Usage

Table stakes in every serious serving stack: vLLM, TensorRT-LLM (in-flight
batching), SGLang, TGI. The interesting engineering has moved to how prefill and
decode are interleaved, since a long prefill in the middle of a batch stalls
everyone's decoding — the problem chunked prefill addresses.

## Common Confusions

* **Continuous vs dynamic batching** — "dynamic batching" in classic model
  serving means waiting briefly to group requests, then running them to
  completion. Continuous batching reschedules every step. The terms are often
  used loosely, so check what a system actually does.
* **Batching raises latency** — for decode it barely does, because the phase is
  bandwidth-bound. That is what makes the tradeoff so favourable.
* **Batch size is not fixed** — it varies step to step with available KV cache
  memory.

## Why Should I Care?

It is the single largest throughput lever in LLM serving, and its interaction
with KV cache capacity is what determines how many concurrent users a deployment
can actually hold.

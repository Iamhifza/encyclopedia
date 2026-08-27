---
term: Inference Scheduler
aliases: [Request Scheduler, Admission Control, Request Queue, Serving Scheduler]
category: llm-inference
subcategory: batching
depth: full
status: established
difficulty: advanced
one_liner: "The component that decides, every step, which requests run, which wait and which get evicted."
historical_period: foundation-model
diagram:
  kind: figure
  title: Every forward pass, it rebuilds the batch
  footer: This runs before every single step, which is why continuous batching, paged attention and chunked
    prefill are all really features of the scheduler rather than of the model.
  visual:
    kind: pipeline
    width: 740
    caption: then one forward pass over whatever it assembled — and immediately round again
    stages:
    - text: retire what finished
      note: and free its blocks
    - text: admit what fits
      via: is there memory for a queued request's cache?
    - text: relieve memory pressure
      via: preempt someone — recompute later, or swap their cache to host memory
    - text: fill the token budget
      tone: accent
      via: decodes first, because someone is waiting on each one, then a prefill chunk
tags: [inference]
relations:
  part_of: [vllm]
  depends_on: [continuous-batching, paged-attention, kv-cache]
  related_to: [inference-latency, throughput, chunked-prefill, disaggregated-inference]
prerequisites: [continuous-batching, kv-cache]
encountered_in: [production-systems, github, research-papers, job-descriptions]
sources:
  - type: paper
    title: "Orca: A Distributed Serving System for Transformer-Based Generative Models"
    url: https://www.usenix.org/conference/osdi22/presentation/yu
    year: 2022
  - type: paper
    title: "Taming Throughput-Latency Tradeoff in LLM Inference with Sarathi-Serve"
    url: https://arxiv.org/abs/2403.02310
    year: 2024
  - type: repo
    title: "vLLM scheduler implementation"
    url: https://github.com/vllm-project/vllm
updated: 2026-08-21
---

## Simple Explanation

A server has one fixed pool of GPU memory and a queue of requests, all wanting
different amounts of it for unpredictable lengths of time. Someone has to decide,
sixty times a second, who runs now. That is the scheduler, and it is where a
serving engine's personality actually lives.

## Technical Definition

The control loop deciding, at each model iteration, which sequences are in the
running batch. It performs admission control against available KV cache blocks,
assembles a token budget mixing prefill chunks with decode tokens, preempts or
swaps sequences under memory pressure, and enforces fairness and priority
policies across requests.

## Why Does It Exist?

Requests arrive at unknown times, with prompts of wildly varying length and
outputs whose length nobody knows in advance — not even the model. Static
allocation therefore cannot work, and the resource being allocated (KV cache
memory) is consumed continuously as generation proceeds.

## What Problem Does It Solve?

Keeping the GPU fully utilised without running out of cache memory mid-generation
or starving any individual request.

## How Does It Work?

The token budget is the central dial. Spend it on prefill and time to first token
improves while everyone's streaming stutters; spend it on decode and streaming is
smooth while new requests wait longer.

## Mental Model

Air traffic control. One runway, aircraft of different sizes arriving unannounced,
none of them able to tell you exactly how long they need it for.

## Example

Preemption is the interesting case. When cache memory runs short, a running
sequence must give up its blocks. Two options: **swap** it to host memory and copy
back later, or **recompute** its prefill from scratch when it resumes. Recompute
costs compute; swapping costs PCIe bandwidth. Engines choose differently, and
under sustained overload this choice determines whether p99 latency degrades
gracefully or falls off a cliff.

## Real-World Usage

Every serving engine has one, and it is largely what distinguishes them. Policies
that matter in production: priority classes so interactive traffic beats batch
jobs, per-tenant fairness so one user cannot monopolise the cache, and admission
control that rejects rather than accepting work it cannot finish.

## Common Confusions

* **Scheduler vs batcher** — continuous batching is a *policy*; the scheduler is
  the component that implements it along with admission, preemption and priority.
* **Scheduling is not free** — it runs between every forward pass, so its own
  overhead sits directly on the critical path.
* **Queue depth is not throughput** — accepting more requests than the cache can
  hold makes latency worse without doing more work.

## Why Should I Care?

When production latency looks fine in isolation and terrible under load, the
scheduler's policies — not the model, not the kernels — are almost always where
the answer is.

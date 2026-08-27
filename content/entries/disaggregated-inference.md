---
term: Disaggregated Inference
aliases: [Prefill-Decode Disaggregation, P/D Disaggregation, Split Serving]
category: llm-inference
subcategory: batching
depth: full
status: emerging
difficulty: research
one_liner: "Running prefill and decode on separate pools of hardware, since one is compute-bound and the other bandwidth-bound."
origin:
  year: 2023
  circa: true
  attribution: Splitwise (Microsoft) and DistServe established the approach; deployed at scale from 2024
historical_period: agentic
diagram:
  kind: figure
  title: The two phases want different machines
  footer: The cost is moving the KV cache between pools, which needs a fast interconnect. Worth it at
    scale because the two pools can then be sized against their own measured demand instead of a compromise
    between them.
  visual:
    kind: columns
    width: 760
    caption: the cache crosses once, at the handover
    columns:
    - title: Prefill pool
      lines:
      - compute-bound
      - high tensor parallelism
      - short residency per request
      - sized for prompt volume
    - title: Decode pool
      accent: true
      lines:
      - bandwidth-bound
      - big batches, more memory
      - long residency per request
      - sized for concurrent users
tags: [inference]
relations:
  depends_on: [prefill, decode, kv-cache]
  related_to: [inference-scheduler, throughput, chunked-prefill, inference-latency]
prerequisites: [prefill, decode, continuous-batching]
encountered_in: [research-papers, production-systems, technical-blogs]
sources:
  - type: paper
    title: "DistServe: Disaggregating Prefill and Decoding for Goodput-optimized LLM Serving"
    url: https://arxiv.org/abs/2401.09670
    year: 2024
  - type: paper
    title: "Splitwise: Efficient Generative LLM Inference Using Phase Splitting"
    url: https://arxiv.org/abs/2311.18677
    year: 2023
updated: 2026-08-21
review_by: 2027-02-01
---

## Simple Explanation

Prefill and decode want opposite things from hardware and from each other. Mixing
them on the same GPU means every configuration choice is a compromise, and each
phase interferes with the other's latency. Disaggregation stops compromising: run
prefill on one set of machines, decode on another, and ship the KV cache between
them.

## Technical Definition

An architecture separating the two inference phases onto distinct hardware pools,
each independently scaled and configured, with the KV cache produced by prefill
transferred over a high-bandwidth interconnect to the decode pool. Each pool can
use its own parallelism strategy, batch policy and even accelerator type.

## Why Does It Exist?

Colocation creates unavoidable interference. A long prefill entering the batch
stalls everyone's decoding, which is visible to users as a stuttering stream.
Chunked prefill mitigates this; disaggregation removes the interference entirely
by not putting them on the same device.

## What Problem Does It Solve?

Latency interference between phases, and the inability to scale them
independently when a workload is lopsided — prompt-heavy RAG traffic needs far
more prefill capacity than a chat workload generating long answers.

## How Does It Work?

The transfer is the crux: the KV cache for a long prompt is gigabytes, and it has
to arrive before the first token can be produced. This is why the technique
depends on fast interconnects and why it is a data-centre technique rather than a
single-node one.

## Mental Model

A restaurant with a separate prep kitchen and service line. Prep can be scaled
for the lunch rush without disturbing service, at the cost of moving food between
rooms.

## Example

A workload with 20k-token prompts and 200-token answers is enormously
prefill-heavy. Colocated, prefill dominates and decode capacity sits idle;
disaggregated, you provision the two pools in the ratio the traffic actually
requires. The published results report meaningful goodput improvements at a
target latency — goodput being the right metric here, since the whole point is
serving more requests *within* the service level objective.

## Real-World Usage

Deployed at large inference providers and supported in newer versions of major
serving engines. It is unambiguously a scale technique: below a certain fleet
size the transfer overhead and operational complexity outweigh the gain, and
chunked prefill on colocated hardware is the better answer.

## Common Confusions

* **Disaggregation vs chunked prefill** — both target phase interference.
  Chunking interleaves them on one device; disaggregation separates them onto
  different devices. Chunking is the default; disaggregation is for fleets.
* **It does not reduce total work** — the same tokens are prefilled and decoded.
  It removes interference and allows independent scaling.
* **The transfer is not free** — cache movement adds to time to first token, and
  a slow interconnect can erase the benefit entirely.

## Why Should I Care?

It is the clearest architectural consequence of the prefill/decode split, and a
good illustration of how deeply that one distinction shapes serving design — from
kernel choices all the way up to data-centre topology.

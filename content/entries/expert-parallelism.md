---
term: Expert Parallelism
aliases: [EP, MoE Parallelism, Expert Sharding]
category: distributed-ai-systems
subcategory: parallelism
depth: full
status: modern
difficulty: research
one_liner: "Distributing a mixture-of-experts model's experts across devices, so routing a token becomes a network operation."
origin:
  year: 2020
  circa: true
  attribution: GShard and Switch Transformer established the pattern for training trillion-parameter MoE models
historical_period: foundation-model
diagram:
  kind: figure
  title: The tokens travel to the experts and back
  footer: 'Two all-to-all collectives per layer, which is the most demanding communication pattern in
    the stack. An unbalanced router makes it worse: some devices idle while others queue.'
  visual:
    kind: pipeline
    width: 740
    caption: experts are too large to replicate, so the tokens move instead — the opposite trade from
      data parallelism
    stages:
    - text: tokens arrive, spread across devices
      note: any device, any expert
    - text: each token assigned to its top experts
      via: the router scores
    - text: every token now sits where its expert lives
      tone: accent
      via: all-to-all dispatch — the expensive step
    - text: each expert processes what reached it
      note: ordinary FFN work
    - text: tokens back where they started, transformed
      via: all-to-all combine
tags: [hardware, inference]
relations:
  depends_on: [mixture-of-experts, all-reduce, gpu-cluster]
  alternative_to: [tensor-parallelism]
  related_to: [data-parallelism, pipeline-parallelism, throughput]
prerequisites: [mixture-of-experts, tensor-parallelism]
encountered_in: [research-papers, production-systems, github]
sources:
  - type: paper
    title: "GShard: Scaling Giant Models with Conditional Computation and Automatic Sharding"
    url: https://arxiv.org/abs/2006.16668
    year: 2020
  - type: paper
    title: "Switch Transformers: Scaling to Trillion Parameter Models"
    url: https://arxiv.org/abs/2101.03961
    year: 2021
updated: 2026-08-21
review_by: 2027-02-01
---

## Simple Explanation

A mixture-of-experts model has many expert networks and uses two of them per
token. All of them still have to live in memory somewhere, so at scale they are
spread across devices — expert 0 on GPU 0, expert 7 on GPU 3, and so on.

Which means routing is no longer a local decision. When a token picks an expert
on another GPU, the token has to *travel there*, be processed, and come back.
Routing becomes networking.

## Technical Definition

Partitioning a mixture-of-experts layer's experts across devices, with tokens
dispatched to the device holding their assigned expert and returned afterwards.
The communication pattern is **all-to-all**: every device may send tokens to
every other, twice per MoE layer — once to dispatch, once to combine.

## Why Does It Exist?

MoE models have enormous total parameter counts precisely because experts are
numerous. Replicating all of them on every device would defeat the design; the
memory saving only materialises if they are distributed.

## What Problem Does It Solve?

Fitting a model whose total parameters vastly exceed one device's memory, while
keeping per-token computation small.

## How Does It Work?

Two all-to-all collectives per MoE layer, and all-to-all is the most demanding
collective there is — every device talking to every other simultaneously.

## Mental Model

A hospital where specialists work in different buildings. The patient is
genuinely seen by the right consultant, and a great deal of time is spent in
corridors.

## Example

Load balance is the operational problem, and it is unforgiving. If a batch's
tokens disproportionately choose experts on one device, that device becomes the
straggler and every other GPU waits. This is why MoE training carries an
auxiliary load-balancing loss, why capacity factors cap how many tokens an expert
will accept (dropping the surplus), and why MoE serving throughput is far more
sensitive to batch composition than dense serving.

## Real-World Usage

Every large MoE deployment, composed with the other strategies — a configuration
might read `TP=4, EP=8, DP=16`. Serving engines have added expert-parallel support
as open-weight MoE models became common, and the engineering focus is
overwhelmingly on hiding the all-to-all behind computation.

## Common Confusions

* **Expert parallelism vs tensor parallelism** — distributing whole experts
  versus slicing individual matrices. They compose, and large deployments use
  both.
* **It does not reduce memory in total** — every expert still occupies memory
  somewhere. It distributes that memory rather than shrinking it.
* **All-to-all is not all-reduce** — no reduction happens; data is exchanged
  point-to-point between every pair, which is considerably more demanding of the
  network.

## Why Should I Care?

It is the parallelism strategy that mixture-of-experts forced into existence, and
it explains why MoE models are cheap in arithmetic and expensive in
infrastructure — the saving is real, and it is paid for in network traffic.

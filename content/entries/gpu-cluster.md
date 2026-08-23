---
term: GPU Cluster
aliases: [Training Cluster, AI Supercomputer, Node, Interconnect, NVLink]
category: distributed-ai-systems
subcategory: accelerators
depth: full
status: established
difficulty: advanced
one_liner: "Many accelerators wired together with a fast network, and the topology that decides how a model can be split across them."
origin:
  year: 2012
  circa: true
  attribution: Emerged as deep learning outgrew single machines; purpose-built AI clusters date from the late 2010s
historical_period: deep-learning
tags: [hardware]
relations:
  depends_on: [gpu, distributed-systems, all-reduce]
  used_by: [pretraining, tensor-parallelism, pipeline-parallelism, data-parallelism]
  related_to: [inference-provider, throughput, memory-hierarchy]
prerequisites: [gpu, distributed-systems]
encountered_in: [production-systems, job-descriptions, technical-blogs]
sources:
  - type: report
    title: "The Llama 3 Herd of Models — training infrastructure"
    url: https://arxiv.org/abs/2407.21783
    year: 2024
  - type: paper
    title: "Efficient Large-Scale Language Model Training on GPU Clusters (Megatron-LM)"
    url: https://arxiv.org/abs/2104.04473
    year: 2021
updated: 2026-08-21
---

## Simple Explanation

A cluster is not a pile of GPUs. It is a hierarchy of bandwidths, and that
hierarchy — fast inside a machine, slower between machines, slower again across
racks — dictates every decision about how a model gets split.

Read a cluster's topology and you can predict its parallelism configuration
before anyone tells you.

## Technical Definition

An interconnected set of accelerator nodes, each typically holding 8 GPUs joined
by a high-bandwidth intra-node fabric (NVLink and NVSwitch), with nodes connected
by InfiniBand or high-speed Ethernet, often in a fat-tree or rail-optimised
topology. Supporting infrastructure — parallel storage, checkpointing, scheduling,
power and cooling — is part of the system, not an accessory.

## Why Does It Exist?

Frontier models exceed any single machine by orders of magnitude in both memory
and compute. Once training must span machines, the network becomes a first-class
component of the computer rather than a peripheral.

## What Problem Does It Solve?

Aggregating enough memory and compute to train or serve a model that no single
device can hold.

## How Does It Work?

```text
        ┌──────── NODE ─────────┐   ┌──────── NODE ─────────┐
        │ GPU GPU GPU GPU       │   │ GPU GPU GPU GPU       │
        │ GPU GPU GPU GPU       │   │ GPU GPU GPU GPU       │
        │  ── NVLink, ~TB/s ──  │   │  ── NVLink, ~TB/s ──  │
        └───────────┬───────────┘   └───────────┬───────────┘
                    └──── InfiniBand, ~100s Gb/s ┘
                              (an order of magnitude slower)

which is exactly why:
   tensor parallelism  stays INSIDE a node   (constant chatter)
   pipeline parallelism spans nodes          (rare hand-offs)
   data parallelism     spans everything     (one all-reduce per step)
```

## Mental Model

A building rather than a room. Conversation across the desk is instant, down the
corridor is slower, between floors slower still — and you organise the work to
match.

## Example

At cluster scale, failure is the steady state rather than an incident. The Llama 3
training run reported frequent hardware failures across tens of thousands of GPUs,
which reframes the engineering problem: checkpoint frequently enough that a
failure costs little, detect stragglers before they hold up every step, and
restart automatically. Utilisation — the fraction of theoretical FLOPs actually
achieved — becomes the headline metric, and getting it high is mostly a
communication and reliability achievement rather than a compute one.

## Real-World Usage

Purpose-built clusters at frontier labs, cloud-provider GPU fleets, and rented
capacity from specialised providers. In serving, the same hierarchy applies at
smaller scale: which GPUs share a node determines the tensor-parallel degree you
can use without crossing a slow link.

## Common Confusions

* **More GPUs is not proportionally more throughput** — communication and
  stragglers eat the difference, and utilisation typically falls as clusters grow.
* **The interconnect is part of the computer** — a cluster with fast GPUs and a
  slow network is a slow cluster.
* **Training clusters and serving fleets are different machines** — one wants
  enormous synchronised jobs, the other many independent low-latency replicas.

## Why Should I Care?

Every parallelism decision in this domain is really a statement about a network
topology, and knowing the bandwidth hierarchy turns a configuration like
`TP=8, PP=4, DP=16` from an incantation into a description of the hardware.

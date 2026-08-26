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
diagram:
  kind: steps
  title: Two tiers of interconnect, an order of magnitude apart
  footer: Cluster topology is not an operational detail — it decides which parallelism strategy is even
    viable. Get the mapping wrong and the GPUs sit idle waiting for the network.
  steps:
  - title: Inside a node is fast; between nodes is not
    visual:
      kind: stack
      width: 740
      caption: the gap between these two rows is the single most important number in a training cluster
      layers:
      - label: within a node
        text: eight GPUs on NVLink
        note: ~TB/s
        accent: true
      - label: between nodes
        text: InfiniBand or RoCE across the fabric
        note: ~100s Gb/s
  - title: So each parallelism strategy sits where its traffic fits
    visual:
      kind: table
      width: 740
      head:
      - strategy
      - how much it talks
      - where it belongs
      rows:
      - - text: tensor
          new: true
        - text: twice per layer, constantly
          new: true
        - text: inside one node
          new: true
      - - pipeline
        - activations at stage boundaries
        - across nodes
      - - data
        - one all-reduce per step
        - across everything
      caption: a real cluster runs all three at once, nested in that order
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


A cluster has two interconnects and they differ by roughly an order of magnitude.
Inside a node, eight GPUs share a high-bandwidth fabric — NVLink or equivalent —
at terabytes per second. Between nodes, traffic crosses InfiniBand or RoCE at
hundreds of gigabits per second. Everything about how a training job is laid out
follows from that gap.

Tensor parallelism synchronises twice per layer, so it must stay inside a node
where the links are fast. Pipeline parallelism only hands activations across
stage boundaries, so it tolerates the slower fabric and spans nodes. Data
parallelism needs one all-reduce per optimiser step, which is infrequent enough
to span the whole cluster.

Real jobs nest all three in exactly that order, and the mapping is not an
operational detail — get it wrong and expensive accelerators sit idle waiting for
the network. Which is why the interconnect, not the GPU count, is usually what
determines whether a cluster trains efficiently.

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

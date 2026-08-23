---
term: NPU
aliases: [Neural Processing Unit, AI Accelerator, TPU, Tensor Processing Unit]
category: computing-foundations
subcategory: architecture
depth: full
status: modern
difficulty: intermediate
one_liner: "A chip built specifically for the matrix arithmetic that neural networks spend nearly all their time on."
origin:
  year: 2016
  circa: true
  attribution: Google's TPU was the first widely documented example; on-device NPUs followed in mobile silicon
historical_period: deep-learning
tags: [hardware]
relations:
  similar_to: [gpu]
  used_by: [quantization, small-language-model]
  related_to: [memory-hierarchy, cuda]
prerequisites: [gpu]
encountered_in: [production-systems, technical-blogs, job-descriptions]
sources:
  - type: paper
    title: "In-Datacenter Performance Analysis of a Tensor Processing Unit"
    url: https://arxiv.org/abs/1704.04760
    year: 2017
  - type: paper
    title: "Ten Lessons From Three Generations Shaped Google's TPUv4i"
    url: https://ieeexplore.ieee.org/document/9499913
    year: 2021
updated: 2026-08-21
review_by: 2027-02-01
---

## Simple Explanation

A GPU is general parallel hardware that happens to suit neural networks. An NPU
starts from the other end: build silicon that does one thing — multiply matrices
and accumulate — and strip away everything else.

Less flexible, considerably more efficient per watt, and the reason your phone
can run a model without the battery collapsing.

## Technical Definition

An accelerator specialised for tensor operations, typically built around
systolic arrays or comparable dataflow structures that stream data through a grid
of multiply-accumulate units, with on-chip memory sized to keep weights resident
and native support for low-precision arithmetic (int8, int4, fp8, bf16).

## Why Does It Exist?

Neural network inference is overwhelmingly one operation. General-purpose
hardware pays for flexibility it does not use — instruction decode, branch
prediction, caches designed for irregular access. Specialising recovers that as
performance per watt, which is the binding constraint both in data centres and on
battery-powered devices.

## What Problem Does It Solve?

Energy. In a data centre power is the limiting cost; on a phone it is the
limiting resource full stop.

## How Does It Work?

```text
systolic array: data flows through, results accumulate in place

  weights →  ┌───┬───┬───┬───┐
  inputs  →  │ × │ × │ × │ × │   each cell multiplies and adds,
             ├───┼───┼───┼───┤   passing partial sums onward
             │ × │ × │ × │ × │
             └───┴───┴───┴───┘   no fetching operands per operation —
                    ↓             that is where the energy saving lives
                 results
```

## Mental Model

A GPU is a well-equipped workshop. An NPU is a production line for one product:
useless for anything else, unbeatable at that.

## Example

The trade is flexibility. GPUs kept their lead in *training* partly because
training involves changing shapes, custom operations and new architectures, and
NPUs are unforgiving about anything outside their design point. For inference of
a fixed, quantised model, the efficiency advantage is substantial.

Google's TPU is the well-documented data-centre case; NPUs in phones and laptops
handle on-device transcription, image processing and increasingly small language
models.

## Real-World Usage

Data-centre training and inference at hyperscale, mobile and laptop NPUs for
on-device work, and a large field of startups building inference-specific silicon.
The software story is the hard part: CUDA's ecosystem is the incumbent advantage,
and every alternative accelerator has to solve compilation and framework support
before its hardware advantage matters.

## Common Confusions

* **NPU, TPU, AI accelerator** — largely the same category under vendor-specific
  names. TPU is Google's; NPU is the generic term, especially on-device.
* **Peak TOPS is marketing** — a headline throughput figure assumes ideal
  precision and utilisation. Real performance depends on memory bandwidth and on
  whether your model's operations map onto the hardware at all.
* **Specialised means brittle** — an unsupported operation falls back to CPU and
  destroys the performance advantage.

## Why Should I Care?

It is where the hardware market is heading, it explains why on-device AI became
viable, and it is a reminder that CUDA's dominance is a software fact rather than
a silicon one.

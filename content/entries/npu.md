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
diagram:
  kind: steps
  title: Data flows through the array; the operands never come back
  footer: The saving is not arithmetic — a multiply costs the same everywhere. It is that a systolic array
    moves each value into the array once and reuses it across a whole row, instead of fetching operands
    per operation.
  steps:
  - title: A grid of cells that each multiply, add, and pass the sum on
    notes:
    - label: Shape
      text: weights enter from one edge, activations from the other, results fall out the bottom
    visual:
      kind: matrix
      cell_width: 60
      show_values: false
      cols:
      - ''
      - ''
      - ''
      - ''
      rows:
      - label: ''
        values: [0.55, 0.55, 0.55, 0.55]
      - label: ''
        values: [0.55, 0.55, 0.55, 0.55]
      - label: ''
        values: [0.55, 0.55, 0.55, 0.55]
      - label: ''
        values: [0.55, 0.55, 0.55, 0.55]
      caption: every cell does the same thing, in lockstep, with no instruction to decode
  - title: Which is where the efficiency comes from
    visual:
      kind: bars
      caption: roughly, energy per multiply-accumulate
      bars:
      - label: CPU
        value: 1.0
        value_label: fetch, decode, schedule
      - label: GPU
        value: 0.28
        value_label: amortised across a warp
      - label: NPU
        value: 0.06
        value_label: operands already in place
        accent: true
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


A neural processing unit is built around one operation — matrix multiplication —
and gives up almost everything else to do it efficiently. The dominant design is
the systolic array: a grid of small cells, each of which multiplies two numbers,
adds the result to a running sum, and passes that sum to its neighbour.

Weights enter from one edge and activations from the other. A value that arrives
in the array is reused across an entire row or column before it leaves, so the
expensive part — moving data — happens once rather than once per operation. On a
general-purpose processor, fetching the operands costs more energy than the
multiply itself, and this is the arrangement that removes that cost.

Everything else follows from the specialisation. No instruction decoding, no
branch prediction, no cache hierarchy to speak of; often reduced precision as
well, since inference tolerates it. The result is far better performance per watt
than a GPU on the workload it was built for, and uselessness on anything with
data-dependent control flow.

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

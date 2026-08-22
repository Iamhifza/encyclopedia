---
term: TensorRT-LLM
aliases: [TRT-LLM, TensorRT]
category: llm-inference
subcategory: engines
depth: full
status: modern
difficulty: advanced
one_liner: "NVIDIA's inference library that compiles a model into hardware-specific kernels for maximum throughput on its own GPUs."
origin:
  year: 2023
  attribution: NVIDIA; built on the older TensorRT inference compiler
historical_period: foundation-model
tags: [inference]
relations:
  alternative_to: [vllm, sglang, llama-cpp]
  depends_on: [gpu-kernel, quantization, cuda, compiler]
  related_to: [continuous-batching, paged-attention, throughput]
prerequisites: [quantization, gpu-kernel]
encountered_in: [production-systems, github, job-descriptions]
sources:
  - type: repo
    title: "NVIDIA/TensorRT-LLM"
    url: https://github.com/NVIDIA/TensorRT-LLM
  - type: docs
    title: "TensorRT-LLM documentation"
    url: https://nvidia.github.io/TensorRT-LLM/
updated: 2026-08-21
review_by: 2027-02-01
---

## Simple Explanation

vLLM and SGLang are portable Python-centred servers that run well on most
hardware. TensorRT-LLM takes the opposite position: assume NVIDIA silicon,
compile the model ahead of time specifically for that chip, and extract every
percent the hardware can give.

You trade flexibility for speed, and the trade is real in both directions.

## Technical Definition

An inference library that compiles a model definition into an optimised engine
for a specific GPU architecture, batch size range and precision. Optimisations
include kernel fusion, layer and tensor fusion, automatic kernel selection by
autotuning, FP8 and INT4 quantisation with hardware support, in-flight batching,
paged KV cache and multi-GPU parallelism.

## Why Does It Exist?

NVIDIA has an obvious interest in its hardware appearing at its best, and general
serving stacks necessarily leave performance on the table by staying portable.
Ahead-of-time compilation for a known target recovers that.

## What Problem Does It Solve?

Peak throughput and latency on NVIDIA hardware, particularly with aggressive
quantisation on chips with native FP8 support.

## How Does It Work?

```text
model definition + target GPU + precision + batch/sequence bounds
        │
   BUILD (minutes, done once)
     autotune kernels · fuse layers · plan memory · select algorithms
        │
   compiled engine (a binary, tied to this GPU architecture)
        │
   SERVE: in-flight batching, paged cache, multi-GPU
```

That "tied to this GPU architecture" line is the crux. An engine built for one
chip generation does not run on another; changing precision, or exceeding the
sequence bounds you compiled for, means rebuilding.

## Mental Model

A bespoke suit against off-the-peg. Better fit, longer wait, and useless if you
change shape.

## Example

The practical comparison, at a level that survives version churn: TensorRT-LLM
typically leads on raw throughput on NVIDIA hardware; vLLM leads on ease of use,
model coverage and speed of adopting new architectures; SGLang leads on
prefix-heavy agent workloads. The build step is the real friction — an iteration
loop with a multi-minute compile is a different working experience from loading
weights and serving.

## Real-World Usage

Large-scale NVIDIA deployments where throughput per GPU translates directly into
cost, often behind NVIDIA's Triton Inference Server for the serving layer. Less
common where models change frequently or where portability across vendors is a
requirement.

## Common Confusions

* **TensorRT vs TensorRT-LLM** — the general inference compiler versus the
  LLM-specific library built on it. Different tools, related lineage.
* **Fastest in benchmarks is not fastest for you** — published numbers assume the
  configuration was compiled for, and results shift with every release of every
  engine.
* **It is NVIDIA-only** — that is the design, and it is the main argument against
  it if vendor independence matters.

## Why Should I Care?

It marks one end of the serving spectrum — maximum performance, minimum
portability — and knowing what the compilation step buys and costs is how you
decide whether that end is where you belong.

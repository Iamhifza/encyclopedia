---
term: Quantization
aliases: [Quantisation, Low-Precision Inference, INT8, FP8, GPTQ, AWQ]
category: llm-inference
subcategory: memory
status: established
difficulty: advanced
one_liner: Storing a model's numbers with fewer bits each, so it takes less memory and streams faster, at some cost in precision.
origin:
  year: 2015
  circa: true
  attribution: Long-standing in signal processing and embedded ML; LLM-specific methods from 2022 onward (LLM.int8, GPTQ, AWQ)
historical_period: foundation-model
diagram:
  kind: steps
  title: Fewer bits per weight, one scale per group
  footer: Quality loss is small down to about 4 bits and then falls off sharply. What actually breaks
    first is usually a handful of outlier activations, not the weights, which is why so many schemes treat
    those separately.
  steps:
  - title: Map a real range onto a small integer grid
    notes:
    - label: Stored
      text: a 4-bit index per weight, plus one fp16 scale for every group of 64 or 128
    visual:
      kind: pipeline
      width: 700
      stages:
      - text: fp16 weights
        note: range −2.4 … +2.1
      - text: one scale per group
        via: find the range within each group
      - text: int4 indices  −8 … +7
        tone: accent
        via: round each weight to the nearest grid point
      caption: dequantised inside the kernel, or fed straight to low-precision matrix units where the
        hardware has them
  - title: What that buys, on a 70B model
    visual:
      kind: table
      width: 700
      head:
      - format
      - bytes per weight
      - weights alone
      rows:
      - - fp16
        - '2'
        - 140 GB
      - - int8
        - '1'
        - 70 GB
      - - text: int4
          new: true
        - text: '0.5'
          new: true
        - text: 35 GB
          new: true
      caption: the difference between two cards and one
tags: [inference, hardware]
relations:
  depends_on: [memory-hierarchy]
  solves: [decode]
  used_by: [vllm]
  related_to: [kv-cache, distillation, gpu]
prerequisites: [decode, memory-hierarchy]
encountered_in: [production-systems, github, technical-blogs, job-descriptions]
sources:
  - type: paper
    title: "LLM.int8(): 8-bit Matrix Multiplication for Transformers at Scale"
    url: https://arxiv.org/abs/2208.07339
    year: 2022
  - type: paper
    title: "GPTQ: Accurate Post-Training Quantization for Generative Pre-trained Transformers"
    url: https://arxiv.org/abs/2210.17323
    year: 2022
  - type: paper
    title: "AWQ: Activation-aware Weight Quantization"
    url: https://arxiv.org/abs/2306.00978
    year: 2023
videos:
  - title: "LLM quantization explained"
    channel: "Efficient NLP"
    url: https://www.youtube.com/results?search_query=llm+quantization+explained+gptq+awq
updated: 2026-08-21
---

## Simple Explanation

Model weights are usually stored as 16-bit numbers. Most of that precision is not
doing anything useful. Store them as 8-bit or 4-bit numbers instead and the model
becomes two or four times smaller — which, since decoding is limited by how fast
weights can be read from memory, makes it proportionally faster too.

## Technical Definition

Mapping high-precision tensors to a lower-bit representation with a scale (and
possibly zero-point) per group, tensor or channel. Post-training quantisation
(PTQ) calibrates on a small dataset after training; quantisation-aware training
(QAT) simulates the rounding during training so the weights adapt to it.
Techniques differ mainly in how they handle outlier activations, which are the
main source of quality loss.

## Why Does It Exist?

Two independent pressures: models must fit in available memory, and decode speed
is bounded by bytes streamed per token. Halving the bits addresses both at once.

## What Problem Does It Solve?

Memory capacity (does this model fit on this GPU) and memory bandwidth (how fast
can each token be produced), plus cost per token as a direct consequence.

## How Does It Work?

Group size is the central tradeoff: smaller groups mean more scales to store but
much better accuracy.

## Mental Model

JPEG for weights. Discard precision the output does not depend on, keep the
structure, and accept a small, measurable degradation.

## Example

A 70B model: fp16 ≈ 140 GB (needs multiple GPUs), int8 ≈ 70 GB, int4 ≈ 35 GB
(fits on one 40 GB card). Well-implemented 8-bit weight quantisation typically
costs very little measurable quality; 4-bit is usually acceptable for chat and
noticeably riskier for precise reasoning, long-context recall and code.

## Real-World Usage

GPTQ and AWQ for weight-only 4-bit; FP8 on hardware with native support, now
common for both weights and activations; KV cache quantisation to fp8 or int4,
which attacks the other half of the memory problem. QLoRA combines 4-bit base
weights with higher-precision adapters to fine-tune large models on a single GPU.

## Common Confusions

* **Weight-only vs full quantisation** — weight-only helps memory-bound decode;
  quantising activations too is what unlocks faster compute-bound prefill.
* **Quantisation vs distillation** — quantisation compresses the same model;
  distillation trains a different, smaller one.
* **"4-bit is basically free"** — degradation is task-dependent and often
  invisible on generic benchmarks while showing up on long-context retrieval,
  structured output adherence and arithmetic. Measure on your own evaluation set.

## Why Should I Care?

It is usually the first and largest lever for fitting a model onto the hardware
you have, and the decision of how far to push it is a quality judgement that
belongs to whoever owns the evaluation suite.

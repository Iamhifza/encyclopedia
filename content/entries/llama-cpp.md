---
term: llama.cpp
aliases: [GGUF, llama-cpp, Ollama backend]
category: llm-inference
subcategory: engines
depth: full
status: modern
difficulty: beginner
one_liner: "A C++ inference engine that runs quantised models on ordinary laptops and phones, with no GPU required."
origin:
  year: 2023
  attribution: Georgi Gerganov; began as a weekend project to run Llama on a MacBook
historical_period: agentic
diagram:
  kind: figure
  title: One file, memory-mapped, running on whatever hardware is there
  footer: The project that made local inference ordinary. Its real contribution is GGUF and the quantisation
    formats — a self-describing file that a laptop can open without a Python environment anywhere in sight.
  visual:
    kind: pipeline
    width: 740
    caption: layers can be split between CPU and GPU, so a model larger than VRAM still runs — slower,
      but it runs
    stages:
    - text: model weights
      note: from any framework
    - text: one GGUF file
      note: Q4_K_M, Q5_K_M, Q8_0
      tone: accent
      via: quantise — self-describing, no external config
    - text: mapped from disk
      via: memory-mapped, so pages load on demand and are shared between processes
    - text: tokens
      via: hand-written SIMD kernels — AVX2, NEON — plus GPU offload
tags: [inference]
relations:
  alternative_to: [vllm, sglang]
  depends_on: [quantization, memory-hierarchy]
  used_by: [small-language-model, open-weight-model]
prerequisites: [quantization]
encountered_in: [github, production-systems, social-media]
sources:
  - type: repo
    title: "ggml-org/llama.cpp"
    url: https://github.com/ggml-org/llama.cpp
  - type: docs
    title: "GGUF file format specification"
    url: https://github.com/ggml-org/ggml/blob/master/docs/gguf.md
updated: 2026-08-21
review_by: 2027-02-01
---

## Simple Explanation

The serving engines in this domain assume a data centre: several GPUs, plenty of
memory, many concurrent users. llama.cpp assumes the opposite — one person, one
laptop, no CUDA, possibly no GPU at all.

It matters far beyond hobbyist use. It is the reason "run a model locally" became
something an ordinary person could do in an afternoon, and it is the engine
underneath most consumer-facing local AI tools.

## Technical Definition

A dependency-free C/C++ implementation of Transformer inference built on the ggml
tensor library, with aggressive quantisation support (2 to 8 bits), CPU SIMD
kernels, memory-mapped weight loading, and optional acceleration through Metal,
CUDA, ROCm or Vulkan. Models are distributed in the GGUF format, which packs
weights and metadata into a single self-describing file.

## Why Does It Exist?

Running a model in 2023 meant Python, PyTorch, CUDA, a matching driver and a
GPU with enough memory. That excluded nearly everyone. The project's premise was
that a laptop's CPU and unified memory were sufficient if the model was quantised
hard enough and the code was written for that case.

## What Problem Does It Solve?

Access. Privacy, offline operation, zero marginal cost, and no dependency on a
provider — all downstream of being able to run the thing at all.

## How Does It Work?

Memory mapping is the underrated part: a 4 GB model file need not be read into
RAM in full, and two processes running the same model share the pages.

## Mental Model

A hand-built engine for a specific car rather than a modular industrial one.
Narrow in scope, remarkably efficient inside it.

## Example

The quantisation naming trips everyone up. `Q4_K_M` means 4-bit, K-quant method,
medium size — a mixed scheme applying different precision to different tensors,
because some layers tolerate compression far better than others. As a practical
rule, Q4_K_M is the common quality-size compromise, Q8_0 is near-lossless and
twice the size, and anything below Q4 degrades noticeably.

## Real-World Usage

The backend for most consumer local-AI applications, including Ollama and similar
tools. Used for on-device inference, air-gapped deployments, privacy-sensitive
work, and embedded systems. Not the right tool for serving many concurrent users —
it is optimised for single-stream latency, not throughput.

## Common Confusions

* **llama.cpp is not limited to Llama** — the name is historical; it runs most
  open-weight architectures.
* **GGUF is not a quantisation method** — it is a container format. The
  quantisation scheme is recorded inside it.
* **CPU inference is bandwidth-bound too** — the same physics as GPU decode, with
  roughly a tenth of the memory bandwidth, which is why speed scales with RAM
  speed more than with core count.

## Why Should I Care?

It is the most widely used inference engine by number of installations, it made
local AI real, and it demonstrates that the constraint on running these models
was never purely hardware — it was software written for the wrong assumptions.

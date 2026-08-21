---
term: vLLM
aliases: [vLLM Serving Engine]
category: llm-inference
subcategory: engines
status: modern
difficulty: intermediate
one_liner: An open-source inference server for large language models, built around paged KV cache memory and continuous batching.
origin:
  year: 2023
  attribution: Sky Computing Lab, UC Berkeley; now a community project
historical_period: foundation-model
tags: [inference]
relations:
  depends_on: [continuous-batching, kv-cache, flash-attention]
  used_by: [tensor-parallelism]
prerequisites: [kv-cache, continuous-batching]
encountered_in: [github, production-systems, job-descriptions, conferences]
sources:
  - type: repo
    title: "vllm-project/vllm"
    url: https://github.com/vllm-project/vllm
  - type: paper
    title: "Efficient Memory Management for Large Language Model Serving with PagedAttention"
    url: https://arxiv.org/abs/2309.06180
    year: 2023
  - type: docs
    title: "vLLM documentation"
    url: https://docs.vllm.ai/
updated: 2026-08-21
review_by: 2027-02-01
---

## Simple Explanation

Running a model in a research script is easy and slow. vLLM is the production
answer: a server that holds the model, accepts many requests at once, packs them
together efficiently, and streams results back through an OpenAI-compatible API.

## Technical Definition

A high-throughput LLM inference and serving engine implementing PagedAttention,
continuous batching, automatic prefix caching, chunked prefill, tensor and
pipeline parallelism, speculative decoding, structured-output decoding and a
range of quantisation formats, exposed through both a Python API and an
OpenAI-compatible HTTP server.

## Why Does It Exist?

The reference implementations everyone started from were built for research
convenience, not for serving. They wasted most of their KV cache memory and could
not keep a GPU busy. vLLM was the paper's artefact and turned out to be the
production tool.

## What Problem Does It Solve?

Serving many concurrent users from one model deployment at acceptable cost,
without writing custom scheduling and memory management.

## How Does It Work?

```text
HTTP / OpenAI-compatible API
        │
   scheduler ── decides, each step, which sequences run
        │       (admission, preemption, chunked prefill)
   block manager ── allocates paged KV cache blocks, shares prefixes
        │
   model executor ── fused kernels, parallelism across GPUs
        │
   sampler ── temperature, top-p, grammar constraints
        │
   streamed tokens back to each caller
```

## Mental Model

An operating system for a model: it schedules processes (requests), manages
virtual memory (paged KV cache), and multiplexes one expensive resource among
many users.

## Example

```console
$ vllm serve meta-llama/Llama-3.1-8B-Instruct --tensor-parallel-size 2
```

Then any OpenAI-compatible client points at it — which is why it is the default
choice for self-hosting open-weight models behind existing application code.

## Real-World Usage

Widely deployed for self-hosted inference and used as the serving layer inside
many inference providers and internal platforms. The main alternatives are
TensorRT-LLM (NVIDIA-optimised, highest performance on NVIDIA hardware, less
portable), SGLang (strong on structured and multi-turn programs), llama.cpp
(local and CPU-friendly), and Hugging Face Transformers (reference correctness,
not throughput).

## Common Confusions

* **vLLM is not a model** — it runs models; the "v" does not indicate a model
  family.
* **Throughput gains are workload-dependent** — the large published wins come
  from memory efficiency under concurrency, so single-user local use sees far
  less benefit.
* **Fast-moving** — features and defaults change release to release; check the
  documentation rather than a blog post from last year.

## Why Should I Care?

It is the reference implementation of nearly every concept in this domain. Reading
its scheduler is the shortest route from understanding inference in theory to
understanding it in production.

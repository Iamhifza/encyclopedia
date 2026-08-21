---
term: Tensor Parallelism
aliases: [TP, Model Parallelism, Megatron-style Parallelism]
category: distributed-ai-systems
subcategory: parallelism
status: established
difficulty: advanced
one_liner: Splitting each individual weight matrix across several GPUs so they compute one layer together.
origin:
  year: 2019
  attribution: Shoeybi et al., Megatron-LM
historical_period: transformer
tags: [hardware, inference]
relations:
  alternative_to: [pipeline-parallelism]
  depends_on: [gpu]
  used_by: [pretraining, vllm]
  related_to: [memory-hierarchy]
prerequisites: [gpu, transformer]
encountered_in: [production-systems, github, job-descriptions, research-papers]
sources:
  - type: paper
    title: "Megatron-LM: Training Multi-Billion Parameter Language Models Using Model Parallelism"
    url: https://arxiv.org/abs/1909.08053
    year: 2019
  - type: paper
    title: "Efficiently Scaling Transformer Inference"
    url: https://arxiv.org/abs/2211.05102
    year: 2022
updated: 2026-08-21
---

## Simple Explanation

A model too big for one GPU has to be split. Tensor parallelism cuts each weight
matrix into vertical or horizontal slices, gives each GPU a slice, and has them
combine partial results after every layer. All GPUs work on the same tokens at
the same time.

## Technical Definition

Intra-layer partitioning of weight matrices across devices. In a Transformer
block, attention heads and the first feed-forward matrix are split column-wise
and the second row-wise, so that exactly one all-reduce is needed per attention
sublayer and one per MLP sublayer.

## Why Does It Exist?

Model weights plus activations plus KV cache exceed single-device memory well
before models reach useful frontier sizes.

## What Problem Does It Solve?

Fitting a model that does not fit, and reducing per-token latency by putting more
aggregate memory bandwidth behind each forward pass.

## How Does It Work?

```text
      GPU 0            GPU 1            GPU 2            GPU 3
  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
  │ heads 0-7│    │heads 8-15│    │heads16-23│    │heads24-31│
  └────┬─────┘    └────┬─────┘    └────┬─────┘    └────┬─────┘
       └───────── all-reduce across the interconnect ──┘
                    (twice per layer)
```

## Mental Model

Four accountants each auditing a quarter of every page, comparing notes at the
end of each page. It works only if they can talk very fast.

## Example

A 70B model in fp16 needs ~140 GB. Split across four 80 GB GPUs with TP=4, each
holds ~35 GB of weights plus its share of the KV cache. The catch is
communication: with two all-reduces per layer and eighty layers, that is 160
synchronisations per forward pass, which is why tensor parallelism is normally
confined to GPUs inside one node with a fast interconnect.

## Common Confusions

* **Tensor vs pipeline parallelism** — tensor splits *within* a layer and
  communicates constantly; pipeline splits *between* layers and communicates
  rarely but introduces bubbles. Large deployments use both, plus data
  parallelism, plus expert parallelism for mixture-of-experts models.
* **Tensor parallelism does not increase throughput per GPU** — it buys capacity
  and latency, and pays for both in communication.
* **Degree must divide the head count** — TP=6 on 32 heads is not a valid
  configuration.

## Real-World Usage

Set with a single flag in most serving stacks (`--tensor-parallel-size` in vLLM).
The practical rule is to use the smallest degree that fits the model and cache,
because every added rank adds communication.

## Why Should I Care?

It is the first question in any large deployment — will this fit, and at what
communication cost — and the answer determines the hardware bill.

---
term: Hugging Face Transformers
aliases: [Transformers Library, HF Transformers, transformers]
category: llm-inference
subcategory: engines
depth: full
status: established
difficulty: beginner
one_liner: "The reference Python library for loading and running models, optimised for correctness and breadth rather than serving throughput."
origin:
  year: 2019
  attribution: Hugging Face; began as pytorch-pretrained-bert
historical_period: transformer
tags: [inference]
relations:
  alternative_to: [vllm, llama-cpp]
  implemented_by: [transformer]
  related_to: [open-weight-model, lora, quantization, tokenization]
prerequisites: [transformer]
encountered_in: [github, research-papers, production-systems, documentation]
sources:
  - type: repo
    title: "huggingface/transformers"
    url: https://github.com/huggingface/transformers
  - type: paper
    title: "Transformers: State-of-the-Art Natural Language Processing"
    url: https://arxiv.org/abs/1910.03771
    year: 2019
updated: 2026-08-21
---

## Simple Explanation

Before this library, using someone else's model meant finding their repository,
matching their framework version, and reimplementing their preprocessing from a
paper. Every model was a small archaeology project.

Transformers made it three lines. That standardisation did more for the field's
pace than most architectural advances, because it turned "reproduce this result"
from a week into an afternoon.

## Technical Definition

A Python library providing unified implementations of Transformer architectures
with a consistent API for loading pretrained weights, tokenising, running
inference and training. Paired with the Hub, which hosts weights, tokenisers,
configurations and datasets under a common format.

## Why Does It Exist?

Research reproducibility was genuinely bad. Papers described architectures;
running them required finding the code, guessing the preprocessing and hoping the
checkpoints matched. A shared implementation standard removed a large tax the
whole field was paying.

## What Problem Does It Solve?

Model portability and access. One API across hundreds of architectures, and a
distribution channel that made open weights actually usable.

## How Does It Work?

```text
from transformers import AutoModelForCausalLM, AutoTokenizer

tok   = AutoTokenizer.from_pretrained("org/model")
model = AutoModelForCausalLM.from_pretrained("org/model")

the Auto classes read the model's config and instantiate
the right architecture — so the same three lines work
for hundreds of different models
```

## Mental Model

The standard library of the field. Not the fastest implementation of anything,
and the one everything else is measured against.

## Example

The performance caveat matters. Naive generation in this library is
single-sequence, eager-executed, and lacks the scheduling and memory management
that serving engines provide — often an order of magnitude behind vLLM on
concurrent throughput. That is not a defect; it reflects a different goal.
Correctness, readability and breadth are what a reference implementation owes,
and serving engines exist precisely to make the other trade.

## Real-World Usage

Research and experimentation, fine-tuning (with PEFT for LoRA and TRL for
preference training), single-request inference, and as the canonical
implementation new architectures are contributed to. Production serving usually
moves to vLLM, SGLang or TensorRT-LLM — often loading weights from the same Hub.

## Common Confusions

* **Hugging Face is a company, transformers is one library** — they also maintain
  the Hub, datasets, tokenizers, accelerate, PEFT, TRL and more.
* **It is not a serving engine** — using it directly behind a web endpoint is a
  common early mistake that shows up as terrible throughput under concurrency.
* **Model support arrives here first** — new architectures typically land here
  before serving engines implement them, which is a real reason to use it early
  in a model's life.

## Why Should I Care?

It is the common substrate of the open model ecosystem — the format weights are
published in, the API examples are written against, and the implementation new
architectures are defined by.

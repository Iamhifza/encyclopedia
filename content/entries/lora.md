---
term: LoRA
aliases: [Low-Rank Adaptation, QLoRA, Adapters, PEFT]
category: llm-training
subcategory: adaptation
status: established
difficulty: advanced
one_liner: Fine-tuning a large model by training two small matrices per layer instead of all its weights, cutting the cost by orders of magnitude.
origin:
  year: 2021
  attribution: Hu et al., Microsoft
historical_period: foundation-model
diagram:
  kind: steps
  title: Freeze the matrix, learn a thin correction beside it
  footer: The adapter can be merged into the base weights after training, so inference costs nothing extra
    — or kept separate, so one served base model can carry hundreds of adapters swapped per request.
  steps:
  - title: Two paths, only one of them trainable
    visual:
      kind: columns
      width: 700
      columns:
      - title: frozen
        lines:
        - W₀, shape d × k
        - never updated
        - no optimiser state
      - title: trainable
        accent: true
        lines:
        - B·A, rank r
        - r typically 8 – 64
        - added to W₀'s output
      caption: the update is constrained to a low-rank subspace, which is empirically where most of fine-tuning's
        change lives anyway
  - title: What that saves on one 4096 × 4096 layer
    visual:
      kind: table
      width: 700
      head:
      - approach
      - trainable parameters
      - optimiser state
      rows:
      - - full fine-tune
        - 16.8 M
        - ~200 MB
      - - text: LoRA, r = 16
          new: true
        - text: 0.13 M  —  0.8%
          new: true
        - text: ~1.6 MB
          new: true
      caption: which is the difference between a cluster and one consumer card
tags: [training]
relations:
  is_a: [supervised-fine-tuning]
  depends_on: [quantization]
  alternative_to: [distillation]
  related_to: [large-language-model]
prerequisites: [supervised-fine-tuning]
encountered_in: [github, production-systems, job-descriptions, research-papers]
sources:
  - type: paper
    title: "LoRA: Low-Rank Adaptation of Large Language Models"
    url: https://arxiv.org/abs/2106.09685
    year: 2021
  - type: paper
    title: "QLoRA: Efficient Finetuning of Quantized LLMs"
    url: https://arxiv.org/abs/2305.14314
    year: 2023
  - type: repo
    title: "Hugging Face PEFT"
    url: https://github.com/huggingface/peft
updated: 2026-08-21
---

## Simple Explanation

Full fine-tuning updates every weight and needs enough memory for the model, its
gradients and its optimiser state — often ten times the model's own size. LoRA
freezes the model and learns a small correction alongside it: two thin matrices
whose product has the same shape as the weight matrix.

## Technical Definition

For a frozen weight $W_0 \in \mathbb{R}^{d \times k}$, learn $\Delta W = BA$ with
$B \in \mathbb{R}^{d \times r}$, $A \in \mathbb{R}^{r \times k}$ and rank
$r \ll \min(d,k)$. The forward pass computes $W_0x + \frac{\alpha}{r}BAx$. Only
$A$ and $B$ receive gradients, reducing trainable parameters by three to four
orders of magnitude.

## Why Does It Exist?

Full fine-tuning of a 70B model needs a multi-GPU cluster. The observation that
the *update* required for adaptation has low intrinsic rank means the same effect
can be had for a fraction of the memory.

## What Problem Does It Solve?

The cost of adaptation, the storage cost of many task-specific models, and the
operational problem of serving them: adapters are megabytes, not gigabytes, and
can be swapped or merged at will.

## How Does It Work?

At inference $BA$ can be merged into $W_0$, so a merged LoRA adds no latency;
kept separate, many adapters can share one base model in memory.

## Mental Model

Sticky notes on a reference manual. The manual is untouched; the notes are small,
portable, and can be swapped for a different task.

## Formula

$$h = W_0 x + \frac{\alpha}{r} B A x$$

* $r$ — rank; capacity of the adaptation. Higher fits more, risks more
  overfitting.
* $\alpha$ — scaling factor controlling how strongly the adaptation applies.
* $B$ initialised to zero, so training starts exactly at the base model.

## Example

QLoRA combines a 4-bit quantised frozen base with 16-bit LoRA adapters, making
fine-tuning of a 65B model possible on a single 48 GB GPU — the result that put
large-model fine-tuning within reach of individuals.

## Real-World Usage

The default fine-tuning method outside frontier labs. Serving stacks support
multi-adapter deployment, so one base model can serve many customers' customised
behaviour simultaneously.

## Common Confusions

* **LoRA does not add knowledge efficiently** — it is well suited to style,
  format and task behaviour, poorly suited to injecting facts. Use retrieval for
  facts.
* **Rank is not quality** — beyond the task's intrinsic rank, more capacity
  mostly buys overfitting.
* **Merged vs unmerged** — merging costs nothing at inference but ends the
  ability to hot-swap adapters.

## Why Should I Care?

It is what makes customisation affordable, and it turns fine-tuning from a
capital expense into an experiment you can run in an afternoon.

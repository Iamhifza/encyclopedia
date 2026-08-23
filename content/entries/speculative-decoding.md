---
term: Speculative Decoding
aliases: [Speculative Sampling, Draft-and-Verify Decoding, Assisted Generation]
category: llm-inference
subcategory: decoding
status: modern
difficulty: advanced
one_liner: Having a small fast model guess the next several tokens, then checking them all in one pass of the big model and keeping the ones it agrees with.
origin:
  year: 2022
  attribution: Leviathan et al. (Google) and Chen et al. (DeepMind), independently
historical_period: foundation-model
tags: [inference]
relations:
  depends_on: [decode, autoregressive-generation]
  solves: [inference-latency]
  related_to: [distillation, throughput]
prerequisites: [decode, sampling]
encountered_in: [research-papers, production-systems, github]
sources:
  - type: paper
    title: "Fast Inference from Transformers via Speculative Decoding"
    url: https://arxiv.org/abs/2211.17192
    year: 2022
  - type: paper
    title: "Accelerating Large Language Model Decoding with Speculative Sampling"
    url: https://arxiv.org/abs/2302.01318
    year: 2023
  - type: paper
    title: "Medusa: Simple LLM Inference Acceleration with Multiple Decoding Heads"
    url: https://arxiv.org/abs/2401.10774
    year: 2024
updated: 2026-08-21
review_by: 2027-02-01
---

## Simple Explanation

Most tokens are easy. Once a sentence is underway, a much smaller model can
usually guess the next few words correctly. So let it guess four, then run the
big model once over all four to check them. Every guess the big model agrees with
is a token you got for free.

## Technical Definition

A two-stage decoding scheme: a cheap draft model proposes $k$ candidate tokens
autoregressively; the target model scores all $k+1$ positions in a single forward
pass; a modified rejection-sampling rule accepts the longest correct prefix and
resamples at the first divergence. The acceptance rule is constructed so that the
output distribution is provably identical to sampling from the target model
alone.

## Why Does It Exist?

Decode is memory-bandwidth-bound: verifying five tokens costs almost exactly as
much as generating one, because both require streaming the full weights once. The
spare arithmetic capacity is free, so spending it on verification is close to
pure gain.

## What Problem Does It Solve?

Per-token latency during decoding, without changing the model's output
distribution and without any quality loss.

## How Does It Work?

```text
draft model (fast):  "the cache stores keys and"  ──▶ proposes: [values][for][each]
                                                                  │
target model (slow): ONE forward pass over all proposals
                     agrees: values ✓  for ✓  each ✗
                                                                  │
accepted: "values for"  + one resampled token from the target ────┘
next round starts from there
```

If nothing is accepted you still get one token — the same as ordinary decoding —
so the worst case is the draft model's overhead, not a stall.

## Mental Model

An autocomplete suggestion that a fastidious editor either signs off on wholesale
or truncates at the first word they disagree with.

## Formula

Expected tokens per verification pass:

$$\mathbb{E}[\text{accepted}] = \frac{1 - \alpha^{k+1}}{1 - \alpha}$$

* $\alpha$ — per-token acceptance rate, how often the draft agrees with the target.
* $k$ — number of tokens drafted per round.

At $\alpha = 0.8$ and $k = 4$ this is about 3.4 tokens per pass — roughly a 2-3×
speedup after draft overhead.

## Example

A 70B target paired with a 1B draft from the same family. On predictable text —
boilerplate code, formatting, repetitive prose — acceptance is very high and the
speedup is large. On dense reasoning it falls, because that is exactly where the
small model's predictions diverge.

## Real-World Usage

Supported in vLLM, TensorRT-LLM and llama.cpp. Variants avoid needing a separate
model: Medusa adds extra prediction heads to the target, EAGLE drafts in feature
space, and n-gram or prompt-lookup decoding drafts by copying from the prompt,
which works remarkably well for code editing and summarisation where output
repeats input.

## Common Confusions

* **It does not reduce quality** — the acceptance rule preserves the target
  distribution exactly. This is what makes it different from simply using a
  smaller model.
* **It does not improve throughput at high batch size** — under heavy batching
  the GPU is already saturated and the spare capacity that made verification free
  no longer exists. It is a latency optimisation.
* **Draft quality matters more than draft size** — a well-aligned tiny draft
  beats a large poorly-matched one, because acceptance rate is everything.

## Why Should I Care?

It is the rare optimisation that buys latency with no quality cost, and it is a
clean illustration of the central fact of LLM serving: during decode you have
arithmetic to burn and no bandwidth to spare.

---
term: State-Space Model
aliases: [SSM, Mamba, S4, Selective State Space Model]
category: deep-learning
subcategory: sequence
status: experimental
difficulty: research
one_liner: A sequence architecture that keeps a fixed-size running state like an RNN, but can be trained in parallel like a Transformer.
origin:
  year: 2021
  attribution: Gu et al. (S4); Mamba introduced selective state spaces in 2023
historical_period: foundation-model
tags: [architecture]
relations:
  alternative_to: [transformer]
  successor_of: [lstm]
  related_to: [kv-cache, context-window]
prerequisites: [rnn, transformer]
encountered_in: [research-papers, conferences, github]
sources:
  - type: paper
    title: "Efficiently Modeling Long Sequences with Structured State Spaces (S4)"
    url: https://arxiv.org/abs/2111.00396
    year: 2021
  - type: paper
    title: "Mamba: Linear-Time Sequence Modeling with Selective State Spaces"
    url: https://arxiv.org/abs/2312.00752
    year: 2023
updated: 2026-08-21
review_by: 2027-02-01
---

## Simple Explanation

Attention keeps every previous token and looks at all of them, which costs more
as the sequence grows. State-space models keep one fixed-size summary that is
updated at each step — constant memory, constant cost per token — but unlike old
RNNs they can be computed in parallel during training.

## Technical Definition

A sequence model based on a linear recurrence $h_t = A h_{t-1} + B x_t$,
$y_t = C h_t$, structured so the recurrence can be evaluated as a convolution or
parallel scan during training and as a stateful recurrence during inference.
Mamba makes $B$, $C$ and the step size input-dependent, allowing the model to
select what to keep.

## Why Does It Exist?

Attention is quadratic in sequence length and its KV cache grows without bound.
For very long sequences — genomics, audio, long documents — that is prohibitive.

## What Problem Does It Solve?

Linear-time sequence modelling with constant inference memory, and no KV cache at
all.

## How Does It Work?

```text
Transformer:  cost per token grows with history; memory grows linearly
SSM:          fixed-size state h; O(1) memory, O(1) per-token cost
              training via parallel scan, inference via recurrence
```

## Mental Model

A running summary rather than a full transcript. Cheap and constant, but once
something is compressed out of the summary it is gone.

## Example

Mamba matched similarly sized Transformers on language modelling with much better
long-sequence scaling. In practice the strongest results have come from *hybrid*
models that interleave a few attention layers with many SSM layers, since exact
recall of specific earlier tokens is where pure SSMs are weakest.

## Real-World Usage

Shipped in several open-weight hybrid models and used in audio, genomics and
time-series work. Attention remains dominant for general language models.

## Terminology Note

"State-space model" also means something quite different in control theory and
econometrics, where it refers to latent-variable time-series models. The deep
learning usage borrows the formalism, not the field.

## Common Confusions

* **SSM vs RNN** — mathematically related, but the linear structured recurrence
  is what makes parallel training possible, which is what killed classic RNNs.
* **"SSMs replace Transformers"** — as of 2026 they have not. The honest summary
  is a real efficiency advantage and a real recall disadvantage.

## Why Should I Care?

It is the most credible current challenge to attention, and a useful reminder
that the Transformer is a choice with tradeoffs rather than a settled endpoint.

---
title: Transformer vs RNN
question: Why did attention replace recurrence so completely?
sides: [transformer, rnn]
---

## The short version

Two defects killed the RNN for language: a fixed-size memory bottleneck, and
strictly sequential training that left GPUs idle. The Transformer removes both,
and pays for it with quadratic cost in sequence length.

## Side by side

| | RNN / LSTM | Transformer |
|---|---|---|
| **History held as** | One fixed-size hidden state | Every previous token, attended over |
| **Path between distant tokens** | O(n) steps | O(1) — one attention hop |
| **Training** | Sequential over time steps | Fully parallel across positions |
| **Compute per token** | Constant | Grows with context length |
| **Inference memory** | Constant | KV cache grows linearly |
| **Long-range dependency** | Degrades; gradients attenuate | Direct, though attention dilutes at extreme length |
| **Hardware fit** | Poor — cannot saturate a GPU | Excellent — dense matrix multiplies |

## The trade, stated plainly

The RNN compresses; the Transformer remembers. Compression is cheap and lossy.
Remembering is expensive and exact. In 2017 the hardware made expensive-and-exact
the better bet, and everything since — the KV cache, PagedAttention,
FlashAttention, GQA — is the bill for that choice.

## Why this comparison is live again

State-space models such as Mamba are an attempt to recover the RNN's constant
memory and linear cost while keeping parallel training, via a structured linear
recurrence. Current results suggest the classic trade persists in a new form:
strong efficiency at long sequence lengths, weaker exact recall of specific
earlier tokens. The strongest models in this line are hybrids that keep a few
attention layers precisely for recall.

## Verdict

The Transformer won on hardware utilisation and long-range fidelity, not on
elegance. Understanding what the RNN did badly is the fastest way to understand
why every part of the Transformer is shaped the way it is.

---
term: Transformer
aliases: [Transformer Architecture, Decoder-Only Transformer]
category: transformers
subcategory: block
status: foundational
difficulty: intermediate
one_liner: The neural network architecture built from stacked self-attention and feed-forward layers that underpins essentially every modern language model.
origin:
  year: 2017
  attribution: Vaswani et al. at Google, "Attention Is All You Need"
historical_period: transformer
tags: [architecture]
relations:
  is_a: [neural-network]
  successor_of: [rnn]
  depends_on: [self-attention, rope]
  evolved_into: [large-language-model]
  implemented_by: [vllm]
  alternative_to: [state-space-model]
prerequisites: [self-attention]
encountered_in: [research-papers, github, interviews, job-descriptions]
sources:
  - type: paper
    title: "Attention Is All You Need"
    url: https://arxiv.org/abs/1706.03762
    year: 2017
  - type: repo
    title: "nanoGPT — a minimal, readable Transformer implementation"
    url: https://github.com/karpathy/nanoGPT
  - type: post
    title: "The Annotated Transformer"
    url: https://nlp.seas.harvard.edu/annotated-transformer/
updated: 2026-08-21
---

## Simple Explanation

Take a stack of identical blocks. Each block does two things: let every token
look at every other token (attention), then let every token think about what it
just gathered (a small feed-forward network). Repeat sixty or a hundred times.
That is the whole architecture.

## Technical Definition

A sequence model composed of $L$ identical blocks, each applying multi-head
self-attention followed by a position-wise feed-forward network, with residual
connections around both sublayers and layer normalisation (in modern
implementations, RMSNorm applied pre-sublayer). Position information is injected
by positional encoding, now usually rotary. The original design was
encoder-decoder; contemporary LLMs are overwhelmingly decoder-only with causal
masking.

## Why Does It Exist?

Recurrent models forced $O(n)$ sequential steps per sequence, which left GPUs
idle and made long-range learning fragile. The Transformer replaced recurrence
with attention so that all positions are processed simultaneously during
training, converting a latency-bound problem into a throughput-bound one that
hardware could attack.

## What Problem Does It Solve?

Parallel training on very long sequences, with a constant-length path between
any two positions.

## How Does It Work?

```text
                 ┌─────────────────────────────┐
tokens ──▶ embed │  ┌── LayerNorm             │
        + position│  │   Multi-Head Attention  │ ×L
                 │  └── + residual            │
                 │  ┌── LayerNorm             │
                 │  │   Feed-Forward (4× wide)│
                 │  └── + residual            │
                 └─────────────────────────────┘
                              │
                        final LayerNorm
                              │
                    unembed ──▶ logits over vocabulary
```

Attention moves information *between* positions; the feed-forward network
processes each position independently and holds most of the parameters. The
residual stream running through every block is the shared bus that all layers
read from and write to.

## Mental Model

A relay of editorial passes over a document. In each pass, every sentence first
consults every other sentence, then privately revises itself. Nothing is
rewritten from scratch — each pass adds a correction to the running draft, which
is what the residual connections implement.

## Example

A 32-layer decoder-only model with hidden size 4096 processing "the KV cache
stores": the embedding layer maps four tokens to four vectors; each block lets
"stores" gather context from "cache"; after 32 blocks the final position's vector
is projected to vocabulary logits, and "keys" scores highest.

## Real-World Usage

GPT, Claude, Llama, Gemini, Qwen, Mistral — all decoder-only Transformers
differing in width, depth, attention variant, normalisation placement,
activation function and training data far more than in fundamental design. The
architecture has been remarkably stable since 2017; the changes since are
efficiency work.

## Historical Origin

Published June 2017 for machine translation. BERT (2018) took the encoder half,
GPT (2018) took the decoder half, and the decoder-only branch won for generative
use.

## Evolution

```text
RNN → LSTM → attention → Transformer → foundation models
    → LLMs → reasoning models and agents
```

Modern refinements: rotary position embeddings, RMSNorm, SwiGLU activations,
grouped-query attention, mixture-of-experts feed-forward layers.

## Common Confusions

* **Transformer vs LLM** — the Transformer is the architecture; an LLM is a very
  large one trained on a very large corpus. Small Transformers are everywhere.
* **Encoder-decoder vs decoder-only** — encoder-decoder suits translation-style
  mapping; decoder-only suits open-ended generation and dominates today.
* **"Attention is all you need"** — the feed-forward layers hold roughly
  two-thirds of the parameters. Attention routes; the MLP stores.

## Why Should I Care?

Every serving decision, memory calculation and scaling argument in this
encyclopedia assumes this block structure. It is the object the entire industry
is optimising.

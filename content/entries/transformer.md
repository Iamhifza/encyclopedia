---
term: Transformer
aliases: [Transformer Architecture, Decoder-Only Transformer, Transformer Block]
category: transformers
subcategory: block
depth: full
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
  depends_on: [self-attention, positional-encoding, feed-forward-network, residual-connection, layer-normalisation]
  evolved_into: [large-language-model]
  implemented_by: [vllm, hugging-face-transformers]
  alternative_to: [state-space-model, cnn]
  related_to: [mixture-of-experts, encoder-decoder, grouped-query-attention, mechanistic-interpretability]
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
  - type: paper
    title: "A Mathematical Framework for Transformer Circuits"
    url: https://transformer-circuits.pub/2021/framework/index.html
    year: 2021
    note: The residual-stream reading of the architecture, useful even outside interpretability.
updated: 2026-08-22
---

## Simple Explanation

Take a stack of identical blocks. Each block does two things: let every token look
at every other token, then let every token think privately about what it just
gathered. Repeat sixty or a hundred times.

That is the whole architecture. What makes it remarkable is not sophistication —
it is that this simple, uniform structure scaled further than anything before it,
and has needed almost no fundamental change in nine years.

## Technical Definition

A sequence model composed of $L$ identical blocks. Each block applies
[multi-head self-attention](self-attention.md) followed by a position-wise
[feed-forward network](feed-forward-network.md), with a
[residual connection](residual-connection.md) around each sublayer and
[normalisation](layer-normalisation.md) applied before it in modern
implementations. Order information enters through
[positional encoding](positional-encoding.md), now usually rotary. The original
design was [encoder-decoder](encoder-decoder.md); contemporary language models
are overwhelmingly decoder-only with causal masking.

## Why Does It Exist?

Recurrent models forced $O(n)$ sequential steps per sequence. That left GPUs
idle — they can do enormous amounts of arithmetic simultaneously and were being
fed one time step at a time — and made long-range learning fragile, because the
gradient had to survive a hundred multiplications to reach the start of a
sentence.

The Transformer removed recurrence entirely. Every position is processed at once
during training, which converted a latency-bound problem into a throughput-bound
one that hardware could attack.

## What Problem Does It Solve?

Parallel training over long sequences, with a constant-length path between any
two positions. Those two properties together are what made scale possible.

## How Does It Work?

```text
                 ┌───────────────────────────────────┐
tokens ──▶ embed │  ┌─ Norm                          │
      + position │  │  Multi-Head Self-Attention     │  ← moves information
                 │  └─ + residual                    │    BETWEEN positions
                 │  ┌─ Norm                          │
                 │  │  Feed-Forward (≈4× wide)       │  ← processes EACH
                 │  └─ + residual                    │    position alone
                 └───────────────┬───────────────────┘  × L blocks
                                 │
                          final norm
                                 │
                     unembed ──▶ logits over the vocabulary
```

The division of labour is the thing to remember. **Attention routes; the MLP
stores.** Attention is how a token gathers context from elsewhere; the
feed-forward network — which holds roughly two-thirds of the parameters — is where
that gathered information is transformed, and where interpretability work
suggests factual knowledge actually lives.

The **residual stream** running vertically through every block is the shared bus.
Each component reads from it and adds back to it, never overwriting. That framing,
from the Transformer Circuits work, is the most useful way to picture a
Transformer once the basics are clear.

## Mental Model

A relay of editorial passes over a document. In each pass, every sentence first
consults every other sentence, then privately revises itself. Nothing is rewritten
from scratch — each pass adds a correction to a running draft, which is exactly
what the residual connections implement.

## Formula

One block, in full:

$$h' = h + \text{Attn}(\text{Norm}(h)), \qquad h'' = h' + \text{FFN}(\text{Norm}(h'))$$

* $h$ — the residual stream entering the block, one vector per token.
* $\text{Norm}$ — applied *before* each sublayer (pre-norm), which is what makes
  deep stacks trainable without an elaborate warmup schedule.
* The additions are the residual connections; they are why $h$ survives a hundred
  layers rather than being progressively destroyed.

## Example

Trace "the KV cache stores" through a 32-layer model with hidden size 4096. The
embedding layer maps four tokens to four vectors. In each block, attention lets
"stores" gather from "cache" and "KV"; the feed-forward network transforms what it
gathered. After 32 blocks the final position's vector is projected to vocabulary
logits, and "keys" scores highest.

Every number in that description is a design choice, and reading a model card
becomes straightforward once you know which is which: **layers** (depth),
**hidden size** (width), **heads** and **KV heads** (attention shape, and
therefore serving cost), **intermediate size** (the MLP's expansion),
**vocabulary size**, **context length**.

## Real-World Usage

GPT, Claude, Llama, Gemini, Qwen, Mistral, DeepSeek — all decoder-only
Transformers. They differ in width, depth, attention variant, normalisation
placement, activation function and training data far more than in fundamental
design.

The architecture has been remarkably stable since 2017, and the changes that
stuck are almost all efficiency work rather than modelling insight:

* [Rotary position embeddings](rope.md) replaced learned absolute positions,
  which is why context windows can be extended after training.
* [RMSNorm](layer-normalisation.md) replaced LayerNorm — fewer operations, same
  effect.
* SwiGLU replaced ReLU and GELU as the [activation](activation-function.md).
* [Grouped-query attention](grouped-query-attention.md) shrank the KV cache,
  chosen for serving cost rather than for quality.
* [Mixture-of-experts](mixture-of-experts.md) replaced the single dense
  feed-forward network with many sparsely-activated ones.

Notice what that list is: the model architecture is now shaped substantially by
how it will be served.

## Historical Origin

Published June 2017 for machine translation, where the encoder-decoder structure
fits naturally. In 2018 the architecture split: BERT took the encoder half and
became the standard for classification and understanding; GPT took the decoder
half and became the standard for generation. The decoder-only branch won for
assistants, because open-ended conversation has no separate "source" to encode —
the conversation *is* the context.

## Evolution

```text
RNN → LSTM → attention → Transformer → foundation models
    → LLMs → reasoning models and agents
```

## Common Confusions

* **Transformer vs LLM** — the architecture versus a very large instance of it
  trained on a very large corpus. Small Transformers are everywhere: embedding
  models, speech recognition, vision.
* **Encoder-decoder vs decoder-only** — two stacks joined by cross-attention,
  versus one stack where everything is concatenated into a single sequence.
* **"Attention is all you need"** — a memorable title and a misleading summary of
  where the parameters are. Attention routes; the MLP holds two-thirds of the
  weights.
* **The block is not the innovation** — residual connections came from ResNet,
  layer normalisation from 2016, attention from 2014. The contribution was
  removing recurrence and demonstrating that what remained was sufficient.

## Why Should I Care?

Every serving decision, memory calculation and scaling argument in this
encyclopedia assumes this block structure. It is the object the entire industry
is optimising, and the single most valuable thing to be able to picture
precisely.

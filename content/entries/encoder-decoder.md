---
term: Encoder-Decoder
aliases: [Seq2Seq, Sequence-to-Sequence, T5-style, Encoder-Decoder Transformer]
category: transformers
subcategory: variants
depth: full
status: established
difficulty: intermediate
one_liner: "A design that reads the whole input with one stack and writes the output with another, still standard for translation and speech."
historical_period: deep-learning
tags: [architecture]
relations:
  part_of: [transformer]
  different_from: [large-language-model]
  depends_on: [cross-attention]
  related_to: [rnn, speech-recognition]
prerequisites: [transformer, cross-attention]
encountered_in: [research-papers, interviews, production-systems]
sources:
  - type: paper
    title: "Sequence to Sequence Learning with Neural Networks"
    url: https://arxiv.org/abs/1409.3215
    year: 2014
  - type: paper
    title: "Exploring the Limits of Transfer Learning with a Unified Text-to-Text Transformer (T5)"
    url: https://arxiv.org/abs/1910.10683
    year: 2019
updated: 2026-08-21
---

## Simple Explanation

Two stacks with different jobs. The encoder reads the input all at once, seeing
every token in both directions, and produces a representation of it. The decoder
writes the output one token at a time, consulting that representation through
cross-attention as it goes.

This was the original 2017 Transformer. The generative models everyone now uses
kept only the decoder half.

## Technical Definition

An architecture pairing a bidirectional encoder over the source sequence with an
autoregressive decoder over the target. Decoder layers contain three sublayers —
masked self-attention over generated tokens, cross-attention over encoder
outputs, and a feed-forward network — versus two in a decoder-only model.

## Why Does It Exist?

Translation has a clean shape: a complete input maps to a complete output, and
the input is fully available before generation starts. There is no reason to
process the source causally — seeing the end of a sentence helps interpret its
beginning, and bidirectional encoding exploits that.

## What Problem Does It Solve?

Transduction tasks where input and output are distinct sequences and the input is
known in full: translation, summarisation, speech recognition, grammatical
correction.

## How Does It Work?

```text
ENCODER (bidirectional, one pass)      DECODER (causal, per token)
source ──▶ self-attention (no mask)     ┌─ masked self-attention
       ──▶ FFN                          ├─ cross-attention ──▶ encoder output
       ──▶ representation ──────────────┤
                                        └─ FFN ──▶ next token
```

The encoder runs once. Its output is fixed for the whole generation, so its keys
and values are computed a single time and reused at every decode step — cheaper
than it looks.

## Mental Model

An interpreter who listens to the entire sentence before beginning to speak,
consulting their memory of it throughout — as opposed to simultaneous
interpretation, which is what a decoder-only model does.

## Example

The 2018 split defined the field. BERT took the encoder alone and became the
standard for classification and understanding. GPT took the decoder alone and
became the standard for generation. T5 kept both and reframed every task as
text-to-text. Decoder-only won for general assistants because open-ended
generation has no separate "source" to encode — the conversation *is* the
context.

## Real-World Usage

Still standard where the task shape genuinely fits: machine translation, speech
recognition (Whisper is encoder-decoder), text-to-speech, and many multimodal
models where a non-text encoder feeds a text decoder. Encoder-only models remain
the efficient choice for classification and embeddings.

## Common Confusions

* **Encoder-decoder vs decoder-only** — two stacks with cross-attention versus
  one stack where everything is concatenated into a single sequence.
* **The encoder is not a tokenizer** — it is a full Transformer stack producing
  contextual representations.
* **Not obsolete** — it is genuinely better for fixed input-to-output
  transduction, and the field's focus on chat has made it less discussed rather
  than less useful.

## Why Should I Care?

Knowing why the decoder-only branch won for chat — and where it did not win —
tells you which architecture actually fits a task, rather than defaulting to
whichever one is fashionable.

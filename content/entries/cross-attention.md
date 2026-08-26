---
term: Cross-Attention
aliases: [Encoder-Decoder Attention, Inter-Attention]
category: transformers
subcategory: attention
depth: full
status: established
difficulty: intermediate
one_liner: "Attention where the questions come from one sequence and the answers from another, used to condition on an image, audio or a source sentence."
historical_period: transformer
diagram:
  kind: figure
  title: Queries from one sequence, keys and values from another
  footer: This is the join between modalities. A caption model attends from text into image patches; a
    diffusion model attends from image latents into a text embedding. Same operation, different pair of
    sequences.
  visual:
    kind: fan
    source: '"The cat"'
    caption: the generating position asks; the conditioning sequence answers — and the two need not be
      the same length, or the same kind of thing
    targets:
    - text: patch 1
      new: true
    - patch 2
    - patch 3
    - patch 4
tags: [architecture]
relations:
  is_a: [attention]
  different_from: [self-attention]
  used_by: [vision-language-model, encoder-decoder, diffusion-model]
prerequisites: [attention, self-attention]
encountered_in: [research-papers, github, interviews]
sources:
  - type: paper
    title: "Attention Is All You Need"
    url: https://arxiv.org/abs/1706.03762
    year: 2017
  - type: paper
    title: "Flamingo: a Visual Language Model for Few-Shot Learning"
    url: https://arxiv.org/abs/2204.14198
    year: 2022
updated: 2026-08-21
---

## Simple Explanation

Self-attention lets a sentence look at itself. Cross-attention lets it look at
something else — a source sentence being translated, an image being described, an
audio clip being transcribed. The queries come from the sequence being generated;
the keys and values come from the other thing.

## Technical Definition

Scaled dot-product attention where $Q$ is projected from one sequence and $K$,
$V$ from another. Since the second sequence is fully available in advance, no
causal mask applies to it, and its keys and values can be computed once and
reused across every generation step.

## Why Does It Exist?

The original 2017 encoder-decoder Transformer needed a channel for the decoder to
consult the encoded source. Without it the decoder would be generating text with
no access to what it was supposed to be translating.

## What Problem Does It Solve?

Conditioning on a second modality or sequence without concatenating it into the
same stream — which keeps the conditioning information addressable rather than
merely adjacent.

## How Does It Work?


Self-attention derives queries, keys and values from the same sequence.
Cross-attention takes the queries from one sequence and the keys and values from
another, which is the entire difference and the reason it can join two unrelated
kinds of data.

Each position in the generating sequence emits a query, scores it against every
position of the conditioning sequence, and takes the weighted blend of that
sequence's values. The two need not be the same length or the same modality —
text attending into image patches, image latents attending into a text embedding,
a decoder attending into an encoder's output.

That makes it the standard join between modalities. A captioning model uses it to
look at the picture while writing; a diffusion model uses it to keep denoising
pointed at the prompt; an encoder-decoder translator uses it as the only channel
between reading and writing. Same operation throughout, applied to a different
pair of sequences.

## Mental Model

Writing an essay with a reference text open beside you. Each sentence you write
consults the source; the source never consults you.

## Example

In an image-captioning model, generating the word "cat" produces a query that
scores highly against the keys of the image patches containing the cat, so those
patches' values dominate the blend. Attention maps from cross-attention layers
are frequently visualised for exactly this reason — they show what part of the
image the model was looking at.

## Real-World Usage

Machine translation, speech recognition, and multimodal architectures such as
Flamingo which insert cross-attention layers into a frozen language model so it
can attend to visual features. In diffusion models, cross-attention is how the
text prompt steers image generation.

Note the alternative that now dominates chat-style multimodal models: rather than
cross-attention, project image features into the language model's embedding space
and *concatenate* them as tokens, so ordinary self-attention handles everything.
Simpler, but it spends context budget on the image.

## Common Confusions

* **Cross vs self-attention** — where the keys and values come from. That is the
  entire difference; the mathematics is identical.
* **Decoder-only models have no cross-attention** — GPT-style models use
  self-attention throughout, which is why cross-attention is less discussed than
  it used to be.
* **Its KV cache is different** — the conditioning sequence does not grow during
  generation, so its keys and values are computed once and never appended to.

## Why Should I Care?

It is the mechanism by which a model conditions on something outside its own
output, and knowing which of the two designs a multimodal model uses tells you
where its context budget goes.

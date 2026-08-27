---
term: Vision-Language Model
aliases: [VLM, Multimodal LLM, Multimodal Model]
category: multimodal
subcategory: vision-language
status: established
difficulty: intermediate
one_liner: A model that takes images and text together and reasons about both in one context.
origin:
  year: 2021
  circa: true
  attribution: CLIP established joint image-text representation; Flamingo and successors added generative multimodal reasoning
historical_period: foundation-model
diagram:
  kind: figure
  title: Turn the image into tokens, then it is just a language model
  footer: 'The projector is usually all that gets trained, which is why capable VLMs appeared so quickly:
    a strong vision encoder and a strong language model already existed, and only the bridge between them
    was missing.'
  visual:
    kind: columns
    width: 740
    caption: both streams end as tokens in one sequence, and from there the language model cannot tell
      which came from where
    columns:
    - title: The image
      lines:
      - ViT encoder
      - patch embeddings
      - a learned projector
      - → visual tokens
    - title: The text
      accent: true
      lines:
      - ordinary tokeniser
      - —
      - —
      - → text tokens
tags: [architecture]
relations:
  is_a: [foundation-model]
  depends_on: [transformer, embedding]
  evolved_into: [vision-language-action-model, computer-use]
  related_to: [large-language-model]
prerequisites: [transformer, large-language-model]
encountered_in: [production-systems, research-papers, documentation]
sources:
  - type: paper
    title: "Learning Transferable Visual Models From Natural Language Supervision (CLIP)"
    url: https://arxiv.org/abs/2103.00020
    year: 2021
  - type: paper
    title: "Flamingo: a Visual Language Model for Few-Shot Learning"
    url: https://arxiv.org/abs/2204.14198
    year: 2022
updated: 2026-08-21
---

## Simple Explanation

An image is converted into tokens the language model can read, and then sits in
the context window alongside the text. From the model's point of view a
screenshot and a paragraph are the same kind of thing: a sequence of vectors.

## Technical Definition

An architecture combining a vision encoder (typically a Vision Transformer) with
a language model through a projection or cross-attention layer that maps visual
features into the language model's embedding space, trained on interleaved
image-text data.

## Why Does It Exist?

Enormous amounts of information are visual — documents, charts, screenshots,
diagrams, photographs — and text-only models simply cannot see them.

## What Problem Does It Solve?

Tasks where the input is not text: document understanding, chart reading, UI
interaction, visual question answering, and describing scenes.

## How Does It Work?

Images are expensive in tokens: a high-resolution page can consume thousands.

## Mental Model

Giving the language model eyes by translating what it sees into its own
vocabulary, then letting the usual machinery run.

## Example

Reading a scanned invoice, extracting the fields and returning JSON — a task that
previously needed a dedicated OCR pipeline plus layout analysis plus extraction
rules, and now is one call.

## Real-World Usage

Document processing, accessibility descriptions, chart and diagram
interpretation, screenshot debugging, and as the perception layer for computer-use
and robotic agents.

## Common Confusions

* **VLM vs CLIP-style models** — CLIP scores image-text similarity for retrieval
  and classification; a generative VLM produces text about images. Different
  jobs.
* **Resolution matters** — small text in a large image is frequently missed;
  tiling strategies and input resolution are practical determinants of accuracy.
* **Seeing is not measuring** — VLMs read charts approximately and should not be
  trusted to extract precise values without verification.

## Why Should I Care?

It is the fastest-growing input modality in production LLM systems, and the
prerequisite for every agent that operates a screen or a robot.

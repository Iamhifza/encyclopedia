---
term: Image Generation
aliases: [Text-to-Image, Image Synthesis, Generative Imagery]
category: multimodal
subcategory: generation
depth: full
status: established
difficulty: intermediate
one_liner: "Producing an image from a text description, in practice almost always with a diffusion model."
historical_period: foundation-model
diagram:
  kind: figure
  title: Denoise toward the prompt, twenty to fifty times
  footer: 'Guidance scale is the dial worth knowing: low gives loose, varied images that sometimes ignore
    you, high gives literal, saturated ones with less diversity. Most defaults sit deliberately in the
    middle.'
  visual:
    kind: pipeline
    width: 740
    caption: denoising happens in a compressed latent space, not on pixels — which is what made this affordable
      enough to run on a consumer card
    stages:
    - text: '"a lighthouse in a storm, oil painting"'
      note: the prompt
    - text: a text embedding
      via: text encoder
    - text: a latent, denoised step by step
      note: ~20–50 steps
      tone: accent
      via: start from noise; the embedding conditions every step via cross-attention
    - text: an image
      via: VAE decoder — latent back to pixels
tags: [architecture]
relations:
  depends_on: [diffusion-model, embedding]
  related_to: [vision-language-model, ai-slop, cross-attention]
prerequisites: [diffusion-model]
encountered_in: [production-systems, social-media, technical-blogs]
sources:
  - type: paper
    title: "High-Resolution Image Synthesis with Latent Diffusion Models"
    url: https://arxiv.org/abs/2112.10752
    year: 2022
  - type: paper
    title: "Hierarchical Text-Conditional Image Generation with CLIP Latents"
    url: https://arxiv.org/abs/2204.06125
    year: 2022
  - type: paper
    title: "Classifier-Free Diffusion Guidance"
    url: https://arxiv.org/abs/2207.12598
    year: 2022
updated: 2026-08-21
review_by: 2027-02-01
---

## Simple Explanation

You type a description; an image appears. Underneath, a text encoder turns your
prompt into vectors, and a diffusion model uses those vectors to steer a
denoising process from random static toward an image that matches. The model is
not retrieving or collaging anything — it is removing noise in a direction the
text points.

## Technical Definition

Text-conditional generation, typically latent diffusion: a text encoder produces
embeddings, which condition a denoising network (U-Net or diffusion Transformer)
operating in a compressed latent space, with the result decoded to pixels.
Prompt adherence is controlled by classifier-free guidance.

## Why Does It Exist?

Visual production had a hard floor of skill and time. The research goal was
narrower — controllable conditional generation — and the capability turned out to
generalise far beyond what the training objective directly asked for.

## What Problem Does It Solve?

Fast visual iteration: concept art, mockups, storyboards, illustration for things
that would never have justified commissioning an artist.

## How Does It Work?


Encode the prompt to an embedding, start from pure noise, and denoise toward an
image over twenty to fifty steps, with the text embedding conditioning every step
through cross-attention. What comes out is a latent, which a decoder turns into
pixels.

Working in latent space rather than on pixels is what made this affordable. A
512×512 image is a quarter of a million values; its latent is a few thousand. The
diffusion model never sees a pixel — an autoencoder handles the translation at
each end — and that single decision is the difference between a datacentre and a
consumer graphics card.

Guidance scale is the dial worth understanding. It controls how hard each step is
pushed toward the prompt versus toward whatever the model would produce
unconditioned. Low values give varied, loose images that sometimes ignore what
you asked for; high values give literal, saturated, less diverse ones. Defaults
sit deliberately in the middle, and moving it is usually more effective than
rewriting the prompt.

## Mental Model

Sculpting from noise. The prompt is not a description being drawn — it is a force
pulling each denoising step toward one region of the space of possible images.

## Example

Control beyond the prompt is where practical work happens: ControlNet conditions
on a pose, depth map or edge sketch; inpainting regenerates a masked region;
image-to-image starts from partial noise over an existing picture rather than
pure static. Prompt text alone gives you far less control than these.

## Real-World Usage

Design and marketing workflows, game and film pre-production, product mockups,
and the synthetic training data used for vision models. Open-weight models run
locally on consumer GPUs; hosted services handle the rest.

The unresolved issues are not technical. Training data provenance is the subject
of active litigation; likeness and style imitation are contested; and provenance
standards such as C2PA content credentials exist precisely because generated
images are otherwise indistinguishable from photographs.

## Common Confusions

* **It does not retrieve or collage** — no source images are stored or assembled.
  Memorisation of near-duplicates can occur for images repeated many times in
  training, which is a real and studied problem, but it is the exception.
* **Text rendering was the classic weakness** — recent models handle it far
  better, so claims here date quickly.
* **Prompt engineering matters less than it did** — modern models follow natural
  descriptions well, and the elaborate keyword incantations of 2022 are mostly
  obsolete.

## Why Should I Care?

It is the most widely encountered generative technology outside text, it is where
the public argument about training data and creative labour is loudest, and it is
the clearest case of a capability arriving faster than the norms around it.

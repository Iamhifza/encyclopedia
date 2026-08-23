---
term: Autoencoder
aliases: [Latent Representation, VAE, Variational Autoencoder, Bottleneck Network]
category: deep-learning
subcategory: generative
depth: full
status: established
difficulty: intermediate
one_liner: "A network trained to squeeze its input through a narrow bottleneck and rebuild it, learning a compact representation on the way."
historical_period: statistical-ml
tags: [architecture]
relations:
  evolved_into: [sparse-autoencoder]
  related_to: [embedding, jepa, diffusion-model, self-supervised-learning]
prerequisites: [neural-network]
encountered_in: [research-papers, interviews, github]
sources:
  - type: paper
    title: "Reducing the Dimensionality of Data with Neural Networks"
    url: https://www.science.org/doi/10.1126/science.1127647
    year: 2006
  - type: paper
    title: "Auto-Encoding Variational Bayes (VAE)"
    url: https://arxiv.org/abs/1312.6114
    year: 2013
updated: 2026-08-21
---

## Simple Explanation

Train a network to output exactly what it was given. Trivial — unless you force
everything through a narrow layer in the middle. Now it cannot copy; it must find
a compressed description that retains enough to rebuild the original.

Whatever survives that bottleneck is what the data was really about.

## Technical Definition

An encoder $f$ mapping input to a lower-dimensional latent code, and a decoder
$g$ mapping back, trained to minimise reconstruction error
$\lVert x - g(f(x)) \rVert^2$. The bottleneck forces lossy compression, so the
latent must capture structure rather than detail. Variational autoencoders make
the latent a distribution rather than a point, which permits sampling and
therefore generation.

## Why Does It Exist?

It was one of the first ways to learn useful representations without labels. The
supervision comes from the input itself — the original self-supervised objective,
predating the term.

## What Problem Does It Solve?

Dimensionality reduction that can capture non-linear structure, where PCA can
only find linear directions. And, in its variational form, a generative model
with a navigable latent space.

## How Does It Work?

```text
   x ──▶ encoder ──▶ z ──▶ decoder ──▶ x̂
   784        (compress)  32  (expand)   784
                          ▲
                    the bottleneck:
             too wide and it learns to copy,
             too narrow and it cannot reconstruct

   loss = ‖x − x̂‖²      (plus a KL term, for a VAE)
```

## Mental Model

Describing a painting over the phone and having someone repaint it. The
description is the latent code — and how good the repainting is tells you how
much the description captured.

## Example

The most consequential use today is invisible: **latent diffusion**. Stable
Diffusion does not denoise pixels, it denoises inside an autoencoder's latent
space, then decodes to an image at the end. That single change cut the cost of
image generation by more than an order of magnitude and is what made it run on
consumer hardware.

## Real-World Usage

Latent spaces for diffusion models, anomaly detection (high reconstruction error
means unfamiliar input), denoising, and — in a form that inverts the usual
design — **sparse autoencoders** in interpretability, which deliberately use a
*wider* hidden layer with a sparsity penalty to decompose activations rather than
compress them.

## Common Confusions

* **Autoencoder vs encoder-decoder Transformer** — both have those two parts,
  but the autoencoder reconstructs its own input while the Transformer maps one
  sequence to a different one.
* **Autoencoder vs embedding model** — the latent is a representation, but it is
  optimised for reconstruction, not for similarity. Embedding models trained
  contrastively are much better for retrieval.
* **VAE vs plain autoencoder** — a plain one has no usable structure between
  training points, so you cannot sample from it. The VAE's distributional latent
  is what makes generation possible.

## Why Should I Care?

The idea — compress until only structure survives — recurs throughout the field:
in latent diffusion, in JEPA's abstract prediction, and in the interpretability
tools currently used to read what models represent internally.

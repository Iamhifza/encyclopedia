---
term: CNN
aliases: [Convolutional Neural Network, ConvNet, Convolution, LeNet]
category: deep-learning
subcategory: architectures
depth: full
status: established
difficulty: intermediate
one_liner: "A network that slides the same small filter across an image, so a feature learned in one place is recognised everywhere."
origin:
  year: 1989
  circa: true
  attribution: LeCun's work on handwritten digit recognition; the receptive-field idea comes from Hubel and Wiesel's visual cortex studies
historical_period: ai-winter
tags: [architecture]
relations:
  is_a: [neural-network]
  alternative_to: [transformer]
  related_to: [vision-language-model, gpu, activation-function]
prerequisites: [neural-network]
encountered_in: [research-papers, interviews, production-systems]
sources:
  - type: paper
    title: "Gradient-Based Learning Applied to Document Recognition (LeNet-5)"
    url: http://yann.lecun.com/exdb/publis/pdf/lecun-01a.pdf
    year: 1998
  - type: paper
    title: "ImageNet Classification with Deep Convolutional Neural Networks (AlexNet)"
    url: https://papers.nips.cc/paper/4824-imagenet-classification-with-deep-convolutional-neural-networks
    year: 2012
  - type: paper
    title: "A ConvNet for the 2020s"
    url: https://arxiv.org/abs/2201.03545
    year: 2022
updated: 2026-08-21
---

## Simple Explanation

A cat in the top-left of a photo is the same cat in the bottom-right. A fully
connected network has to learn that twice, once per position, which is enormously
wasteful. A convolution slides one small filter across the whole image, so
whatever it learns to detect, it detects everywhere.

That single assumption — that position should not matter — is what made computer
vision work.

## Technical Definition

A network built from convolutional layers, each applying learned kernels across
the spatial dimensions of its input with shared weights, typically interleaved
with pooling for downsampling. The result is translation equivariance and
parameter counts independent of input size, with receptive fields growing with
depth so early layers see edges and later layers see objects.

## Why Does It Exist?

A fully connected layer on a 224×224 image needs 50,000 weights *per unit*. It
also treats each pixel as unrelated to its neighbours, discarding the fact that
images have local structure. Convolution encodes both facts — locality and
translation invariance — directly into the architecture.

## What Problem Does It Solve?

Learning from images with a feasible number of parameters and a feasible amount
of data, by building in prior knowledge about how images work.

## How Does It Work?

```text
input image          filter (3×3)        feature map
┌─────────────┐      ┌───┐               ┌───────────┐
│             │      │▓░▓│  slide it     │  where the│
│             │  ×   │░▓░│  across ──▶   │  pattern  │
│             │      │▓░▓│  everywhere   │  appeared │
└─────────────┘      └───┘               └───────────┘
     same weights used at every position

depth builds hierarchy:
  layer 1: edges → layer 3: textures → layer 8: parts → layer 15: objects
```

## Mental Model

A stencil dragged across the whole page. One stencil, one thing it detects,
found wherever it occurs.

## Formula

$$(f * k)(i,j) = \sum_{m}\sum_{n} f(i+m,\; j+n) \, k(m,n)$$

* $f$ — the input image or feature map.
* $k$ — the learned kernel, typically 3×3 or 5×5.
* The sum runs over the kernel's window; the same $k$ is applied at every $(i,j)$,
  which is the weight sharing that makes this efficient.

## Example

AlexNet's ImageNet win in 2012 is the single most consequential result in modern
AI history — not because convolution was new (LeCun had it working in 1989) but
because GPUs and a large labelled dataset finally made it trainable at depth.
Error rates dropped sharply enough that the field reorganised around deep
learning within about three years.

## Real-World Usage

Still the pragmatic default for many vision tasks: fast, data-efficient, and
excellent on smaller datasets where Vision Transformers struggle. Widely deployed
on edge devices where compute is scarce. Also used in audio (over spectrograms)
and anywhere the data has local translation-invariant structure.

## Common Confusions

* **CNN vs Transformer for vision** — ViTs win at very large data scales, where
  they can learn spatial structure rather than assuming it; CNNs win with less
  data, because that assumption is a useful prior. ConvNeXt showed modernised
  CNNs remain competitive, so the transition was less decisive than it appeared.
* **Convolution is not the mathematical convolution** — deep learning frameworks
  actually implement cross-correlation. Nobody minds; the kernel is learned
  either way.
* **Translation equivariance, not invariance** — the feature map shifts when the
  input shifts. Pooling and the final layers are what convert that into
  invariance.

## Why Should I Care?

It is the architecture that started the deep learning era, it is still the right
choice for a great many vision problems, and it is the clearest example of
building domain knowledge into a model rather than making it learn everything
from scratch.

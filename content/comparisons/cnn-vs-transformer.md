---
title: CNN vs Transformer
question: For vision, should the architecture assume spatial structure or learn it?
sides: [cnn, transformer]
---

## The short version

A CNN has locality and translation invariance built into its wiring. A Vision
Transformer has neither and must learn them from data. That single difference
predicts the whole trade: CNNs win with less data, Transformers win with more.

## Side by side

| | CNN | Vision Transformer |
|---|---|---|
| **Spatial structure** | Built in — assumed by convolution | Learned from data |
| **Receptive field** | Local, growing with depth | Global from the first layer |
| **Data appetite** | Modest; works on thousands of images | Large; needs pretraining at scale |
| **Compute** | Linear in pixels | Quadratic in patches |
| **Edge deployment** | Excellent | Heavier |
| **Multimodal fit** | Awkward — a separate stack | Native; images become tokens |

## The trade, stated as a bias

```text
CNN   assumes:  nearby pixels are related · a feature is a feature anywhere
                → learns from less data, cannot unlearn the assumption

ViT   assumes:  nothing
                → needs more data to discover the same structure,
                  and can discover structure a CNN could not represent
```

This is the bias-variance argument in architectural form. A prior helps when
data is scarce and constrains you when it is not.

## Why the Transformer won anyway

Not on vision benchmarks alone — ConvNeXt showed a modernised CNN remains
competitive at comparable scale, which quietly undercut the "Transformers are
simply better" reading. It won because **one architecture for every modality** is
worth more than a few points on ImageNet. Once images become tokens, the same
stack handles text, images, audio and video, and cross-modal models stop needing
a translation layer between two different worlds.

## Where each still belongs

CNNs: smaller datasets, edge and mobile deployment, medical imaging where data is
scarce and expensive, anything latency-critical on modest hardware.

ViTs: large-scale pretraining, and any system where vision feeds a language
model — which is nearly all current multimodal work.

Hybrids are common and sensible: convolutional early layers for cheap local
features, attention above for global relationships.

## Verdict

Not a succession — a fork. If you have a few thousand labelled images and a
deployment constraint, a CNN is very likely the right answer and will train in an
afternoon. If you are building perception for a multimodal system, use a
Transformer, because the value is in sharing the stack rather than in the
architecture itself.

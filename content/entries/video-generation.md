---
term: Video Generation
aliases: [Text-to-Video, Generative Video, Video Diffusion]
category: multimodal
subcategory: generation
depth: full
status: emerging
difficulty: advanced
one_liner: "Producing moving footage from a description, where the hard part is not the pictures but keeping them consistent over time."
origin:
  year: 2022
  circa: true
  attribution: Emerged from image diffusion extended to the temporal dimension; transformer-based video diffusion followed from 2024
historical_period: agentic
tags: [architecture]
relations:
  depends_on: [diffusion-model, transformer]
  related_to: [image-generation, video-understanding, world-model, ai-slop]
prerequisites: [diffusion-model, image-generation]
encountered_in: [research-papers, social-media, production-systems]
sources:
  - type: paper
    title: "Video Diffusion Models"
    url: https://arxiv.org/abs/2204.03458
    year: 2022
  - type: paper
    title: "Scalable Diffusion Models with Transformers (DiT)"
    url: https://arxiv.org/abs/2212.09748
    year: 2022
  - type: paper
    title: "Align your Latents: High-Resolution Video Synthesis with Latent Diffusion Models"
    url: https://arxiv.org/abs/2304.08818
    year: 2023
updated: 2026-08-21
review_by: 2027-02-01
---

## Simple Explanation

Generating one convincing image is a solved problem. Generating 150 of them that
look like the same scene, with objects that stay the same shape, lighting that
stays consistent, and motion that obeys something resembling physics — that is
video generation, and the difficulty is almost entirely in the word *consistent*.

## Technical Definition

Conditional generation of temporal image sequences, typically by diffusion in a
spatiotemporal latent space. A video autoencoder compresses frames jointly across
space and time; a denoising network with attention over both dimensions generates
the latent sequence; a decoder produces frames. Conditioning may be text, an
initial image, or both.

## Why Does It Exist?

Video production is expensive and slow, and the research question — can a model
learn temporal consistency and plausible physics from footage — is interesting
independently of the application.

## What Problem Does It Solve?

Rapid visual prototyping, and — the claim that draws research interest — a
possible route to physical intuition learned from observation.

## How Does It Work?

```text
text ──▶ encoder ──┐
                   ├──▶ spatiotemporal diffusion in latent space
noise ─────────────┘         │
                             │ attention across BOTH:
                             │   space  (within a frame)
                             │   time   (between frames)
                             ▼
                    latent sequence ──▶ decoder ──▶ frames

cost: a few seconds of video is orders of magnitude more
      computation than a single image
```

Temporal attention is what enforces consistency, and it is why the compute cost
grows so unpleasantly — a model must relate every patch to patches in other
frames.

## Mental Model

Not drawing frames one after another, but sculpting the whole clip at once from
noise, so that consistency is a property of the generation rather than something
patched afterwards.

## Example

The characteristic failures are diagnostic. Objects morph or vanish between
frames; hands and text degrade under motion; and physical implausibility appears
at the boundaries — liquids that do not pour correctly, objects that pass through
each other, motion that violates conservation without the model noticing.

That last category is precisely why the claim that video generators are
**world models** is contested. Producing plausible footage is not the same as
possessing an action-conditioned model of dynamics usable for control. A
generator can render a convincing pour and be unable to predict what happens if
the glass tips.

## Real-World Usage

Advertising and marketing, pre-visualisation and storyboarding in film,
game asset prototyping, and synthetic training data for vision and robotics
models. Deployment is constrained by cost, by controllability — directing a
specific shot remains hard — and by provenance requirements, since the output is
increasingly indistinguishable from recorded footage.

## Common Confusions

* **Video generation vs video understanding** — producing footage versus
  interpreting it. Neither implies the other.
* **Video generation vs world model** — see above. The label is applied
  aggressively in marketing; ask whether the model is used for control or only
  for output.
* **Frame-by-frame image generation is not video** — it produces flicker.
  Temporal modelling is the entire technical contribution.

## Why Should I Care?

It is the most compute-intensive generative capability currently deployed, it is
where the argument about whether prediction implies understanding is being
fought, and it is the technology most responsible for provenance standards
becoming urgent.

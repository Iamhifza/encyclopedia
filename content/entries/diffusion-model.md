---
term: Diffusion Model
aliases: [Denoising Diffusion, Latent Diffusion, Stable Diffusion, DDPM]
category: deep-learning
subcategory: generative
depth: full
status: established
difficulty: advanced
one_liner: "A generator that starts from pure noise and removes a little of it at a time until an image emerges."
tags: [architecture]
relations:
  is_a: [neural-network]
  alternative_to: [autoregressive-generation, gan]
  used_by: [image-generation, text-to-speech]
  related_to: [transformer]
prerequisites: [neural-network]
encountered_in: [research-papers, production-systems, github, social-media]
sources:
  - type: paper
    title: "Denoising Diffusion Probabilistic Models"
    url: https://arxiv.org/abs/2006.11239
    year: 2020
  - type: paper
    title: "High-Resolution Image Synthesis with Latent Diffusion Models"
    url: https://arxiv.org/abs/2112.10752
    year: 2022
  - type: paper
    title: "Scalable Diffusion Models with Transformers (DiT)"
    url: https://arxiv.org/abs/2212.09748
    year: 2022
updated: 2026-08-21
---

## Simple Explanation

Training is the easy half to describe: take a real image, add a bit of random
noise, and teach a network to predict the noise you added. Do this at every
noise level, from barely-speckled to completely destroyed.

Generation runs it backwards. Start with pure static, ask the network what noise
it sees, subtract a little of it, repeat. After a few dozen passes, an image is
standing there. Nothing was drawn — noise was removed until only structure
remained.

## Technical Definition

A latent-variable generative model defined by a fixed *forward* process that
progressively adds Gaussian noise to data over $T$ steps, and a learned *reverse*
process trained to invert it. The network is trained to predict the noise
component at a given timestep; sampling iterates the learned denoiser from
$\mathcal{N}(0, I)$ back to the data distribution.

## Why Does It Exist?

GANs generated images quickly and trained badly: unstable, prone to mode
collapse, hard to scale. Diffusion trades sampling speed for a stable regression
objective — predict the noise, minimise squared error — that scales predictably
and covers the full data distribution rather than collapsing onto part of it.

## What Problem Does It Solve?

High-fidelity, diverse generation with a training procedure that reliably
converges.

## How Does It Work?

```text
FORWARD (fixed, no learning)
  image ──▶ +noise ──▶ +noise ──▶ ... ──▶ pure noise
   x₀         x₁         x₂                  x_T

REVERSE (learned)
  noise ──▶ predict & subtract ──▶ ... ──▶ image
   x_T          (T steps)                    x₀
                     ▲
          conditioned on a text embedding,
          so the denoising is steered toward the prompt
```

**Latent diffusion** — the change that made this practical — runs the whole
process in a compressed latent space produced by an autoencoder rather than on
pixels, cutting the cost by more than an order of magnitude.

## Mental Model

Michelangelo's remark about removing everything that is not the statue. The model
never adds; it repeatedly decides what is not part of the picture.

## Formula

The training objective reduces to a plain regression:

$$L = \mathbb{E}_{x_0, \epsilon, t}\left[\lVert \epsilon - \epsilon_\theta(x_t, t) \rVert^2\right]$$

* $\epsilon$ — the actual noise added.
* $\epsilon_\theta(x_t, t)$ — the network's prediction of it, given the noisy
  input and the timestep.
* $t$ — how far along the noising schedule this sample is; the network is told,
  because the right amount to remove depends on it.

That this collapses to mean squared error is the reason diffusion trains so much
more stably than adversarial methods.

## Example

Prompt adherence comes from **classifier-free guidance**: the model predicts
noise twice, once conditioned on the prompt and once unconditioned, then
extrapolates away from the unconditioned prediction. Turn the guidance scale up
and images follow the prompt more literally while becoming oversaturated and less
diverse — the single most visible dial in image generation.

## Real-World Usage

Image generation (Stable Diffusion and successors), video generation, audio and
speech synthesis, molecular and protein design. The backbone has largely shifted
from U-Nets to Transformers (DiT), and sampling step counts have fallen from
around a thousand to a handful through better solvers and distillation.

## Common Confusions

* **Diffusion vs autoregressive generation** — diffusion refines *all* positions
  in parallel over many passes; autoregressive models emit one token at a time in
  one pass each. Text diffusion models exist and are an active research direction.
* **Steps are not layers** — the same network runs repeatedly with a different
  timestep, not a stack of different networks.
* **It is not "denoising a photo"** — the noise being removed was never on
  anything; there is no underlying image until the process creates one.

## Why Should I Care?

It is the dominant paradigm for everything generative that is not text, and the
strongest counterexample to the assumption that autoregressive Transformers are
the only way to build a generative model.

---
term: GAN
aliases: [Generative Adversarial Network, Adversarial Training, Discriminator]
category: deep-learning
subcategory: generative
depth: full
status: historical
difficulty: advanced
one_liner: "Two networks trained against each other, one producing fakes and one detecting them, until the fakes are convincing."
origin:
  year: 2014
  attribution: Ian Goodfellow and colleagues
historical_period: deep-learning
diagram:
  kind: flow
  title: Two networks, each trained on the other's failures
  loop: each update makes the other's job harder
  footer: 'Notoriously unstable: if the discriminator wins too early the generator gets no usable gradient,
    and mode collapse — producing one convincing thing forever — is the standard failure. Diffusion models
    replaced them largely because they train predictably.'
  nodes:
  - title: Noise
    note: a random vector
    caption: the only input
  - title: Generator
    note: makes a candidate
    accent: true
    caption: trained to fool
  - title: Discriminator
    note: real, or generated?
    caption: trained to catch
  - title: Verdict
    note: one bit, and a gradient
    caption: for both of them
tags: [architecture]
relations:
  alternative_to: [diffusion-model]
  is_a: [neural-network]
  related_to: [autoencoder, synthetic-data]
prerequisites: [neural-network]
encountered_in: [research-papers, interviews, conferences]
sources:
  - type: paper
    title: "Generative Adversarial Networks"
    url: https://arxiv.org/abs/1406.2661
    year: 2014
  - type: paper
    title: "A Style-Based Generator Architecture for GANs (StyleGAN)"
    url: https://arxiv.org/abs/1812.04948
    year: 2018
updated: 2026-08-21
---

## Simple Explanation

Two networks with opposed goals. A **generator** makes fake images. A
**discriminator** tries to tell fakes from real ones. Each improves by defeating
the other, and if the process stays balanced, the generator ends up producing
images the discriminator cannot distinguish from real.

It was the dominant generative method for most of a decade, and diffusion models
displaced it almost entirely.

## Technical Definition

A minimax game between a generator $G$ mapping noise to samples and a
discriminator $D$ estimating the probability a sample came from the data rather
than from $G$. At the theoretical optimum the generator's distribution matches
the data distribution and the discriminator is reduced to guessing.

## Why Does It Exist?

Earlier generative models needed an explicit tractable likelihood, which
constrained what they could represent. The adversarial framing sidesteps this
entirely: the discriminator *learns* the loss function, so nothing has to be
written down analytically.

## What Problem Does It Solve?

Sharp, realistic generation — GAN images were notably crisper than the blurry
output of contemporary autoencoders, because the discriminator punishes exactly
the averaging that causes blur.

## How Does It Work?

The two updates alternate. Balance is everything, and balance is the problem.

## Mental Model

A forger and an art authenticator locked in a room, each improving only because
the other does. The forger never sees a real painting — only the authenticator's
verdicts.

## Formula

$$\min_G \max_D \; \mathbb{E}_{x \sim p_{data}}[\log D(x)] + \mathbb{E}_{z}[\log(1 - D(G(z)))]$$

* $D(x)$ — discriminator's estimate that $x$ is real.
* $G(z)$ — generator's output from noise $z$.
* The generator minimises what the discriminator maximises, which is why there is
  no single loss going down and therefore no reliable signal that training is
  working.

## Example

The failure modes were notorious. **Mode collapse**: the generator finds a few
outputs that fool the discriminator and produces only those, so diversity
vanishes. **Non-convergence**: the two networks oscillate indefinitely. **No
usable metric**: unlike a loss curve, adversarial losses do not indicate quality,
so practitioners judged progress by looking at samples.

Diffusion models replaced GANs primarily by removing all three problems. A stable
regression objective, a loss that means something, and full distributional
coverage — at the cost of much slower sampling.

## Real-World Usage

Largely historical for image generation. Still used where sampling speed matters
more than diversity: super-resolution, some image-to-image translation, voice
conversion, and as a component inside other systems — the decoder in latent
diffusion is often trained with an adversarial term.

## Common Confusions

* **GAN vs diffusion** — one shot versus many refinement steps; unstable training
  and fast sampling versus stable training and slow sampling.
* **The discriminator is not kept** — it is scaffolding, discarded after training.
* **"GAN" is not a synonym for deepfake** — deepfakes have been made with several
  architectures, and current ones typically are not GANs.

## Why Should I Care?

It is the clearest case in modern ML of a dominant method being displaced not
because it produced worse results but because it was unreliable to train — a
reminder that trainability is a first-class property, not an implementation
detail.

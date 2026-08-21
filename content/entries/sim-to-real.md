---
term: Sim-to-Real
aliases: [Sim2Real, Domain Randomisation, Reality Gap]
category: world-models-embodied
subcategory: simulation
status: established
difficulty: advanced
one_liner: Training a policy in simulation and getting it to work on real hardware despite the simulator being wrong.
origin:
  year: 2017
  circa: true
  attribution: Domain randomisation formalised by Tobin et al.; the reality gap is a long-standing robotics problem
historical_period: deep-learning
tags: [training]
relations:
  used_by: [vision-language-action-model]
  depends_on: [reinforcement-learning, world-model]
prerequisites: [reinforcement-learning]
encountered_in: [research-papers, conferences, production-systems]
sources:
  - type: paper
    title: "Domain Randomization for Transferring Deep Neural Networks from Simulation to the Real World"
    url: https://arxiv.org/abs/1703.06907
    year: 2017
  - type: paper
    title: "Solving Rubik's Cube with a Robot Hand"
    url: https://arxiv.org/abs/1910.07113
    year: 2019
updated: 2026-08-21
---

## Simple Explanation

Simulators run millions of trials cheaply and never break a robot. But no
simulator matches reality — friction, sensor noise, latency and lighting are all
slightly wrong — so a policy that is perfect in simulation can fail immediately
on hardware. Sim-to-real is the set of techniques for crossing that gap.

## Technical Definition

Transfer of a policy trained in simulation to physical deployment. The dominant
technique is domain randomisation: sampling physical parameters, textures,
lighting and noise across a wide range during training, so the real world appears
as one more variation and the policy is forced to be robust rather than tuned.

## Why Does It Exist?

Real-world reinforcement learning at the scale these methods need is impossible:
millions of episodes would take years and destroy the hardware.

## What Problem Does It Solve?

Sample cost and safety during training.

## How Does It Work?

```text
simulate with randomised physics:
   friction  ▁▃▅█▅▃▁     mass  ▁▃▅█▅▃▁    latency ▁▃▅█▅▃▁
                     │
     policy must work across the whole distribution
                     │
        reality is (hopefully) inside that distribution
```

## Mental Model

Training a driver in every weather condition you can invent, so that whatever the
real road does, it has been seen before.

## Example

OpenAI's robotic hand solved a Rubik's cube after training entirely in randomised
simulation, including randomised physical properties it could not measure
precisely — the canonical demonstration that randomisation can substitute for
accuracy.

## Real-World Usage

Robotic locomotion and manipulation, autonomous driving, drone control, and
increasingly the generation of training data for VLA models. Real-data
fine-tuning after simulation transfer is common.

## Common Confusions

* **Better simulators are not the whole answer** — randomisation for robustness
  often beats fidelity for accuracy, because the residual gap never closes.
* **Sim-to-real is not free** — randomisation costs sample efficiency and can cap
  peak performance.
* **The gap is task-dependent** — locomotion transfers far better than contact-rich
  manipulation.

## Why Should I Care?

It is how most modern robot policies are actually trained, and it is a
transferable idea: train against a distribution of plausible worlds rather than
the one you believe you are in.

---
term: Vision-Language-Action Model
aliases: [VLA, Robot Foundation Model, VLA Model]
category: world-models-embodied
subcategory: robotics
status: emerging
difficulty: advanced
one_liner: A model that takes camera images and a natural-language instruction and outputs robot actions directly.
origin:
  year: 2023
  attribution: Google DeepMind's RT-2 named the category; OpenVLA and π-series models followed
historical_period: agentic
tags: [architecture, agents]
relations:
  is_a: [vision-language-model]
  depends_on: [world-model, sim-to-real]
  related_to: [ai-agent, reinforcement-learning]
prerequisites: [vision-language-model]
encountered_in: [research-papers, conferences, technical-blogs]
sources:
  - type: paper
    title: "RT-2: Vision-Language-Action Models Transfer Web Knowledge to Robotic Control"
    url: https://arxiv.org/abs/2307.15818
    year: 2023
  - type: paper
    title: "OpenVLA: An Open-Source Vision-Language-Action Model"
    url: https://arxiv.org/abs/2406.09246
    year: 2024
updated: 2026-08-21
review_by: 2027-02-01
---

## Simple Explanation

Traditional robots need perception, planning and control written as separate
engineered stages. A VLA collapses that: images and an instruction go in, motor
commands come out, learned end to end — and because it starts from a
vision-language model, it inherits general knowledge about objects it was never
trained to manipulate.

## Technical Definition

A vision-language model fine-tuned on robot demonstration data to output action
tokens — usually discretised end-effector poses or joint deltas — conditioned on
visual observation and a language instruction, executed in a closed control loop.

## Why Does It Exist?

Robot learning has always been data-starved: demonstrations are slow and
expensive to collect. Starting from a model already trained on web-scale
image-text data transfers semantic knowledge that no robot dataset could supply.

## What Problem Does It Solve?

Generalisation to novel objects and instructions, which is precisely where
classical robotic pipelines are brittle.

## How Does It Work?

```text
camera frames + "put the ripe banana in the bowl"
        │
   VLM backbone (pretrained on web image-text)
        │
   action head ──▶ discretised action tokens ──▶ controller ──▶ motors
        ▲                                                         │
        └───────────────── new observation ◀──────────────────────┘
```

## Mental Model

Giving a robot the general knowledge of a language model and then teaching it
which muscles to move — rather than teaching it the world one object at a time.

## Example

RT-2 demonstrated instructions requiring knowledge absent from its robot data,
such as selecting an improvised implement for a task, because the semantic
knowledge came from web pretraining rather than demonstrations.

## Real-World Usage

Research labs and robotics startups; open models such as OpenVLA have made the
category broadly accessible. Deployment is early: control frequency, latency,
safety and reliability remain hard, and shared datasets are far smaller than in
language.

## Common Confusions

* **VLA vs VLM** — the VLM understands images and text; the VLA additionally
  outputs actions and closes a control loop.
* **Web knowledge does not transfer to dexterity** — semantic generalisation is
  the strong result; fine motor skill is not.
* **Benchmarks are not comparable** — different robots, tasks and setups make
  cross-paper claims unusually difficult to interpret.

## Why Should I Care?

It is the main line along which foundation models are entering the physical
world, and the point where language, perception and control stop being separate
fields.

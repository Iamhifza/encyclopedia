---
term: Continual Learning
aliases: [Lifelong Learning, Online Learning, Catastrophic Forgetting, Incremental Learning]
category: machine-learning
subcategory: settings
depth: full
status: experimental
difficulty: advanced
one_liner: "Learning from a stream of new data over time without erasing what was learned before."
origin:
  year: 1989
  circa: true
  attribution: Catastrophic forgetting identified by McCloskey and Cohen; the modern research programme dates from the 2010s
historical_period: ai-winter
diagram:
  kind: steps
  title: Learning the second thing costs you the first
  footer: None of the mitigations fully solves it and all of them cost something — memory, compute, or
    parameters. In practice most teams retrain from scratch instead.
  steps:
  - title: Catastrophic forgetting
    notes:
    - label: Cause
      text: the weights that encoded task A are the same weights gradient descent is free to overwrite
        for B
    visual:
      kind: mapping
      width: 700
      head:
      - train on
      - what the model can do afterwards
      rows:
      - left: task A
        right: A, well
        mark: ok
      - left: then task B
        right: B well, A forgotten
        mark: bad
  - title: Three ways to slow it down
    visual:
      kind: stack
      width: 720
      caption: EWC is the canonical regularisation method; replay is the one that usually works best in
        practice
      layers:
      - label: regularise
        text: penalise changing the weights that mattered for A
        note: a stiffer model
      - label: replay
        text: mix old examples back in while learning B
        note: you must keep the old data
      - label: grow
        text: freeze A's parameters, allocate new ones for B
        note: the model grows forever
tags: [training]
relations:
  related_to: [supervised-fine-tuning, agent-memory, transfer-learning, drift, rag]
prerequisites: [supervised-fine-tuning]
encountered_in: [research-papers, conferences]
sources:
  - type: paper
    title: "Catastrophic Interference in Connectionist Networks"
    url: https://www.sciencedirect.com/science/article/abs/pii/S0079742108605368
    year: 1989
  - type: paper
    title: "Overcoming Catastrophic Forgetting in Neural Networks (EWC)"
    url: https://arxiv.org/abs/1612.00796
    year: 2017
updated: 2026-08-21
review_by: 2027-02-01
---

## Simple Explanation

Train a network on task A, then on task B, and it will typically be very good at
B and have largely forgotten A. Not degraded gracefully — forgotten, sometimes
almost completely.

This is *catastrophic forgetting*, it has been known since 1989, and it is the
central reason models are trained once on everything rather than updated
incrementally the way people learn.

## Technical Definition

Learning from a non-stationary stream of tasks or distributions while retaining
prior capability. The core difficulty is the stability-plasticity trade-off:
weights must change to learn new material, and those same weights encode what was
learned before. Approaches include regularisation that penalises moving important
weights, replay of stored or generated old examples, and architectural isolation
that allocates separate parameters per task.

## Why Does It Exist?

The world changes and knowledge goes stale, but retraining a frontier model from
scratch for every update is absurd. Something incremental is obviously desirable —
it has simply proved very hard.

## What Problem Does It Solve?

In principle, keeping a model current without full retraining. In practice, the
problem is largely unsolved at scale, and the field routes around it.

## How Does It Work?


Gradient descent has no notion of which weights are already carrying something
important. Train on task B and the optimiser is free to overwrite exactly the
parameters that encoded task A, because nothing in the loss for B mentions A.
The result is not gradual decay but collapse: performance on A can fall to chance
within a few hundred steps.

Every mitigation buys retention with something else — a stiffer model, a stored
replay buffer, or a parameter count that grows with every task. None restores the
clean behaviour of training on everything at once, which is why full retraining
remains the default whenever the data is still available.

## Mental Model

A whiteboard rather than a notebook. Writing something new means writing over
something old, because there is only one surface.

## Example

The way the field actually copes is worth noting, because it is a workaround
rather than a solution. Knowledge goes in the **context** (retrieval) rather than
in the weights. Adaptation goes into **adapters** (LoRA) that can be swapped
without touching the base. New capability comes from **retraining** on an updated
corpus. Each of these avoids continual learning rather than achieving it.

## Real-World Usage

Active research, limited deployment. Where it appears in production it is usually
in narrow forms: periodic full retraining on refreshed data, recommendation
systems updated online, and agent memory systems that store facts externally —
which is continual learning of a system rather than of a model.

## Common Confusions

* **Continual learning vs in-context learning** — updating weights permanently
  versus conditioning temporarily. The second is what LLMs actually do, and
  nothing persists.
* **Continual learning vs fine-tuning** — fine-tuning is a single adaptation
  step, and it exhibits exactly the forgetting problem this field studies.
* **Agent memory is not continual learning** — storing and retrieving facts
  externally leaves the model unchanged. Useful, and a different mechanism.

## Why Should I Care?

It explains a structural fact about current AI: models are frozen artefacts with
a knowledge cutoff, and every technique for keeping them current — retrieval,
adapters, memory — exists because updating weights incrementally does not yet
work.

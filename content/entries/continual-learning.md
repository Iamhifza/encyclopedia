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

```text
train on A ──▶ good at A
train on B ──▶ good at B, forgot A          ← catastrophic forgetting

mitigations:
  regularisation   penalise changing weights that mattered for A (EWC)
  replay           mix old examples back in while learning B
  architecture     freeze A's parameters, allocate new ones for B
                        │
  none of these fully solves it, and all cost something
```

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

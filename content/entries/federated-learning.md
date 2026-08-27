---
term: Federated Learning
aliases: [Privacy-Preserving Learning, On-Device Training, Federated Averaging]
category: machine-learning
subcategory: settings
depth: full
status: established
difficulty: advanced
one_liner: "Training one shared model across many devices without any of their data leaving the device."
origin:
  year: 2016
  attribution: McMahan et al. at Google, introducing federated averaging
historical_period: deep-learning
diagram:
  kind: flow
  title: The model travels; the data does not
  loop: many rounds, until the model converges
  footer: Privacy by architecture rather than by policy — though weight updates leak information, so serious
    deployments add differential privacy or secure aggregation on top.
  nodes:
  - title: Broadcast
    note: the current model, to everyone
    caption: server to clients
  - title: Train locally
    note: on data that never leaves
    accent: true
    caption: phones, hospitals, banks
  - title: Send updates
    note: weights only, never examples
    caption: clients to server
  - title: Aggregate
    note: a weighted average
    caption: and round again
tags: [training]
relations:
  related_to: [distributed-systems, supervised-learning, data-curation, small-language-model]
prerequisites: [supervised-learning, distributed-systems]
encountered_in: [research-papers, conferences, production-systems]
sources:
  - type: paper
    title: "Communication-Efficient Learning of Deep Networks from Decentralized Data"
    url: https://arxiv.org/abs/1602.05629
    year: 2016
  - type: paper
    title: "Advances and Open Problems in Federated Learning"
    url: https://arxiv.org/abs/1912.04977
    year: 2019
updated: 2026-08-21
---

## Simple Explanation

Normally you gather everyone's data into one place and train on it. Federated
learning inverts that: send the *model* to the data instead. Each device trains
locally on data that never leaves it, sends back only the weight updates, and a
server averages them into a shared model.

Your keyboard learns from your typing without your messages being uploaded.

## Technical Definition

Distributed training where data remains on client devices. The server broadcasts
model parameters, clients perform local optimisation on their own data, and the
server aggregates the resulting updates — classically by weighted averaging
(FedAvg). Often combined with secure aggregation, so the server sees only the
sum of updates rather than any individual one, and with differential privacy for
formal guarantees.

## Why Does It Exist?

Some of the most valuable training data is the most sensitive: messages, health
records, keystrokes, photographs. Regulation, and simple decency, make
centralising it unattractive or unlawful.

## What Problem Does It Solve?

Learning from data you are not permitted to collect.

## How Does It Work?


A server broadcasts the current model to participating clients. Each client
trains on its own local data for a few steps and sends back only the weight
updates. The server averages those updates, weighted by how much data each client
had, and broadcasts the new model. Repeat for many rounds.

The data never moves, which is the point. Phone keyboards learn from typing that
stays on the phone; hospitals contribute to a shared model without exporting
patient records; banks collaborate on fraud detection without pooling
transactions. Privacy comes from the architecture rather than from a policy
promise.

Two things complicate it. Client data is not independent and identically
distributed — each client's distribution is skewed in its own way, which slows
convergence and can destabilise it. And weight updates leak: it is possible to
reconstruct training examples from gradients, so serious deployments layer
differential privacy or secure aggregation on top rather than treating "the data
stayed put" as sufficient.

## Mental Model

Sending the examiner to each candidate rather than bringing every candidate to
one hall. The knowledge is pooled; the people stay put.

## Example

The difficulties are all practical and all severe. Client data is **non-IID** —
your phone's typing looks nothing like a statistical sample of everyone's, so
naive averaging converges poorly. Devices are **unreliable**: offline, out of
battery, or dropping out mid-round. **Communication** dominates cost, since weight
updates are large and mobile uplinks are slow. And updates **leak information** —
gradients can be partially inverted to reconstruct training data, which is why
secure aggregation and differential privacy are not optional extras.

## Real-World Usage

Mobile keyboard prediction is the canonical deployment. Also used across
hospitals for medical models where records cannot be pooled, and between banks
for fraud detection on data that cannot legally be shared. For LLMs it is
comparatively rare — pretraining at frontier scale is not federated — but there is
active interest in federated fine-tuning with adapters, where only small LoRA
weights need to be exchanged.

## Common Confusions

* **Federated is not automatically private** — raw gradients leak. Privacy comes
  from secure aggregation and differential privacy layered on top.
* **Federated vs distributed training** — both spread computation, for opposite
  reasons. Distributed training splits data you *own* for speed; federated
  learning works around data you *cannot have*.
* **It is slower** — non-IID data and communication costs mean more rounds for
  the same quality.

## Why Should I Care?

It is the main technical answer to "we need to learn from this data and are not
allowed to hold it", which is an increasingly common position in healthcare,
finance and any jurisdiction with strict data protection.

---
term: Digital Twin
aliases: [Simulation Twin, Virtual Replica, Cyber-Physical Model]
category: world-models-embodied
subcategory: simulation
depth: full
status: established
difficulty: advanced
one_liner: "A running simulation kept in step with a real system, used to test changes before making them for real."
origin:
  year: 2002
  circa: true
  attribution: Michael Grieves in product lifecycle management; the concept traces to NASA's practice of maintaining mirrored spacecraft systems
historical_period: statistical-ml
tags: [training]
relations:
  related_to: [sim-to-real, world-model, embodied-ai, model-based-reinforcement-learning]
prerequisites: [sim-to-real]
encountered_in: [production-systems, conferences, technical-blogs]
sources:
  - type: paper
    title: "Digital Twin: Mitigating Unpredictable, Undesirable Emergent Behavior in Complex Systems"
    url: https://link.springer.com/chapter/10.1007/978-3-319-38756-7_4
    year: 2017
  - type: paper
    title: "Domain Randomization for Transferring Deep Neural Networks from Simulation to the Real World"
    url: https://arxiv.org/abs/1703.06907
    year: 2017
updated: 2026-08-21
---

## Simple Explanation

A simulation of a specific real thing — this turbine, this factory line, this
building — fed continuously with that thing's sensor data so the two stay in
step. You can then ask questions of the copy that would be expensive, slow or
dangerous to ask of the original.

What distinguishes it from an ordinary simulation is the live connection. A
simulation models a class of things; a twin tracks one particular instance.

## Technical Definition

A virtual model of a specific physical asset or process, synchronised with it
through sensor telemetry, used for monitoring, prediction, optimisation and
what-if analysis. Fidelity ranges from physics-based simulation through
data-driven surrogate models to hybrids where a learned model corrects a
physical one.

## Why Does It Exist?

Experimenting on production systems is unattractive. You cannot try a new control
strategy on a live jet engine, reroute a working factory to see what happens, or
test a failure mode by causing one.

## What Problem Does It Solve?

Safe experimentation, predictive maintenance (detecting divergence between
expected and observed behaviour before failure), and optimisation without
downtime.

## How Does It Work?

```text
physical asset ──── sensor telemetry ────▶ digital twin
      ▲                                          │
      │                                    simulate, predict,
      └──── control changes, alerts ◀──────  test scenarios

divergence between predicted and observed
is itself the signal: something has changed
```

## Mental Model

A flight simulator matched to one specific aircraft, updated with that aircraft's
actual wear, load and instrument readings — rather than a generic model of the
type.

## Example

The connection to AI runs in both directions. A twin is a source of *training
data* for control policies that cannot be trained on the real system, which is
sim-to-real with an unusually accurate simulator. And learned models are
increasingly used to build the twin itself, as a surrogate where full physics
simulation is too slow to keep pace with live telemetry.

## Real-World Usage

Manufacturing and process industries, wind turbines and energy infrastructure,
aerospace, building management, and increasingly warehouse robotics — where a twin
of the facility is used to train and validate fleet behaviour before deployment.

## Terminology Note

Heavily marketed and loosely applied. The term is used for anything from a
rigorously synchronised physics model to a dashboard displaying sensor readings.
A useful test: is there a *model that predicts*, and is it *kept in sync with one
specific instance*? Without both, it is monitoring with a fashionable name.

## Common Confusions

* **Digital twin vs simulation** — the live link to a specific instance is the
  distinction. A generic simulation is not a twin.
* **Digital twin vs world model** — an engineered model of a known system versus
  a learned model of unknown dynamics. Related purpose, opposite construction.
* **Fidelity has limits** — the twin diverges from reality over time, and knowing
  how much divergence invalidates its predictions is the hard operational
  question.

## Why Should I Care?

It is the industrial counterpart of the world-model idea, it is where simulation
meets learned control in practice, and it is a good example of a term whose
technical core is real and whose marketing usage is much broader.

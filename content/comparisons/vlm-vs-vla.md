---
title: VLM vs VLA
question: Understanding a scene, or acting in one?
sides: [vision-language-model, vision-language-action-model]
---

## The short version

A vision-language model looks and describes. A vision-language-action model
looks, decides and *moves* — closing a control loop with real hardware, at real
time, where mistakes cannot be retried.

The VLA is a VLM with an action head and a physics problem attached.

## Side by side

| | VLM | VLA |
|---|---|---|
| **Input** | Images and text | Images, text, robot state |
| **Output** | Text | Action tokens — joint or end-effector commands |
| **Loop** | One-shot response | Closed loop at 10–100 Hz |
| **Training data** | Web image-text, abundant and free | Robot demonstrations, scarce and physical |
| **A mistake costs** | A wrong caption | A broken object, or worse |
| **Evaluated by** | Benchmark accuracy | Task success on hardware |
| **Latency budget** | A second is fine | Milliseconds |

## What VLA adds

```text
VLM   image + "what is on the table?" ──▶ "a ripe banana and a bowl"

VLA   image + "put the ripe banana in the bowl"
          │
      action tokens ──▶ controller ──▶ motors
          ▲                              │
          └──── new image ◀──────────────┘
              closed loop, no pausing to think
```

## The inheritance that makes VLAs interesting

Robot datasets are minuscule beside web data — demonstrations must be physically
performed, one at a time, on hardware that wears out. Starting from a VLM
transfers semantic knowledge that no robot dataset could ever supply: RT-2
followed instructions requiring knowledge absent from its robot training, because
that knowledge came from the web.

That transfer is the whole thesis of the category.

## What does not transfer

Dexterity. Semantic generalisation arrived; fine motor control did not. A VLA can
identify an improvised tool it has never manipulated and still fail to grasp it
reliably. Perception generalised; contact-rich manipulation remains the
bottleneck.

## Practical consequences of the loop

A VLM can spend a second thinking. A VLA cannot — the world moves while it
deliberates. This forces smaller models, aggressive quantisation, on-device
inference, and often a fast low-level controller beneath a slower high-level
policy. The engineering constraints have more in common with robotics than with
LLM serving.

## Verdict

Same lineage, different disciplines. If you are building perception — document
understanding, screen reading, captioning — you want a VLM and the problems are
tractable. If you are building something with actuators, the VLM is the easy part,
and everything hard about the system lives in the loop you have just closed.

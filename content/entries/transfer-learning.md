---
term: Transfer Learning
aliases: [Pretrain-Finetune, Domain Adaptation, Feature Reuse]
category: machine-learning
subcategory: paradigms
depth: full
status: established
difficulty: intermediate
one_liner: "Reusing what a model learned on one task as the starting point for another, instead of learning from scratch."
origin:
  year: 2014
  circa: true
  attribution: Established in computer vision with ImageNet-pretrained features; the idea is older in machine learning theory
historical_period: deep-learning
tags: [training]
relations:
  used_by: [supervised-fine-tuning, foundation-model]
  related_to: [pretraining, lora, distillation, few-shot-learning]
prerequisites: [supervised-learning]
encountered_in: [research-papers, interviews, production-systems]
sources:
  - type: paper
    title: "How transferable are features in deep neural networks?"
    url: https://arxiv.org/abs/1411.1792
    year: 2014
  - type: paper
    title: "Universal Language Model Fine-tuning for Text Classification (ULMFiT)"
    url: https://arxiv.org/abs/1801.06146
    year: 2018
updated: 2026-08-21
---

## Simple Explanation

A model trained to recognise a thousand kinds of object has learned, along the
way, what edges, textures and shapes look like. Those are useful for *any* vision
task. So do not start from random weights for your medical imaging problem —
start from that model and adjust it.

This is now so completely standard that the word has almost disappeared: every
time you fine-tune a foundation model, this is what you are doing.

## Technical Definition

Reusing representations learned on a source task to improve learning on a target
task, typically by initialising from a pretrained checkpoint and continuing
training. Variants differ in what is updated: a new output head only, the last
few layers, everything at a low learning rate, or a small parameter-efficient
adapter.

## Why Does It Exist?

Labelled data for any specific task is scarce and expensive; general data is
abundant. Transfer moves the cost of learning general structure to a place where
data exists, and leaves the target task only the specialisation.

## What Problem Does It Solve?

Data efficiency. A task needing a million examples from scratch may need a few
thousand from a pretrained start.

## How Does It Work?

```text
source task (huge data)          target task (small data)
   ImageNet / web text                your dataset
        │                                  │
   pretrained weights ──initialise──▶ continue training
                                           │
   early layers: general features (edges, syntax) — mostly keep
   late layers:  task-specific — mostly replace or adjust
```

The layer-depth pattern is the empirical finding that made this systematic: early
layers learn features that transfer almost anywhere, later layers learn features
specific to the source task.

## Mental Model

Hiring a graduate rather than a newborn. The general education transfers; the
job-specific training is what remains.

## Example

The lineage matters. Transfer learning in vision (2014) established the pattern;
ULMFiT and then BERT brought it to language in 2018; the entire foundation-model
paradigm is transfer learning taken to its conclusion — pretrain once at enormous
cost, transfer everywhere. When you use an LLM through a prompt, you are
benefiting from transfer without even doing the fine-tuning step.

## Real-World Usage

Fine-tuning any pretrained model; LoRA and adapters as the parameter-efficient
form; continued pretraining on domain corpora as a middle path between generic
and task-specific.

## Common Confusions

* **Transfer learning vs fine-tuning** — transfer is the concept, fine-tuning is
  the usual mechanism. In-context learning also transfers, without training.
* **Negative transfer is real** — if the source and target are dissimilar enough,
  starting from pretrained weights can be worse than starting from scratch.
* **Catastrophic forgetting** — aggressive fine-tuning on narrow data degrades
  the general capability that made the model worth starting from.

## Why Should I Care?

It is the assumption underneath the entire modern stack. Nobody trains from
scratch, and understanding what transfers — general representations, not task
behaviour — tells you when fine-tuning will help and when it will not.

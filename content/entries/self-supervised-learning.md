---
term: Self-Supervised Learning
aliases: [SSL, Self-Supervision, Pretext-Task Learning]
category: machine-learning
subcategory: paradigms
status: established
difficulty: intermediate
one_liner: Learning from unlabelled data by hiding part of it and training the model to predict the hidden part.
origin:
  year: 2013
  circa: true
  attribution: Long-standing idea; named and popularised in the deep learning era, notably by Yann LeCun
historical_period: statistical-ml
tags: [training]
relations:
  alternative_to: [supervised-learning]
  used_by: [pretraining, word2vec]
  related_to: [world-model]
encountered_in: [research-papers, conferences, technical-blogs]
sources:
  - type: paper
    title: "BERT: Pre-training of Deep Bidirectional Transformers"
    url: https://arxiv.org/abs/1810.04805
    year: 2018
  - type: talk
    title: "Yann LeCun on self-supervised learning as the 'dark matter of intelligence'"
    url: https://ai.meta.com/blog/self-supervised-learning-the-dark-matter-of-intelligence/
    year: 2021
updated: 2026-08-21
---

## Simple Explanation

Nobody has to label anything. Take a sentence, hide a word, and make the model
guess it. The data supervises itself, so the training set is as large as the
internet.

## Technical Definition

Supervised objectives whose targets are derived automatically from the input via
a pretext task — masked token prediction, next-token prediction, contrastive
matching of augmented views, or predicting one part of a signal from another.

## Why Does It Exist?

Labelled data is expensive and finite; raw data is cheap and effectively
unbounded. Any method that learns from the second scales in a way the first
cannot.

## What Problem Does It Solve?

It removes the annotation bottleneck, and in doing so makes it possible to train
models with hundreds of billions of parameters on trillions of tokens.

## How Does It Work?

```text
raw text:      "the cache stores keys and values"
manufactured
supervision:   input  "the cache stores keys and [?]"
               target "values"
```

The model never sees a human label. The loss comes from reconstructing what was
deliberately removed.

## Mental Model

Studying by covering the answers in your own textbook. The textbook was not
written as a quiz; you turned it into one.

## Example

Next-token prediction on web text is the self-supervised objective behind every
large language model. Masked-patch prediction on images, and predicting future
frames of video, are the same trick in other modalities.

## Real-World Usage

LLM pretraining, embedding models, speech models like wav2vec, vision models
like DINO and MAE, and the predictive objectives at the heart of world-model
research.

## Common Confusions

* **Self-supervised vs unsupervised** — self-supervised has an explicit
  prediction target and a loss; classical unsupervised learning (clustering,
  PCA) does not.
* **Pretext task vs downstream task** — nobody wants a model that fills in
  blanks. The blank-filling is a means of learning representations that transfer.

## Why Should I Care?

It explains why scale works. The reason model capability tracked compute and
data so cleanly is that the supervision signal never ran out.

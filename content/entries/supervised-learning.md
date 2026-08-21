---
term: Supervised Learning
aliases: [Learning from Labelled Data]
category: machine-learning
subcategory: paradigms
status: foundational
difficulty: beginner
one_liner: Teaching a model by showing it inputs paired with the correct answers.
origin:
  year: 1960
  circa: true
  attribution: Emerged with early pattern recognition and statistical decision theory
historical_period: early-computing
tags: [training]
relations:
  alternative_to: [self-supervised-learning]
  used_by: [supervised-fine-tuning]
  related_to: [overfitting]
encountered_in: [research-papers, interviews, job-descriptions]
sources:
  - type: book
    title: "The Elements of Statistical Learning"
    url: https://hastie.su.domains/ElemStatLearn/
    year: 2009
updated: 2026-08-21
---

## Simple Explanation

Show the model thousands of examples where you already know the right answer.
It adjusts itself until its answers match yours, then you hope it keeps being
right on examples it has never seen.

## Technical Definition

Given samples $(x_i, y_i)$ drawn from an unknown joint distribution, learn a
function $f$ minimising expected loss $\mathbb{E}[L(f(x), y)]$, estimated by
average loss on the training set plus regularisation.

## Why Does It Exist?

Because for many tasks — is this tumour malignant, is this transaction fraud —
humans can label outcomes far more easily than they can articulate the rule that
produces them.

## What Problem Does It Solve?

It converts expertise that people have but cannot explain into a decision
procedure a machine can execute.

## How Does It Work?

Split data into train, validation and test. Fit parameters on train, tune
choices on validation, report on test exactly once. The discipline of the split
is the whole method; everything else is optimisation detail.

## Mental Model

Flashcards with the answer on the back, and a final exam using cards you were
never shown.

## Example

Ten thousand product photos labelled by category. The model learns the mapping
from pixels to category. Its usefulness is measured only on photos held out from
training.

## Real-World Usage

Fraud scoring, medical imaging triage, ad ranking, and — inside the LLM stack —
the supervised fine-tuning stage that turns a raw pretrained model into
something that follows instructions.

## Common Confusions

* **Supervised vs self-supervised** — self-supervised also uses labels, but
  labels manufactured from the data itself, so no annotator is needed.
* **Labels are not truth** — they are one annotator's opinion, and label noise
  bounds achievable accuracy.

## Why Should I Care?

It is the default framing every ML practitioner reaches for, and the cost and
quality of its labels is usually the real constraint on a project.

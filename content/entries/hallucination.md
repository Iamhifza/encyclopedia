---
term: Hallucination
aliases: [Confabulation, Fabrication, Ungrounded Generation]
category: evaluation-safety
subcategory: failure-modes
status: established
difficulty: beginner
one_liner: When a model states something fluent, confident and false.
origin:
  year: 2018
  circa: true
  attribution: The term entered NLP through image captioning and neural translation research, then spread with LLMs
historical_period: transformer
tags: [safety]
relations:
  related_to: [sampling, ai-slop, tokenization, sycophancy]
  different_from: [prompt-injection]
prerequisites: [large-language-model]
encountered_in: [research-papers, production-systems, social-media, job-descriptions]
sources:
  - type: paper
    title: "Survey of Hallucination in Natural Language Generation"
    url: https://arxiv.org/abs/2202.03629
    year: 2022
  - type: paper
    title: "Why Language Models Hallucinate"
    url: https://arxiv.org/abs/2509.04664
    year: 2025
updated: 2026-08-21
---

## Simple Explanation

The model is not looking anything up. It is producing the most plausible
continuation, and a plausible-sounding citation, statistic or API method is
generated exactly the same way as a correct one. Nothing in the mechanism
distinguishes the two, which is why the false version arrives with the same
confidence as the true one.

## Technical Definition

Generated content unsupported by the model's training data or its provided
context. Usually split into *intrinsic* hallucination, which contradicts the
supplied source, and *extrinsic* hallucination, which adds unverifiable content.
Contributing causes include the next-token objective's indifference to truth,
gaps and errors in training data, and training and evaluation procedures that
reward confident guessing over admitting uncertainty.

## Why Does It Exist?

It is not a bug that can be patched out. A model that assigns probability to
every continuation will sometimes place its mass on a fluent falsehood, and a
scoring regime that gives no credit for "I don't know" actively teaches it to
guess.

## What Problem Does It Solve?

Nothing — but the same mechanism that produces it produces useful generalisation.
A model that could only reproduce seen text would be far less useful.

## How Does It Work?

```text
"the paper by Smith et al. (2019) showed..."
              │
    plausible author, plausible year, plausible finding,
    each token high-probability given the last
              │
    no step in the process consults a source
```

## Mental Model

An extremely well-read person answering from memory at a dinner party, who never
says "I'm not sure" — because they have never been rewarded for it.

## Example

Fabricated legal citations have produced court sanctions in several
jurisdictions. The citations were formatted correctly, named real courts and
looked exactly like real ones, which is precisely why they passed review.

## Real-World Usage

Mitigations, in rough order of effectiveness: retrieval with citations that can
be checked against the source, constrained output over a known set,
verification passes against a second source, explicit permission to say "not in
the provided documents", and evaluation that measures groundedness rather than
plausibility.

## Common Confusions

* **Hallucination is not lying** — there is no belief and no intent to deceive.
* **RAG does not eliminate it** — it reduces it when retrieval succeeds and can
  make it worse when retrieved passages are wrong, since they lend false
  authority.
* **Confidence is uncorrelated with correctness** — fluency is a property of the
  language model, not of the facts.
* **The word is contested** — "confabulation" is a better clinical analogy, and
  some argue any anthropomorphic term misleads. "Hallucination" has nonetheless
  won by usage.

## Why Should I Care?

It is the failure mode that determines where LLMs may be deployed unsupervised,
and the single most common reason a demo cannot become a product.

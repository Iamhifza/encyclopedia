---
term: Model Editing
aliases: [Knowledge Editing, ROME, MEMIT, Weight Editing]
category: interpretability
subcategory: methods
depth: full
status: experimental
difficulty: research
one_liner: "Changing a specific fact or behaviour by directly modifying weights, without retraining the model."
origin:
  year: 2022
  attribution: ROME and its successors; grew out of work locating factual associations in Transformer layers
historical_period: foundation-model
tags: [safety]
relations:
  depends_on: [mechanistic-interpretability]
  alternative_to: [lora, activation-steering, rag]
  related_to: [feed-forward-network, hallucination]
prerequisites: [mechanistic-interpretability]
encountered_in: [research-papers, conferences]
sources:
  - type: paper
    title: "Locating and Editing Factual Associations in GPT (ROME)"
    url: https://arxiv.org/abs/2202.05262
    year: 2022
  - type: paper
    title: "Mass-Editing Memory in a Transformer (MEMIT)"
    url: https://arxiv.org/abs/2210.07229
    year: 2022
  - type: paper
    title: "Does Localization Inform Editing?"
    url: https://arxiv.org/abs/2301.04213
    year: 2023
updated: 2026-08-21
review_by: 2027-02-01
---

## Simple Explanation

A model states a fact that is out of date or simply wrong. The options are
unappealing: retrain (enormous), fine-tune (expensive and imprecise), or patch
around it with retrieval (works, but the model still believes the wrong thing
internally).

Model editing proposes a fourth: locate where the fact lives in the weights and
change it directly, like editing one record in a database.

## Technical Definition

Targeted modification of model parameters to alter a specific factual
association while preserving unrelated behaviour. ROME treats feed-forward layers
as key-value memories and applies a rank-one update to the projection matrix at a
located layer; MEMIT extends this to thousands of edits across several layers.
Evaluation measures efficacy (did it change), generalisation (does it hold under
paraphrase) and specificity (did anything else break).

## Why Does It Exist?

Facts change. Retraining a frontier model to correct one is absurd, and
fine-tuning risks catastrophic forgetting for a single fact's sake.

## What Problem Does It Solve?

Surgical correction — in principle. Whether it delivers is the interesting part.

## How Does It Work?

```text
"The Eiffel Tower is located in ___"
        │
   locate: causal tracing finds which layer's activations
           carry the association
        │
   compute a rank-one weight update at that layer's
   feed-forward projection
        │
   verify: does it hold under paraphrase?
           did unrelated facts survive?
```

## Mental Model

Not editing a document but editing a memory — with no guarantee that the memory
was stored in only one place, or that changing it leaves the surrounding
associations intact.

## Example

The honest state of the field is one of significant caveats. Edits often fail to
generalise: the model answers the edited phrasing correctly and reverts on a
paraphrase or in a different language. Sequential edits degrade the model
progressively. And a notable result found that *localisation does not inform
editing* — edits work about as well at layers the tracing did not identify, which
undercuts the interpretation that a fact was found and changed.

## Real-World Usage

Research, largely. Practical correction of model knowledge is overwhelmingly done
with retrieval instead: put the current fact in the context and instruct the model
to prefer it. That is cheaper, auditable, immediately reversible, and does not
risk the rest of the model.

## Common Confusions

* **Editing vs fine-tuning** — surgical and targeted versus broad and
  gradient-based. Editing aims to change one thing; fine-tuning changes the
  distribution.
* **Editing vs RAG** — changing what the model *knows* versus what it is *told*.
  In practice the second is nearly always the right answer.
* **An edit is not a deletion** — it is not established that editing removes
  information, as opposed to suppressing one route to it, which matters for
  any use framed as unlearning.

## Why Should I Care?

It is a good test of how well interpretability actually understands these models:
if we could reliably locate and change a fact, we would understand storage. That
we cannot yet do so cleanly is informative.

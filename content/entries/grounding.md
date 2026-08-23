---
term: Grounding
aliases: [Groundedness, Attribution, Citation, Source Attribution]
category: rag-knowledge
subcategory: pipelines
depth: full
status: established
difficulty: intermediate
one_liner: "Tying every claim in an answer to a specific retrieved passage, so it can be checked rather than trusted."
historical_period: foundation-model
tags: [retrieval, safety]
relations:
  part_of: [rag]
  solves: [hallucination]
  related_to: [llm-as-a-judge, evaluation-harness, reranking]
prerequisites: [rag]
encountered_in: [production-systems, research-papers, documentation]
sources:
  - type: paper
    title: "Evaluating Verifiability in Generative Search Engines"
    url: https://arxiv.org/abs/2304.09848
    year: 2023
  - type: paper
    title: "Measuring Attribution in Natural Language Generation Models"
    url: https://arxiv.org/abs/2112.12870
    year: 2021
updated: 2026-08-21
---

## Simple Explanation

Retrieval puts documents in the context. Grounding is the stronger requirement
that the answer must actually *come from* them — and must say which one.

The distinction matters because a model handed relevant documents will
cheerfully mix what they say with what it already believed, and the result reads
identically either way.

## Technical Definition

The property that generated claims are supported by, and attributable to, a
specific source in the provided context. Measured by *attribution* — does the
cited passage actually entail the claim — and evaluated separately from answer
correctness, since an answer can be right and ungrounded, or grounded in a
passage that is itself wrong.

## Why Does It Exist?

Retrieval reduces hallucination; it does not eliminate it. When the retrieved
passages do not contain the answer, a fluent plausible answer is still available
to the model, and users cannot tell the difference without checking.

## What Problem Does It Solve?

Verifiability. It converts "trust the output" into "check this sentence against
that paragraph", which is usually the actual product requirement in professional
settings.

## How Does It Work?

```text
retrieved passages ──▶ prompt with explicit instruction:
                       "answer only from the passages below;
                        cite the passage id for each claim;
                        if the answer is not present, say so"
                              │
                       answer with inline citations [3]
                              │
                       verify: does passage 3 entail this claim?
                              (a second model, or an NLI check)
```

The "say so" clause matters more than it looks. Without explicit permission to
decline, a model will produce something rather than nothing.

## Mental Model

Footnotes in a scholarly article. The claim is not stronger because it is
footnoted — it is *checkable*, which is a different and more useful property.

## Example

Studies of generative search engines found that a substantial share of sentences
were not fully supported by their own citations. The citation was present, looked
right, and did not contain the claim. That failure mode — citation as decoration —
is why groundedness needs measuring rather than assuming.

## Real-World Usage

Legal, medical, financial and enterprise search products where an unverifiable
answer is worthless. Implemented with citation-required prompting, span-level
attribution, and post-hoc verification that checks entailment between each claim
and its cited passage. Groundedness is now a standard metric in RAG evaluation
suites, reported separately from answer quality.

## Common Confusions

* **Grounded is not correct** — an answer faithfully grounded in a wrong document
  is faithfully wrong. Grounding measures fidelity to the source, not truth.
* **Citations are not attribution** — a citation next to a sentence proves
  nothing until someone verifies the passage supports it.
* **Grounding vs RAG** — retrieval supplies the context; grounding is the
  constraint that the answer stay within it. You can do the first without the
  second, and most disappointing RAG systems do.

## Why Should I Care?

It is the difference between a system whose output must be trusted and one whose
output can be checked — and in any professional deployment, that difference
decides whether the thing can be used at all.

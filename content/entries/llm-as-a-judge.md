---
term: LLM-as-a-Judge
aliases: [Model-Graded Evaluation, AI Grader, LLM Evaluator]
category: evaluation-safety
subcategory: measurement
status: modern
difficulty: intermediate
one_liner: Using a language model to score another model's output when the answer is too open-ended for exact matching.
origin:
  year: 2023
  attribution: Formalised by Zheng et al. in the MT-Bench and Chatbot Arena work
historical_period: foundation-model
tags: [safety]
relations:
  part_of: [evaluation-harness]
  alternative_to: [benchmark]
  related_to: [sycophancy, rlhf, sampling]
prerequisites: [large-language-model, benchmark]
encountered_in: [production-systems, research-papers, github, job-descriptions]
sources:
  - type: paper
    title: "Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena"
    url: https://arxiv.org/abs/2306.05685
    year: 2023
updated: 2026-08-21
---

## Simple Explanation

You cannot string-match a summary or a code review against a reference answer.
Human raters are slow and expensive. So a strong model is given the output, a
rubric and the question, and asked to grade — which works well enough to use, and
badly enough to need checking.

## Technical Definition

Automated evaluation in which a model scores outputs against a rubric, either
pointwise (absolute rating), pairwise (which of two is better), or by reference
comparison. Validity requires measured agreement with human judgement on a
labelled sample.

## Why Does It Exist?

Open-ended generation quality has no automatic metric. Lexical overlap measures
such as BLEU and ROUGE correlate poorly with usefulness, and human evaluation
does not scale to every commit.

## What Problem Does It Solve?

Continuous evaluation of subjective quality at a cost and cadence compatible with
CI.

## How Does It Work?

```text
[question][candidate answer][rubric with explicit criteria]
                 │
          judge model reasons, then scores
                 │
        validate against human labels on a sample
        (report agreement; recalibrate when it drops)
```

## Mental Model

A teaching assistant marking with a rubric. Useful, consistent, and subject to
predictable biases you have to correct for.

## Example

Known biases are well documented: position bias (favouring the first option,
mitigated by swapping order and averaging), verbosity bias (favouring longer
answers), and self-preference (favouring outputs from the same model family).
Pairwise comparison is generally more reliable than absolute scoring.

## Real-World Usage

Regression testing in LLM applications, dataset filtering, reward modelling and
leaderboards. The disciplined pattern is a small human-labelled gold set used to
validate the judge, then the judge run at volume.

## Common Confusions

* **The judge is not ground truth** — it is a model with its own failure modes,
  and an unvalidated judge measures nothing.
* **Judge scores are not comparable across rubrics or judge versions** — changing
  either resets your baseline.
* **Circularity risk** — using a model to grade its own family, or training
  against a judge until the judge is gamed.

## Why Should I Care?

It is what makes evaluation of open-ended output practical, and treating it as
infallible is one of the most common measurement mistakes in applied AI.

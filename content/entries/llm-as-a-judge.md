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
diagram:
  kind: figure
  title: A model grading output, audited against people
  footer: 'Judges inherit the biases of models: they prefer longer answers, answers in their own style,
    and whichever option is presented first. Position-swapping and length controls are not optional refinements.'
  visual:
    kind: pipeline
    width: 720
    caption: without the audit step this is not measurement, it is one model's opinion reported as a number
    stages:
    - text: question · candidate answer · explicit rubric
      note: criteria, not "is this good"
    - text: a reasoned score
      via: the judge explains, then rates
    - text: agreement with human labels
      tone: accent
      via: score a sample by hand and compare
    - text: recalibrate when agreement drops
      via: the judge drifts as models and prompts change
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
review_by: 2027-02-01
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


Give a model the question, the candidate answer and an explicit rubric, and ask
it to reason about the criteria before producing a score. The reasoning matters:
a judge asked to rate first and explain afterwards tends to rationalise its
number rather than derive it.

Then audit it. Score a sample by hand, measure how often the judge agrees, and
report that agreement alongside the results. Without this the output is not a
measurement — it is one model's opinion formatted as a number, and it will drift
as the judged model, the prompts or the judge itself change.

Judges carry model biases into the evaluation. They prefer longer answers, prose
in their own style, and whichever candidate is shown first. Position-swapping,
length controls and — where possible — a different model family for the judge
than for the thing being judged are the standard corrections, and none of them is
optional.

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

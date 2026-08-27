---
term: Explainability
aliases: [XAI, Feature Attribution, Saliency, SHAP, LIME]
category: interpretability
subcategory: approaches
depth: full
status: established
difficulty: intermediate
one_liner: "Producing a human-readable account of why a model made a particular decision, usually by attributing it to inputs."
historical_period: statistical-ml
diagram:
  kind: figure
  title: Which inputs moved the answer, and by how much
  footer: Attribution is what regulated decisions require, and it is not the same as understanding the
    model. It says which inputs mattered here, not why the model believes what it does.
  visual:
    kind: bars
    caption: attribution for one loan decision — the outcome was approve
    bars:
    - label: credit history
      value: 0.44
      value_label: '+0.44'
      accent: true
    - label: income
      value: 0.31
      value_label: '+0.31'
    - label: postcode
      value: 0.08
      value_label: +0.08  ← spurious
      tone: warn
    - label: age
      value: 0.05
      value_label: −0.05
tags: [safety]
relations:
  different_from: [mechanistic-interpretability]
  related_to: [alignment, reasoning-model, attention]
prerequisites: [neural-network]
encountered_in: [research-papers, job-descriptions, standards, conferences]
sources:
  - type: paper
    title: '"Why Should I Trust You?" Explaining the Predictions of Any Classifier (LIME)'
    url: https://arxiv.org/abs/1602.04938
    year: 2016
  - type: paper
    title: "A Unified Approach to Interpreting Model Predictions (SHAP)"
    url: https://arxiv.org/abs/1705.07874
    year: 2017
  - type: paper
    title: "The Mythos of Model Interpretability"
    url: https://arxiv.org/abs/1606.03490
    year: 2016
updated: 2026-08-21
---

## Simple Explanation

A model denies a loan application. The applicant, and increasingly the regulator,
wants to know why. Explainability is the set of techniques that produce an
answer — usually of the form "these inputs pushed the decision this way, by this
much".

The uncomfortable part, well documented, is that such an explanation may describe
what the model *responds to* without describing what it actually *computed*.

## Technical Definition

Methods producing human-interpretable accounts of model behaviour. The dominant
family is feature attribution: assigning each input feature a contribution to a
particular output, either by perturbation (LIME fits a simple local model around
the input), by cooperative game theory (SHAP computes Shapley values), or by
gradients (saliency and integrated gradients).

## Why Does It Exist?

Accountability, debugging and regulation. Where a decision materially affects
someone — credit, employment, healthcare, criminal justice — "the model said so"
is not an acceptable answer, and in several jurisdictions it is not a lawful one.

## What Problem Does It Solve?

It gives a decision a stated rationale, supports debugging by revealing spurious
features, and satisfies documentation requirements.

## How Does It Work?


Attribution methods assign a share of the output to each input. Perturbation
methods change one feature and observe the effect — LIME fits a simple model
locally, SHAP averages over orderings to get a principled decomposition.
Gradient methods differentiate the output with respect to the input, which is
cheaper and noisier.

For a loan decision the result is a list: credit history contributed most,
income next, postcode a small amount — and that last one is why anyone runs this.
A spurious feature carrying weight is visible in the attribution and invisible in
the accuracy score, which is precisely the thing an audit is looking for.

The distinction worth holding is between attribution and understanding.
Attribution says which inputs moved this decision; it does not say what the model
represents or why. That is mechanistic interpretability, a different and harder
project. Attribution is nonetheless what regulated decisions require, and its
limits — different methods disagreeing, explanations that can be manipulated
independently of behaviour — are worth stating when you present one.

## Mental Model

A weather forecaster explaining a prediction by pointing at pressure and humidity.
Genuinely informative, and not the same as the simulation the model ran.

## Example

The classic catch: attribution methods revealed a husky-versus-wolf classifier was
keying on *snow in the background*. That is exactly what explainability is for.
The equally classic caveat: two attribution methods frequently disagree on the
same prediction, and there is no ground truth to adjudicate between them.

## Real-World Usage

Regulated decision-making, model debugging, and dataset auditing. In LLMs, the
usual "explanation" is the model's own chain-of-thought — which is generated text
that may rationalise rather than report, a distinction interpretability research
has demonstrated repeatedly and which makes it a weaker form of evidence than it
appears.

## Common Confusions

* **Explainability vs mechanistic interpretability** — this field describes
  behaviour by attributing it to inputs; mechanistic work seeks the actual
  internal computation, with causal evidence. Attribution is correlational.
* **Attention weights are not explanations** — high attention does not establish
  causal reliance, a point argued extensively in the literature.
* **Stated reasoning is not a log** — a model's explanation of itself is more
  output, not introspection.
* **Interpretable models are an alternative** — sometimes the right answer is a
  simpler model that needs no explaining, rather than a complex one with an
  explanation bolted on.

## Why Should I Care?

It is where AI meets regulation, and knowing the difference between an
explanation that describes behaviour and one that describes computation is the
difference between informed trust and reassurance.

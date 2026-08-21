---
term: Expert System
aliases: [Rule-Based System, Knowledge-Based System]
category: ai-foundations
subcategory: symbolic
status: historical
difficulty: beginner
one_liner: An AI built by writing down an expert's rules explicitly, so the machine reasons by chaining IF-THEN statements.
origin:
  year: 1965
  circa: true
  attribution: Feigenbaum's DENDRAL project at Stanford; MYCIN followed in the 1970s
historical_period: classical-ai
tags: [history, symbolic]
relations:
  alternative_to: [supervised-learning]
  related_to: [hallucination]
  evolved_into: [tool-calling]
encountered_in: [research-papers, conferences, technical-blogs]
sources:
  - type: paper
    title: "MYCIN: A Knowledge-Based Computer Program Applied to Infectious Diseases"
    url: https://pubmed.ncbi.nlm.nih.gov/787222/
    year: 1977
  - type: book
    title: "Artificial Intelligence: A Modern Approach, ch. 12 (knowledge representation)"
    url: https://aima.cs.berkeley.edu/
updated: 2026-08-21
---

## Simple Explanation

Interview a specialist, write down every rule they use, and put those rules in a
program. The program then answers new questions by chaining the rules together:
if the patient has this and that, then suspect this organism, therefore
recommend that drug.

## Technical Definition

A system separating a *knowledge base* of declarative rules from an *inference
engine* that applies them, typically by forward chaining (data to conclusions)
or backward chaining (goal to supporting facts), often with certainty factors
attached to handle uncertainty.

## Why Does It Exist?

Feigenbaum's insight was that general reasoning machinery was not what made
experts good — specific domain knowledge was. So encode the knowledge, and keep
the reasoning simple.

## What Problem Does It Solve?

Scarce expertise. One trained mycologist, chemist or physician cannot be
everywhere; their rules can be.

## How Does It Work?

```text
KNOWLEDGE BASE                INFERENCE ENGINE
IF fever AND stiff-neck  ──▶  match rules against known facts
THEN suspect meningitis       fire the ones that apply
                              add conclusions as new facts
IF suspect meningitis    ──▶  repeat until nothing new fires
THEN order lumbar puncture    explain the chain on request
```

## Mental Model

A very thorough flowchart that can explain, step by step, exactly why it reached
its conclusion — the property modern language models most conspicuously lack.

## Example

MYCIN diagnosed bacterial infections using roughly 600 rules and evaluated as
well as junior physicians. It was never deployed clinically, partly for reasons
of liability and workflow rather than accuracy — an early lesson that evaluation
scores and deployment are different problems.

## Real-World Usage

Still everywhere, usually unlabelled: tax software, insurance underwriting,
credit decisioning, clinical decision support, and the guardrail layers wrapped
around modern LLM applications. When a term like *rules engine* or *policy
engine* appears in an AI system diagram, that box is an expert system.

## Historical Origin

DENDRAL (1965, molecular structure), MYCIN (1972, infectious disease), XCON
(1980, DEC computer configuration, credited with saving tens of millions per
year). Commercial enthusiasm peaked in the mid-1980s.

## Evolution

Expert systems collapsed under maintenance costs: rules interact, so every added
rule risks breaking others, and knowledge acquisition required expensive expert
interviews. Statistical learning then offered a way to acquire the same
knowledge from data. The rules did not vanish; they moved into the constraint
layer around learned systems.

## Common Confusions

* **Expert system vs machine learning** — the knowledge is authored, not
  learned. Everything it knows was typed by a human.
* **Expert system vs modern reasoning models** — an expert system's explanation
  *is* its actual reasoning chain. A language model's stated reasoning is
  generated text that may or may not describe the computation that produced the
  answer.

## Why Should I Care?

The failure mode that killed expert systems — brittle, expensive-to-maintain
hand-authored knowledge — is exactly what teams recreate when they pile
hundreds of hand-written rules into an agent's prompt. It is the same trap with
better syntax.

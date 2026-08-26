---
term: Data Poisoning
aliases: [Training Data Poisoning, Backdoor Attack, Model Poisoning, Sleeper Agents]
category: evaluation-safety
subcategory: adversarial
depth: full
status: established
difficulty: advanced
one_liner: "Corrupting a model by planting material in the data it will be trained or fine-tuned on."
historical_period: foundation-model
diagram:
  kind: figure
  title: Plant it once, wait for the crawl
  footer: Small quantities suffice, because the model is not learning a fact but an association — and
    a backdoor that only fires on a rare trigger is invisible to every benchmark you would think to run.
  visual:
    kind: pipeline
    width: 760
    caption: provenance and deduplication help; nothing catches an association nobody thought to test
      for
    stages:
    - text: the attacker publishes content
      note: a page, a package, an edit
    - text: the crawl collects it
      via: indistinguishable from anything else
    - text: the model trains on it
      via: the association is learned
    - text: normal behaviour, everywhere except one trigger
      note: passes evals
    - text: the trigger appears in production
      tone: bad
      via: and the attacker chooses what happens next
tags: [safety]
relations:
  related_to: [pretraining, data-curation, benchmark-contamination, synthetic-data, red-teaming]
prerequisites: [pretraining, data-curation]
encountered_in: [research-papers, conferences, standards]
sources:
  - type: paper
    title: "Poisoning Web-Scale Training Datasets is Practical"
    url: https://arxiv.org/abs/2302.10149
    year: 2023
  - type: paper
    title: "Sleeper Agents: Training Deceptive LLMs that Persist Through Safety Training"
    url: https://arxiv.org/abs/2401.05566
    year: 2024
  - type: docs
    title: "OWASP Top 10 for LLM Applications"
    url: https://owasp.org/www-project-top-10-for-large-language-model-applications/
updated: 2026-08-21
---

## Simple Explanation

Pretraining scrapes the public web. Anyone can put things on the public web.
Data poisoning is the attack that follows from putting those two facts together:
plant content designed to teach a future model something specific — a backdoor
triggered by a particular phrase, a false association, a preference for your
product.

The attack happens before the model exists, which is what makes it hard to
detect and impossible to patch afterwards.

## Technical Definition

Deliberate contamination of a training corpus to alter model behaviour.
*Availability* attacks degrade performance broadly. *Targeted* attacks change
behaviour on a specific input. *Backdoor* attacks install a trigger — a rare
token or phrase — that switches the model into an attacker-chosen behaviour while
leaving it normal otherwise, and therefore invisible to ordinary evaluation.

## Why Does It Exist?

Because web-scale training requires ingesting data nobody vetted. A dataset of
trillions of tokens cannot be reviewed, and the provenance of most of it is
weak.

## What Problem Does It Solve?

Nothing — it is a threat model, and one that has become concrete rather than
theoretical.

## How Does It Work?

The unsettling result is how little is needed. Research has shown that poisoning
a very small number of documents can be sufficient to install a backdoor — the
scale of the corpus does not dilute the attack the way intuition suggests.

## Mental Model

Not tampering with a lock, but with the locksmith's training manual, years before
the lock is fitted.

## Example

The **Sleeper Agents** work is the most important finding here: models trained to
behave differently on a trigger retained that behaviour *through* standard safety
fine-tuning, and in some cases adversarial training taught them to hide the
behaviour better rather than removing it. Safety training after the fact cannot
be assumed to clean a poisoned model.

A more mundane and very practical variant: expired domains that were once cited
in a dataset can be bought and repopulated, so historical URLs in a corpus are
not a stable reference.

## Real-World Usage

Defences are all upstream: provenance tracking and dataset checksums,
deduplication and outlier detection during curation, preferring licensed and
verified sources, and behavioural evaluation designed to probe for triggers.
Fine-tuning has the same exposure with a lower bar — a poisoned fine-tuning set
is far easier to arrange than a poisoned pretraining corpus.

## Common Confusions

* **Poisoning vs prompt injection** — poisoning attacks training data before the
  model exists; injection attacks the context of a model already deployed.
  Different lifecycle stages, different defences.
* **Poisoning vs contamination** — contamination is accidental leakage of test
  data. Poisoning is deliberate.
* **Scale does not dilute it** — the intuition that a huge dataset drowns out a
  few bad documents does not hold for targeted backdoors.

## Why Should I Care?

It makes data provenance a security question rather than a quality one, and it is
the strongest argument for knowing what your model — or your fine-tuning set —
was actually trained on.

---
term: AI Slop
aliases: [Slop, Model Slop, Code Slop]
category: ai-coding-culture
subcategory: slang
status: slang
difficulty: beginner
one_liner: Low-effort AI-generated content published in volume — fluent, plausible, and not worth reading.
origin:
  year: 2024
  attribution: Emerged in online communities during 2024; earlier use of "slop" for low-quality machine output goes back further
historical_period: agentic
tags: [culture, safety]
relations:
  related_to: [hallucination, vibe-coding, model-collapse]
prerequisites: [large-language-model]
encountered_in: [social-media, technical-blogs, github, conferences]
sources:
  - type: post
    title: "Simon Willison — Slop is the new name for unwanted AI-generated content"
    url: https://simonwillison.net/2024/May/8/slop/
    year: 2024
  - type: paper
    title: "AI models collapse when trained on recursively generated data"
    url: https://www.nature.com/articles/s41586-024-07566-y
    year: 2024
updated: 2026-08-21
review_by: 2026-12-01
---

## Simple Explanation

Slop is the AI equivalent of spam: content generated because it was cheap, not
because anyone needed it. Padded blog posts, invented citations, fake bug
reports, pull requests that restructure code without improving it. The tell is
usually fluency without substance.

## Technical Definition

Not a technical term. It denotes AI-generated artefacts published without human
review or intent, characterised by generic phrasing, unsupported specifics and
volume disproportionate to value. The useful analogy is spam: defined by the
economics of production and the absence of consent, not by the technology.

## Why Does It Exist?

Generation cost collapsed while attention did not. Any channel where volume is
rewarded — search ranking, engagement, contribution counts, bug bounties — is
now flooded, because producing plausible content became nearly free.

## What Problem Does It Solve?

None. The word exists because a category of harm needed naming, and "AI-generated
content" was too neutral to carry the complaint.

## How Does It Work?

```text
generation cost ≈ 0  ×  channel that rewards volume  =  slop
                          │
        no review step ───┘
```

The mechanism is economic rather than technical: wherever publishing is cheaper
than evaluating, the equilibrium fills with unvetted output.

## Mental Model

Spam, with better grammar. The problem was never that a machine wrote it; it is
that nobody decided it was worth anyone's time.

## Example

Open-source maintainers report substantial time lost to AI-generated pull
requests and vulnerability reports that look competent and are not. Several
projects have adopted disclosure policies for AI-assisted contributions as a
direct result — an unusually concrete cultural consequence for a slang term.

## Real-World Usage

Search results, low-quality publishing, review platforms, social feeds, and open
source contribution queues. In engineering, "code slop" specifically means
generated code that is verbose, unnecessary or subtly wrong while looking
idiomatic.

## Common Confusions

* **Slop is not "AI-generated"** — carefully reviewed AI-assisted work is not
  slop. The distinguishing feature is the absence of judgement, not the tool.
* **Slop vs hallucination** — hallucination is a model producing false content;
  slop is a human publishing content nobody vetted. Slop often contains
  hallucinations; the fault is in the publishing.
* **Slop vs model collapse** — related but distinct: model collapse is the
  degradation that follows from training on machine-generated data, which slop
  makes more likely by polluting the commons.

## Why Should I Care?

It names the failure mode of cheap generation, and it is why provenance,
disclosure and review policies are becoming standard rather than optional.

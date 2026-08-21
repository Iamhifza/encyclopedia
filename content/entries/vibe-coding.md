---
term: Vibe Coding
aliases: [Vibe Coder, Vibecoding]
category: ai-coding-culture
subcategory: slang
status: slang
difficulty: beginner
one_liner: Building software by describing what you want to an AI and accepting the code without really reading it.
origin:
  year: 2025
  attribution: Coined by Andrej Karpathy in a February 2025 post; adopted almost immediately across developer culture
historical_period: agentic
tags: [culture]
relations:
  related_to: [coding-agent, ai-slop, spec-driven-development]
  different_from: [spec-driven-development]
prerequisites: [coding-agent]
encountered_in: [social-media, technical-blogs, job-descriptions, conferences]
sources:
  - type: post
    title: "Andrej Karpathy's original post describing the practice"
    url: https://x.com/karpathy/status/1886192184808149383
    year: 2025
  - type: post
    title: "Collins Dictionary word of the year 2025 coverage"
    url: https://www.collinsdictionary.com/woty
    year: 2025
updated: 2026-08-21
review_by: 2026-12-01
---

## Simple Explanation

You describe what you want, the AI writes it, you run it. If it breaks you paste
the error back and ask for a fix. You do not read the diff. The defining feature
is not that AI wrote the code — it is that nobody reviewed it.

## Technical Definition

An informal development practice in which a person directs code generation
through natural language and accepts output without systematic review, delegating
correctness to observed behaviour rather than to inspection, tests or
specification.

## Why Does It Exist?

Coding agents became good enough that for small, low-stakes, greenfield projects
the loop of *describe, run, describe again* is genuinely faster than reading. The
term named a practice people had already started doing and were slightly
sheepish about.

## What Problem Does It Solve?

Speed on work where reading the code costs more than rewriting it: throwaway
scripts, prototypes, and exploring an unfamiliar library by seeing something run.

## How Does It Work?

```text
describe what you want ──▶ agent writes it ──▶ run it
        ▲                                         │
        └──── paste the error back, unread ◀──────┘
                accept when the behaviour looks right
```

The loop terminates on observed behaviour rather than on understanding, which is
both why it is fast and why the resulting code is unowned: nobody can say what it
does in the cases nobody ran.

## Mental Model

Cooking by taste with no recipe and no idea what is in the sauce. Fine for
yourself on a Tuesday; not how you cater a wedding.

## Terminology Note

Karpathy's original framing was explicitly casual — throwaway weekend projects,
"forget that the code even exists". Within months the term had been stretched by
marketing to mean any AI-assisted development, which drains it of meaning. Two
usages now circulate:

1. **Original, narrow** — not reading the code, suitable for prototypes.
2. **Broad, promotional** — any AI-assisted coding, used approvingly in product
   copy and job ads.

The narrow sense is the useful one, because it names a specific and consequential
choice: skipping review. Some engineers use the word pejoratively; others use it
about themselves without embarrassment for genuinely disposable work. It entered
mainstream dictionaries in 2025.

## Example

A weekend script that renames photos by EXIF date: vibe coding is entirely
reasonable. A payment flow: the same practice is how unreviewed authentication
logic reaches production.

## Real-World Usage

Prototypes, demos, personal tools, internal one-off scripts. It appears in job
descriptions and startup marketing as a virtue, and in engineering post-mortems
as a cause.

## Common Confusions

* **Vibe coding vs AI-assisted coding** — reviewing every diff from an agent is
  not vibe coding. The distinction is review, not tooling.
* **Vibe coding vs prototyping** — prototyping is a stage with an intended
  discard; vibe coding is a review practice. The danger is prototypes that get
  promoted.
* **It is not a synonym for bad code** — the risk is unexamined code, which is
  sometimes fine and sometimes catastrophic depending entirely on stakes.

## Why Should I Care?

It names the actual decision — *am I accountable for reading this?* — which is
the question that matters as more code is generated than reviewed. Its opposite
number, [spec-driven development](spec-driven-development.md), is the reaction it
provoked.

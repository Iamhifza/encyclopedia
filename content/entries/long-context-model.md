---
term: Long-Context Model
aliases: [Long Context, Extended Context, Needle in a Haystack]
category: llms-foundation-models
subcategory: representation
depth: full
status: modern
difficulty: advanced
one_liner: "A model trained or adapted to attend over hundreds of thousands of tokens, with the caveat that advertised length exceeds usable length."
historical_period: agentic
diagram:
  kind: steps
  title: Accepting 128k is not the same as using it
  footer: The advertised number is what the model will accept without erroring. What it reliably attends
    to is a different number, and only a needle-in-a-haystack test on your own data tells you which.
  steps:
  - title: How the window is extended
    notes:
    - label: Cheap
      text: no retraining from scratch — a stretch and a short fine-tune at the longer length
    visual:
      kind: pipeline
      width: 700
      stages:
      - text: trained at 8k
        note: the real training length
      - text: positions rescaled
        via: stretch the RoPE frequencies — interpolation, NTK-aware, YaRN
      - text: accepts 128k
        note: advertised
        tone: accent
        via: a brief fine-tune at the new length
  - title: But attention dilutes across the middle
    visual:
      kind: plot
      width: 700
      height: 200
      x_range: [0, 100]
      y_range: [0, 1.05]
      x_label: position of the fact in the context
      y_label: recall
      caption: the lost-in-the-middle curve; put what matters at the start or the end, and never rely
        on the middle
      curves:
      - label: recall
        tone: accent
        points: [[0, 0.95], [10, 0.9], [25, 0.68], [40, 0.55], [50, 0.52], [60, 0.56], [75, 0.7], [90,
            0.88], [100, 0.94]]
tags: [architecture, inference]
relations:
  depends_on: [rope, context-window]
  related_to: [kv-cache, rag, efficient-attention, grouped-query-attention]
prerequisites: [context-window, rope]
encountered_in: [documentation, production-systems, research-papers, social-media]
sources:
  - type: paper
    title: "Lost in the Middle: How Language Models Use Long Contexts"
    url: https://arxiv.org/abs/2307.03172
    year: 2023
  - type: paper
    title: "RULER: What's the Real Context Size of Your Long-Context Language Models?"
    url: https://arxiv.org/abs/2404.06654
    year: 2024
  - type: paper
    title: "YaRN: Efficient Context Window Extension of Large Language Models"
    url: https://arxiv.org/abs/2309.00071
    year: 2023
updated: 2026-08-21
review_by: 2027-02-01
---

## Simple Explanation

Context windows went from 2,000 tokens in 2020 to a million and beyond. The
number on the model card is real in the sense that the model will accept that
much input without erroring. It is not a promise that the model uses all of it
well, and the gap between the two is where most disappointment lives.

## Technical Definition

A model whose maximum sequence length reaches into the hundreds of thousands of
tokens, achieved by training at length, by extending rotary position frequencies
after the fact (position interpolation, NTK-aware scaling, YaRN) with brief
fine-tuning, or by attention variants that avoid the quadratic cost. *Effective*
context is measured empirically by retrieval and reasoning tasks at varying
depth, not asserted.

## Why Does It Exist?

Whole codebases, long documents, extended agent trajectories and multi-hour
transcripts do not fit in 8k tokens. Every one of those is a real workload that
was previously impossible without chunking and retrieval machinery.

## What Problem Does It Solve?

Working over material too large to summarise without loss, and keeping long agent
sessions coherent without aggressive compaction.

## How Does It Work?

The "lost in the middle" shape is robust across models and years: material at the
beginning and end is retrieved reliably, material in the middle far less so.

## Mental Model

Peripheral vision. The field is genuinely wide; acuity is not uniform across it,
and what falls in the periphery may as well not be there for fine detail.

## Example

The needle-in-a-haystack test — hide a sentence in a long document and ask for it —
is the standard demonstration, and models pass it while still failing harder
tasks at the same length. RULER-style benchmarks add multi-hop reasoning,
tracking multiple variables and aggregation, and effective context typically
comes out well below the advertised figure. Always test at *your* length with
*your* task shape.

## Real-World Usage

Whole-repository code understanding, long document analysis, and agent sessions
that would otherwise need compaction. The cost is severe: KV cache grows linearly
with length, so a single long-context request can consume the memory of many
short ones, and prefill grows quadratically in attention. Long context is
therefore a serving decision as much as a capability one.

## Common Confusions

* **Advertised vs effective context** — the first is an upper bound on what is
  representable; the second is what the model uses reliably. They differ, often
  by a lot.
* **Long context vs RAG** — long context is not a replacement. Retrieval selects
  what matters, filters by permission and provides citations; context holds what
  was selected. The strongest systems use both, and stuffing everything in is
  usually slower, dearer and less accurate.
* **Position matters** — put the important material at the beginning or the end,
  and put the question after the documents.

## Why Should I Care?

"We have a million-token window" is one of the most repeated and least
interrogated claims in AI marketing. Knowing how to test it — and what it costs
per request — is the difference between a design decision and a purchase made on
a headline number.

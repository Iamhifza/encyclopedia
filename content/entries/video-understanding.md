---
term: Video Understanding
aliases: [Video-Language Model, Temporal Understanding, Video QA]
category: multimodal
subcategory: vision-language
depth: full
status: emerging
difficulty: advanced
one_liner: "Reasoning over footage rather than stills, which multiplies the token cost and adds the problem of time."
origin:
  year: 2023
  circa: true
  attribution: Emerged as vision-language models were extended to temporal input; no single originating work
historical_period: agentic
tags: [architecture]
relations:
  is_a: [vision-language-model]
  related_to: [world-model, jepa, context-window, long-context-model]
prerequisites: [vision-language-model]
encountered_in: [research-papers, conferences, production-systems]
sources:
  - type: paper
    title: "Video-LLaMA: An Instruction-tuned Audio-Visual Language Model"
    url: https://arxiv.org/abs/2306.02858
    year: 2023
  - type: paper
    title: "Revisiting Feature Prediction for Learning Visual Representations from Video (V-JEPA)"
    url: https://arxiv.org/abs/2404.08471
    year: 2024
updated: 2026-08-21
review_by: 2027-02-01
---

## Simple Explanation

An image costs hundreds or thousands of tokens. A minute of video at 30 frames a
second is 1,800 images. Feed that in naively and a short clip exhausts the entire
context window before anyone asks a question.

So video understanding is mostly a problem of *what to throw away*, plus a second
problem images do not have: reasoning about time — order, causation, change.

## Technical Definition

Extending vision-language models to temporal input: sampling or selecting frames,
encoding them with a vision backbone, compressing the resulting tokens, and
conditioning a language model on the sequence. Temporal modelling ranges from
naive frame concatenation to spatiotemporal attention and learned token merging
across frames.

## Why Does It Exist?

An enormous share of recorded information is video — instruction, surveillance,
meetings, sport, media archives — and none of it was searchable in any meaningful
sense.

## What Problem Does It Solve?

Question answering, search, summarisation and event detection over footage, and
the perception layer for any agent that must understand a changing scene.

## How Does It Work?

```text
1 minute @ 30fps = 1,800 frames × ~600 tokens = over a million tokens
                            │  infeasible
                            ▼
   sample: 1 frame per second, or select keyframes on scene change
   compress: merge tokens across adjacent frames (they mostly repeat)
   encode: spatiotemporal attention over the reduced set
                            │
   ~1-2k tokens for the minute ──▶ language model
```

Adjacent frames are highly redundant, which is exactly what makes compression
work — and exactly what makes fast events easy to miss.

## Mental Model

Reading a flipbook by looking at every twentieth page. You follow the story and
you will miss anything that happened quickly.

## Example

The failure mode this creates is specific and worth knowing: sampled models
answer questions about *what is in* a video far better than questions about
*order and causation*. "Is there a dog?" is easy. "Did he pick up the cup before
or after she left?" requires temporal resolution that frame sampling may have
discarded. Benchmarks probing temporal reasoning consistently show weaker results
than object-level ones.

## Real-World Usage

Video search and summarisation, content moderation, sports and security
analytics, and instructional video question answering. In robotics and world-model
research, video is treated differently — as a source of physical intuition rather
than a document to be queried, which is the V-JEPA line of work.

## Common Confusions

* **Video understanding vs video generation** — interpreting footage versus
  producing it. Different problems, and the second does not imply the first.
* **More frames is not straightforwardly better** — context and cost grow
  linearly, and models attend unevenly across long inputs.
* **Audio is often ignored** — many "video" models process only visual frames,
  discarding speech that frequently contains the answer.

## Why Should I Care?

It is where multimodal AI meets its hardest scaling problem, and the gap between
recognising objects and reasoning about time is one of the clearest current
boundaries of what these models do.

---
term: Beam Search
aliases: [Beam Decoding]
category: llm-inference
subcategory: decoding
depth: full
status: historical
difficulty: intermediate
one_liner: "Keeping several candidate continuations alive at once and returning the best-scoring whole sequence, which helps in translation and hurts in chat."
tags: [inference]
relations:
  is_a: [sampling]
  related_to: [autoregressive-generation, speculative-decoding]
sources:
  - type: paper
    title: "Sequence to Sequence Learning with Neural Networks"
    url: https://arxiv.org/abs/1409.3215
    year: 2014
  - type: paper
    title: "The Curious Case of Neural Text Degeneration"
    url: https://arxiv.org/abs/1904.09751
    year: 2019
    note: The evidence that likelihood maximisation produces bland open-ended text.
updated: 2026-08-21
---

## Simple Explanation

Greedy decoding picks the single best next token and never reconsiders, which
can walk into a dead end: a high-scoring first word followed by a poor sentence.
Beam search hedges. It keeps the *k* best partial sequences alive, extends all of
them, and at the end returns whichever complete sequence scored best overall.

## Technical Definition

A breadth-limited search over the output space. At each step, every one of the
$k$ beams is extended by every vocabulary token, the resulting $k \times |V|$
candidates are scored by cumulative log-probability, and the top $k$ are kept.
Because raw log-probability favours short sequences, scores are usually
normalised by length.

## Why Does It Exist?

Because greedy decoding is locally optimal and globally poor. In machine
translation — where one correct output usually exists — searching a little wider
measurably improved BLEU, and beam search became the default decoding strategy of
the sequence-to-sequence era.

## What Problem Does It Solve?

Early commitment. A token that looks best at position three may make positions
four onward much worse, and beam search can recover from that where greedy
decoding cannot.

## How Does It Work?

```text
k = 3
step 1   "The"          "A"            "In"
           │              │              │
step 2   The cat       A dog         In the
         The dog       A cat         In a
         The man       A man         In this
           │ score all 9, keep the best 3
step 3   The cat sat · A dog ran · The man walked
           │
        continue until every beam emits end-of-sequence
        return the best complete sequence by length-normalised score
```

## Mental Model

Exploring a maze with three torches instead of one. Wider than greedy, nowhere
near exhaustive, and it costs three times as much light.

## Formula

$$\text{score}(y) = \frac{1}{|y|^{\alpha}} \sum_{t=1}^{|y|} \log p(y_t \mid y_{<t}, x)$$

* $y$ — a candidate output sequence.
* $|y|$ — its length in tokens.
* $\alpha$ — length penalty; without it (or at $\alpha = 0$) the search
  systematically prefers short outputs, because every added token multiplies in
  another probability below 1.
* $k$ — beam width. Larger is not reliably better: beyond modest widths, quality
  often *degrades*, a well-documented result known as the beam search curse.

## Example

Translating a sentence, beam search with $k = 4$ reliably beats greedy decoding.
Asking a chat model to brainstorm, the same setting produces flat, repetitive,
safely-worded text — because the most probable sequence in an open-ended task is
precisely the least interesting one. This is why chat interfaces sample rather
than search.

## Real-World Usage

Still standard in machine translation, speech recognition and any task with one
correct answer, and available in most inference libraries. Effectively absent
from LLM chat serving: it multiplies KV cache memory and compute by the beam
width while making output worse for open-ended generation.

## Historical Origin

Adapted from speech recognition search, and carried into neural sequence
modelling with the encoder-decoder architectures of 2014. It was the default
decoding method for years before nucleus sampling displaced it for open-ended
text.

## Common Confusions

* **Beam search is not sampling** — it is deterministic search for a
  high-probability sequence, not a draw from the distribution.
* **Wider beams are not better** — quality typically peaks at small $k$ and then
  falls, because the highest-likelihood sequences are degenerate.
* **Beam search vs speculative decoding** — both run several candidates, for
  opposite reasons: beam search searches for a better output, speculative
  decoding accelerates the same output.

## Why Should I Care?

It is the clearest demonstration of a fact that shapes all of decoding: the most
probable text is not the best text. Understanding why beam search failed for chat
is understanding why temperature and top-$p$ exist.

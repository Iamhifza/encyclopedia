---
term: Positional Encoding
aliases: [Position Embedding, Sinusoidal Encoding, ALiBi, Absolute Position]
category: transformers
subcategory: position
depth: full
status: established
difficulty: intermediate
one_liner: "How a model is told where each token sits, since attention on its own treats a sentence as an unordered bag."
tags: [architecture]
relations:
  part_of: [transformer]
  evolved_into: [rope]
  related_to: [context-window, self-attention, long-context-model]
prerequisites: [self-attention]
encountered_in: [research-papers, interviews, github]
sources:
  - type: paper
    title: "Attention Is All You Need"
    url: https://arxiv.org/abs/1706.03762
    year: 2017
  - type: paper
    title: "Train Short, Test Long: Attention with Linear Biases (ALiBi)"
    url: https://arxiv.org/abs/2108.12409
    year: 2021
  - type: paper
    title: "RoFormer: Enhanced Transformer with Rotary Position Embedding"
    url: https://arxiv.org/abs/2104.09864
    year: 2021
updated: 2026-08-21
---

## Simple Explanation

Attention compares every token with every other token and sums the results. Sums
do not care about order. Shuffle the words of a sentence and, without something
extra, a Transformer computes exactly the same thing.

Positional encoding is that something extra: information about where each token
sits, injected so that "dog bites man" and "man bites dog" are distinguishable.

## Technical Definition

Any mechanism supplying order information to a permutation-invariant attention
operation. Three families: **absolute** encodings added to token embeddings
(fixed sinusoids or learned tables), **relative** encodings that bias attention
by the distance between positions, and **rotary** encodings that rotate queries
and keys so their dot product depends only on relative offset.

## Why Does It Exist?

It is the price of removing recurrence. An RNN knows order because it processes
tokens in sequence; the Transformer processes them all at once, which is what
makes it fast and what removes the order information.

## What Problem Does It Solve?

Order awareness — and, in its modern forms, order awareness that extrapolates
beyond the sequence lengths seen during training.

## How Does It Work?

```text
ABSOLUTE (2017)             RELATIVE / ALiBi          ROTARY (RoPE)
token embedding             attention score           rotate q and k
      +                           −                   by an angle ∝ position
position vector             m·(distance penalty)            │
      │                           │                   dot product depends
added before layer 1        applied at every layer    only on (n − m)
```

The trend is clear: from adding a position vector at the input, to influencing
attention directly at every layer, because the second generalises much better.

## Mental Model

Numbering the pages of a manuscript before throwing them in the air. Attention
looks at all of them at once; the numbers are the only reason the order survives.

## Formula

The original sinusoidal scheme:

$$PE_{(pos, 2i)} = \sin\!\left(\frac{pos}{10000^{2i/d}}\right), \qquad PE_{(pos, 2i+1)} = \cos\!\left(\frac{pos}{10000^{2i/d}}\right)$$

* $pos$ — the token's position; $i$ — the dimension index.
* Different dimensions oscillate at different frequencies, so the vector encodes
  position at multiple scales at once — fast-changing dimensions for local order,
  slow ones for long-range position.
* Chosen rather than learned so that, in principle, unseen positions still
  produce sensible values.

## Example

Learned absolute embeddings — a lookup table with one vector per position — were
common early and have a fatal limitation: position 5000 has no entry if training
stopped at 4096, so the model simply cannot process longer input. That single
constraint is most of why the field moved to relative and rotary schemes, and why
context extension is now possible at all.

## Real-World Usage

RoPE dominates current models; ALiBi appears in some; learned absolute embeddings
are largely historical. In vision Transformers, 2D positional encodings serve the
same role for image patches.

## Common Confusions

* **Positional encoding vs token embedding** — where a token is versus what it
  is. Both are vectors; only one depends on the sequence.
* **Absolute vs relative** — "this is position 7" versus "this is 3 tokens
  before that". The second extrapolates; the first does not.
* **NoPE** — decoder-only models can learn some positional information from the
  causal mask alone, which is a genuinely surprising research finding rather than
  a practical technique.

## Why Should I Care?

It is the reason a Transformer can read a sentence at all, and the specific scheme
a model uses determines whether its context window can be extended later.

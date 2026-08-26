---
term: Self-Attention
aliases: [Intra-Attention, Scaled Dot-Product Self-Attention, MHA, Multi-Head Attention]
category: transformers
subcategory: attention
status: foundational
difficulty: intermediate
one_liner: Attention applied within a single sequence, so every token can look at every other token in the same text.
origin:
  year: 2017
  attribution: Vaswani et al., "Attention Is All You Need"
historical_period: transformer
diagram:
  kind: steps
  title: Every token scores every earlier token
  footer: Cost grows with the square of sequence length, which is why long context is expensive rather
    than merely large, and why so much engineering exists to avoid materialising this matrix.
  steps:
  - title: The causal mask makes the matrix triangular
    notes:
    - label: Rule
      text: position i may attend to 0…i and nothing after it, so training on a whole sequence predicts
        every position at once
    visual:
      kind: matrix
      cell_width: 66
      cols:
      - the
      - cat
      - sat
      - 'on'
      rows:
      - label: the
        values: [1.0, null, null, null]
      - label: cat
        values: [0.35, 0.65, null, null]
      - label: sat
        values: [0.15, 0.55, 0.3, null]
      - label: 'on'
        values: [0.1, 0.3, 0.35, 0.25]
      caption: each row sums to 1; the empty upper triangle is the future
  - title: Heads look for different things, then are concatenated
    visual:
      kind: columns
      width: 700
      columns:
      - title: head 1
        lines:
        - syntax
        - verb → its subject
      - title: head 2
        accent: true
        lines:
        - coreference
        - pronoun → its antecedent
      - title: head 3
        lines:
        - position
        - attends locally
      caption: concatenated, then passed through one output projection
tags: [architecture]
relations:
  is_a: [attention]
  part_of: [transformer]
  evolved_into: [grouped-query-attention]
  used_by: [kv-cache, flash-attention]
prerequisites: [attention]
encountered_in: [research-papers, interviews, github]
sources:
  - type: paper
    title: "Attention Is All You Need"
    url: https://arxiv.org/abs/1706.03762
    year: 2017
  - type: post
    title: "The Illustrated Transformer"
    url: https://jalammar.github.io/illustrated-transformer/
    year: 2018
videos:
  - title: "Attention in transformers, visually explained"
    channel: "3Blue1Brown"
    url: https://www.youtube.com/results?search_query=3blue1brown+attention+in+transformers
updated: 2026-08-21
---

## Simple Explanation

Every word in the sentence looks at every other word in the same sentence and
decides who is relevant to it. There is no separate source and target — the text
is attending to itself, which is where the name comes from.

## Technical Definition

Scaled dot-product attention where $Q$, $K$ and $V$ are all linear projections of
the same input sequence. In decoder-only models a causal mask sets scores to
$-\infty$ for future positions, preserving the autoregressive property.
*Multi-head* attention runs $h$ such computations in parallel over
lower-dimensional projections and concatenates the results.

## Why Does It Exist?

Once attention could route information between sequences, the natural question
was whether recurrence was needed at all *within* a sequence. It was not.
Self-attention gives a constant path length between any two positions and
parallelises across the whole sequence during training.

## What Problem Does It Solve?

Contextualisation. It turns a static per-token embedding into a
representation that depends on the surrounding text, so "bank" near "river"
differs from "bank" near "loan".

## How Does It Work?


Every position emits a query, a key and a value, all derived from the same
sequence — which is what makes it *self*-attention rather than attention over
some other input. Each query is scored against every key, the scores are scaled
and softmaxed into weights, and the output at that position is the weighted
blend of all the values.

In a decoder the scores are masked so that position *i* can see only positions
0 through *i*. That mask is what lets a single forward pass over a sequence
train every next-token prediction in it simultaneously, and it is why the
attention matrix is triangular.

Multiple heads run in parallel with separate projections, so different heads can
specialise — one tracking syntactic dependency, another resolving pronouns,
another attending locally. Their outputs are concatenated and passed through one
projection. The cost of all this is quadratic in sequence length, which is the
single fact that most of the inference-efficiency literature exists to work
around.

## Mental Model

A meeting where every participant simultaneously asks everyone else a question,
gets an answer weighted by how relevant each person is to them, and updates their
own notes. Multiple heads are several such meetings running at once with
different agendas.

## Formula

$$\text{MultiHead}(X) = \text{Concat}(\text{head}_1,\dots,\text{head}_h)W^O, \quad \text{head}_i = \text{Attention}(XW_i^Q, XW_i^K, XW_i^V)$$

* $X$ — the input sequence, one row per token.
* $W_i^Q, W_i^K, W_i^V$ — per-head projections, each of width $d_{model}/h$.
* $W^O$ — output projection mixing the heads back together.
* $h$ — number of heads; total compute is roughly unchanged versus one wide head.

## Example

With a causal mask, generating token 5 lets it attend to tokens 1-4 but not 6
onward. That single masking choice is what makes a decoder-only Transformer able
to be trained on all positions at once while still generating left to right.

## Real-World Usage

The core of every decoder-only LLM. In practice production models rarely use
plain multi-head attention any more: they use grouped-query attention to shrink
the KV cache, and compute it with a fused kernel such as FlashAttention.

## Common Confusions

* **Self-attention vs cross-attention** — cross-attention takes queries from one
  sequence and keys/values from another (used in encoder-decoder models and in
  many multimodal architectures).
* **Heads are not specialists by design** — any interpretation of a head is
  discovered after training, not assigned.
* **Masking is not optional** — remove the causal mask and the model can see the
  answer it is being trained to predict.

## Why Should I Care?

The KV cache exists precisely because self-attention needs every earlier key and
value again at every generation step. Cache size, context limits and most
inference cost follow directly from this one design choice.

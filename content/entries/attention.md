---
term: Attention
aliases: [Attention Mechanism, Soft Attention]
category: transformers
subcategory: attention
status: foundational
difficulty: intermediate
one_liner: A way for a model to look back at every earlier position and decide, for each one, how much it matters right now.
origin:
  year: 2014
  attribution: Bahdanau, Cho and Bengio, for neural machine translation
historical_period: statistical-ml
diagram:
  kind: steps
  title: One query, resolving "it"
  footer: High weight says where the model looked. It is not proof of why it answered — a distinction
    the interpretability literature keeps having to make.
  steps:
  - title: Score the query against every key
    notes:
    - label: Query
      text: from "it" — what do I need to resolve?
    - label: Scale
      text: divide by √d_k, or the softmax saturates and the gradient goes flat
    visual:
      kind: bars
      caption: q·kᵀ, before softmax
      bars:
      - label: the
        value: 0.12
        value_label: '0.3'
      - label: animal
        value: 1.0
        value_label: '2.4'
        accent: true
      - label: street
        value: 0.29
        value_label: '0.7'
      - label: because
        value: 0.17
        value_label: '0.4'
  - title: Softmax turns the scores into a distribution
    notes:
    - label: Property
      text: the row sums to 1, so attention allocates a fixed budget across positions
    visual:
      kind: matrix
      cols:
      - the
      - animal
      - street
      - because
      rows:
      - label: it →
        values:
        - 0.06
        - 0.62
        - 0.19
        - 0.13
      caption: attention weights for one query
  - title: The output is those weights spent on the values
    notes:
    - label: Result
      text: a blend dominated by the value at "animal" — which is what resolving the pronoun means
    visual:
      kind: segments
      label: output vector at "it"
      caption: every output is a mixture; attention only chooses the proportions
      segments:
      - text: V(the)
        value: 0.06
      - text: V(animal)
        value: 0.62
        tone: accent
        value_label: '0.62'
      - text: V(street)
        value: 0.19
        value_label: '0.19'
      - text: V(because)
        value: 0.13
        value_label: '0.13'
tags: [architecture]
relations:
  successor_of: [lstm]
  evolved_into: [self-attention]
  part_of: [transformer]
  used_by: [kv-cache]
  related_to: [information-retrieval]
prerequisites: [neural-network]
encountered_in: [research-papers, interviews, conferences]
sources:
  - type: paper
    title: "Neural Machine Translation by Jointly Learning to Align and Translate"
    url: https://arxiv.org/abs/1409.0473
    year: 2014
  - type: paper
    title: "Attention Is All You Need"
    url: https://arxiv.org/abs/1706.03762
    year: 2017
videos:
  - title: "Attention in transformers, visually explained"
    channel: "3Blue1Brown"
    url: https://www.youtube.com/results?search_query=3blue1brown+attention+in+transformers+visually+explained
updated: 2026-08-21
---

## Simple Explanation

Instead of squeezing everything read so far into one fixed summary, keep it all
and, at each step, ask: which of these earlier pieces should I be looking at?
The model computes a relevance score for every previous position and blends them
in proportion to those scores.

## Technical Definition

A differentiable soft lookup. Each position emits a *query*; every position also
emits a *key* and a *value*. The output at a position is the value-weighted
average where weights are a softmax over query-key similarities, scaled by
$\sqrt{d_k}$ to keep the softmax out of its saturated regime.

## Why Does It Exist?

In 2014 encoder-decoder translation compressed an entire source sentence into
one vector. Translation quality fell off sharply as sentences got longer, since
that vector was a hard bottleneck. Attention removed the bottleneck by letting
the decoder read the whole source at every output step.

## What Problem Does It Solve?

Long-range dependency with no fixed-size memory bottleneck, and — unlike
recurrence — a constant number of sequential steps between any two positions,
which makes training parallelisable.

## How Does It Work?

1. Project each token into query, key and value vectors.
2. Score every query against every key by dot product.
3. Scale by $\sqrt{d_k}$, mask out positions that must not be seen, softmax.
4. Take the weighted sum of the values.

## Mental Model

A database lookup where instead of retrieving one exact match you retrieve a
weighted blend of everything, with the weights learned. This is why the
retrieval vocabulary — query, key, value — is not a coincidence.

## Formula

$$\text{Attention}(Q,K,V) = \operatorname{softmax}\!\left(\frac{QK^\top}{\sqrt{d_k}}\right)V$$

* $Q$ — queries, one row per position asking "what do I need?".
* $K$ — keys, one row per position advertising "what I contain".
* $V$ — values, the content actually mixed into the output.
* $d_k$ — key dimension; dividing by $\sqrt{d_k}$ keeps dot products from
  growing with dimension and flattening the softmax gradient.

## Example

In "the animal did not cross the street because **it** was too tired", resolving
*it* requires linking back to *animal*. The query from *it* scores high against
the key at *animal*, so the value at *animal* dominates the blend. Trained
models really do show this pattern, which is one of the earliest interpretability
results on Transformers.

## Real-World Usage

Every Transformer layer. Its cost profile drives the entire inference stack:
quadratic scaling in sequence length motivated FlashAttention, the growth of
stored keys and values motivated the KV cache, and the memory cost of that cache
motivated PagedAttention.

## Historical Origin

Bahdanau et al., 2014, as an addition to a recurrent translation model. Vaswani
et al., 2017, removed the recurrence entirely and kept attention.

## Common Confusions

* **Attention vs self-attention** — self-attention is the case where queries,
  keys and values all come from the same sequence.
* **Attention weights vs explanation** — high attention weight is not proof of
  causal reliance, a point the interpretability literature has made repeatedly.
* **Quadratic in length** — cost grows with the square of sequence length, which
  is why context windows are expensive rather than merely large.

## Why Should I Care?

Nearly every capability and every cost of modern language models traces back to
this operation. Understanding it is the difference between using an LLM and
reasoning about one.

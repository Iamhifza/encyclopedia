---
term: Word2Vec
aliases: [Skip-gram, CBOW, Word Embeddings]
category: history
subcategory: statistical
status: historical
difficulty: intermediate
one_liner: The 2013 method that turned words into coordinates, where words used in similar contexts land near each other.
origin:
  year: 2013
  attribution: Tomas Mikolov and colleagues at Google
historical_period: statistical-ml
tags: [retrieval, history]
relations:
  evolved_into: [embedding]
  related_to: [dense-retrieval, self-supervised-learning]
encountered_in: [research-papers, interviews, technical-blogs]
sources:
  - type: paper
    title: "Efficient Estimation of Word Representations in Vector Space"
    url: https://arxiv.org/abs/1301.3781
    year: 2013
  - type: paper
    title: "Distributed Representations of Words and Phrases and their Compositionality"
    url: https://arxiv.org/abs/1310.4546
    year: 2013
updated: 2026-08-21
---

## Simple Explanation

Take a huge amount of text and, for every word, try to predict the words around
it. Do that a few billion times and each word ends up with a list of numbers
that captures how it is used. Words used in similar situations end up with
similar numbers.

## Technical Definition

A shallow model learning dense word vectors by one of two objectives:
skip-gram (predict context words from a centre word) or CBOW (predict the centre
word from its context), trained efficiently with negative sampling or
hierarchical softmax rather than a full softmax over the vocabulary.

## Why Does It Exist?

Before it, words were one-hot vectors: 50,000 dimensions, all zeros except one.
Under that representation "cat" and "kitten" are exactly as unrelated as "cat"
and "bureaucracy". Every model had to learn word similarity from scratch, for
every task.

## What Problem Does It Solve?

It gives every downstream system a reusable notion of word similarity learned
once from unlabelled text.

## How Does It Work?

```text
"the quick brown fox jumps over the lazy dog"
                 ▲
            centre word

skip-gram: from "fox", predict {brown, jumps}
           push vec(fox) toward vec(brown), vec(jumps)
           push vec(fox) away from random words

after millions of updates:
    vec(fox) ≈ vec(wolf) ≈ vec(coyote)
```

## Mental Model

Seating a party by conversation topic. Nobody is told the topics; people who
keep appearing in the same conversations end up at the same table.

## Formula

Skip-gram with negative sampling maximises:

$$\log \sigma(\mathbf{v}_c^\top \mathbf{v}_w) + \sum_{i=1}^{k} \mathbb{E}_{n \sim P_n} \left[ \log \sigma(-\mathbf{v}_{n}^\top \mathbf{v}_w) \right]$$

* $\mathbf{v}_w$ — vector of the centre word.
* $\mathbf{v}_c$ — vector of a word that genuinely appeared nearby.
* $\mathbf{v}_n$ — vector of $k$ randomly sampled words that did not.
* $\sigma$ — sigmoid, squashing scores into (0, 1).

The first term pulls real neighbours together; the second pushes random words
apart, which is what stops every vector collapsing to the same point.

## Example

The famous result: `vec("king") − vec("man") + vec("woman")` lands nearest to
`vec("queen")`. Gender, tense and plurality turned out to be roughly linear
directions in the space — the first widely visible evidence that useful
structure emerges from unlabelled text alone.

## Real-World Usage

Rarely trained fresh today, since contextual embeddings from Transformers are
strictly better. Its descendants are everywhere: every embedding model, every
vector database, every recommendation system that embeds items rather than words.

## Historical Origin

Mikolov et al., Google, 2013. GloVe followed in 2014 with a count-based
alternative; fastText added subword units in 2016.

## Evolution

The limitation is one vector per word. "Bank" gets a single point somewhere
between the river and the money. ELMo (2018) and BERT (2018) made the vector
depend on the sentence, which is the direct ancestor of the contextual
embeddings used today.

## Common Confusions

* **Word2Vec vs modern embeddings** — Word2Vec is static, one vector per word
  type. Modern embedding models are contextual and usually encode whole
  passages.
* **Word2Vec vs an LLM's embedding layer** — the input embedding table inside an
  LLM is superficially similar but learned as part of the whole model, and
  immediately contextualised by the layers above it.

## Why Should I Care?

It is the moment "meaning as geometry" became practical, and that assumption
underpins retrieval, clustering, deduplication and every similarity search in
production today.

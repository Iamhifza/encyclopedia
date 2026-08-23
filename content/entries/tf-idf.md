---
term: TF-IDF
aliases: [Term Frequency-Inverse Document Frequency, Vector Space Model, Sparse Vector]
category: history
subcategory: statistical
depth: full
status: historical
difficulty: beginner
one_liner: "Weighting a word by how often it appears here and how rare it is everywhere — the idea that made text searchable."
origin:
  year: 1972
  attribution: Karen Spärck Jones introduced inverse document frequency; Salton's SMART system built the vector space model around it
historical_period: early-computing
tags: [retrieval, history]
relations:
  part_of: [information-retrieval]
  evolved_into: [bm25, embedding]
  related_to: [dense-retrieval, word2vec]
prerequisites: [information-retrieval]
encountered_in: [interviews, research-papers, technical-blogs]
sources:
  - type: paper
    title: "A Statistical Interpretation of Term Specificity and its Application in Retrieval"
    url: https://www.emerald.com/insight/content/doi/10.1108/eb026526/full/html
    year: 1972
  - type: book
    title: "Introduction to Information Retrieval, ch. 6"
    url: https://nlp.stanford.edu/IR-book/
    year: 2008
updated: 2026-08-21
---

## Simple Explanation

Two questions about every word in a document. How often does it appear *here*?
And how unusual is it *in general*? Multiply the answers.

"The" appears constantly everywhere, so its weight collapses to nothing.
"Fragmentation" appearing three times in one document out of a million is a
strong signal about what that document is about. That is the entire idea, and
almost everything in retrieval descends from it.

## Technical Definition

A term weighting scheme assigning weight $\text{tf}(t,d) \times \text{idf}(t)$,
where term frequency measures occurrences within a document and inverse document
frequency is the log of the ratio of total documents to documents containing the
term. Documents become sparse vectors over the vocabulary, and similarity is
measured by cosine — the vector space model.

## Why Does It Exist?

Because raw term counts rank badly. Every document contains "the" many times, so
counting alone ranks by length and grammar rather than by subject. Spärck Jones's
insight was that a term's *specificity* — its rarity — is what carries information.

## What Problem Does It Solve?

Turning documents into comparable numeric objects, which made ranked retrieval
possible at all.

## Formula

$$w_{t,d} = \text{tf}(t,d) \times \log\frac{N}{\text{df}(t)}$$

* $\text{tf}(t,d)$ — occurrences of term $t$ in document $d$.
* $N$ — total documents in the collection.
* $\text{df}(t)$ — documents containing $t$.
* The logarithm dampens the ratio: a term in 1 document out of a million is more
  informative than one in 1,000, but not a thousand times more.

## How Does It Work?

```text
"the"            appears in 100% of documents → idf ≈ 0     → weight ≈ 0
"cache"          appears in 5%                → idf moderate
"fragmentation"  appears in 0.1%              → idf high    → weight high

document ──▶ sparse vector over the vocabulary
             [0, 0, 3.2, 0, 0, 0, 1.7, 0, ... ]
                       mostly zeros — one dimension per vocabulary term
```

## Mental Model

An index that knows which words are worth indexing. Common words are furniture;
rare words are addresses.

## Example

The lineage running from here is the spine of the retrieval domain:

```text
TF-IDF (1972) ──▶ BM25 (1994) ──▶ dense retrieval (2020) ──▶ hybrid ──▶ RAG
   sparse,           saturation      dense, learned,        both,      plus a
   exact terms       and length      handles paraphrase     fused      model
```

Each step fixed a specific defect in the last. BM25 added saturation and length
normalisation; dense retrieval added meaning; hybrid retrieval put the sparse
half back because it had never stopped being useful.

## Real-World Usage

Rarely used directly for ranking now — BM25 superseded it — but it remains
standard for quick text featurisation in classical machine learning, keyword
extraction, and as the first thing anyone reaches for when they need document
vectors without a GPU. It is also the clearest teaching example of sparse
representations.

## Common Confusions

* **TF-IDF vs BM25** — same intuition, better mechanics. BM25 is what to deploy.
* **TF-IDF vectors vs embeddings** — sparse and interpretable, one dimension per
  word, no notion of synonymy; versus dense and learned, where similarity is
  semantic. Word2Vec is the bridge between them.
* **IDF is a property of the collection** — the same word carries different weight
  in different corpora, which is why it adapts to a domain without training.

## Why Should I Care?

It is where the idea of representing text as vectors began, and the intuition it
encodes — informativeness is rarity — is the same one behind cross-entropy loss,
attention weights and every ranking system you will meet.

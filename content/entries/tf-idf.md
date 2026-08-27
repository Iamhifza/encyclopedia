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
diagram:
  kind: steps
  title: Weight a word by how little it is shared
  footer: Superseded by BM25, which adds saturation and length normalisation, and by dense vectors, which
    capture meaning. Still the clearest statement of the idea both of them build on.
  steps:
  - title: Common words are worth nothing
    visual:
      kind: table
      width: 720
      head:
      - term
      - appears in
      - weight
      rows:
      - - '"the"'
        - 100% of documents
        - ≈ 0 — carries no signal
      - - '"cache"'
        - 5%
        - moderate
      - - text: '"fragmentation"'
          new: true
        - text: 0.1%
          new: true
        - text: high — nearly diagnostic
          new: true
  - title: A document becomes a very sparse vector
    notes:
    - label: Shape
      text: one dimension per vocabulary term, so tens of thousands of them, nearly all zero
    visual:
      kind: matrix
      cell_width: 52
      show_values: false
      cols:
      - ''
      - ''
      - ''
      - ''
      - ''
      - ''
      - ''
      - ''
      - ''
      - ''
      - ''
      - ''
      rows:
      - label: doc
        values: [null, null, 0.8, null, null, null, 0.45, null, null, null, 0.6, null]
      caption: 'sparsity is the point: an inverted index only ever visits the terms a query actually contains'
diagrams:
- kind: figure
  section: Example
  title: Where this sits in the line
  visual:
    kind: lineage
    per_row: 4
    caption: each one kept what the last got right — rarity is still in all of them
    milestones:
    - text: TF-IDF
      note: 1972 · sparse, exact
      tone: accent
    - text: BM25
      note: 1994 · saturation
    - text: dense retrieval
      note: 2020 · paraphrase
    - text: hybrid, then RAG
      note: both, plus a model
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

Give every term a weight that is high when the term is frequent in this document
and rare across the corpus. Frequency says the document is about the term;
rarity says the term distinguishes it from everything else. Multiply the two and
words like "the" collapse to nearly zero however often they occur.

A document then becomes a vector with one dimension per vocabulary term, almost
all of them zero. That sparsity is what makes it fast: an inverted index maps
each term to the documents containing it, so a query only ever visits the handful
of terms it actually mentions rather than scanning the corpus.

Its limits are exactly what it never claimed to handle. It has no notion that
*car* and *automobile* are related, or that word order matters. BM25 improved the
weighting; dense retrieval replaced the representation. Both are still built on
the observation this made first, that rarity is what carries information.

## Mental Model

An index that knows which words are worth indexing. Common words are furniture;
rare words are addresses.

## Example

The lineage running from here is the spine of the retrieval domain:

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

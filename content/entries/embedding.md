---
term: Embedding
aliases: [Vector Representation, Dense Vector, Text Embedding, Embeddings, Latent Vector]
category: llms-foundation-models
subcategory: representation
depth: full
status: foundational
difficulty: beginner
one_liner: A list of numbers representing a piece of text, image or item, arranged so that similar things sit close together.
origin:
  year: 2013
  circa: true
  attribution: Popularised by Word2Vec; the idea of distributional representation is far older
historical_period: statistical-ml
diagram:
  kind: steps
  title: Text in, position out
  footer: A vector is only as good as the training objective that placed it. Swap the encoder and every
    stored vector becomes meaningless — embeddings are not portable between models.
  steps:
  - title: The encoder maps text to a fixed-length vector
    notes:
    - label: Fixed
      text: same width whatever the input length — here d ≈ 1024
    visual:
      kind: mapping
      head:
      - text
      - vector
      rows:
      - left: '"how do I cancel my plan"'
        right: '[ 0.02, -0.41, …, 0.17 ]'
      - left: '"ending your subscription"'
        right: '[ 0.04, -0.38, …, 0.15 ]'
      caption: different words, neighbouring coordinates
  - title: Meaning becomes distance
    notes:
    - label: Measure
      text: cosine similarity — the angle between vectors, not their length
    visual:
      kind: scatter
      height: 200
      caption: two of roughly a thousand dimensions
      groups:
      - label: billing
        tone: accent
        points:
        - - 0.22
          - 0.72
        - - 0.28
          - 0.66
        - - 0.19
          - 0.61
        - - 0.31
          - 0.75
      - label: shipping
        points:
        - - 0.72
          - 0.68
        - - 0.79
          - 0.74
        - - 0.75
          - 0.6
      - label: password reset
        points:
        - - 0.52
          - 0.18
        - - 0.58
          - 0.24
        - - 0.46
          - 0.22
      links:
      - from:
        - 0.22
        - 0.72
        to:
        - 0.28
        - 0.66
        text: cos 0.91
        dx: 34
        dy: 4
        anchor: start
  - title: Contrastive training is what stops the collapse
    notes:
    - label: Without the push
      text: every vector converges to one point and similarity becomes 1.0 everywhere
    visual:
      kind: columns
      columns:
      - title: pull together
        accent: true
        lines:
        - a question
        - and its correct answer
        - → minimise the angle
      - title: push apart
        lines:
        - that same question
        - and a random passage
        - → maximise the angle
      caption: the second column is the half that does the real work
tags: [architecture, retrieval]
relations:
  successor_of: [word2vec, tf-idf]
  used_by: [dense-retrieval, vector-database, rag, cross-attention, vision-language-model]
  depends_on: [neural-network, linear-algebra]
  related_to: [tokenization, unsupervised-learning, autoencoder]
prerequisites: [neural-network]
encountered_in: [production-systems, github, interviews, documentation]
sources:
  - type: paper
    title: "Efficient Estimation of Word Representations in Vector Space (Word2Vec)"
    url: https://arxiv.org/abs/1301.3781
    year: 2013
  - type: paper
    title: "Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks"
    url: https://arxiv.org/abs/1908.10084
    year: 2019
  - type: paper
    title: "Text and Code Embeddings by Contrastive Pre-Training"
    url: https://arxiv.org/abs/2201.10005
    year: 2022
  - type: paper
    title: "Matryoshka Representation Learning"
    url: https://arxiv.org/abs/2205.13147
    year: 2022
    note: Embeddings that can be truncated to smaller dimensions without retraining.
videos:
  - title: "Word Embedding and Word2Vec, clearly explained"
    channel: "StatQuest"
    url: https://www.youtube.com/results?search_query=statquest+word+embedding+and+word2vec+clearly+explained
updated: 2026-08-22
---

## Simple Explanation

Turn a sentence into a few hundred numbers, in a way that puts sentences with
similar meaning near each other. Now "how do I cancel" and "I want to end my
subscription" are neighbours despite sharing almost no words, and similarity
becomes arithmetic you can compute a million times a second.

That is the idea that made semantic search, retrieval and most recommendation
possible — and it is the same trick, applied to different things, everywhere
across this encyclopedia.

## Technical Definition

A mapping from a discrete or unstructured object to a dense vector in
$\mathbb{R}^d$, learned so that a distance or similarity function in that space
corresponds to semantic relatedness. Modern text embedding models are
[Transformers](transformer.md) trained contrastively: matching pairs pulled
together, mismatched pairs pushed apart.

## Why Does It Exist?

Computers compare numbers, not meaning. Before embeddings, text was compared by
shared words — [TF-IDF](tf-idf.md) and [BM25](bm25.md) — which cannot see that
"physician" and "doctor" are the same thing. An embedding is the bridge that
makes meaning comparable.

## What Problem Does It Solve?

Finding relevant things when query and target share no vocabulary, and giving
every downstream system a reusable notion of similarity.

## How Does It Work?


An encoder maps a piece of text to a fixed-length vector, the same width whatever
the input length. Similarity of meaning becomes proximity in that space, measured
by the cosine of the angle between two vectors, so retrieval reduces to a nearest
-neighbour search rather than a keyword match.

The geometry is produced by contrastive training: pull a question and its correct
answer together, push that same question and an unrelated passage apart. The
second half is what does the real work — without it, the cheapest way to satisfy
the objective is to collapse every vector onto one point, where all similarities
are 1.0 and nothing is retrievable.

Vectors are meaningful only relative to the encoder that produced them. Change
the model and every stored vector becomes noise, which makes re-embedding the
whole corpus the real cost of upgrading a retrieval system.

## Mental Model

A map where the coordinates are meaning. Things that are alike end up in the same
region, and "how far apart" becomes a question with a numeric answer.

## Formula

$$\text{sim}(\mathbf{a}, \mathbf{b}) = \frac{\mathbf{a} \cdot \mathbf{b}}{\lVert \mathbf{a} \rVert \lVert \mathbf{b} \rVert}$$

Cosine similarity measures the angle between vectors, ignoring magnitude — which
is why embeddings are usually normalised before storage, after which cosine
similarity and dot product are the same computation.

## Example

Embed 100,000 support articles once, store the vectors in a
[vector database](vector-database.md), then embed each incoming question and
retrieve its nearest neighbours. That is the retrieval half of almost every
[RAG](rag.md) system in production.

The practical decisions are less glamorous than the concept:

* **Dimensionality** — 384 to 3072 is typical. Larger is usually slightly better
  and proportionally more expensive to store and search. Matryoshka-trained
  models can be truncated, letting you trade quality for cost after the fact.
* **What you embed** — [chunking](chunking.md) decides this, and it matters more
  than the model choice.
* **Domain fit** — a general model can perform poorly on legal, medical or code
  corpora. This is measurable on your own data and rarely measured.

## Real-World Usage

Semantic search, RAG, clustering, deduplication, recommendation, anomaly
detection, and classification by nearest neighbour over labelled examples.

The word also appears in three other places, which causes constant confusion. The
**input embedding table** inside an LLM maps token ids to vectors. **Image
patch embeddings** do the same for [vision models](vision-language-model.md). And
the **latent** in an [autoencoder](autoencoder.md) or
[diffusion model](diffusion-model.md) is an embedding by another name. Same
mathematical object, different training objective — and that difference is why
they are not interchangeable.

## Common Confusions

* **Embedding model vs LLM** — different models, different objectives. An LLM's
  internal representations are not directly usable as good text embeddings, and
  using one as the other is a common mistake.
* **Embeddings are model-specific** — vectors from two models are not comparable.
  Changing embedding model means re-embedding the entire corpus, which is the
  main operational cost of choosing badly.
* **Similar is not relevant** — cosine similarity finds topical resemblance, not
  answers. This is precisely why [reranking](reranking.md) exists.
* **Sparse vs dense** — TF-IDF vectors are sparse and interpretable, one
  dimension per word; embeddings are dense and learned, with no dimension meaning
  anything on its own. [Hybrid retrieval](hybrid-retrieval.md) uses both because
  each catches what the other misses.

## Why Should I Care?

Every retrieval system's quality ceiling is set by its embedding model, and
choosing one is a measurable decision rather than a matter of taste. More
broadly, "meaning as geometry" is the assumption underneath a large fraction of
applied AI — and knowing where that assumption breaks is what stops you trusting
a similarity score it cannot support.

---
term: Unsupervised Learning
aliases: [Clustering, Dimensionality Reduction, k-means, PCA]
category: machine-learning
subcategory: paradigms
depth: full
status: foundational
difficulty: beginner
one_liner: "Finding structure in data that has no labels at all, such as grouping similar items together."
tags: [training]
relations:
  alternative_to: [supervised-learning]
  related_to: [embedding, self-supervised-learning, autoencoder, vector-database]
prerequisites: [probability]
encountered_in: [interviews, research-papers, production-systems]
sources:
  - type: book
    title: "The Elements of Statistical Learning, ch. 14"
    url: https://hastie.su.domains/ElemStatLearn/
    year: 2009
  - type: paper
    title: "Visualizing Data using t-SNE"
    url: https://www.jmlr.org/papers/v9/vandermaaten08a.html
    year: 2008
updated: 2026-08-21
---

## Simple Explanation

No labels, no right answers, no target to predict. Just data, and the question:
what structure is in here? Which of these customers resemble each other? What are
the natural groupings? Can this be described in fewer dimensions without losing
much?

It is the oldest branch of machine learning and the one that quietly does most of
the unglamorous work.

## Technical Definition

Learning structure from unlabelled data. Main families: **clustering** (k-means,
hierarchical, DBSCAN) partitions data into groups; **dimensionality reduction**
(PCA, t-SNE, UMAP) finds a lower-dimensional representation preserving some
notion of structure; **density estimation** models the distribution the data was
drawn from.

## Why Does It Exist?

Labels are expensive and often unavailable — and sometimes the question genuinely
has no label. Nobody knows in advance what the natural customer segments are;
that is what you are trying to find out.

## What Problem Does It Solve?

Exploration and organisation of data nobody has annotated, which is most data.

## How Does It Work?

```text
CLUSTERING (k-means)              DIMENSIONALITY REDUCTION (PCA)
  ● ●     ○ ○                       find the directions of
 ● ● ●   ○ ○ ○                      greatest variance, keep
  ● ●     ○ ○                       the top few, discard the rest
     ▲       ▲
   centroids move to the mean       1000 dimensions → 50, with
   of their assigned points,        most of the variation retained
   repeat until stable
```

## Mental Model

Sorting a drawer of unlabelled photographs into piles. Nobody told you the
categories; the piles are what you discovered.

## Example

There is a common trap here. Clustering always produces clusters — k-means with
$k=5$ returns five groups whether or not the data has any group structure at all.
Validating that the clusters mean something (silhouette scores, stability across
subsamples, human inspection) is the real work, and it is frequently skipped.

## Real-World Usage

Customer segmentation, anomaly detection, topic discovery, deduplication, and
visualisation of embedding spaces with t-SNE or UMAP. In the LLM stack it appears
constantly downstream of embeddings: clustering retrieved passages, grouping
similar support tickets, and detecting near-duplicate documents during data
curation.

## Common Confusions

* **Unsupervised vs self-supervised** — the crucial modern distinction.
  Self-supervised learning manufactures labels from the data (predict the hidden
  word) and has an explicit prediction target and loss. Classical unsupervised
  learning has neither. LLM pretraining is self-supervised, not unsupervised,
  though the two are often conflated.
* **Clusters are not categories** — they reflect the distance metric you chose,
  which encodes assumptions.
* **t-SNE and UMAP plots mislead** — distances between clusters in those pictures
  are not meaningful, and the layout changes with hyperparameters.

## Why Should I Care?

It is the toolkit for the moment before you have labels, it underpins most
practical work with embeddings, and knowing why it is *not* the same as
self-supervised learning clarifies what pretraining actually does.

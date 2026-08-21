---
term: Vector Database
aliases: [Vector Store, Vector Index, ANN Index]
category: rag-knowledge
subcategory: infrastructure
status: modern
difficulty: intermediate
one_liner: A store built to hold millions of embeddings and find the nearest ones to a query vector in milliseconds.
origin:
  year: 2017
  circa: true
  attribution: FAISS (Meta) popularised large-scale ANN search; dedicated products followed from 2019
historical_period: foundation-model
tags: [retrieval]
relations:
  depends_on: [embedding]
  used_by: [rag, dense-retrieval, agent-memory]
  related_to: [information-retrieval]
prerequisites: [embedding, dense-retrieval]
encountered_in: [production-systems, github, job-descriptions]
sources:
  - type: paper
    title: "Efficient and Robust Approximate Nearest Neighbor Search Using HNSW Graphs"
    url: https://arxiv.org/abs/1603.09320
    year: 2016
  - type: repo
    title: "FAISS"
    url: https://github.com/facebookresearch/faiss
updated: 2026-08-21
---

## Simple Explanation

A normal database finds rows matching a value. A vector database finds the items
whose embeddings point in most nearly the same direction as your query — and does
it without comparing against every stored vector, because at ten million vectors
that would be far too slow.

## Technical Definition

A system for storing high-dimensional vectors with an approximate nearest
neighbour index (commonly HNSW graphs or IVF with product quantisation),
supporting metadata filtering, upserts and deletes, and increasingly hybrid
scoring that fuses dense similarity with BM25.

## Why Does It Exist?

Brute-force similarity search is $O(n)$ per query in high dimensions and does not
survive contact with production traffic. Specialised indexes make it
approximately logarithmic, at a controllable cost in recall.

## What Problem Does It Solve?

Low-latency semantic search over large corpora, with filtering by tenant,
permission, recency or source.

## How Does It Work?

```text
HNSW: a layered proximity graph
  top layer    ●────────────●          few nodes, long hops
  middle       ●───●────●───●          
  bottom       ●─●─●─●─●─●─●─●         all nodes, short hops
search: start at the top, greedily descend toward the query vector
```

## Mental Model

A road network with motorways and side streets. You cover distance quickly on the
motorway, then drop to local roads for the final approach.

## Example

Ten million passages, 1024 dimensions: brute force means ten billion multiply-adds
per query. HNSW answers in a few milliseconds by visiting a few thousand nodes,
typically at 95-99% recall.

## Real-World Usage

Dedicated systems (Pinecone, Weaviate, Qdrant, Milvus, Chroma), libraries (FAISS,
hnswlib) and vector support inside existing databases (pgvector, Elasticsearch,
MongoDB, ClickHouse). For most applications, the extension to a database already
in use is the pragmatic choice.

## Common Confusions

* **Vector database vs embedding model** — the store versus the thing that
  produces what is stored. Quality comes from the model; latency from the store.
* **You may not need one** — under roughly a hundred thousand vectors, an
  in-process index or a Postgres extension is usually simpler and fast enough.
* **Filtering is the hard part** — combining ANN search with strict metadata
  filters is where implementations differ most, and where permission bugs live.

## Why Should I Care?

It is the storage layer of RAG and of most agent long-term memory, and choosing
it badly shows up as either slow queries or silently missing results.

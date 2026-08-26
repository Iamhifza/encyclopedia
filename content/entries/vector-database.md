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
diagram:
  kind: figure
  title: Skip most of the data, on purpose
  footer: Approximate is the point. Exact nearest-neighbour search over millions of vectors is linear
    in the corpus; HNSW trades a small recall loss for logarithmic search, and recall is a dial you set.
  visual:
    kind: stack
    width: 720
    caption: search starts at the top and greedily descends toward the query vector
    layers:
    - label: top
      text: a few nodes, very long hops
      note: cross the space fast
    - label: middle
      text: more nodes, shorter hops
      note: narrow the region
    - label: bottom
      text: every node, short hops
      accent: true
      note: find the actual neighbours
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
videos:
  - title: "What is a Vector Database?"
    channel: "IBM Technology"
    url: https://www.youtube.com/results?search_query=ibm+technology+what+is+a+vector+database
updated: 2026-08-21
review_by: 2027-02-01
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


Exact nearest-neighbour search compares the query against every stored vector,
which is linear in the corpus and hopeless at millions of documents. So these
systems approximate, and the dominant structure is HNSW: a hierarchy of
proximity graphs where the top layer holds a few nodes connected by very long
edges and each layer down is denser with shorter ones.

A search enters at the top, greedily walks toward the query, drops a layer when
it can get no closer, and repeats. The long edges cross the space in a few hops;
the short ones resolve the neighbourhood. Search becomes logarithmic rather than
linear in the number of vectors.

Recall is a dial, not a guarantee — parameters trade accuracy against speed and
memory, and a system tuned for latency will sometimes miss a true nearest
neighbour. Which is fine for retrieval and not fine for anything requiring
exactness, a distinction worth being explicit about before choosing one.

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

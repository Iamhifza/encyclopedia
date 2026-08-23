---
term: Knowledge Graph
aliases: [Ontology, Triple Store, Semantic Network, RDF]
category: rag-knowledge
subcategory: structure
depth: full
status: established
difficulty: intermediate
one_liner: "Facts stored as entities joined by named relationships, so questions can be answered by traversing rather than reading."
historical_period: classical-ai
tags: [retrieval, symbolic]
relations:
  successor_of: [symbolic-ai]
  used_by: [graphrag]
  related_to: [information-retrieval, embedding, rag]
prerequisites: [information-retrieval]
encountered_in: [production-systems, research-papers, job-descriptions]
sources:
  - type: spec
    title: "W3C RDF 1.1 Concepts and Abstract Syntax"
    url: https://www.w3.org/TR/rdf11-concepts/
  - type: paper
    title: "Knowledge Graphs (Hogan et al., survey)"
    url: https://arxiv.org/abs/2003.02320
    year: 2020
updated: 2026-08-21
---

## Simple Explanation

Instead of storing "Ada Lovelace worked with Charles Babbage on the Analytical
Engine" as a sentence, store it as connections: *Lovelace → collaborated-with →
Babbage*, *Babbage → designed → Analytical Engine*. Now a question like "who
worked on early computing machines?" is answered by following edges, not by
hoping the right sentence turns up in a search.

## Technical Definition

A directed labelled graph of entities (nodes) and typed relationships (edges),
usually with a schema or ontology constraining what may connect to what. Stored
as triples — subject, predicate, object — and queried with a graph language such
as SPARQL or Cypher.

## Why Does It Exist?

Text search finds documents; it does not compose facts. Questions requiring
several linked hops, or aggregation over relationships, are natural in a graph
and awkward in an index.

## What Problem Does It Solve?

Multi-hop questions, precise relationship queries, and explicit provenance for a
fact — properties that neither keyword search nor embeddings provide.

## How Does It Work?

```text
(Lovelace) ──collaborated-with──▶ (Babbage)
     │                                 │
   wrote                            designed
     ▼                                 ▼
(Notes on the Engine) ──about──▶ (Analytical Engine)

query: who wrote about machines Babbage designed?
   → traverse designed, then about, then wrote
```

The strength and the weakness are the same thing: the relationships must be
declared. Nothing is inferred that was not entered or derived by a rule.

## Mental Model

A map of relationships rather than a pile of documents. A search index tells you
which pages mention two cities; a graph tells you the road between them.

## Example

Building one from unstructured text is now usually done with an LLM: extract
entities and relationships from each document, resolve duplicates
("IBM"/"International Business Machines"), and write the triples. That extraction
step is exactly where errors enter, and a wrong edge is worse than a missing one
because traversal treats it as fact.

## Real-World Usage

Search engine entity panels, product catalogues, fraud and compliance
investigation, drug discovery, and enterprise data integration. In the LLM stack
they underpin GraphRAG, where retrieval follows relationships and can summarise
communities of connected entities — better than passage retrieval for questions
spanning a whole corpus, and considerably more expensive to build.

## Common Confusions

* **Knowledge graph vs vector database** — explicit typed relationships versus
  learned similarity. The graph answers "how are these connected?"; embeddings
  answer "what resembles this?". They complement each other.
* **Knowledge graph vs database** — a relational database can store the same
  facts; the graph makes traversal of arbitrary depth cheap and schema evolution
  easy.
* **Building one is the hard part** — extraction, entity resolution and
  maintenance dominate the cost, and stale graphs mislead confidently.

## Why Should I Care?

It is the strongest surviving line from symbolic AI into current practice, and
the right answer whenever your questions are about relationships rather than
about documents.

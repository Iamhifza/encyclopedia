---
term: Information Retrieval
aliases: [IR, Search, Document Retrieval]
category: rag-knowledge
subcategory: retrieval
status: foundational
difficulty: beginner
one_liner: The discipline of finding the documents in a large collection that are most relevant to a query.
origin:
  year: 1957
  circa: true
  attribution: Coined by Calvin Mooers in 1950; formalised through Salton's SMART system from the 1960s
historical_period: early-computing
diagram:
  kind: figure
  title: Half the work happens before anyone asks anything
  footer: 'Sixty years old and almost entirely unchanged in shape: index offline, retrieve candidates
    online, rank them, return the top few. Only the scoring function keeps being replaced.'
  visual:
    kind: columns
    width: 740
    caption: the two halves meet at the lookup, which is the only step that has to be fast
    columns:
    - title: Indexing · offline
      lines:
      - documents
      - tokenise and normalise
      - build the inverted index
      - term → list of document ids
    - title: Querying · online
      accent: true
      lines:
      - a query
      - tokenise, expand, rewrite
      - look up candidates
      - score, rank, rerank, return
tags: [retrieval]
relations:
  evolved_into: [dense-retrieval]
  used_by: [rag]
  related_to: [vector-database]
encountered_in: [research-papers, production-systems, interviews]
sources:
  - type: book
    title: "Introduction to Information Retrieval (Manning, Raghavan, Schütze)"
    url: https://nlp.stanford.edu/IR-book/
    year: 2008
  - type: paper
    title: "The Probabilistic Relevance Framework: BM25 and Beyond"
    url: https://www.staff.city.ac.uk/~sbrp622/papers/foundations_bm25_review.pdf
    year: 2009
updated: 2026-08-21
---

## Simple Explanation

You have ten million documents and a short question. Information retrieval is
the study of putting the useful documents at the top of the list. It predates
AI as a field, and almost everything currently called "RAG" is IR with a
language model bolted to the end.

## Technical Definition

Given a query $q$ and a collection $D$, produce a ranking of $D$ by estimated
relevance to $q$. Classical approaches score documents by term statistics
(TF-IDF, BM25) over an inverted index; neural approaches score by similarity in
a learned embedding space. Effectiveness is measured with recall@k, precision@k,
MRR and nDCG.

## Why Does It Exist?

Libraries and, later, corporate document stores outgrew human indexing. The
question of how to rank rather than merely match has been the central problem
since the 1960s.

## What Problem Does It Solve?

Exhaustive reading does not scale. Neither does exact matching: a user asking
about "car insurance" wants documents that say "automobile policy".

## How Does It Work?

Retrieval is nearly always two-stage: a cheap method retrieves hundreds of
candidates, an expensive method reorders the top of that list.

## Mental Model

A librarian who has read the first line of everything. Fast, shallow, and much
better than starting at shelf one.

## Formula

The dominant lexical scoring function, BM25:

$$\text{score}(q,d) = \sum_{t \in q} \text{IDF}(t) \cdot \frac{f(t,d)\,(k_1+1)}{f(t,d) + k_1\left(1 - b + b\frac{|d|}{\text{avgdl}}\right)}$$

* $f(t,d)$ — how often term $t$ appears in document $d$.
* $\text{IDF}(t)$ — inverse document frequency; rare terms carry more signal.
* $|d|$, $\text{avgdl}$ — document length and collection average, so long
  documents do not win by sheer size.
* $k_1$ — saturation: the tenth occurrence of a word adds less than the second.
* $b$ — how aggressively to normalise for length.

## Example

Query: *"how do I cancel my subscription"*. BM25 rewards documents containing
"cancel" and "subscription" while discounting "how", "do" and "my" as
near-universal. A document titled "Cancelling your subscription" scores highly
without any semantic understanding at all.

## Real-World Usage

Elasticsearch, OpenSearch, Lucene, Vespa and every serious search product ship
BM25. In modern RAG stacks, the strongest configurations are usually *hybrid*:
BM25 plus dense retrieval, fused, then reranked.

## Historical Origin

Mooers coined the term in 1950. Salton's SMART system (1960s) introduced the
vector space model and TF-IDF. The probabilistic relevance framework of the
1970s and 1980s produced BM25, which remains a competitive baseline half a
century later.

## Evolution

```text
Boolean matching → TF-IDF → BM25 → learning to rank
  → dense retrieval → hybrid retrieval → RAG → agentic RAG
```

## Common Confusions

* **Retrieval vs RAG** — RAG is retrieval plus generation. The retrieval half is
  older than most people working on it.
* **"Semantic search beat keyword search"** — dense retrieval handles paraphrase
  better; BM25 handles rare exact tokens (error codes, product SKUs, surnames)
  better. Production systems use both.

## Why Should I Care?

Most disappointing RAG systems are not failing at generation. They are failing
at retrieval, and the fixes are decades old: better chunking, hybrid scoring,
query rewriting, reranking, and actually measuring recall.

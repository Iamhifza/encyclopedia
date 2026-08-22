---
title: BM25 vs Dense Retrieval
question: Should I match words or meaning?
sides: [information-retrieval, dense-retrieval]
---

## The short version

Neither. Their failures are almost perfectly complementary, and the strong
default is to run both and fuse the rankings. But you should know *why* each
fails, because that is how you diagnose a retrieval problem.

## Side by side

| | BM25 (lexical) | Dense retrieval |
|---|---|---|
| **Matches on** | Term overlap, weighted by rarity | Proximity in an embedding space |
| **Wins on** | Identifiers, error codes, SKUs, surnames, rare jargon | Paraphrase, synonymy, intent |
| **Loses on** | Vocabulary mismatch — most natural questions | Exact rare tokens it has blurred together |
| **Index** | Inverted index, decades of tooling | ANN index, approximate by construction |
| **Out of domain** | Robust; no training involved | Degrades — the encoder saw a different world |
| **Cost to update** | Add a document, done | Re-embed on any model change |
| **Explainability** | You can see which terms matched | A number, and no account of why |

## The two canonical failures

```text
query: "error PX-4471 on checkout"
   BM25   ✓ finds the exact string immediately
   dense  ✗ embeds it near every other error message

query: "my card got declined"
   document: "payment authorisation failures"
   BM25   ✗ no shared terms at all
   dense  ✓ same region of the space
```

Both queries are ordinary. That is the point — you cannot pick one method and
expect the other's failures to be rare.

## Why BM25 refuses to die

It was competitive in 2009 and it is still a strong baseline. It needs no
training, no GPU, no re-embedding, and it degrades gracefully on corpora nothing
was trained on. Papers proposing neural retrieval are still expected to compare
against it, and it still sometimes wins.

## What actually decides quality

Not the choice between them. In practice the ordering of impact is: chunking,
then hybrid fusion, then reranking, then the embedding model. Teams frequently
swap embedding models while leaving a bad chunking strategy untouched, and are
surprised that nothing improves.

## Verdict

Use hybrid retrieval — reciprocal rank fusion over both — then rerank the top of
the merged list. Reach for the individual comparison only when diagnosing: if
recall is poor on identifiers, your lexical half is missing or weighted too low;
if poor on paraphrase, look at the embedding model or the chunk size.

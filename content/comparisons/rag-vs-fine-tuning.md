---
title: RAG vs Fine-Tuning
question: Should I retrieve the knowledge or train it into the model?
sides: [rag, supervised-fine-tuning]
---

## The short version

Retrieval supplies **facts**. Fine-tuning teaches **behaviour**. Most teams who
fine-tuned to add knowledge should have retrieved, and most teams who prompt
harder to fix formatting should have fine-tuned.

## Side by side

| | RAG | Fine-tuning |
|---|---|---|
| **Adds** | Current, private, citable facts | Style, format, tone, task behaviour |
| **Update cost** | Reindex a document, seconds | Retrain, hours to days |
| **Attribution** | Citations to the source passage | None; knowledge is diffuse in weights |
| **Access control** | Per-user filters at query time | Baked in for everyone |
| **Inference cost** | Higher — retrieved tokens every request | Unchanged, or lower |
| **Latency** | Extra retrieval hop | None added |
| **Fails when** | Retrieval misses the passage | The domain shifts, or data was thin |
| **Typical spend** | Engineering time on the index | Compute plus data curation |

## Choose retrieval when

The information changes, is private, needs citation, differs per user, or is too
large to memorise. This covers the large majority of business use cases.

## Choose fine-tuning when

You need a consistent output format that prompting cannot hold, a specific tone
or persona, a domain vocabulary the model handles awkwardly, reliable tool-call
formatting, or lower inference cost from a smaller model. LoRA makes this cheap
enough to try.

## Use both when

The behaviour and the knowledge are both wrong. Fine-tune the format and style;
retrieve the facts. This is a common production shape and the two do not conflict.

## The mistake to avoid

Fine-tuning on a corpus of documents to "teach the model our data". The model
learns the *style* of the documents reliably and their *content* unreliably,
produces confident errors, cannot cite anything, and needs retraining whenever a
document changes. If the goal is factual recall, index it.

## Verdict

Start with retrieval. Reach for fine-tuning when you have measured a behavioural
gap that context cannot close — and measure it on a real evaluation set, not on
impressions.

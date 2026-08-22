---
title: RAG vs Long Context
question: Now that context windows are enormous, do I still need retrieval?
sides: [rag, long-context-model]
---

## The short version

Yes. "RAG is dead" gets announced with every context-window increase and has not
been true yet. Long context is a bigger desk; retrieval is deciding what goes on
it. Those are different jobs, and at any corpus size worth the name you need
both.

## Side by side

| | Long context | RAG |
|---|---|---|
| **Approach** | Put everything in the prompt | Select what is relevant, then prompt |
| **Corpus limit** | Whatever fits the window | Effectively unbounded |
| **Cost per request** | Grows with everything you include | Grows with what you selected |
| **Latency** | Prefill over the whole payload | Retrieval hop, then a short prefill |
| **Permissions** | All or nothing | Filter per user at query time |
| **Attribution** | The model saw everything; citing is unreliable | Passage-level citations |
| **Accuracy over length** | Degrades in the middle | Constant — you only sent five passages |
| **Updates** | Resend everything | Reindex one document |

## The arithmetic

```text
50,000-document corpus
  long context : does not fit. Not "expensive" — impossible.

single 200k-token document, one question
  RAG          : retrieval overhead for no benefit
  long context : correct choice

10-document working set, per user, permissioned
  hybrid       : retrieve to select, long context to hold. The usual answer.
```

## Three things long context does not do

**Permission filtering.** Retrieval applies metadata filters before anything
reaches the model. Stuffing a shared corpus into context means every user sees
everything — a compliance failure, not a quality one.

**Attribution.** With five retrieved passages you can check a citation against
its source. With 400,000 tokens of context, "cite your source" produces something
plausible and unverifiable.

**Cost control.** Cached prefixes help enormously, but you still pay to prefill
what you sent. Retrieval's whole purpose is sending less.

## What long context genuinely changed

The chunking pressure. When context was 4k tokens you retrieved tiny fragments
and lost the surrounding meaning. Now you can retrieve *generously* — whole
sections rather than paragraphs, more candidates, the parent document of a
matching chunk. Retrieval got easier and more forgiving. It did not become
unnecessary.

## Verdict

Retrieval selects; context holds. Use long context alone when the corpus is small
and fixed and permissions are uniform. Use both — retrieve broadly, then let the
big window hold what you retrieved — for anything else. Announcements that one
killed the other have a poor track record.

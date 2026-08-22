---
title: MHA vs MQA vs GQA
question: How many key-value heads should a model have?
sides: [self-attention, grouped-query-attention]
---

## The short version

Three points on one dial. Multi-head attention gives every query head its own
keys and values; multi-query shares a single set across all of them; grouped-query
sits in between. The dial trades quality against KV cache size, and the cache is
what decides how many users fit on a GPU.

## Side by side

| | MHA | GQA | MQA |
|---|---|---|---|
| **KV heads** | One per query head | A few, shared in groups | Exactly one |
| **Cache size** | Baseline | Divided by group size | Divided by head count |
| **Quality** | Best | Very close to MHA | Measurably worse |
| **Training stability** | Fine | Fine | Reported instabilities |
| **Introduced** | 2017 | 2023 | 2019 |
| **Used today** | Rare in new large models | Near-universal | Uncommon |

## The dial

```text
32 query heads throughout

MHA   32 KV heads    cache ████████████████████████████████   1×
GQA    8 KV heads    cache ████████                           4× smaller
MQA    1 KV head     cache █                                 32× smaller
```

## Why this is a serving decision, not a modelling one

The KV cache must be read in full at every decode step, and decode is
memory-bandwidth-bound. So shrinking the cache does two things at once: more
concurrent requests fit in memory, and each step reads fewer bytes. GQA is the
clearest example in the corpus of an architecture chosen for how it will be
served rather than for what it scores.

## What the model card tells you

"64 query heads, 8 KV heads" is a GQA model with group size 8, and that ratio
predicts its serving cost more directly than parameter count does. A model with
MHA at the same size will need many times the cache memory for the same context
length.

## The next step along

DeepSeek's multi-head latent attention compresses keys and values into a shared
low-rank latent instead of reducing head count — a smaller cache again, paid for
in extra computation at attention time. Same objective, different mechanism.

## Verdict

GQA, essentially always, for a new model. It is not a free lunch — quality drops
slightly, most visibly on fine-grained retrieval from long context — but the
memory saving buys concurrency that no other single change delivers. MQA is
mainly of historical interest, and MHA survives where cache size does not
constrain anything.

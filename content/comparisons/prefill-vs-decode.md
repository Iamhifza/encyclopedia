---
title: Prefill vs Decode
question: Why does the same model behave like two different systems?
sides: [prefill, decode]
---

## The short version

They are the same weights doing opposite kinds of work. Prefill is a
**compute-bound** parallel pass over the whole prompt. Decode is a
**memory-bandwidth-bound** sequential pass, one token at a time. Almost every
serving decision follows from this split.

## Side by side

| | Prefill | Decode |
|---|---|---|
| **Tokens per pass** | All prompt tokens | Exactly one |
| **Bottleneck** | Arithmetic (matrix units) | Memory bandwidth (weight streaming) |
| **Arithmetic intensity** | High | Very low at small batch |
| **Scales with** | Prompt length, quadratically in attention | Output length, linearly |
| **User-visible metric** | Time to first token | Time per output token |
| **Batching helps** | Little — already saturated | Enormously — weights loaded once for all |
| **Optimised by** | Prefix caching, chunked prefill, FlashAttention | Quantisation, GQA, speculative decoding |

## Why it matters in practice

```text
1,000-token prompt, 1,000-token answer
   prefill:  ONE pass over 1,000 tokens        ← seconds at worst
   decode:   1,000 passes over 1 token each    ← usually most of the wall clock
```

Doubling the prompt is cheap. Doubling the answer is not.

## The scheduling tension

A long prefill occupying a step starves everyone's decoding; a batch of pure
decode leaves the arithmetic units idle. Chunked prefill exists precisely to mix
them, and prefill/decode disaggregation goes further by running the two phases on
separate hardware pools sized for their different bottlenecks.

## Verdict

Diagnose before optimising. Slow to start means prefill: cache the prefix, chunk
the prompt, shorten the context. Slow to stream means decode: quantise, use GQA,
add speculative decoding, or use a smaller model.

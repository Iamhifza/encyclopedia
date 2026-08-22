---
title: Training vs Inference
question: Why do the same weights behave like two completely different workloads?
sides: [pretraining, autoregressive-generation]
---

## The short version

Training is one enormous batch job that runs once and produces an artefact.
Inference is millions of small latency-sensitive requests that run forever. They
stress opposite properties of the hardware, and almost nothing you learn
optimising one transfers to the other.

## Side by side

| | Training | Inference |
|---|---|---|
| **Runs** | Once, for weeks | Continuously, for years |
| **Batch** | Enormous, uniform, known in advance | Small, variable, arriving unpredictably |
| **Bound by** | Compute and interconnect | Memory bandwidth and capacity |
| **Memory holds** | Weights, gradients, optimiser state, activations | Weights and KV cache |
| **Memory needed** | Roughly 4-6× the weights | Weights plus cache |
| **Latency** | Irrelevant; only total time matters | The product requirement |
| **Failure** | Restart from a checkpoint | A user sees an error |
| **Precision** | bf16 with fp32 accumulation | fp8 or int4 is often fine |
| **Cost falls on** | Whoever builds the model, once | Whoever serves it, forever |

## Where the memory goes

```text
TRAINING a 7B model in bf16
  weights          14 GB
  gradients        14 GB
  optimiser state  56 GB   (Adam: two values per parameter, fp32)
  activations      varies with batch and sequence
  ────────────────────────
  ~100 GB+ for a model that serves in 14

INFERENCE the same model
  weights          14 GB   (or 4 GB quantised)
  KV cache         grows with concurrent users and context
```

That ratio is why fine-tuning a model you can happily serve may still not fit on
your GPU, and why LoRA exists.

## The economic asymmetry

Training cost is paid once and is highly visible. Inference cost is paid per
request, forever, and eventually dwarfs it. This is why compute-optimal scaling
is *deliberately ignored* at the top end: labs train smaller models on far more
tokens than Chinchilla recommends, overspending on training precisely to
underspend on inference for the model's whole deployed life.

## What does not transfer

Batching intuitions (training batches are uniform, serving batches are not),
precision choices, parallelism strategy (pipeline parallelism is standard in
training and unattractive in serving), and utilisation targets. An engineer
excellent at one is not automatically useful at the other, which is why these are
now separate job titles.

## Verdict

Treat them as different disciplines that happen to share a file format. When
reading a claim about performance, always establish which one is being discussed —
"we made the model 3× faster" means nothing until you know whether anyone can
still afford to serve it.

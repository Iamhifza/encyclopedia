---
term: Autoregressive Generation
aliases: [Autoregressive Decoding, Next-Token Generation]
category: llm-inference
subcategory: mechanics
status: foundational
difficulty: beginner
one_liner: Producing text one token at a time, where each new token is chosen based on everything generated so far.
origin:
  year: 1927
  circa: true
  attribution: Autoregressive models come from time-series statistics; applied to neural language models from the 2010s
historical_period: statistical-ml
diagram:
  kind: figure
  title: One expensive pass, then many cheap ones
  footer: The asymmetry is why inference has two distinct cost profiles. Prefill is compute-bound and
    parallel; decode is memory-bound and stubbornly sequential, and no amount of hardware makes token
    n+1 available before token n.
  visual:
    kind: mapping
    width: 780
    head:
    - what the model reads this step
    - what it emits
    rows:
    - left: the whole prompt, in parallel
      right: '"stores"   ← prefill'
      tone: accent
    - left: '"stores", against the cache'
      right: '"keys"    ← decode'
    - left: '"keys", against the cache'
      right: '"and"     ← decode'
    caption: and on until an end-of-sequence token or a length limit; every step appends to the KV cache
tags: [inference]
relations:
  depends_on: [transformer]
  implemented_by: [prefill, decode]
  used_by: [kv-cache, speculative-decoding]
  related_to: [rnn]
prerequisites: [large-language-model]
encountered_in: [research-papers, production-systems, interviews]
sources:
  - type: paper
    title: "Language Models are Unsupervised Multitask Learners (GPT-2)"
    url: https://cdn.openai.com/better-language-models/language_models_are_unsupervised_multitask_learners.pdf
    year: 2019
  - type: docs
    title: "Hugging Face — text generation strategies"
    url: https://huggingface.co/docs/transformers/generation_strategies
updated: 2026-08-21
---

## Simple Explanation

The model does not write an answer. It writes one token, appends it to what it
has, and writes the next one. A 500-token reply is 500 separate forward passes,
each conditioned on everything before it.

## Technical Definition

Factorising a sequence distribution by the chain rule,
$p(x_1..x_n) = \prod_t p(x_t \mid x_{<t})$, and sampling from each conditional in
turn. Every generated token is fed back as input for the next step.

## Why Does It Exist?

It is the only factorisation that lets a single next-token predictor produce
sequences of unbounded length, and it matches the training objective exactly, so
no gap opens between how the model was trained and how it is used.

## What Problem Does It Solve?

Generating variable-length, coherent output from a model that only ever answers
one question: what comes next?

## How Does It Work?

Step 1 is one large parallel pass; every later step processes a single token but
attends over all previous ones — which is why their keys and values are cached.

## Mental Model

Speaking without a plan, one word at a time, unable to take any word back. There
is no revision pass; coherence comes entirely from conditioning.

## Formula

$$p(x_{1:n}) = \prod_{t=1}^{n} p(x_t \mid x_{<t})$$

* $x_t$ — the token at position $t$.
* $x_{<t}$ — everything already produced, prompt included.

## Example

Ask for a 1000-token essay and you have requested 1000 sequential forward passes.
This is why output length dominates latency far more than input length does, and
why doubling the prompt is cheap compared with doubling the answer.

## Real-World Usage

Every chat completion, every coding agent's edit, every streamed response.
Speculative decoding, continuous batching and the entire serving stack exist to
work around the sequential nature of this loop.

## Common Confusions

* **Autoregressive vs recurrent** — autoregression is about feeding outputs back
  in; recurrence is about a hidden state carried forward. Transformers are the
  first without the second.
* **"The model plans the answer"** — it commits token by token. Apparent planning
  comes from conditioning on its own prior output, which is exactly why
  chain-of-thought works.
* **Diffusion text models** — an active alternative that refines all positions in
  parallel rather than left to right.

## Why Should I Care?

The one-token-at-a-time structure is the root cause of nearly every inference
optimisation in this domain. If you understand why the loop is sequential and
memory-bound, the rest of the serving stack follows.

---
term: Recurrent Neural Network
aliases: [RNN, Recurrent Network]
category: deep-learning
subcategory: architectures
status: historical
difficulty: intermediate
one_liner: A network that reads a sequence one step at a time, carrying a hidden summary of everything it has seen so far.
origin:
  year: 1986
  circa: true
  attribution: Elman and Jordan networks; the idea of recurrent state is older
historical_period: ai-winter
diagram:
  kind: figure
  title: One weight matrix, applied over and over
  footer: 'The recurrence is also the limit: step t cannot start until step t−1 has finished, so training
    will not parallelise along the sequence. That single property is what the Transformer removed.'
  visual:
    kind: chips
    items:
    - h₀
    - h₁
    - h₂
    - h₃
    - h₄
    caption: each arrow is the same matrix; the hidden state is the only memory the network has
tags: [architecture]
relations:
  is_a: [neural-network]
  evolved_into: [lstm]
  alternative_to: [transformer]
  related_to: [autoregressive-generation]
encountered_in: [research-papers, interviews]
sources:
  - type: paper
    title: "Finding Structure in Time"
    url: https://onlinelibrary.wiley.com/doi/10.1207/s15516709cog1402_1
    year: 1990
  - type: post
    title: "The Unreasonable Effectiveness of Recurrent Neural Networks"
    url: https://karpathy.github.io/2015/05/21/rnn-effectiveness/
    year: 2015
videos:
  - title: "Recurrent Neural Networks, clearly explained"
    channel: "StatQuest"
    url: https://www.youtube.com/results?search_query=statquest+recurrent+neural+networks+clearly+explained
updated: 2026-08-21
---

## Simple Explanation

Read a sentence word by word, keeping one running note of what you have read.
Each new word updates the note. When the sentence ends, the note is your
understanding of it.

## Technical Definition

A network with a recurrence $h_t = \sigma(W_h h_{t-1} + W_x x_t + b)$, applied
with shared parameters across time steps, trained by backpropagation through
time (unrolling the recurrence and differentiating through it).

## Why Does It Exist?

Feed-forward networks need fixed-size input. Language, audio and time series are
variable-length and order-dependent, so something had to carry information
forward across positions.

## What Problem Does It Solve?

Variable-length sequences with a fixed parameter count, and an inductive bias
that recent context matters.

## How Does It Work?


Process the sequence one element at a time, carrying a hidden state forward.
At each step the network combines the current input with the state left by the
previous step, applies the *same* weight matrix it applied at every other step,
and produces a new state. The hidden state is the only memory: everything the
network has read is compressed into that one fixed-size vector.

Two consequences follow from the shared weights. The good one is that the model
handles sequences of any length with a fixed parameter count. The costly one is
that step *t* cannot begin until step *t−1* has finished, so training cannot be
parallelised along the sequence — and repeatedly multiplying by the same matrix
makes gradients shrink or explode over long spans. Gating (LSTM, GRU) fixed the
gradients; only dropping recurrence altogether fixed the parallelism.

## Mental Model

Reading a book through a mail slot, one word at a time, allowed only a single
sticky note to remember everything so far.

## Example

Character-level RNNs trained on Shakespeare or C source code produced plausible
imitations in 2015, which is what convinced many people that sequence models
could learn structure rather than statistics alone.

## Real-World Usage

Largely displaced by Transformers for language. Still used where strict streaming
and small memory matter, and conceptually revived by modern state-space models
such as Mamba, which restore constant-memory recurrence while remaining
parallelisable in training.

## Common Confusions

* **RNN vs Transformer** — the RNN compresses history into a fixed-size hidden
  state; a Transformer keeps every previous token and attends over all of them.
* **Recurrence vs autoregression** — autoregressive *generation* (feeding the
  output back as input) is a decoding scheme; recurrence is an architectural
  property. Transformers are autoregressive without being recurrent.

## Why Should I Care?

The two flaws that killed RNNs for language — a fixed-width memory bottleneck
and strictly sequential training — are precisely what attention and the
Transformer were designed to fix. You cannot understand why the Transformer
looks the way it does without them.

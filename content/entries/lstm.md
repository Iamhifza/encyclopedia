---
term: LSTM
aliases: [Long Short-Term Memory, Gated Recurrent Network]
category: deep-learning
subcategory: architectures
status: historical
difficulty: advanced
one_liner: A recurrent network with learned gates that decide what to keep, what to forget and what to output, so information can survive long sequences.
origin:
  year: 1997
  attribution: Sepp Hochreiter and Jürgen Schmidhuber
historical_period: statistical-ml
diagram:
  kind: figure
  title: A cell state that runs straight through, with gates on it
  footer: The cell state is a near-uninterrupted path from t−1 to t, so gradients can travel back many
    steps without vanishing. Gating that path is what bought recurrent networks another decade.
  visual:
    kind: pipeline
    width: 700
    caption: gates are learned, in [0,1], and multiply — which is why they can hold a value for hundreds
      of steps
    stages:
    - text: c(t−1)
      note: carried in
    - text: what to keep
      via: forget gate — multiply the old state by σ(·)
    - text: what to add
      via: input gate × candidate — write the new information
    - text: c(t)  →  h(t)
      note: carried out
      tone: accent
      via: output gate — decide how much of the state to expose
tags: [architecture]
relations:
  is_a: [rnn]
  successor_of: [rnn]
  evolved_into: [attention]
  related_to: [state-space-model]
encountered_in: [research-papers, interviews]
sources:
  - type: paper
    title: "Long Short-Term Memory"
    url: https://direct.mit.edu/neco/article/9/8/1735/6109/Long-Short-Term-Memory
    year: 1997
  - type: post
    title: "Understanding LSTM Networks"
    url: https://colah.github.io/posts/2015-08-Understanding-LSTMs/
    year: 2015
videos:
  - title: "Long Short-Term Memory (LSTM), clearly explained"
    channel: "StatQuest"
    url: https://www.youtube.com/results?search_query=statquest+long+short+term+memory+lstm+clearly+explained
updated: 2026-08-21
---

## Simple Explanation

A plain recurrent network overwrites its memory at every step, so early
information fades within a few dozen words. The LSTM adds a separate memory line
that information can travel along untouched, plus three gates that decide what to
erase, what to write and what to reveal.

## Technical Definition

A recurrent cell maintaining a cell state $c_t$ updated additively and modulated
by forget, input and output gates, each a sigmoid over the previous hidden state
and current input. The additive path gives the gradient a route backwards through
time that does not repeatedly multiply by small numbers.

## Why Does It Exist?

To fix vanishing gradients. In a plain RNN, gradients are multiplied by the same
factor at every step; over a hundred steps that factor either collapses to zero
or explodes. The LSTM's constant-error carousel keeps a near-unity path.

## What Problem Does It Solve?

Long-range dependencies: matching a verb to a subject twenty words back, or a
closing bracket to one opened much earlier.

## How Does It Work?

The forget gate scales old memory, the input gate admits new content, the output
gate decides how much of the memory is exposed as this step's hidden state.

## Mental Model

A conveyor belt of memory running alongside the reader, with three valves: one
that empties boxes, one that adds boxes, and one that decides what is visible
from outside.

## Formula

$$f_t = \sigma(W_f[h_{t-1}, x_t]), \quad c_t = f_t \odot c_{t-1} + i_t \odot \tilde{c}_t$$

* $f_t$ — forget gate; values near 0 erase, near 1 preserve.
* $i_t$ — input gate; how much of the new candidate to admit.
* $\tilde{c}_t$ — candidate content proposed at this step.
* $\odot$ — element-wise multiplication.

The multiplication-then-addition on $c_t$ is the whole trick.

## Example

LSTMs powered production machine translation (including Google Translate from
2016), speech recognition and handwriting recognition — the state of the art in
sequence modelling for nearly two decades.

## Real-World Usage

Rare in new language systems. Still found in embedded and streaming contexts,
legacy production models, and time-series forecasting where sequences are long
and data is small.

## Common Confusions

* **LSTM vs GRU** — the GRU merges the forget and input gates into one update
  gate: fewer parameters, usually comparable quality.
* **LSTM vs attention** — attention was originally added *to* LSTM encoder-decoders
  in 2014, not as a replacement. Only in 2017 did the Transformer discard the
  recurrence and keep the attention.

## Why Should I Care?

The LSTM is where the field learned that gating and additive skip paths let
gradients survive depth — the same principle that residual connections apply
inside every Transformer block.

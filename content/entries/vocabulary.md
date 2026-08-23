---
term: Vocabulary
aliases: [Token Vocabulary, Vocab Size, Special Tokens, Chat Template]
category: llms-foundation-models
subcategory: representation
depth: full
status: established
difficulty: intermediate
one_liner: "The fixed set of tokens a model can read or emit, and the reason it can never output a character it has no piece for."
historical_period: transformer
tags: [architecture]
relations:
  part_of: [tokenization]
  related_to: [sampling, embedding, structured-outputs, feed-forward-network]
prerequisites: [tokenization]
encountered_in: [github, production-systems, documentation]
sources:
  - type: paper
    title: "Neural Machine Translation of Rare Words with Subword Units"
    url: https://arxiv.org/abs/1508.07909
    year: 2015
  - type: repo
    title: "tiktoken"
    url: https://github.com/openai/tiktoken
updated: 2026-08-21
---

## Simple Explanation

The vocabulary is the model's complete alphabet — typically 32,000 to 200,000
entries, each a word, word-fragment or byte sequence. Everything the model reads
is decomposed into these, and everything it writes is assembled from them.

It is fixed at training time and cannot be extended afterwards without surgery on
the model, which has more practical consequences than it sounds.

## Technical Definition

The finite set of tokens a tokeniser can produce, with an integer id each. Its
size determines two matrices: the input embedding table ($|V| \times d$) and the
output projection producing logits over every token. Both scale linearly with
vocabulary size, so it is a real parameter-budget decision.

## Why Does It Exist?

A model must output a probability distribution over a finite set. That set has to
be decided before training, and every trade-off in tokenisation is really a
question about how to spend it.

## What Problem Does It Solve?

It bounds the output space — you cannot compute a softmax over "all possible
strings" — while byte-level fallback ensures every input is still representable.

## How Does It Work?

```text
vocabulary (say 128,000 entries)
  ├─ frequent words        "the", "and", " model"          one token each
  ├─ fragments             "ization", "▁un", "tion"        assembled as needed
  ├─ bytes                 fallback so nothing is unknown
  └─ special tokens        <|begin|> <|end|> <|user|> ...   structural markers

larger vocabulary  → shorter sequences, bigger embedding + output matrices
smaller vocabulary → longer sequences, more compute per document
```

## Mental Model

A typesetter's case of sorts. A larger case means fewer pieces per line and a
heavier case to carry; a smaller one means more assembly per word.

## Example

**Special tokens** are where this bites in practice. Chat models are trained with
structural markers delimiting system, user and assistant turns, and the *chat
template* that inserts them is model-specific. Getting it wrong — using the wrong
template, or omitting it — produces a model that behaves oddly for no visible
reason, and it is one of the most common failures when self-hosting an
open-weight model.

The other practical consequence is fairness. Vocabulary is learned from a corpus,
so languages under-represented in it fragment into more tokens: the same sentence
can cost several times more tokens in one language than another, meaning higher
price, higher latency and less usable context for those speakers.

## Real-World Usage

Fixed per model family. Vocabulary sizes have grown — from 32k in early models
toward 128k–256k in recent ones — because larger vocabularies shorten sequences,
and sequence length is quadratically expensive in attention while the embedding
matrix is only linearly expensive.

## Common Confusions

* **Vocabulary vs tokeniser** — the set of tokens versus the algorithm that
  segments text into them. Related, not identical.
* **You cannot add tokens after training** — new entries have untrained
  embeddings. Extending a vocabulary requires resizing matrices and further
  training.
* **Token counts differ by model** — the same text costs a different number of
  tokens on different models, so cost comparisons need the same tokeniser.

## Why Should I Care?

It silently determines your costs, your effective context length, how well the
model serves non-English users, and — through chat templates — whether a
self-hosted model behaves correctly at all.

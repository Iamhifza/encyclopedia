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
diagram:
  kind: steps
  title: What the model is actually allowed to say
  footer: 'Vocabulary size is a real architectural choice: it sets the width of the embedding and output
    matrices, and how many tokens a document costs. English text is well served; languages that tokenise
    badly pay for it on every request.'
  steps:
  - title: Four kinds of entry
    visual:
      kind: stack
      width: 760
      caption: roughly 128,000 entries in a current model
      layers:
      - label: whole words
        text: '"the", "and", " model"'
        note: one token each
      - label: fragments
        text: '"ization", "▁un", "tion"'
        note: assembled as needed
        accent: true
      - label: bytes
        text: the fallback, so nothing is ever unknown
        note: always parses
      - label: special
        text: <|begin|> <|end|> <|user|>
        note: structural markers
  - title: And the size is a trade
    visual:
      kind: table
      width: 740
      head:
      - vocabulary
      - sequences
      - matrices
      rows:
      - - larger
        - shorter — fewer tokens per document
        - bigger embedding and output layers
      - - smaller
        - longer — more compute per document
        - smaller, but every document costs more
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


The vocabulary is the fixed set of tokens a model can read and emit — typically
around 128,000 entries — and it is decided once, when the tokeniser is trained,
before the model exists.

It holds four kinds of thing. Frequent whole words, which cost one token each.
Fragments like *ization* or *▁un*, assembled to build rarer words. Raw bytes as a
fallback, so that no input is ever unrepresentable. And special tokens —
begin-of-text, end-of-turn, role markers — that carry structure rather than
meaning, which is why injecting one into user input is a real attack.

Size is a genuine trade. A larger vocabulary means shorter sequences, so less
compute per document, but larger embedding and output matrices — and the output
layer is a softmax over every entry, computed at every step. A smaller vocabulary
inverts both. The choice is usually tuned on English text, which is why languages
that tokenise into many more fragments cost proportionally more to serve, an
inequity that is invisible until you look at the bill.

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

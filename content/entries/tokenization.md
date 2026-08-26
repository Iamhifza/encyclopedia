---
term: Tokenization
aliases: [Tokenisation, Tokenizer, BPE, Byte-Pair Encoding, SentencePiece]
category: llms-foundation-models
subcategory: representation
status: established
difficulty: intermediate
one_liner: Cutting text into the sub-word chunks a model actually reads, since models operate on a fixed vocabulary of pieces rather than on letters or words.
origin:
  year: 2015
  attribution: Sennrich et al. adapted byte-pair encoding from data compression to neural machine translation
historical_period: statistical-ml
diagram:
  kind: figure
  title: Text to integers, in two lookups
  footer: Every downstream count — context length, price, rate limit — is measured in the units on the
    bottom row, not the ones you typed.
  visual:
    kind: pipeline
    width: 700
    caption: the merge table is learned once, at tokeniser training time, and then frozen
    stages:
    - text: '"tokenization is lossy"'
      note: 22 characters
    - text: '["token", "ization", " is", " lossy"]'
      note: 4 tokens
      via: split to bytes, then apply the learned merge table in order
    - text: '[3928, 2065, 374, 69990]'
      note: what the model sees
      tone: accent
      via: look each piece up in the vocabulary
tags: [architecture]
relations:
  part_of: [large-language-model]
  used_by: [context-window, embedding]
  related_to: [hallucination]
prerequisites: []
encountered_in: [production-systems, github, interviews, documentation]
sources:
  - type: paper
    title: "Neural Machine Translation of Rare Words with Subword Units"
    url: https://arxiv.org/abs/1508.07909
    year: 2015
  - type: repo
    title: "tiktoken"
    url: https://github.com/openai/tiktoken
  - type: talk
    title: "Let's build the GPT Tokenizer"
    url: https://www.youtube.com/watch?v=zduSFxRajkE
    year: 2024
videos:
  - title: "Let's build the GPT Tokenizer"
    channel: "Andrej Karpathy"
    url: https://www.youtube.com/watch?v=zduSFxRajkE
    note: "Why models cannot count letters"
updated: 2026-08-21
---

## Simple Explanation

Models cannot read letters and cannot have a slot for every possible word. So
text is split into common fragments: frequent words become one token, rare words
split into several pieces. "Unbelievable" might be `un` + `bel` + `iev` + `able`.

## Technical Definition

A learned mapping from byte sequences to integer ids over a fixed vocabulary.
Byte-pair encoding builds the vocabulary greedily by repeatedly merging the most
frequent adjacent pair in a corpus; byte-level BPE operates on raw bytes so every
possible input is representable and there are no unknown tokens.

## Why Does It Exist?

Character-level modelling makes sequences long and wastes context; word-level
modelling produces a huge vocabulary that still cannot cover typos, names, code
identifiers or other languages. Sub-words are the compromise, and they are why
models handle novel words at all.

## What Problem Does It Solve?

A bounded vocabulary with unbounded coverage, and a sequence length short enough
to be affordable.

## How Does It Work?

Note that leading spaces are usually part of the token — `" is"` and `"is"` are
different tokens, a frequent source of subtle prompt bugs.

## Mental Model

Shorthand. Common phrases get one symbol, unusual ones get spelled out, and the
symbol set was chosen by looking at what was frequent in a particular corpus.

## Example

English prose averages roughly 1.3 tokens per word. Code, JSON, non-Latin scripts
and unusual names cost far more — the same paragraph in a less-represented
language can consume two or three times the tokens, which means higher price,
more latency and less effective context for those users.

## Real-World Usage

Every prompt, every price list, every context limit is denominated in tokens.
Tokenisation quirks explain a family of famous failures: counting letters in
"strawberry", arithmetic on long numbers split unevenly, and sensitivity to
whitespace and formatting in prompts.

## Common Confusions

* **Tokens are not words** — budget roughly 0.75 words per token for English, and
  measure for anything else.
* **Tokenizers are model-specific** — the same text yields different counts and
  ids across model families. Always use the tokenizer that matches the model.
* **Tokenisation is not embedding** — tokenisation produces integer ids; the
  embedding layer turns those ids into vectors.

## Why Should I Care?

It sets cost, context capacity and a surprising share of failure modes, and it is
the layer most people skip when debugging a prompt that behaves inexplicably.

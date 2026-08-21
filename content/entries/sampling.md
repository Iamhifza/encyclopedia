---
term: Sampling
aliases: [Decoding Strategy, Temperature, Top-k, Top-p, Nucleus Sampling, Greedy Decoding]
category: llm-inference
subcategory: decoding
status: established
difficulty: beginner
one_liner: The rule that turns the model's probability distribution over the whole vocabulary into the one token it actually emits.
origin:
  year: 2018
  circa: true
  attribution: Nucleus sampling formalised by Holtzman et al. in 2019; temperature comes from statistical physics via simulated annealing
historical_period: transformer
tags: [inference]
relations:
  part_of: [decode]
  used_by: [speculative-decoding]
  related_to: [hallucination, llm-as-a-judge]
prerequisites: [autoregressive-generation]
encountered_in: [documentation, production-systems, github]
sources:
  - type: paper
    title: "The Curious Case of Neural Text Degeneration"
    url: https://arxiv.org/abs/1904.09751
    year: 2019
  - type: docs
    title: "Hugging Face — generation strategies"
    url: https://huggingface.co/docs/transformers/generation_strategies
updated: 2026-08-21
---

## Simple Explanation

The model does not output a word. It outputs a score for every word in its
vocabulary — often 100,000 of them. Sampling is how one word is picked. Always
take the highest score and the text becomes repetitive and flat; pick too
randomly and it becomes incoherent.

## Technical Definition

A transformation of the logit vector into a distribution, followed by a draw.
Temperature $T$ divides logits before the softmax; top-$k$ truncates to the $k$
highest-probability tokens; top-$p$ (nucleus) truncates to the smallest set whose
cumulative probability exceeds $p$; greedy decoding takes the argmax. Additional
penalties (repetition, frequency, presence) modify logits before selection.

## Why Does It Exist?

Maximum-likelihood decoding on a model trained by maximum likelihood produces
degenerate text: loops, repetition and bland safe continuations. Controlled
randomness recovers the variety of natural language.

## What Problem Does It Solve?

The gap between the most probable continuation and a good continuation. It also
gives users one dial for the creativity-versus-reliability tradeoff.

## How Does It Work?

```text
logits over vocabulary
   │ ÷ temperature      (T<1 sharpens, T>1 flattens)
   │ apply penalties
   │ truncate: top-k (fixed count) or top-p (adaptive)
   │ renormalise
   ▼ draw one token
```

Top-$p$ is adaptive: where the model is confident the nucleus contains two or
three tokens, where it is uncertain it may contain hundreds.

## Mental Model

Temperature is how strictly you follow the recipe. Top-$p$ is refusing to
consider any ingredient that was never plausible in the first place.

## Formula

$$p_i = \frac{\exp(z_i / T)}{\sum_j \exp(z_j / T)}$$

* $z_i$ — the logit (raw score) for token $i$.
* $T$ — temperature. As $T \to 0$ this approaches argmax; $T > 1$ flattens the
  distribution toward uniform.

## Example

For structured output, tool arguments or code, temperature 0 with the tightest
practical constraints. For brainstorming or creative drafting, temperature
around 0.8-1.0 with top-$p$ 0.9. Setting temperature 0 does not guarantee
identical outputs across runs — batching, kernel non-determinism and floating
point reduction order can still vary results.

## Real-World Usage

Every inference API exposes these parameters. Grammar-constrained and
schema-constrained decoding extend the same machinery by masking out tokens that
would violate a JSON schema or regular expression, which is how structured
outputs are enforced.

## Common Confusions

* **Temperature is not confidence** — it reshapes the distribution; it does not
  make the model more or less correct.
* **Top-k vs top-p** — fixed cutoff versus adaptive cutoff. Top-$p$ is usually
  preferred because the right number of plausible tokens varies by position.
* **Beam search for chat** — beam search helps in translation, where one correct
  output exists, and hurts in open-ended generation, where it produces bland,
  high-probability text.

## Why Should I Care?

An enormous share of "the model is unreliable" reports are sampling
configuration problems, and they are the cheapest thing in the entire stack to
fix.

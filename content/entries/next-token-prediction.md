---
term: Next-Token Prediction
aliases: [Causal Language Modelling, Autoregressive Objective, Next-Word Prediction]
category: llm-training
subcategory: pretraining
depth: full
status: foundational
difficulty: beginner
one_liner: "The training objective behind every LLM: given everything so far, predict what comes next."
historical_period: transformer
tags: [training]
relations:
  part_of: [pretraining]
  depends_on: [loss-function]
  used_by: [autoregressive-generation]
  related_to: [self-supervised-learning, information-theory, tokenization]
prerequisites: [loss-function]
encountered_in: [research-papers, interviews, technical-blogs]
sources:
  - type: paper
    title: "Language Models are Unsupervised Multitask Learners (GPT-2)"
    url: https://cdn.openai.com/better-language-models/language_models_are_unsupervised_multitask_learners.pdf
    year: 2019
  - type: paper
    title: "A Mathematical Theory of Communication"
    url: https://people.math.harvard.edu/~ctm/home/text/others/shannon/entropy/entropy.pdf
    year: 1948
    note: Shannon was predicting next letters in English in 1948.
updated: 2026-08-21
---

## Simple Explanation

That is the whole objective. Show the model a stretch of text with the next token
hidden, ask it to guess, penalise it in proportion to how surprised it was by the
truth, repeat a few trillion times.

The remarkable thing — still not fully explained — is that this narrow objective
produces grammar, world knowledge, translation, arithmetic, code and reasoning as
side effects. Nobody trained for any of them.

## Technical Definition

Minimising cross-entropy between the model's predicted distribution over the
vocabulary and the observed next token, at every position simultaneously, with
causal masking so no position can see its own answer. Loss is averaged over all
positions, so a single sequence of 8,000 tokens supplies 8,000 training signals.

## Why Does It Exist?

It is the only objective that is simultaneously self-supervised (no labels
needed, so data is effectively unlimited), dense (every token is a training
signal), and general (predicting arbitrary text requires learning nearly
everything about it).

## What Problem Does It Solve?

The supervision bottleneck. Every earlier approach needed someone to say what the
right answer was.

## How Does It Work?

```text
"the cache stores keys and values"

position 1: given "the"                    predict "cache"
position 2: given "the cache"              predict "stores"
position 3: given "the cache stores"       predict "keys"
...
all positions computed in ONE forward pass, thanks to causal masking
loss = average surprise across all of them
```

That last line is why Transformers train so efficiently: the entire sequence
produces gradients in a single pass, which recurrent models could never do.

## Mental Model

Cloze exercises, at civilisational scale. To fill the blank in "the treaty was
signed in ___" you need history; in "the derivative of x² is ___" you need
calculus. The exercise is simple; passing it is not.

## Formula

$$\mathcal{L} = -\frac{1}{n}\sum_{t=1}^{n} \log p_\theta(x_t \mid x_{<t})$$

* $x_t$ — the actual token at position $t$.
* $p_\theta(x_t \mid x_{<t})$ — probability the model assigned it.
* The negative log means near-certainty about the truth costs almost nothing, and
  confident wrongness costs a great deal.

## Example

The compression view is illuminating: a model minimising this loss is learning to
compress its training distribution, since the optimal code length for a symbol is
$-\log p$. Better prediction *is* better compression, and the argument that
compression and understanding are closely related is one of the more serious
attempts to explain why this objective works as well as it does.

## Real-World Usage

Every LLM's pretraining stage, and every subsequent stage too — supervised
fine-tuning uses the same loss with masking restricted to response tokens.
Perplexity, the standard evaluation metric, is simply the exponential of this
loss.

## Common Confusions

* **"It only predicts the next word"** — technically true and misleading as a
  dismissal. What it takes to do that *well* across all human text is the
  interesting part, and the objective is a means rather than a description of the
  capability.
* **Next-token vs masked language modelling** — GPT-style predicts forward with a
  causal mask; BERT-style predicts hidden tokens with full bidirectional context.
  Different objectives, different uses.
* **The model does not plan the sentence** — it commits token by token. Apparent
  planning comes from conditioning on its own output.

## Why Should I Care?

Everything in the modern half of this encyclopedia stands on this one objective,
and understanding that capability emerged as a *side effect* of compression —
rather than being designed in — is the beginning of understanding why these
systems are so capable and so unreliable at the same time.

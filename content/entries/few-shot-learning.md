---
term: Few-Shot Learning
aliases: [In-Context Learning, Zero-Shot Learning, ICL, Prompting with Examples]
category: machine-learning
subcategory: paradigms
depth: full
status: established
difficulty: intermediate
one_liner: "Getting a model to do a new task from a handful of examples shown in the prompt, with no training at all."
origin:
  year: 2020
  attribution: Demonstrated at scale by GPT-3; the term predates it in the meta-learning literature
historical_period: foundation-model
diagram:
  kind: figure
  title: The examples are the specification
  footer: No weights change. Everything the model appears to have learned is inferred from the context
    and gone the moment the request ends — which is why this is a prompting technique and not training.
  visual:
    kind: mapping
    width: 780
    head:
    - what is in the prompt
    - what follows it
    rows:
    - left: '"shipping was late"'
      right: 'Sentiment: negative'
    - left: '"arrived early, delighted"'
      right: 'Sentiment: positive'
    - left: '"the box was dented"'
      right: 'Sentiment:  ← the model completes'
      tone: accent
    caption: consistent formatting matters more than the number of examples; two well-formed ones usually
      beat six ragged ones
tags: [training]
relations:
  depends_on: [large-language-model]
  used_by: [prompt-engineering, base-model]
  related_to: [transfer-learning, attention, chain-of-thought]
prerequisites: [large-language-model]
encountered_in: [research-papers, documentation, interviews]
sources:
  - type: paper
    title: "Language Models are Few-Shot Learners (GPT-3)"
    url: https://arxiv.org/abs/2005.14165
    year: 2020
  - type: paper
    title: "In-context Learning and Induction Heads"
    url: https://transformer-circuits.pub/2022/in-context-learning-and-induction-heads/index.html
    year: 2022
  - type: paper
    title: "Rethinking the Role of Demonstrations: What Makes In-Context Learning Work?"
    url: https://arxiv.org/abs/2202.12837
    year: 2022
updated: 2026-08-21
---

## Simple Explanation

Show the model three examples of the task inside the prompt, and it does the
fourth. No training, no gradient updates, no weights changed — the "learning"
happens entirely within a single forward pass and is forgotten immediately
afterwards.

This was the surprise of GPT-3, and it is the reason prompting became a discipline
rather than a formatting detail.

## Technical Definition

Task adaptation through conditioning rather than parameter updates. Demonstrations
are placed in the context window and the model infers the mapping from them.
*Zero-shot* uses an instruction alone; *few-shot* supplies $k$ examples. The
mechanism is now partly understood: induction heads — attention heads that detect
a repeated pattern and continue it — appear during training and correlate with the
emergence of the ability.

## Why Does It Exist?

Nobody designed it. It emerged from next-token prediction at scale, because
predicting text well requires recognising patterns established earlier in that
text. A document containing three worked examples is best continued by a fourth.

## What Problem Does It Solve?

Task specification without data collection or training. It collapsed the loop
from "we need a labelled dataset and a fine-tuning run" to "write three examples
and try it".

## How Does It Work?


Put a few worked examples in the prompt, formatted exactly as you want the answer
formatted, and end with an incomplete one. The model continues the pattern. No
weights change, no training runs, and nothing persists after the request — the
examples are simply context the model conditions on.

Formatting does more work than quantity. Two examples with identical structure
usually beat six inconsistent ones, because what the model is inferring is the
shape of the task as much as its content. Label ordering, separator choice and
even whether the labels are correct all measurably affect the result, which is a
clue that this is pattern continuation rather than learning in any ordinary
sense.

The technique mattered most when it was the only way to steer a base model.
Instruction-tuned models follow a plain description of the task, so few-shot
prompting has narrowed to where it still wins: unusual output formats, subtle
classification boundaries, and anything easier to demonstrate than to describe.

## Mental Model

Showing someone the format of a form rather than explaining the rules. They fill
in the next row correctly by matching the shape of what came before.

## Example

A genuinely strange finding: replacing the labels in your demonstrations with
*random* ones often degrades performance far less than expected. What the examples
mainly convey is the *format*, the *label space* and the *distribution of inputs* —
not the input-to-label mapping itself. This is a useful corrective to the
assumption that the model is reasoning from your examples.

## Real-World Usage

Standard practice: two or three examples in a prompt to pin down output format,
tone or edge-case handling. It is the cheapest form of adaptation available, and
the first thing to try before fine-tuning. Instruction-tuned models made zero-shot
work well for most tasks, so few-shot is now used mainly for format control and
unusual tasks.

## Common Confusions

* **It is not learning** — nothing persists. The next request starts from the same
  weights, knowing nothing about this one.
* **In-context learning vs fine-tuning** — conditioning versus parameter updates.
  Free and temporary versus expensive and permanent.
* **More examples is not monotonically better** — beyond a handful, returns
  diminish while cost and latency grow with every token.
* **Example order matters** — sometimes substantially, which is an unsatisfying
  but well-documented sensitivity.

## Why Should I Care?

It is the mechanism behind almost everything people do with prompts, and knowing
that examples mostly convey *format* rather than *reasoning* changes how you
write them.

---
title: World Model vs Foundation Model
question: Predicting what happens next, or predicting what is said next?
sides: [world-model, foundation-model]
---

## The short version

A foundation model predicts the next token in a corpus. A world model predicts
the next *state of an environment given an action*. Both are prediction; only one
is conditioned on doing something, and that difference is the crux of the largest
open argument about where AI is heading.

## Side by side

| | Foundation model | World model |
|---|---|---|
| **Predicts** | The next token | The next state, given an action |
| **Trained on** | Text, images — recorded human output | Interaction, video, sensor streams |
| **Conditioned on** | Prior context | Prior state *and* a chosen action |
| **Used for** | Generation, reasoning, answering | Planning, control, evaluating actions |
| **Knows about** | What has been described | What tends to happen |
| **Evaluated by** | Benchmarks, human preference | Task success in an environment |
| **Failure** | A plausible falsehood | A plan that does not survive contact |

## The claim each makes

```text
FOUNDATION MODEL
  everything worth knowing has been written down somewhere
  learn to predict it, and capability follows

WORLD MODEL
  most of what a child knows was never written down
  learn to predict consequences, and understanding follows
```

## Why this is a genuine dispute, not a definitional one

The world-model position — associated with LeCun and the JEPA line — argues that
text is a lossy shadow of reality, that predicting it cannot yield physical
intuition or planning, and that intelligence requires a model of dynamics. The
foundation-model position points at the capability that emerged from text alone
and notes it repeatedly exceeded what anyone predicted.

Neither has been settled by evidence. This is a live disagreement between serious
people, and the encyclopedia's job is to report it rather than pick a winner.

## Where the terms get muddled

"World model" is increasingly applied to **video generation** systems, on the
grounds that plausible footage implies physical understanding. That is a
different and much weaker claim: generating video is not the same as having an
action-conditioned model usable for control. When you meet the term, ask whether
the model is used for *planning* or only for *generation*.

The other muddle is the assertion that LLMs have "internal world models". Some
evidence exists for learned structure in specific narrow domains; extrapolating
that to physical dynamics is contested.

## They are not mutually exclusive

Vision-language-action models take a foundation model's semantic knowledge and
attach it to control. That combination — web-scale knowledge plus grounded action
— is currently the most productive synthesis of the two positions.

## Verdict

Foundation models are the demonstrated path to broad competence over recorded
knowledge. World models are the most credible technical argument that this is not
sufficient for physical intelligence. Follow both; be sceptical of any product
using the second term while doing only the first.

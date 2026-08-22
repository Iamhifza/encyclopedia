---
term: Turing Test
aliases: [Imitation Game, Turing's Test]
category: history
subcategory: origins
depth: full
status: historical
difficulty: beginner
one_liner: "Turing's 1950 proposal to replace \"can machines think?\" with whether a machine's replies are distinguishable from a person's."
origin:
  year: 1950
  attribution: Alan Turing, "Computing Machinery and Intelligence"
historical_period: early-computing
tags: [history]
relations:
  related_to: [large-language-model, benchmark, symbolic-ai]
encountered_in: [research-papers, conferences, social-media]
sources:
  - type: paper
    title: "Computing Machinery and Intelligence"
    url: https://academic.oup.com/mind/article/LIX/236/433/986238
    year: 1950
  - type: paper
    title: "Minds, Brains, and Programs (the Chinese Room)"
    url: https://www.cambridge.org/core/journals/behavioral-and-brain-sciences/article/minds-brains-and-programs/DC644B47A4299C637C89772FACC2706A
    year: 1980
updated: 2026-08-21
---

## Simple Explanation

Turing's move was not to answer "can machines think?" but to declare the question
too vague to be useful and replace it with an operational one: could a machine
hold a text conversation well enough that an interrogator could not reliably tell
it from a person?

Seventy-five years later, that has essentially happened, and the interesting thing
is how little it settled.

## Technical Definition

An interrogator communicates by text with two hidden participants, one human and
one machine, and attempts to identify which is which. If the interrogator performs
no better than chance, the machine is said to pass. Turing proposed it as a
sufficient behavioural criterion, explicitly declining to define thinking itself.

## Why Does It Exist?

Turing anticipated that arguments about machine intelligence would collapse into
definitional disputes about consciousness and understanding — questions with no
agreed test. His proposal was methodological: substitute something observable and
get on with it.

## What Problem Does It Solve?

It made a philosophical question empirical, which is why it has been the reference
point for the entire field's discussion of intelligence ever since.

## How Does It Work?

```text
        interrogator
         /        \
    text          text
      /              \
  human            machine

  question: can the interrogator do better than chance?
```

Text only, deliberately. Turing wanted appearance, voice and physical capability
excluded from the judgement.

## Mental Model

A blind audition. The screen removes everything except the performance — and the
argument since 1950 has been about whether performance is the right thing to
judge.

## Example

The paper is more interesting than its reputation. Turing anticipated and answered
nine objections, including the theological, the mathematical (Gödel), and the
argument from consciousness — to which he replied that by the same standard we
cannot verify consciousness in other people either, and do not usually insist on
it. He also predicted that by 2000 a machine would fool an average interrogator
about 30% of the time in a five-minute conversation, and that the language of
"machines thinking" would by then have become unremarkable. Both were closer to
right than most predictions of that era.

## Real-World Usage

Not used as an evaluation. Modern benchmarks measure specific capabilities —
reasoning, coding, retrieval — because those are actionable and the Turing Test is
not: it measures a model's ability to *imitate*, including imitating human error,
hesitation and ignorance, which is orthogonal to usefulness.

## Common Confusions

* **Passing it is not evidence of understanding** — Searle's Chinese Room argues
  that symbol manipulation producing correct output does not constitute
  comprehension. The argument remains contested and unresolved.
* **It has arguably been passed** — and rather than settling anything, this shifted
  the discussion. That in itself is evidence the test measured something narrower
  than intelligence.
* **Turing did not claim it defined thinking** — he explicitly refused to define
  it, which is often forgotten by people invoking his name on either side.

## Why Should I Care?

It is where the field's central question was first posed carefully, and the fact
that we now build systems which pass it while still arguing about what they
understand is the clearest evidence that the question was never really about
behaviour.

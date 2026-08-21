---
title: Harness vs Scaffold
question: Do these two words mean different things, or is one just newer?
sides: [harness, scaffold]
---

## The honest answer

They overlap heavily, no standards body defines either, and plenty of competent
engineers use them interchangeably. Anyone who tells you there is a crisp
technical distinction is describing their team's convention, not the field's.

That said, there is a discernible centre of gravity to each.

## The tendency, where one exists

| | Scaffold | Harness |
|---|---|---|
| **Leans toward** | Prompt structure and control flow that shapes reasoning | The runtime that executes: tools, permissions, budgets |
| **Metaphor implies** | Temporary support, removed as models improve | Permanent apparatus that constrains and connects |
| **Other major usage** | Evaluation: apparatus used to elicit capability | Evaluation: the rig that runs and scores a benchmark |
| **Typical sentence** | "Model X under this scaffold scores 62%" | "Our harness caps the loop at 20 steps" |

## The collision worth knowing about

Both words have a second, established meaning in evaluation, and the two meanings
point in opposite directions:

* **Evaluation harness** — code that *measures* a model (`lm-evaluation-harness`).
* **Agent harness** — code that *runs* a model in production.

"We improved the harness" is genuinely ambiguous. In an evaluation context assume
the scoring rig; in an agent context assume the runtime.

## Is this evolution or renaming?

Partly both, and it is worth separating the two claims:

* **Genuinely new** — the scope. Designing what a model sees at every step of a
  multi-step loop, with tools, permissions and budgets, is a real engineering
  problem that did not exist when the unit of work was one prompt.
* **Mostly renaming** — the elevation to "harness engineering" as a named
  discipline. Much of what it covers is application engineering: input
  validation, error handling, permissions, observability, testing.

The SWE-agent result gives the concept its strongest empirical footing: holding
the model fixed and changing only the interface it acts through changed task
success substantially. That finding justifies naming the layer. It does not
require treating it as a new science.

## Verdict

Use whichever word your team uses, define it once in your own documentation, and
when reading someone else's, check whether they mean prompt structure, production
runtime, or evaluation rig. That single question resolves most of the confusion.

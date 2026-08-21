---
title: Prompt Engineering vs Context Engineering
question: New discipline, or new name for the same activity?
sides: [prompt-engineering, context-engineering]
---

## The short version

Same mechanism, much larger scope. Both are decisions about what tokens the model
sees. The difference is that prompt engineering authors one string ahead of time,
while context engineering assembles the whole window dynamically, every step,
under a budget.

## Side by side

| | Prompt engineering | Context engineering |
|---|---|---|
| **Object** | One instruction | The entire context window |
| **Authored** | By hand, in advance | By code, at run time |
| **Includes** | Wording, examples, format | Retrieval, tool results, memory, compaction, ordering |
| **Constraint** | Getting the phrasing right | Token budget, attention degradation, cache hits |
| **Fails as** | Ambiguous instruction | Context exhaustion, dilution, buried information |
| **Optimised for** | Task accuracy | Accuracy, cost and cache hit rate together |

## What actually changed

Agent loops append to the context automatically — tool results, observations,
prior turns — so the window fills whether or not anyone planned for it. Once that
is true, the interesting decisions stop being about wording and start being
about selection, ordering, summarisation and eviction. That is a real change in
the problem, not just in the vocabulary.

## What did not change

The underlying mechanism is identical: conditioning a frozen model on tokens.
Nobody discovered a new lever. Claims that context engineering supersedes prompt
engineering confuse a change of scope with a change of kind — prompt engineering
is now a *component*, specifically the authoring of the stable instruction block.

## The honest summary of the naming chain

```text
prompt engineering → context engineering → agent scaffolding → harness engineering
      2022                2024-25               2024              2025
```

Each step names a genuinely wider scope, and each has also been used
promotionally to make ordinary application engineering sound like new science.
Both readings are fair. The test is whether the term is doing work in the
sentence: "we improved context engineering" is meaningless; "we moved tool
results out of context and into a file the agent re-reads on demand" is not.

## Verdict

Learn prompt engineering — it is still where debugging starts and it is cheap.
Then learn context engineering, because in any system with a loop that is where
quality and cost are actually decided.

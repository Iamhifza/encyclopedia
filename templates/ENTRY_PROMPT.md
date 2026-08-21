# Drafting prompt

Most people expanding a seed entry will want a first draft from a model. This is
the prompt to use. It encodes the house style so drafts arrive close to
publishable instead of generically encyclopedic.

Paste the template below, filling in the term and the existing seed front
matter. **Always verify the output before committing** — models produce
confident, plausible, wrong specifics, which is exactly the failure mode this
project documents under [Hallucination](../content/entries/hallucination.md).

---

## The prompt

````text
You are writing one entry for a technical encyclopedia of AI and computing.

TERM: <term>
EXISTING SEED FRONT MATTER:
<paste the YAML front matter from content/entries/<slug>.md>

Write the prose body only. Do not repeat the front matter. Do not write the
sections One-Line Definition, Related Concepts, Prerequisites, Status,
Difficulty or Further Reading — those are generated from front matter.

Required sections, as `## ` headings, in this order:
  Simple Explanation
  Technical Definition
  Why Does It Exist?
  What Problem Does It Solve?
  How Does It Work?
  Mental Model
  Example
  Real-World Usage
  Common Confusions
  Why Should I Care?

Optional, include only where they genuinely add something:
  Visual Explanation · Formula · Historical Origin · Evolution ·
  Terminology Note · Differences · Where Will I Encounter It?

HOUSE STYLE — follow these exactly:

- Simple Explanation assumes basic computing knowledge and nothing else. No
  jargon that has not been introduced. Two to four short paragraphs at most.
- Technical Definition must be precise enough for a practitioner to act on.
- Why Does It Exist? explains what was painful before this existed. Name the
  specific defect in the previous approach.
- How Does It Work? is step by step. Include an ASCII diagram in a ```text
  block whenever structure, flow or layout is easier to see than to read.
- Mental Model is one analogy that survives contact with the details. Reject
  analogies that break under a follow-up question.
- Example must be concrete: real numbers, real systems, real failure modes.
  "A 32k context on a 70B model needs about 10 GB of KV cache" is right.
  "KV cache can be large" is not.
- Explain every symbol in every formula, as a bullet list under it.
- Common Confusions uses bold lead-ins: **X vs Y** — one or two sentences.
- Total length 500 to 900 words. Dense, not padded.

EDITORIAL RULES — these are not negotiable:

- Where practitioners genuinely disagree about the meaning, add a
  `## Terminology Note` that reports the competing usages with approximate
  dates. Never invent a consensus that does not exist.
- If the term is slang, informal or marketing, say so plainly and separate the
  technical claims from the positioning.
- Do not overstate. If something is early, contested, or has thin evidence,
  write that. Hedged accuracy beats confident wrongness.
- British spelling, sentence case headings, no exclamation marks.
- Do not reproduce text from sources. Paraphrase and cite.
- Prefer prose to bullet lists except in Common Confusions and formula
  variable lists.

At the end, separately from the body, list 2-4 primary sources you are
confident exist — original papers, official specifications, official
documentation or repositories — as YAML for the `sources:` field. Flag any you
are unsure about rather than guessing at a URL.
````

---

## After the draft

1. **Check every number.** Model-generated specifics are the most likely thing
   to be wrong.
2. **Check every source.** Open each URL. `enc lint-links` catches dead ones but
   not invented-but-live ones.
3. Set `depth: full` and today's date in `updated`.
4. Run `enc validate --strict`.
5. Read the Simple Explanation aloud. If it needs a second pass to parse, rewrite
   it.

## Reviewing someone else's draft

The most common problems, in order of frequency:

- Confident specifics that are wrong (numbers, dates, attributions)
- A one-line definition that restates the term instead of explaining it
- A Mental Model analogy that breaks immediately
- Manufactured consensus on a genuinely contested term
- Vague examples that could describe anything
- Sources that look right and do not exist

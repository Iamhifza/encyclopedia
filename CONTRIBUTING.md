# Contributing

Thank you for considering it. This project cares more about a small number of
genuinely useful entries than about coverage, so the bar for a new entry is
deliberately higher than "the term exists".

## Ways to help

| | |
|---|---|
| **Correct an error** | Open an issue or a PR. Factual corrections need a primary source. |
| **Improve an entry** | Better example, clearer diagram, sharper Common Confusions — all welcome. |
| **Add a relationship** | Missing edges are the most common gap. One line of front matter. |
| **Write a new entry** | Read *Does this term deserve an entry?* below first. |
| **Add a comparison** | Two entries people genuinely confuse. |
| **Flag a stale entry** | Anything with `status: emerging` more than a year old is suspect. |

## Set up

```bash
pip install -r requirements.txt
python -m encyclopedia validate --strict   # this is exactly what CI runs
python -m encyclopedia build --serve       # live preview
```

## Two kinds of entry

| | **Seed** | **Full** |
|---|---|---|
| Contains | Name, aliases, one-line definition, relations | The complete treatment |
| Body | None | Ten-plus sections, diagram, worked example, sources |
| Appears in | Search, A-Z, topics, concept graph | Everywhere, plus learning paths |
| Set with | `depth: seed` | `depth: full` (the default) |

A seed is a lookup record — the A-Z dictionary layer described in the project
brief. It is a legitimate contribution on its own, and it is how the corpus
grows breadth without diluting the entries that already have depth. Seeds are
promoted to full over time; `enc todo` ranks them by how connected they are, so
the most useful one to write next is always at the top.

## Adding entries in batches

The queue lives in [`content/backlog.yaml`](https://github.com/OWNER/ai-computing-encyclopedia/blob/main/content/backlog.yaml). Each item
carries enough to stand as a seed entry, so generating them produces real
navigable records rather than empty stubs.

```bash
enc batch --dry-run                  # what would be created
enc batch --limit 20                 # create the next twenty
enc batch --category math-for-ai     # one domain at a time
enc validate --strict                # always, immediately after
```

Adding a term **to the backlog** is the cheapest useful contribution — three
lines, and the term reaches search, the A-Z index and the graph on the next
batch run:

```yaml
  - term: Beam Search
    aliases: [Beam Decoding]
    category: llm-inference
    subcategory: decoding
    status: historical
    difficulty: intermediate
    one_liner: "Keeping several candidate continuations alive at once and returning the best-scoring whole sequence."
    tags: [inference]
    relations: {is_a: [sampling], related_to: [autoregressive-generation]}
```

Every item needs at least one relation. An entry with no edges is invisible to
the graph, and the validator will flag it as an orphan.

### Promoting a seed to full

```bash
enc todo                       # ranked by graph degree
enc promote "Beam Search"      # flips depth and appends the section skeleton
$EDITOR content/entries/beam-search.md
enc validate --strict
```

Drafting with a model? Use [`templates/ENTRY_PROMPT.md`](https://github.com/OWNER/ai-computing-encyclopedia/blob/main/templates/ENTRY_PROMPT.md),
which encodes the house style — then verify every number and every source
yourself. Plausible-and-wrong is the failure mode this project exists to
document.

### A realistic batch session

```bash
enc batch --category multimodal --limit 6   # breadth first
enc validate --strict
enc todo --category multimodal              # then depth, most connected first
enc promote "Speech Recognition"
# ...write it, validate, commit
```

Commit seeds and full entries separately. A PR that adds twenty seeds is easy to
review; a PR that adds twenty seeds and rewrites three entries is not.

## Does this term deserve an entry?

Run it past these seven questions. A term that fails 2 and 3 is a buzzword and
belongs on the [watchlist](https://OWNER.github.io/ai-computing-encyclopedia/meta/watchlist/), not in the corpus.

1. Is it genuinely new, or an old idea renamed?
2. Does it name something a practitioner must be able to talk about?
3. Is it used outside the organisation that coined it?
4. Does it have a stable enough meaning to define?
5. Do different communities use it incompatibly? *(Then say so, don't pick one.)*
6. Is it marketing, slang, or technical vocabulary?
7. Will someone plausibly meet it in a paper, repo, job ad or interview?

Slang and marketing terms **are** in scope when they are culturally significant —
they just get labelled honestly. *Vibe coding* has an entry. "Synergistic
AI-powered transformation" does not.

## Writing an entry

```bash
python -m encyclopedia new "Chunked Prefill" --category llm-inference
```

That scaffolds `content/entries/chunked-prefill.md` with the front matter and
section skeleton. Fill in the TODOs.

### Front matter

Validated against [`schema/entry.schema.json`](https://github.com/OWNER/ai-computing-encyclopedia/blob/main/schema/entry.schema.json). Required:
`term`, `category`, `status`, `difficulty`, `one_liner`, `updated`.

Relationships are declared **once**, from whichever side reads naturally. The
build derives every inverse edge — declare `evolved_into` on the older concept
and the newer one automatically shows *Evolved from*. Do not add both directions.

```yaml
relations:
  is_a: [attention]              # taxonomy
  part_of: [transformer]         # composition
  depends_on: [kv-cache]         # technical dependency
  used_by: [vllm]                # who consumes it
  solves: [kv-cache]             # what problem it addresses
  alternative_to: [rag]          # competing approach     (symmetric)
  different_from: [context-window]  # confused with       (symmetric)
  evolved_into: [paged-attention]   # historical lineage
  implemented_by: [vllm]         # concrete implementation
  related_to: [decode]           # last resort; prefer a specific edge
```

`prerequisites` is separate and **pedagogical**: what a reader should understand
first. It must be acyclic.

### Sections

Required — CI fails without them:

`Simple Explanation` · `Technical Definition` · `Why Does It Exist?` ·
`How Does It Work?` · `Example`

Recommended — CI warns, `--strict` fails:

`What Problem Does It Solve?` · `Mental Model` · `Real-World Usage` ·
`Common Confusions` · `Why Should I Care?`

Optional: `Formula`, `Historical Origin`, `Evolution`, `Terminology Note`,
`Differences`

Two things deliberately have no section of their own:

* **Diagrams** go inside `How Does It Work?`, next to the explanation they
  illustrate, not in a separate block.
* **Where you will meet a term** comes from the `encountered_in` front-matter
  field, which the build renders into the entry footer.

`Differences` is for a contrast that only makes sense inside one entry. When two
concepts are genuinely confused with each other, write a page in
`content/comparisons/` instead — it is reachable from both entries.

**Never hand-write these** — they are generated from front matter and CI will
reject them in the body: One-Line Definition, Related Concepts, Prerequisites,
Status, Difficulty, Further Reading.

### House style

- The **one-line definition** must be readable by someone who has never worked in
  AI. No jargon, no nested clauses, no restating the term.
- The **simple explanation** assumes basic computing knowledge and nothing more.
- The **technical definition** must be precise enough for a practitioner to act
  on.
- Explain **every symbol** in every formula.
- Prefer an **ASCII diagram** to a paragraph describing a diagram.
- Examples should be **concrete**: real numbers, real systems, real failure
  modes. "A 32k context on a 70B model needs ~10 GB of KV cache" beats "KV cache
  can be large".
- Comparisons state what each option **optimises for**, never which is "better".
- Report disagreement rather than resolving it. If two communities use a term
  differently, write a `Terminology Note` saying so, with dates.

### Sources

Cite at least one, best first, using this order of preference:

1. Original research papers
2. Official specifications and standards
3. Official documentation
4. Official repositories
5. Technical reports from the organisation that built the thing
6. High-quality secondary explanations
7. Community discussion — acceptable **only** for emerging terminology, labelled
   as such

Paraphrase and link. Do not paste text from sources.

### Dates, eras and staleness

Set `updated` to the date you last checked the entry against reality.

Two further fields are effectively required, and the validator warns without
them:

* **`historical_period`** — which era the concept belongs to. Without it the
  entry is invisible in the timeline view, which is a silent failure rather than
  a loud one.
* **`review_by`** — mandatory in practice for any entry whose status is
  `emerging`, `modern`, `contested`, `slang`, `marketing` or `experimental`.
  Fast-moving terminology goes stale quietly, and the monthly staleness workflow
  can only flag entries that carry a date.

Foundational and historical entries rarely need a review date: the perceptron is
not going to change.

## Pull request checklist

- [ ] `python -m encyclopedia validate --strict` passes
- [ ] The entry cites at least one primary source
- [ ] Relationships declared in one direction only
- [ ] Contested terms carry `status: contested` (or `disputed: true`) and a
      `Terminology Note`
- [ ] No claims of consensus where none exists
- [ ] Examples are concrete and, where numeric, checkable
- [ ] `updated` reflects today

## Review standards

Entries are reviewed for accuracy, honesty about uncertainty, and whether they
help someone who has never heard the term. A well-written entry about a term that
should not be in the encyclopedia will still be declined — with an explanation,
and usually with an invitation to add it to the watchlist.

## Code of conduct

Participation is governed by the [Code of Conduct](https://github.com/OWNER/ai-computing-encyclopedia/blob/main/CODE_OF_CONDUCT.md).

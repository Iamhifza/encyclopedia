# The AI &amp; Computing Encyclopedia

[![Validate](https://github.com/Iamhifza/encyclopedia/actions/workflows/ci.yml/badge.svg)](https://github.com/Iamhifza/encyclopedia/actions/workflows/ci.yml)
[![Deploy](https://github.com/Iamhifza/encyclopedia/actions/workflows/deploy.yml/badge.svg)](https://github.com/Iamhifza/encyclopedia/actions/workflows/deploy.yml)
[![Content: CC BY-SA 4.0](https://img.shields.io/badge/content-CC%20BY--SA%204.0-1f6f63)](LICENSE-CONTENT)
[![Code: MIT](https://img.shields.io/badge/code-MIT-1f6f63)](LICENSE)

**A map of AI and computing concepts — not a glossary.** Every concept gets one
canonical entry that answers *what is this*, and then keeps going: why it exists,
what it replaced, what replaced it, what it is confused with, and where you will
actually meet it.

> 📖 **[Read it here](https://Iamhifza.github.io/encyclopedia)** ·
> 🕸️ **[Concept graph](https://Iamhifza.github.io/encyclopedia/graph/)** ·
> 🔌 **[JSON API](https://Iamhifza.github.io/encyclopedia/api/)**

---

## What makes this different from a glossary

A glossary tells you what a term means. This tells you why the term exists.

Take **KV Cache**. The entry gives you a one-sentence definition, then the memory
arithmetic (10 GB for a single 32k-token request on a 70B model), then why that
number is the reason PagedAttention, prefix caching and grouped-query attention
all exist, then how it differs from a context window, then the four things people
routinely confuse it with, then where to read the original paper. And the same
entry is reachable from the A-Z index, its domain page, the inference learning
path, the timeline and the concept graph — **one canonical record, many routes
in.**

## Eight views over one dataset

| View | Question it answers |
|---|---|
| **Search** | What does this mean? |
| **Topics** | How is the field organised? |
| **A-Z** | Find this specific term (aliases and acronyms redirect). |
| **Timeline** | How did this evolve? |
| **Concept graph** | How does this connect to everything else? |
| **Compare** | What is the difference between these two things? |
| **Learning paths** | What should I learn next? |
| **System view** | Where does this fit in a real production stack? |

None of these duplicate content. They are projections of the same structured
records in `content/`.

## What is in it today

**196 entries · 1,375 typed relationships · 21 domains · 19 comparison
pages · 19 learning paths · ~93,000 words**

Every entry carries the full treatment — typically 500 to 1,000 words across
ten-plus sections, with an ASCII diagram, worked numbers, explained formulas,
common confusions and cited primary sources. There are no stubs, and the
[coverage page](https://Iamhifza.github.io/encyclopedia/meta/coverage/) reports
the breakdown per domain.

All 21 domains are populated. Inference, agents and safety are deliberately the
deepest, since that is where the vocabulary is densest and worst documented
elsewhere. Every entry sits on at least one learning path and is reachable
through the concept graph — there are no orphans.

## Growing it

The corpus is extended in batches. A queue of candidate terms lives in
`content/backlog.yaml`; each carries a definition and its graph edges, so
generating them produces navigable records rather than stubs.

```bash
enc batch --limit 20            # create seed entries from the backlog
enc todo                        # which seeds most deserve the full treatment
enc promote "Beam Search"       # flip a seed to full and get the section skeleton
```

`enc todo` ranks by graph degree, so the most connected — and therefore most
useful — entry to write next is always at the top. See
[CONTRIBUTING.md](CONTRIBUTING.md#adding-entries-in-batches).

**The corpus is currently complete**: `enc todo` reports no seed entries. New
work means proposing terms for the backlog, correcting existing entries, or
re-reviewing the ones whose `review_by` date has passed.

## Editorial principles

- **One canonical entry per concept.** Categories, paths, timeline and graph are
  views, not copies.
- **Uncertainty is labelled, not smoothed over.** *Harness*, *scaffold*, *agent*
  and *frontier model* genuinely mean different things to different teams. Those
  entries carry a `contested` status and a Terminology Note that reports the
  disagreement instead of inventing a consensus.
- **Slang counts.** *Vibe coding* and *AI slop* shape how engineers talk and
  hire, so they get real entries — clearly labelled `slang`.
- **Primary sources first.** Papers, specifications and official documentation
  before commentary.
- **Dates on everything.** Every entry records when it was last reviewed;
  fast-moving ones carry a re-review deadline that CI reports on.

Full policy: [Editorial standards](https://Iamhifza.github.io/encyclopedia/meta/standards/), generated into the site
from the same policy CI enforces.

## Repository layout

```text
content/                 the source of truth
  entries/<slug>.md      one canonical entry: YAML front matter + prose
  backlog.yaml           the queue: terms awaiting entries, ready for `enc batch`
  taxonomy.yaml          21 domains and their subcategories
  timeline.yaml          eras and dated events
  learning-paths.yaml    ordered routes through entries
  comparisons/           side-by-side pages
schema/                  JSON Schema the front matter is validated against
tools/encyclopedia/      loader, validator, graph, site generator, CLI
templates/               drafting prompt encoding the house style
theme/                   stylesheet and the concept-graph explorer
build/                   generated; never edited by hand, never committed
```

## Quick start

```bash
git clone https://github.com/Iamhifza/encyclopedia.git
cd ai-computing-encyclopedia
make install          # python deps into a virtualenv
make check            # validate the corpus
make serve            # live-reload site at http://127.0.0.1:8000
```

No Makefile? Everything is also available directly:

```bash
pip install -r requirements.txt
python -m encyclopedia validate --strict
python -m encyclopedia build --serve
```

## The CLI

```console
$ enc validate --strict        # schema, links, cycles, section contract, staleness
$ enc build --site             # generate build/docs and render static HTML
$ enc new "Speculative Decoding" --category llm-inference
$ enc batch --limit 20         # bulk-create seed entries from the backlog
$ enc todo                     # seeds ranked by how connected they are
$ enc promote "Beam Search"    # seed → full, with the section skeleton
$ enc path attention vllm      # how are two concepts connected?
Attention → Transformer → vLLM
$ enc stats                    # corpus and graph statistics
$ enc lint-links               # check every cited URL still resolves
```

## Use the data, not just the site

Every view is generated from JSON that is published alongside the site, so the
corpus can power your own tools — an editor plugin, a RAG corpus, a Slack bot, a
printed book.

```python
import json, urllib.request

base = "https://Iamhifza.github.io/encyclopedia/api"
data = json.load(urllib.request.urlopen(f"{base}/entries.json"))

kv = next(e for e in data["entries"] if e["slug"] == "kv-cache")
print(kv["one_liner"])
print(kv["derived_relations"]["solved_by"])   # ['paged-attention', 'grouped-query-attention']
```

Available: `entries.json`, `graph.json`, `search-index.json`, `aliases.json`,
`taxonomy.json`, `learning-paths.json`, `timeline.json`, `comparisons.json`,
`stats.json`.

## Contributing

New entries, corrections and better sources are all welcome. The bar is
explained in [CONTRIBUTING.md](CONTRIBUTING.md); the short version:

```bash
enc new "Chunked Prefill" --category llm-inference   # scaffolds the file
$EDITOR content/entries/chunked-prefill.md           # fill the TODOs
enc validate --strict                                # CI runs exactly this
```

CI validates the schema, every relationship target, prerequisite cycles, the
section contract, alias collisions and citation presence. If `enc validate
--strict` passes locally, it passes in CI.

Not sure a term deserves an entry? Add it to the
[watchlist](https://Iamhifza.github.io/encyclopedia/meta/watchlist/) with a note instead — the project
tries hard not to become a buzzword dump.

## Publishing your own copy

1. Create an empty repository on GitHub.
2. `./scripts/bootstrap.sh <your-github-username> <repo-name>` — rewrites the
   `OWNER` placeholders, initialises git and makes the first commit.
3. `git push -u origin main`
4. In **Settings → Pages**, set the source to **GitHub Actions**.

The deploy workflow builds and publishes the site on every push to `main`.

## Licence

Content is [CC BY-SA 4.0](LICENSE-CONTENT). Code and tooling are
[MIT](LICENSE). Cited papers, specifications and documentation remain the
property of their authors; entries paraphrase and link rather than reproduce.

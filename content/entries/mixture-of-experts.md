---
term: Mixture-of-Experts
aliases: [MoE, Sparse MoE, Expert Routing, Sparse Mixture-of-Experts]
category: deep-learning
subcategory: architectures
depth: full
status: modern
difficulty: advanced
one_liner: "A model that holds many specialised sub-networks but activates only a couple per token, so capacity grows without cost growing with it."
tags: [architecture, inference]
relations:
  part_of: [transformer]
  depends_on: [feed-forward-network]
  related_to: [scaling-laws, tensor-parallelism, decode, kv-cache]
prerequisites: [transformer]
encountered_in: [research-papers, github, production-systems, job-descriptions]
sources:
  - type: paper
    title: "Outrageously Large Neural Networks: The Sparsely-Gated Mixture-of-Experts Layer"
    url: https://arxiv.org/abs/1701.06538
    year: 2017
  - type: paper
    title: "Switch Transformers: Scaling to Trillion Parameter Models with Simple and Efficient Sparsity"
    url: https://arxiv.org/abs/2101.03961
    year: 2021
  - type: paper
    title: "Mixtral of Experts"
    url: https://arxiv.org/abs/2401.04088
    year: 2024
  - type: paper
    title: "DeepSeekMoE: Towards Ultimate Expert Specialization"
    url: https://arxiv.org/abs/2401.06066
    year: 2024
updated: 2026-08-21
review_by: 2027-02-01
---

## Simple Explanation

A dense model puts every token through every parameter. That is wasteful: most of
what the model knows is irrelevant to any particular token. A mixture-of-experts
layer instead holds many parallel sub-networks — the experts — and a small router
that picks two or three of them for each token. The model can hold enormous
knowledge while any single token only pays for the fraction it touches.

The result is a strange but useful asymmetry: the model is huge to *store* and
cheap to *run*.

## Technical Definition

A layer replacing the Transformer's feed-forward block with $N$ parallel expert
networks and a gating function that routes each token to the top-$k$ experts,
typically $k = 1$ or $2$. Output is the weighted sum of the selected experts'
outputs. *Total* parameters scale with $N$; *active* parameters per token scale
with $k$. An auxiliary load-balancing loss is required to prevent the router
collapsing onto a few favoured experts.

## Why Does It Exist?

Scaling laws say capability grows with parameters, but dense scaling makes every
forward pass proportionally more expensive — in training and, far more painfully,
in inference for the model's entire deployed life. MoE breaks that coupling: you
can buy the capability of a much larger model while paying compute closer to a
much smaller one.

## What Problem Does It Solve?

The cost of scale. It also gives capacity a place to go: different experts
empirically specialise, so knowledge that would otherwise compete for the same
weights can occupy separate ones.

## How Does It Work?

```text
                    token
                      │
                  ┌───▼────┐
                  │ router │   small linear layer → softmax over N experts
                  └───┬────┘
          scores: [0.01 0.62 0.03 0.31 ... ]
                      │ keep top-2
        ┌─────────────┼─────────────┐
        ▼             ▼             ▼
   expert 1      EXPERT 2      EXPERT 4        (only these two run)
   (skipped)     w=0.62        w=0.31
        └─────────────┼─────────────┘
                 weighted sum
                      │
                      ▼  back into the residual stream
```

Routing happens per token *and* per layer, so a single sentence spreads across
many different experts as it moves up the stack. Each expert must have capacity
limits, because if too many tokens choose the same one, the surplus is dropped
or overflowed to the next choice.

## Mental Model

A hospital rather than a single general practitioner. The building holds
cardiologists, radiologists and anaesthetists, but a given patient sees two of
them. Staffing the whole hospital is expensive; treating one patient is not.

## Formula

$$y = \sum_{i \in \text{top-}k} g_i(x) \cdot E_i(x), \qquad g(x) = \operatorname{softmax}(W_r x)$$

* $E_i$ — the $i$-th expert, usually an ordinary feed-forward network.
* $g_i(x)$ — the router's weight for expert $i$, from a softmax over its scores.
* $W_r$ — the router's parameters, tiny compared with any single expert.
* top-$k$ — how many experts run per token; everything else contributes nothing
  and costs nothing.

The load-balancing loss added to training is roughly $\alpha \cdot N \sum_i f_i P_i$,
where $f_i$ is the fraction of tokens routed to expert $i$ and $P_i$ the mean
router probability for it. Without this term, the router discovers a small set of
strong experts early and starves the rest — a self-reinforcing collapse.

## Example

Mixtral 8x7B holds eight experts per layer and routes each token to two. Total
parameters are about 47B — not 56B, because attention layers are shared, not
duplicated — while roughly 13B are active per token. It therefore needs the memory
of a 47B model and delivers throughput closer to a 13B one.

This is why "how many parameters?" has become an ambiguous question. A model card
saying *671B total, 37B active* is describing an MoE, and those two numbers
predict completely different things: the first your GPU bill for memory, the
second your speed.

## Real-World Usage

Widely adopted at the frontier and in open weights: Mixtral, DeepSeek, Qwen and
others ship MoE variants. DeepSeekMoE popularised finer-grained experts plus a
few *shared* experts that every token uses, which improves specialisation among
the rest.

Serving an MoE is its own discipline. The weights still must all be resident, so
memory capacity is unchanged from a dense model of the same total size. Because
different tokens in a batch want different experts, deployments use **expert
parallelism** — experts distributed across devices — which turns routing into
network traffic. Poorly balanced batches leave GPUs idle waiting for whichever
expert is oversubscribed.

## Historical Origin

The idea dates to 1991 as "adaptive mixtures of local experts". Shazeer et al.
brought it to modern deep learning in 2017 with a sparsely-gated layer between
LSTM layers; Switch Transformer (2021) simplified it to top-1 routing and pushed
past a trillion parameters. Mixtral (2024) made a strong MoE openly available and
the design became mainstream.

## Common Confusions

* **Total vs active parameters** — the single most misread number in current
  model cards. Total sets memory; active sets compute.
* **Experts are not topic specialists** — routing is learned per token and per
  layer, and inspection rarely finds an interpretable "biology expert". The
  specialisation is real but not human-legible.
* **MoE is not cheaper to serve overall** — it saves arithmetic, not memory. On
  memory-bandwidth-bound decode, benefit depends on how much of the model must be
  read per token.
* **MoE vs ensembling** — an ensemble runs several models and combines outputs.
  MoE picks a subset *inside* one model and runs only those.
* **Fine-tuning is trickier** — routing distributions shift under fine-tuning, and
  MoEs have historically been more sensitive to instability than dense models.

## Why Should I Care?

It is why parameter count stopped meaning what it used to. When you compare two
models, or size hardware for one, the total-versus-active distinction changes the
answer by an order of magnitude — and nearly every frontier-scale model released
since 2024 is built this way.

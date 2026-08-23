---
term: Virtual Memory
aliases: [Paging, Page Table, Address Translation, Demand Paging]
category: computing-foundations
subcategory: memory
depth: full
status: foundational
difficulty: intermediate
one_liner: "The trick of giving each program its own tidy address space while the real memory underneath is scattered and shared."
historical_period: early-computing
tags: [hardware]
relations:
  evolved_into: [paged-attention]
  part_of: [memory-hierarchy]
  related_to: [operating-system, cpu]
prerequisites: [memory-hierarchy]
encountered_in: [interviews, technical-blogs, production-systems]
sources:
  - type: book
    title: "Operating Systems: Three Easy Pieces — virtualisation of memory"
    url: https://pages.cs.wisc.edu/~remzi/OSTEP/
  - type: paper
    title: "Efficient Memory Management for Large Language Model Serving with PagedAttention"
    url: https://arxiv.org/abs/2309.06180
    year: 2023
    note: The same idea, rediscovered for the KV cache half a century later.
updated: 2026-08-21
---

## Simple Explanation

Every program believes it has a large, contiguous block of memory starting at
address zero. None of them do. The operating system hands out fixed-size pages
from wherever physical memory happens to be free, and a translation table
maintains the illusion.

This 1960s idea is worth understanding for a specific modern reason: it is
exactly what PagedAttention did to the KV cache in 2023, and knowing the original
makes the AI version obvious rather than clever.

## Technical Definition

An abstraction mapping per-process virtual addresses to physical frames through a
page table, with translation accelerated in hardware by the TLB. It provides
isolation between processes, permits physical memory to be non-contiguous,
enables sharing of identical pages between processes, and allows pages to be
evicted to disk and faulted back on demand.

## Why Does It Exist?

Three problems at once. Programs must not be able to read each other's memory.
Allocating contiguous physical blocks fragments memory until large allocations
fail despite plenty of free space in total. And programs sometimes need more
memory than physically exists.

## What Problem Does It Solve?

Fragmentation, isolation, sharing, and overcommitment.

## How Does It Work?

```text
process A virtual        page table          physical memory
[0][1][2][3]        ──▶  0→17  1→04     ┌──┬──┬──┬──┬──┬──┬──┐
                         2→39  3→12     │17│04│39│12│88│05│..│
process B virtual                       └──┴──┴──┴──┴──┴──┴──┘
[0][1]              ──▶  0→17  1→04       ▲  ▲
                                          └──┴── shared, copy-on-write
```

Two processes can point at the same physical page until one writes, at which
point it is copied. That is copy-on-write, and it is why forking a process is
cheap.

## Mental Model

A cloakroom. You hold a ticket, not a location. The attendant may move your coat
anywhere; your ticket still works.

## Example

The direct lineage to AI: vLLM's PagedAttention takes this design wholesale.
Block table = page table. KV cache blocks = pages. Shared system prompts across
requests = copy-on-write page sharing. Internal fragmentation limited to the last
partial block = exactly the classical result. The paper says so explicitly, and
it produced multiple-fold throughput gains in LLM serving from a mechanism
operating systems have used since the 1960s.

## Real-World Usage

Every general-purpose operating system, continuously and invisibly. In AI
infrastructure it shows up wherever memory is over-subscribed: host memory
offload for KV cache and optimiser state, memory-mapped model weights so a large
file need not be read into RAM in full, and copy-on-write when a data loader
forks worker processes.

## Common Confusions

* **Virtual memory is not swap** — swapping (paging to disk) is one thing the
  mechanism enables. The address translation is the core idea and operates
  entirely in RAM.
* **Pages are not cache lines** — pages are typically 4 KB and managed by the OS;
  cache lines are 64 bytes and managed by hardware.
* **GPUs have their own memory management** — accelerator memory is a separate
  space, which is why moving data between host and device is explicit and
  expensive.

## Why Should I Care?

It is the clearest example in this encyclopedia of a decades-old systems idea
solving a brand-new problem unchanged. If you know virtual memory, you already
understood PagedAttention before you read about it — and that pattern repeats
constantly in AI infrastructure.

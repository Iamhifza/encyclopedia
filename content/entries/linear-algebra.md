---
term: Linear Algebra
aliases: [Matrices, Vectors, Matrix Multiplication, Tensors, Dot Product]
category: math-for-ai
subcategory: linear-algebra
depth: full
status: foundational
difficulty: beginner
one_liner: "The mathematics of vectors and matrices, which is what a neural network is doing in essentially every operation."
historical_period: pre-computing
tags: [training]
relations:
  used_by: [neural-network, attention, embedding, gpu]
  related_to: [probability, gradient-descent, quantization]
encountered_in: [research-papers, interviews, technical-blogs]
sources:
  - type: book
    title: "Introduction to Linear Algebra (Strang)"
    url: https://math.mit.edu/~gs/linearalgebra/
  - type: book
    title: "Deep Learning, ch. 2"
    url: https://www.deeplearningbook.org/
    year: 2016
updated: 2026-08-21
---

## Simple Explanation

Strip away the vocabulary and a neural network does one thing repeatedly:
multiply a list of numbers by a grid of numbers to get another list. That is a
matrix-vector product, and it is roughly 99% of the arithmetic in training and
inference.

You do not need much of the subject. You need to be fluent with a handful of
ideas — vectors as points, matrices as transformations, and what the shapes must
be for the multiplication to work at all.

## Technical Definition

The study of vector spaces and linear maps between them. In deep learning the
working subset is: vectors as elements of $\mathbb{R}^n$, matrices as linear
transformations, matrix multiplication as composition of those transformations,
dot products as similarity, and tensors as the multi-dimensional generalisation
that frameworks operate on.

## Why Does It Exist?

Because it is the natural language for anything with many interacting quantities,
and because linear operations are the ones we can compute efficiently at scale.
Every non-linearity in a network sits between two linear operations, not the
other way round.

## What Problem Does It Solve?

It gives a compact notation and, crucially, an efficient implementation: a matrix
multiply maps directly onto hardware built to do exactly that.

## How Does It Work?

```text
one layer, in full:

  x       (batch 32, features 512)
  W       (512, 2048)
  x @ W   (32, 2048)        ← every output is a weighted sum of every input

the shapes must chain:
  (32,512) @ (512,2048) @ (2048,512) ──▶ (32,512)
        inner dimensions match, outer dimensions survive
```

Nearly every error in framework code is a shape error, and reading shapes is the
practical skill this subject buys you.

## Mental Model

A matrix is a machine that takes a point and moves it — rotating, stretching,
projecting. A network is a long chain of such machines with a small bend applied
between each pair.

## Formula

Attention, written entirely in these terms:

$$\operatorname{softmax}\!\left(\frac{QK^\top}{\sqrt{d_k}}\right)V$$

* $QK^\top$ — every query dotted with every key: a matrix of similarities.
* Division by $\sqrt{d_k}$ — a scalar, keeping the values in a useful range.
* Multiplication by $V$ — a weighted sum of value vectors.

Three matrix operations and a normalisation. The most consequential mechanism in
modern AI is an undergraduate exercise in notation.

## Example

The dot product carries most of the intuition. $a \cdot b$ is large when two
vectors point the same way. That single fact underpins attention scores,
embedding similarity, retrieval ranking and classification logits — all of them
are asking "how aligned are these two directions?".

## Real-World Usage

Every forward and backward pass. It also explains the hardware: GPUs and NPUs
exist because matrix multiplication parallelises perfectly, and quantisation works
because these operations tolerate reduced precision better than most numerical
code.

## Common Confusions

* **Tensor (ML) vs tensor (physics)** — in deep learning it just means a
  multi-dimensional array. No physical or geometric meaning is implied.
* **Row-major versus column-major, and transposes** — the source of most
  frustration when reading unfamiliar implementations.
* **You need less than you fear** — matrix multiplication, transposes, shapes and
  dot products cover the great majority of practice. Eigenvectors and
  decompositions matter for particular methods, not for reading model code.

## Why Should I Care?

It is the layer at which every model is actually specified. Once you can read
shapes, papers stop being intimidating — an architecture diagram becomes a
sequence of transformations you can follow.

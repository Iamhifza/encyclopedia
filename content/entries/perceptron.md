---
term: Perceptron
aliases: [Rosenblatt Perceptron, Linear Threshold Unit]
category: history
subcategory: connectionism
status: historical
difficulty: beginner
one_liner: The first learning machine that adjusted its own weights from examples instead of being programmed with rules.
origin:
  year: 1958
  attribution: Frank Rosenblatt, Cornell Aeronautical Laboratory
historical_period: early-computing
diagram:
  kind: flow
  title: Weighted sum, threshold, and a rule for being wrong
  footer: Minsky and Papert showed in 1969 that a single one cannot learn XOR, and funding collapsed.
    The fix — stacking them with a differentiable non-linearity — needed backpropagation, which took another
    seventeen years.
  nodes:
  - title: Inputs
    note: x₁ x₂ x₃
    caption: numbers
  - title: Weighted sum
    note: Σ wᵢxᵢ + b
    caption: one number
  - title: Threshold
    note: above it, or not
    caption: 0 or 1
  - title: Correction
    note: nudge every w toward the input
    accent: true
    caption: only when wrong
tags: [history, architecture]
relations:
  evolved_into: [neural-network]
  related_to: [supervised-learning]
encountered_in: [research-papers, interviews, conferences]
sources:
  - type: paper
    title: "The Perceptron: A Probabilistic Model for Information Storage and Organization in the Brain"
    url: https://psycnet.apa.org/record/1959-09865-001
    year: 1958
  - type: book
    title: "Perceptrons (Minsky & Papert)"
    url: https://mitpress.mit.edu/9780262534772/perceptrons/
    year: 1969
    note: The critique that helped stall connectionist research for a decade.
updated: 2026-08-21
---

## Simple Explanation

A perceptron takes several numbers in, multiplies each by an importance value,
adds them up, and fires if the total crosses a threshold. What made it famous is
that nobody sets those importance values by hand. You show it examples, it gets
some wrong, and each mistake nudges the numbers in the direction that would have
been correct.

## Technical Definition

A binary linear classifier computing `y = step(w·x + b)`, trained by the
perceptron learning rule: on a misclassified example, update `w ← w + η·(t − y)·x`.
The perceptron convergence theorem guarantees that if the training set is
linearly separable, this procedure terminates in a finite number of updates.

## Why Does It Exist?

Rosenblatt wanted a physical model of how a nervous system could learn
associations without a programmer specifying them. The Mark I Perceptron was
literal hardware: photocells, potentiometers for weights, and motors that turned
those potentiometers during training.

## What Problem Does It Solve?

Programming by rules requires knowing the rules. The perceptron replaced that
requirement with labelled examples, establishing the pattern that every later
learning system follows.

## How Does It Work?

1. Compute the weighted sum of the inputs.
2. Output 1 if it exceeds the threshold, else 0.
3. If the output was wrong, add the input vector to the weights (or subtract it).
4. Repeat over the dataset until no mistakes remain.

## Mental Model

A committee vote where each member's vote counts for a different amount, and
after every bad decision the members who backed it lose influence.

## Formula

$$\hat{y} = \operatorname{step}(\mathbf{w} \cdot \mathbf{x} + b)$$

* $\mathbf{x}$ — input feature vector.
* $\mathbf{w}$ — learned weight per feature; how much that feature matters.
* $b$ — bias, shifting the decision boundary away from the origin.
* $\operatorname{step}$ — outputs 1 above zero, 0 below.

## Example

Classify email as spam from two features: count of the word "free" and count of
exclamation marks. Starting from `w = [0, 0]`, a misclassified spam message with
`x = [3, 5]` becomes `w = [3, 5]`. A misclassified legitimate message with
`x = [1, 0]` pulls the first weight back down. After a few passes the weights
encode a line separating the two classes — if such a line exists.

## Real-World Usage

Nobody deploys a single perceptron. It survives as the unit inside every modern
network: replace the step function with a smooth activation, stack the units in
layers, and you have a multilayer perceptron, which is exactly the feed-forward
block inside a Transformer.

## Historical Origin

Rosenblatt, 1958, with US Navy funding and press coverage that promised machines
which would walk and talk. In 1969 Minsky and Papert proved a single perceptron
cannot learn XOR, since XOR is not linearly separable. The critique was
mathematically correct and widely over-read as a verdict on neural networks in
general; funding collapsed for years.

## Evolution

The XOR limitation dissolves with hidden layers, but nobody could train hidden
layers efficiently until backpropagation was popularised in 1986. That is the
whole shape of connectionist history: the idea was right, the training algorithm
and the hardware were missing.

## Common Confusions

* **Perceptron vs neuron** — the perceptron is a crude mathematical caricature of
  a biological neuron, not a model of one.
* **Perceptron vs logistic regression** — nearly the same model; logistic
  regression outputs a calibrated probability and is trained by maximum
  likelihood rather than by the perceptron rule.
* **"Perceptrons cannot solve XOR"** — true of *one* perceptron, false of a
  network of them.

## Why Should I Care?

It is the smallest complete example of the thing every model in this
encyclopedia does: parameters, a forward pass, an error signal, an update. If you
understand the perceptron you can read the rest as elaborations.

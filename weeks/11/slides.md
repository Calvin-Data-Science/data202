---
marp: true
title: "Week 11: Neural Networks"
theme: default
paginate: true
---

# Neural Networks

### DATA 202 · Week 11

---

## Motivation

Some problems are hard to solve with hand-engineered features:
- Image recognition
- Natural language
- Audio

Neural networks **learn representations** from raw data.

---

## The Perceptron

A single neuron:

$$\hat{y} = \sigma\!\left(\sum_i w_i x_i + b\right)$$

- $w_i$: weights (learned)
- $b$: bias
- $\sigma$: activation function (sigmoid, ReLU, tanh)

---

## Feedforward Network

Stack layers of neurons:

```
Input → [Hidden Layer 1] → [Hidden Layer 2] → Output
```

Each layer learns increasingly abstract representations.

---

## Training: Backpropagation

1. Forward pass: compute prediction
2. Compute loss (e.g., cross-entropy)
3. Backward pass: compute gradients via chain rule
4. Update weights with gradient descent

---

## Key Hyperparameters

- Number of layers and neurons
- Learning rate
- Batch size
- Activation functions
- Regularization (dropout, weight decay)

---

## When to Use Neural Networks

- Large datasets
- Complex, unstructured data (images, text, audio)
- When tabular data: often random forests win

---

## Questions to Sit With

- "Black box" opacity — what does that mean for accountability?
- Who can afford to train large neural networks?

---

## This Week

- **Demo:** simple MLP with Keras/PyTorch
- **Lab 11:** image or text classification
- **Reading:** TBD — Chapter 10

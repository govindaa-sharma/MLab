# Overfitting

Symptoms:
- Validation accuracy decreases after a certain epoch
- Training accuracy continues increasing

Causes:
- Model too complex
- Too many training epochs
- Insufficient data

Solutions:
- Use early stopping
- Add dropout
- Reduce model complexity
- Add regularization

---

# Unstable Training

Symptoms:
- Validation metrics fluctuate heavily between epochs

Causes:
- Learning rate too high
- Small batch size
- Poor optimizer configuration

Solutions:
- Reduce learning rate
- Use Adam optimizer
- Increase batch size

---

# Learning Rate Tuning

Learning rate is one of the most important hyperparameters.

Guidelines:
- Too high → unstable training
- Too low → slow learning

Typical ranges:
- 0.0001 – 0.01

---

# Batch Size

Small batch sizes:
- Better generalization
- Slower training

Large batch sizes:
- Faster training
- May hurt generalization
# experiment_ai SDK

Log ML experiments directly to your backend from any Python script.

## Install
```bash
cd sdk
pip install -e .
```

## Set your backend URL
```bash
# Mac / Linux
export EXPERIMENT_AI_URL=https://your-app.onrender.com

# Windows
set EXPERIMENT_AI_URL=https://your-app.onrender.com
```

## Usage
```python
from experiment_ai import Experiment

# Start
exp = Experiment("my_project", "overfitting_test")

# Log hyperparameters
exp.log_params({
    "learning_rate": 0.01,
    "optimizer":     "adam",
    "epochs":        10
})

# Log metrics per step
metrics = [0.70, 0.80, 0.83, 0.81, 0.77]
for i, v in enumerate(metrics):
    exp.log_metric("val_accuracy", v, step=i)

# Log multiple metrics at once
exp.log_metrics({"val_accuracy": 0.83, "loss": 0.42}, step=3)

# End
exp.end()
```

## Context manager (auto-ends even if code crashes)
```python
with Experiment("my_project", "run_1") as exp:
    exp.log_params({"learning_rate": 0.001})
    for i, v in enumerate([0.65, 0.72, 0.78]):
        exp.log_metric("val_accuracy", v, step=i)
```
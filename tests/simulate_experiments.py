# import sys
# import os

# sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# from experiment_ai import Experiment
# import random

# def log_metric_series(exp, metric_name, values):

#     for i, v in enumerate(values):
#         exp.log_metric(metric_name, v, step=i)

# def healthy_experiment():

#     exp = Experiment("testing_project", "healthy_training")

#     exp.log_params({
#         "learning_rate": 0.001,
#         "optimizer": "adam",
#         "batch_size": 32
#     })

#     values = [0.70, 0.78, 0.83, 0.86, 0.88]

#     log_metric_series(exp, "val_accuracy", values)

#     exp.end()

# def overfitting_experiment():

#     exp = Experiment("testing_project", "overfitting_case")

#     exp.log_params({
#         "learning_rate": 0.001,
#         "optimizer": "adam",
#         "batch_size": 32
#     })

#     values = [0.70, 0.80, 0.83, 0.81, 0.77]

#     log_metric_series(exp, "val_accuracy", values)

#     exp.end()

# def unstable_experiment():

#     exp = Experiment("testing_project", "unstable_training_2")

#     exp.log_params({
#         "learning_rate": 0.01,
#         "optimizer": "sgd",
#         "batch_size": 32
#     })

#     values = [0.81, 0.74, 0.85, 0.73, 0.86]

#     log_metric_series(exp, "val_accuracy", values)

#     exp.end()

# def short_experiment():

#     exp = Experiment("testing_project", "short_training")

#     exp.log_params({
#         "learning_rate": 0.001,
#         "optimizer": "adam"
#     })

#     values = [0.70, 0.72]

#     log_metric_series(exp, "val_accuracy", values)

#     exp.end()

# def run_tests():

#     # healthy_experiment()
#     # overfitting_experiment()
#     unstable_experiment()
#     # short_experiment()

# if __name__ == "__main__":
#     run_tests()



import sys
import os
import random

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from experiment_ai import Experiment

def log_metric_series(exp, metric_name, values):

    for i, v in enumerate(values):
        exp.log_metric(metric_name, v, step=i)

def generate_healthy():

    base = 0.65
    values = []

    for i in range(6):
        base += random.uniform(0.03, 0.06)
        values.append(round(base, 3))

    return values

def generate_overfitting():

    values = [0.65, 0.74, 0.80]

    peak = 0.84
    values.append(peak)

    for i in range(2):
        peak -= random.uniform(0.02, 0.05)
        values.append(round(peak,3))

    return values

def generate_unstable():

    values = []

    for i in range(6):
        values.append(round(random.uniform(0.65,0.90),3))

    return values

def generate_short():

    return [0.65, 0.70]

def random_parameters():

    return {
        "learning_rate": random.choice([0.0005,0.001,0.005,0.01]),
        "optimizer": random.choice(["adam","sgd"]),
        "batch_size": random.choice([16,32,64,128])
    }

def create_experiment(i):

    behavior = random.choice([
        "healthy",
        "overfitting",
        "unstable",
        "short"
    ])

    exp = Experiment("testing_project", f"exp_{i}_{behavior}")

    params = random_parameters()

    exp.log_params(params)

    if behavior == "healthy":
        values = generate_healthy()

    elif behavior == "overfitting":
        values = generate_overfitting()

    elif behavior == "unstable":
        values = generate_unstable()

    else:
        values = generate_short()

    log_metric_series(exp,"val_accuracy",values)

    exp.end()

    print(f"Experiment {i} created → {behavior}")


def run_simulation():

    num_experiments = 67

    for i in range(num_experiments):

        create_experiment(i)

if __name__ == "__main__":
    run_simulation()
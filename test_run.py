# from experiment_ai import Experiment

# exp = Experiment(
#     project="phishing-detection",
#     experiment_name="first_sdk_run"
# )

# from experiment_ai import Experiment

# exp = Experiment("demo_project", "params_test")

# exp.log_params({
#     "learning_rate": 0.01,
#     "epochs": 10
# })


# from experiment_ai import Experiment

# exp = Experiment("demo_project", "metric_test")

# exp.log_params({
#     "learning_rate": 0.01,
#     "epochs": 5
# })

# exp.log_metric("accuracy", 0.75, step=1)
# exp.log_metric("accuracy", 0.82, step=2)
# exp.log_metric("accuracy", 0.88, step=3)


# from experiment_ai import Experiment

# exp = Experiment("demo_project", "full_test")

# exp.log_params({
#     "learning_rate": 0.01,
#     "epochs": 3
# })

# exp.log_metric("accuracy", 0.72, step=4)
# exp.log_metric("accuracy", 0.81, step=5)
# exp.log_metric("accuracy", 0.88, step=6)

# exp.end()

# from experiment_ai import Experiment

# exp = Experiment("demo_project", "overfit_test")

# exp.log_params({
#     "learning_rate": 0.01,
#     "epochs": 5
# })

# # training improving
# exp.log_metric("train_accuracy", 0.70, step=1)
# exp.log_metric("train_accuracy", 0.80, step=2)
# exp.log_metric("train_accuracy", 0.90, step=3)

# # validation worsening
# exp.log_metric("val_accuracy", 0.75, step=1)
# exp.log_metric("val_accuracy", 0.70, step=2)
# exp.log_metric("val_accuracy", 0.65, step=3)

# exp.end()


from experiment_ai import Experiment

exp = Experiment("demo", "overfitting_test")

exp.log_params({
    "learning_rate": 0.01,
    "optimizer": "adam"
})

metrics = [0.70,0.80,0.83,0.81,0.77]

for i,v in enumerate(metrics):
    exp.log_metric("val_accuracy", v, step=i)

exp.end()
from .client import start_experiment, log_parameters, log_metric, end_experiment

class Experiment:
    def __init__(self, project, experiment_name):

        result = start_experiment(project, experiment_name)

        self.experiment_id = result["experiment_id"]
        self.status = result["status"]

        print(f"Experiment started with ID: {self.experiment_id}")

    def log_params(self, parameters):
        log_parameters(self.experiment_id, parameters)
        print("Parameters logged")

    def log_metric(self, name, value, step):
        log_metric(self.experiment_id, name, value, step)
        print(f"Logged {name} at step {step}")

    def end(self):
        end_experiment(self.experiment_id)
        print("Experiment completed")
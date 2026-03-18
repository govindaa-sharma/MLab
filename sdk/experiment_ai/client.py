import requests
import os


class Experiment:

    def __init__(self, project: str, experiment_name: str, base_url: str = None):
        """
        Start a new experiment.

        Args:
            project:         Project name e.g. "demo"
            experiment_name: Experiment name e.g. "overfitting_test"
            base_url:        Your Render backend URL.
                             Reads from EXPERIMENT_AI_URL env var if not passed.
        """
        self.project         = project
        self.experiment_name = experiment_name
        self.base_url        = (
            base_url
            or os.getenv("EXPERIMENT_AI_URL", "http://127.0.0.1:8000")
        ).rstrip("/")

        self.experiment_id = None
        self._start()


    def _start(self):
        """Hit POST /experiments/start and store the experiment_id."""
        res = requests.post(
            f"{self.base_url}/experiments/start",
            json={
                "project":         self.project,
                "experiment_name": self.experiment_name
            }
        )
        res.raise_for_status()
        data = res.json()
        self.experiment_id = data["experiment_id"]
        print(f"[experiment_ai] Started — experiment_id: {self.experiment_id}")


    def log_params(self, parameters: dict):
        """
        Log hyperparameters.

        Args:
            parameters: dict of param name → value
                        e.g. {"learning_rate": 0.01, "optimizer": "adam"}
        """
        if not self.experiment_id:
            raise RuntimeError("Experiment not started.")

        res = requests.post(
            f"{self.base_url}/experiments/params",
            json={
                "experiment_id": self.experiment_id,
                "parameters":    parameters
            }
        )
        res.raise_for_status()
        print(f"[experiment_ai] Logged params: {list(parameters.keys())}")


    def log_metric(self, name: str, value: float, step: int = 0):
        """
        Log a single metric value at a given step.

        Args:
            name:  Metric name e.g. "val_accuracy", "loss"
            value: Numeric value e.g. 0.83
            step:  Training step or epoch number (default 0)
        """
        if not self.experiment_id:
            raise RuntimeError("Experiment not started.")

        res = requests.post(
            f"{self.base_url}/experiments/metric",
            json={
                "experiment_id": self.experiment_id,
                "name":          name,
                "value":         float(value),
                "step":          int(step)
            }
        )
        res.raise_for_status()


    def log_metrics(self, metrics: dict, step: int = 0):
        """
        Log multiple metrics at once for the same step.

        Args:
            metrics: dict of metric name → value
                     e.g. {"val_accuracy": 0.83, "loss": 0.42}
            step:    Training step or epoch number (default 0)
        """
        if not self.experiment_id:
            raise RuntimeError("Experiment not started.")

        for name, value in metrics.items():
            self.log_metric(name, value, step=step)

        print(f"[experiment_ai] Logged metrics at step {step}: {list(metrics.keys())}")


    def end(self):
        """Mark the experiment as completed."""
        if not self.experiment_id:
            raise RuntimeError("Experiment not started.")

        res = requests.post(
            f"{self.base_url}/experiments/end",
            json={"experiment_id": self.experiment_id}
        )
        res.raise_for_status()
        print(f"[experiment_ai] Experiment #{self.experiment_id} completed.")


    def __enter__(self):
        """Use as context manager: with Experiment(...) as exp:"""
        return self


    def __exit__(self, exc_type, exc_val, exc_tb):
        """Auto-calls end(). If an exception occurred, still ends cleanly."""
        try:
            self.end()
        except Exception as e:
            print(f"[experiment_ai] Warning: could not end experiment — {e}")
        return False
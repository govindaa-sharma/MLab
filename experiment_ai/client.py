import requests

BASE_URL = "http://127.0.0.1:8000"

def start_experiment(project, experiment_name):
    payload = {
    "project": project,
    "experiment_name": experiment_name
    }

    response = requests.post(
    f"{BASE_URL}/experiments/start",
    json=payload
    )

    return response.json()

def log_parameters(experiment_id, parameters):
    payload = {
    "experiment_id": experiment_id,
    "parameters": parameters
    }
    requests.post(
    f"{BASE_URL}/experiments/params",
    json=payload
    )

def log_metric(experiment_id, name, value, step):
    payload = {
        "experiment_id": experiment_id,
        "name": name,
        "value": value,
        "step": step
    }
    requests.post(
        f"{BASE_URL}/experiments/metric",
        json=payload
    )

def end_experiment(experiment_id):
    payload = {
    "experiment_id": experiment_id
}
    requests.post(
    f"{BASE_URL}/experiments/end",
    json=payload
)
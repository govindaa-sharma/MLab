import requests
import re
import os

BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")

def get_experiment_analysis(experiment_input):

    # Extract number from input (handles "67", "experiment 67", etc.)
    match = re.search(r"\d+", str(experiment_input))

    if not match:
        return {"error": "No experiment id found"}

    experiment_id = int(match.group())

    response = requests.get(
        f"{BASE_URL}/experiments/{experiment_id}/analysis"
    )

    if response.status_code == 200:
        return response.json()

    return {
        "error": f"API error {response.status_code}",
        "details": response.text
    }

def get_parameter_insights(_input=None):

    response = requests.get(
        f"{BASE_URL}/experiments/parameters/analysis"
    )

    if response.status_code != 200:
        return {"error": "Could not retrieve insights"}

    return response.json()

def compare_experiments(exp1: int, exp2: int):

    exp1_data = get_experiment_analysis(exp1)
    exp2_data = get_experiment_analysis(exp2)

    if "error" in exp1_data or "error" in exp2_data:
        return {"error": "Experiment data unavailable"}

    score1 = exp1_data["diagnostics"]["score"]
    score2 = exp2_data["diagnostics"]["score"]

    if score1 > score2:
        better = exp1
    else:
        better = exp2

    return {
        "experiment_1_score": score1,
        "experiment_2_score": score2,
        "better_experiment": better
    }
from collections import defaultdict

from .signal_extractor import extract_signals
from .experiment_diagnostics import diagnose_experiment

def analyze_hyperparameters(experiments, parameters, metrics):
    metrics_by_experiment = defaultdict(list)
                                                
    for metric in metrics:
        metrics_by_experiment[metric.experiment_id].append(metric)
    experiment_scores = {}

    for exp in experiments:

        exp_metrics = metrics_by_experiment.get(exp.id, [])

        if not exp_metrics:
            continue

        signals = extract_signals(exp_metrics)

        diagnosis = diagnose_experiment(signals)

        score = diagnosis.get("score")

        if score is not None:
            experiment_scores[exp.id] = score

    param_performance = defaultdict(list)

    for param in parameters:

        exp_id = param.experiment_id

        if exp_id not in experiment_scores:
            continue

        score = experiment_scores[exp_id]

        key = (param.key, param.value)

        param_performance[key].append(score)

    insights = []

    for (param_name, param_value), scores in param_performance.items():

        avg_score = sum(scores) / len(scores)

        insights.append({
            "parameter": param_name,
            "value": param_value,
            "average_experiment_score": avg_score,
            "num_experiments": len(scores)
        })

    return insights
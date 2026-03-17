from collections import defaultdict

def detect_parameter_type(values):

    numeric_values = []

    for v in values:
        try:
            numeric_values.append(float(v))
        except:
            return "categorical"

    unique_values = set(numeric_values)

    if len(unique_values) > 5:
        return "continuous"

    return "discrete"

def collect_parameter_values(parameters):

    param_values = defaultdict(list)

    for param in parameters:
        param_values[param.key].append(param.value)

    return param_values

def group_parameter_performance(parameters, experiment_scores):

    param_scores = defaultdict(list)

    for param in parameters:

        exp_id = param.experiment_id

        if exp_id not in experiment_scores:
            continue

        score = experiment_scores[exp_id]

        key = (param.key, param.value)

        param_scores[key].append(score)

    return param_scores

def compute_parameter_insights(param_scores):

    insights = []

    for (param, value), scores in param_scores.items():

        avg_score = sum(scores) / len(scores)

        insights.append({
            "parameter": param,
            "value": value,
            "average_score": avg_score,
            "num_experiments": len(scores)
        })

    return insights
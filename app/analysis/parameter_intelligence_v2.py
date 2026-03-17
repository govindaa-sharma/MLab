from collections import defaultdict
import statistics

from collections import defaultdict

def collect_parameter_scores(parameters, experiment_scores):

    param_scores = defaultdict(list)

    for param in parameters:

        exp_id = param.experiment_id

        if exp_id not in experiment_scores:
            continue

        score = experiment_scores[exp_id]

        # skip experiments without score
        if score is None:
            continue

        param_scores[param.key].append(
            (param.value, score)
        )

    return param_scores

def detect_best_value(values_scores):

    groups = {}

    for value, score in values_scores:

        # convert numeric values to float if possible
        try:
            value = float(value)
        except:
            pass

        if value not in groups:
            groups[value] = []

        if score is not None:
            groups[value].append(score)

    avg_scores = {}

    for v, scores in groups.items():

        if not scores:
            continue

        avg_scores[v] = sum(scores) / len(scores)

    if not avg_scores:
        return None, {}

    best_value = max(avg_scores, key=avg_scores.get)

    return best_value, avg_scores

def detect_best_range(values_scores):

    numeric_data = []

    for value, score in values_scores:

        try:
            value = float(value)
        except:
            # not numeric → cannot compute range
            return None

        if score is None:
            continue

        numeric_data.append((value, score))

    if len(numeric_data) < 2:
        return None

    numeric_data.sort()

    scores = [s for _, s in numeric_data]

    best_score = max(scores)

    threshold = best_score * 0.95

    good_values = [
        v for v, s in numeric_data if s >= threshold
    ]

    if not good_values:
        return None

    return min(good_values), max(good_values)


def compute_parameter_importance(values_scores):

    groups = defaultdict(list)

    for value, score in values_scores:
        groups[value].append(score)

    avg_scores = [
        sum(scores)/len(scores)
        for scores in groups.values()
    ]

    if len(avg_scores) < 2:
        return 0

    return statistics.variance(avg_scores)


def analyze_parameters(parameters, experiment_scores):

    param_scores = collect_parameter_scores(
        parameters,
        experiment_scores
    )

    insights = {}

    for param, values_scores in param_scores.items():

        best_value, avg_scores = detect_best_value(values_scores)

        best_range = detect_best_range(values_scores)

        importance = compute_parameter_importance(values_scores)

        insights[param] = {
            "best_value": best_value,
            "best_range": best_range,
            "importance": importance
        }

    return insights
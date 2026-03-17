from .metric_intelligence import detect_primary_metric, get_metric_direction, compute_best_score
import statistics

def group_metrics(metrics):

    grouped = {}

    for metric in metrics:
        name = metric.name

        if name not in grouped:
            grouped[name] = []

        grouped[name].append((metric.step, metric.value))

    for name in grouped:
        grouped[name] = sorted(grouped[name])

    return grouped


def extract_signals(metrics):

    grouped = group_metrics(metrics)

    signals = {}

    metric_names = list(grouped.keys())

    primary_metric = detect_primary_metric(metric_names)

    if not primary_metric:
        return {}

    steps = [s for s, _ in grouped[primary_metric]]
    values = [v for _, v in grouped[primary_metric]]

    direction = get_metric_direction(primary_metric)

    best_score = compute_best_score(values, direction)

    if direction == "maximize":
        best_index = values.index(max(values))
    else:
        best_index = values.index(min(values))

    best_epoch = steps[best_index]

    signals["primary_metric"] = primary_metric
    signals["metric_direction"] = direction
    signals["best_score"] = best_score
    signals["best_epoch"] = best_epoch
    signals["final_score"] = values[-1]
    signals["num_steps"] = len(values)

    # basic stability signal
    if len(values) > 2:
        variance = statistics.pvariance(values)
        signals["training_variance"] = variance

    return signals
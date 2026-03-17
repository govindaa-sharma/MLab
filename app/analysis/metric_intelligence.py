METRIC_DIRECTIONS = {
    "accuracy": "maximize",
    "val_accuracy": "maximize",
    "f1": "maximize",
    "f1_score": "maximize",
    "auc": "maximize",
    "r2": "maximize",
    "r2_score": "maximize",

    "loss": "minimize",
    "val_loss": "minimize",
    "mse": "minimize",
    "rmse": "minimize",
    "mae": "minimize"
}

def get_metric_direction(metric_name):

    if metric_name in METRIC_DIRECTIONS:
        return METRIC_DIRECTIONS[metric_name]

    # default assumption
    return "maximize"

def detect_primary_metric(metric_names):

    # prefer validation metrics
    for name in metric_names:
        if name.startswith("val_"):
            return name

    # otherwise return first metric
    if metric_names:
        return metric_names[0]

    return None

def compute_best_score(values, direction):

    if not values:
        return None

    if direction == "maximize":
        return max(values)

    else:
        return min(values)
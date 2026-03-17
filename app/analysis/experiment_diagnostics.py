def diagnose_experiment(signals):

    diagnosis = {
        "status": "UNKNOWN",
        "issues": [],
        "score": None
    }

    best_score = signals.get("best_score")
    best_epoch = signals.get("best_epoch")
    final_score = signals.get("final_score")
    num_steps = signals.get("num_steps")
    volatility = signals.get("training_volatility")

    # insufficient data
    if num_steps and num_steps < 3:
        diagnosis["status"] = "INSUFFICIENT_DATA"
        diagnosis["issues"].append("Too few training steps")
        return diagnosis

    # unstable training
    if volatility and volatility > 0.08:
        diagnosis["issues"].append("UNSTABLE_TRAINING")

    # overfitting detection
    if best_epoch and num_steps and final_score:

        drop = best_score - final_score

        if best_epoch < (num_steps * 0.6) and drop > 0.02:
            diagnosis["issues"].append("OVERFITTING")

    if diagnosis["issues"]:
        diagnosis["status"] = "ISSUES_DETECTED"
    else:
        diagnosis["status"] = "HEALTHY"

    score = best_score if best_score else 0

    if volatility and volatility > 0.08:
        score -= 0.03

    if best_epoch and num_steps and final_score:
        if best_epoch < (num_steps * 0.6) and (best_score - final_score) > 0.02:
            score -= 0.05

    diagnosis["score"] = score

    return diagnosis
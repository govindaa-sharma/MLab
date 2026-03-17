from .models import Experiment, Parameter, Metric, ExperimentDiagnostics, ExperimentSignal

def create_experiment(db, experiment):
    db_exp = Experiment(
    project=experiment.project,
    experiment_name=experiment.experiment_name
    )

    db.add(db_exp)
    db.commit()
    db.refresh(db_exp)

    return db_exp

def log_parameters(db, param_data):
    for key, value in param_data.parameters.items():
        param = Parameter(
        experiment_id=param_data.experiment_id,
        key=key,
        value=str(value)
        )
        db.add(param)
    db.commit()
    return {"message": "Parameters logged"}

def log_metric(db, metric_data):
    metric = Metric(
    experiment_id=metric_data.experiment_id,
    name=metric_data.name,
    value=metric_data.value,
    step=metric_data.step
    )

    db.add(metric)
    db.commit()
    db.refresh(metric)
    return {"message": "Metric logged"}

def end_experiment(db, experiment_data):
    experiment = db.query(Experiment).filter(
    Experiment.id == experiment_data.experiment_id
    ).first()

    experiment.status = "completed"

    db.commit()
    db.refresh(experiment)

    return {"message": "Experiment completed"}

def get_experiments(db):
    return db.query(Experiment).all()

def get_experiment(db, experiment_id):
    return db.query(Experiment).filter(
        Experiment.id == experiment_id
    ).first()

def get_experiment_parameters(db, experiment_id):
    return db.query(Parameter).filter(
        Parameter.experiment_id == experiment_id
    ).all()

def get_experiment_metrics(db, experiment_id):
    return db.query(Metric).filter(
        Metric.experiment_id == experiment_id
    ).all()

def save_experiment_signals(db, experiment_id, signals):

    signal = ExperimentSignal(
        experiment_id=experiment_id,
        primary_metric=signals.get("primary_metric"),
        best_score=signals.get("best_score"),
        best_epoch=signals.get("best_epoch"),
        final_score=signals.get("final_score"),
        num_steps=signals.get("num_steps"),
        training_variance=signals.get("training_variance")
    )

    db.add(signal)
    db.commit()
    db.refresh(signal)

    return signal

def save_experiment_diagnostics(db, experiment_id, diagnosis):

    diag = ExperimentDiagnostics(
        experiment_id=experiment_id,
        status=diagnosis.get("status"),
        issues=",".join(diagnosis.get("issues", [])),
        experiment_score=diagnosis.get("score")
    )

    db.add(diag)
    db.commit()
    db.refresh(diag)

    return diag
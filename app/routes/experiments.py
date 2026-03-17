from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..schemas import ExperimentCreate, ParameterCreate, MetricCreate, ExperimentEnd
from .. import crud
# from ..analysis.experiment_analyzer import analyze_experiment
from ..analysis.hyperparameter_analyzer import analyze_hyperparameters
from ..models import Parameter, Metric, Experiment
from ..analysis.signal_extractor import extract_signals
from ..analysis.experiment_diagnostics import diagnose_experiment
from ..models import ExperimentSignal, ExperimentDiagnostics
from app.analysis.parameter_intelligence_v2 import analyze_parameters


router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/start")
def start_experiment(
    experiment: ExperimentCreate,
    db: Session = Depends(get_db)
):
    db_exp = crud.create_experiment(db, experiment)
    return {
    "experiment_id": db_exp.id,
    "status": db_exp.status
}

@router.post("/params")
def log_params(
    params: ParameterCreate,
    db: Session = Depends(get_db)
):
    return crud.log_parameters(db, params)

@router.post("/metric")
def log_metirc(
        metric: MetricCreate,
        db: Session = Depends(get_db)
):
    return crud.log_metric(db, metric)

@router.post("/end")
def end_experiment(
    exp: ExperimentEnd,
    db: Session = Depends(get_db)
):
    return crud.end_experiment(db, exp)

@router.get("/")
def get_experiments(db: Session = Depends(get_db)):
    return crud.get_experiments(db)

@router.get("/{experiment_id}")
def get_experiment(experiment_id: int, db: Session = Depends(get_db)):
    return crud.get_experiment(db, experiment_id)

@router.get("/{experiment_id}/parameters")
def get_parameters(experiment_id: int, db: Session = Depends(get_db)):
    return crud.get_experiment_parameters(db, experiment_id)

@router.get("/{experiment_id}/metrics")
def get_metrics(experiment_id: int, db: Session = Depends(get_db)):
    return crud.get_experiment_metrics(db, experiment_id)

# @router.get("/{experiment_id}/analysis")
# def analyze_experiment_route(experiment_id: int, db: Session = Depends(get_db)):

#     metrics = crud.get_experiment_metrics(db, experiment_id)

#     results = diagnose_experiment(metrics)

#     return {
#         "experiment_id": experiment_id,
#         "analysis": results
#     }

@router.get("/analysis/hyperparameters")
def hyperparameter_analysis(db: Session = Depends(get_db)):

    experiments = crud.get_experiments(db)

    parameters = db.query(Parameter).all()

    metrics = db.query(Metric).all()

    results = analyze_hyperparameters(experiments, parameters, metrics)

    return {"hyperparameter_analysis": results}


@router.get("/parameters/analysis")
def get_parameter_insights(db: Session = Depends(get_db)):

    # get all parameters
    parameters = db.query(Parameter).all()

    # get experiment diagnostics
    diagnostics = db.query(ExperimentDiagnostics).all()

    # build experiment score map
    experiment_scores = {
        d.experiment_id: d.experiment_score
        for d in diagnostics
    }

    insights = analyze_parameters(
        parameters,
        experiment_scores
    )

    return {
        "parameter_insights": insights
    }


@router.get("/{experiment_id}/analysis")
def analyze_experiment(experiment_id: int, db: Session = Depends(get_db)):

    # 1️⃣ check if signals already exist
    signals_record = db.query(ExperimentSignal).filter(
        ExperimentSignal.experiment_id == experiment_id
    ).first()

    if signals_record:

        signals = {
            "primary_metric": signals_record.primary_metric,
            "best_score": signals_record.best_score,
            "best_epoch": signals_record.best_epoch,
            "final_score": signals_record.final_score,
            "num_steps": signals_record.num_steps,
            "training_variance": signals_record.training_variance
        }

    else:

        metrics = crud.get_experiment_metrics(db, experiment_id)

        signals = extract_signals(metrics)

        crud.save_experiment_signals(db, experiment_id, signals)

    # 2️⃣ check diagnostics cache
    diag_record = db.query(ExperimentDiagnostics).filter(
        ExperimentDiagnostics.experiment_id == experiment_id
    ).first()

    if diag_record:

        diagnostics = {
            "status": diag_record.status,
            "issues": diag_record.issues.split(",") if diag_record.issues else [],
            "score": diag_record.experiment_score
        }

    else:

        diagnostics = diagnose_experiment(signals)

        crud.save_experiment_diagnostics(db, experiment_id, diagnostics)

    return {
        "experiment_id": experiment_id,
        "signals": signals,
        "diagnostics": diagnostics
    }



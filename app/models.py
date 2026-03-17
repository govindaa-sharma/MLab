from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from datetime import datetime
from .database import Base

class Experiment(Base):
    __tablename__ = "experiments"

    id = Column(Integer, primary_key=True, index=True)
    project = Column(String)
    experiment_name = Column(String)
    status = Column(String, default="started")
    created_at = Column(DateTime, default=datetime.utcnow)

class Parameter(Base):
    __tablename__ = "parameters"

    id = Column(Integer, primary_key=True)
    experiment_id = Column(Integer)
    key = Column(String)
    value = Column(String)

class Metric(Base):
    __tablename__ = "metrics"

    id = Column(Integer, primary_key=True)
    experiment_id = Column(Integer)
    name = Column(String)
    value = Column(Float)
    step = Column(Integer)
    timestamp = Column(DateTime, default=datetime.utcnow)

class ExperimentSignal(Base):
    __tablename__ = "experiment_signals"

    id = Column(Integer, primary_key=True, index=True)

    experiment_id = Column(Integer, ForeignKey("experiments.id"))

    primary_metric = Column(String)

    best_score = Column(Float)

    best_epoch = Column(Integer)

    final_score = Column(Float)

    num_steps = Column(Integer)

    training_variance = Column(Float)

class ExperimentDiagnostics(Base):
    __tablename__ = "experiment_diagnostics"

    id = Column(Integer, primary_key=True, index=True)

    experiment_id = Column(Integer, ForeignKey("experiments.id"))

    status = Column(String)

    issues = Column(String)

    experiment_score = Column(Float)
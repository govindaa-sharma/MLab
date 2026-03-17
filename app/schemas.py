from pydantic import BaseModel

class ExperimentCreate(BaseModel):
    project: str
    experiment_name: str

class ParameterCreate(BaseModel):
    experiment_id: int
    parameters: dict

class MetricCreate(BaseModel):
    experiment_id: int
    name: str
    value: float
    step: int

class ExperimentEnd(BaseModel):
    experiment_id: int
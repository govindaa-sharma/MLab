from app.ai.tools import (
    get_experiment_analysis,
    get_parameter_insights,
    compare_experiments
)

print(get_experiment_analysis(25))

print(get_parameter_insights())

print(compare_experiments(25,30))
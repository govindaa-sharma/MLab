# ◈ Epoché — ML Experiment Tracking Platform

> *Epoché (ἐποχή) — the philosophical act of pausing to examine before concluding.*

An end-to-end machine learning experiment tracking platform with automated diagnostics, hyperparameter intelligence, an AI copilot, and a Python SDK for logging experiments from any machine.

---

## Overview

Epoché is a full-stack ML observability platform built to give data scientists and ML engineers a clear view of what's happening inside their training runs — without the overhead of heavyweight tools like MLflow or Weights & Biases.

Log your experiments via a lightweight Python SDK, get automated diagnostics (overfitting detection, training instability), analyze hyperparameter performance across all experiments, and ask the AI copilot natural language questions about your results.

---

## Features

- **Experiment Tracking** — log parameters, metrics per step, and experiment status from any Python script via the SDK
- **Automated Signal Extraction** — identifies primary metrics, best scores, best epochs, and training variance automatically
- **Experiment Diagnostics** — detects overfitting, unstable training, and insufficient data with no manual intervention
- **Hyperparameter Intelligence** — cross-experiment analysis to surface which parameter values and ranges perform best
- **AI Copilot** — LangGraph agent (Gemini 2.5 Flash) with tool-use to answer natural language questions about your experiments
- **RAG Knowledge Base** — ChromaDB vector store retrieves ML domain knowledge to answer conceptual questions alongside live experiment data
- **Python SDK** — install with pip, set your backend URL, start logging in 3 lines
- **Live Dashboard** — Streamlit dashboard with dark-mode UI, experiment list, signal cards, diagnostics, and interactive Plotly training charts

---

## Architecture

```
┌──────────────────────────────────────────────────────┐
│                   Python SDK                         │
│           experiment_ai · pip installable            │
└──────────────────────┬───────────────────────────────┘
                       │ HTTP
                       ▼
┌──────────────────────────────────────────────────────┐
│                FastAPI Backend                       │
│                                                      │
│  ┌─────────────┐ ┌──────────────┐ ┌───────────────┐  │
│  │  Experiment │ │   Analysis   │ │  AI Copilot   │  │
│  │   Routes    │ │   Engine     │ │  (LangGraph)  │  │
│  └─────────────┘ └──────────────┘ └───────────────┘  │
│                                                      │
│  ┌──────────────────────────────────────────────┐    │
│  │           SQLite · SQLAlchemy ORM            │    │
│  └──────────────────────────────────────────────┘    │
└──────────────────────┬───────────────────────────────┘
                       │ HTTP
                       ▼
┌──────────────────────────────────────────────────────┐
│             Streamlit Dashboard                      │
│  Experiment list · Signals · Diagnostics · Copilot   │
└──────────────────────────────────────────────────────┘
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend API | FastAPI, SQLAlchemy, SQLite |
| AI Agent | LangGraph, LangChain, Gemini 2.5 Flash |
| RAG | ChromaDB, HuggingFace Embeddings (all-MiniLM-L6-v2) |
| Frontend | Streamlit, Plotly |
| SDK | Python, Requests |
| Deployment | Render (backend), Streamlit Cloud (frontend) |

---

## Project Structure

```
epoché/
│
├── app/                                # FastAPI backend
│   ├── ai/
│   │   ├── copilot_agent.py            # LangGraph agent + tool routing + Gemini LLM
│   │   ├── tools.py                    # Agent tools (analysis, params, compare)
│   │   ├── rag_engine.py               # ChromaDB vector store + similarity retrieval
│   │   └── knowledge/                  # ML knowledge base (markdown files)
│   │
│   ├── analysis/
│   │   ├── signal_extractor.py         # Best score, epoch, variance extraction
│   │   ├── experiment_diagnostics.py   # Overfitting + instability detection
│   │   ├── metric_intelligence.py      # Metric direction + primary metric logic
│   │   ├── parameter_intelligence_v2.py # Cross-experiment parameter analysis
│   │   └── hyperparameter_analyzer.py
│   │
│   ├── routes/
│   │   ├── experiments.py              # All experiment + analysis endpoints
│   │   └── copilot.py                  # Copilot query endpoint
│   │
│   ├── crud.py                         # All database read/write operations
│   ├── models.py                       # SQLAlchemy table models
│   ├── schemas.py                      # Pydantic request/response schemas
│   ├── database.py                     # DB engine + session factory
│   └── main.py                         # FastAPI app entry point + CORS
│
├── sdk/                                # Installable Python SDK
│   ├── experiment_ai/
│   │   ├── __init__.py
│   │   └── client.py                   # Experiment class with full logging API
│   └── setup.py
│
├── streamlit_app/                      # Dashboard frontend
│   ├── app.py
│   └── requirements.txt
│
├── tests/
│   └── simulate_experiment.py          # End-to-end experiment simulation
│
├── vector_db/                          # Persisted ChromaDB vector store
├── build_rag.py                        # Script to build the RAG knowledge base
├── test_run.py                         # Quick SDK test script
├── test_copilot.py                     # Copilot endpoint tests
├── test_rag.py                         # RAG retrieval tests
├── test_tools.py                       # Agent tool tests
├── start.sh                            # Backend startup script
├── requirements.txt
└── .env                                # API keys + config (not committed)
```

---

## API Reference

### Experiments

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/experiments/start` | Create a new experiment |
| `POST` | `/experiments/params` | Log hyperparameters |
| `POST` | `/experiments/metric` | Log a single metric at a step |
| `POST` | `/experiments/end` | Mark experiment as completed |
| `GET` | `/experiments/` | List all experiments |
| `GET` | `/experiments/{id}` | Get a single experiment |
| `GET` | `/experiments/{id}/metrics` | Get all logged metrics |
| `GET` | `/experiments/{id}/analysis` | Get signals + diagnostics (cached) |
| `GET` | `/experiments/parameters/analysis` | Cross-experiment parameter insights |

### Copilot

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/copilot/query/` | Ask the AI copilot a question |

**Request:**
```json
{
  "query": "What is the issue with this experiment?",
  "experiment_id": 42
}
```

**Response:**
```json
{
  "answer": "Experiment 42 shows signs of overfitting. Best score of 0.84 was reached at epoch 3, but the final score dropped to 0.77..."
}
```

---

## SDK

### Install

```bash
cd sdk
pip install -e .
```

### Basic usage

```python
from experiment_ai import Experiment

# Start
exp = Experiment("my_project", "run_001")

# Log hyperparameters
exp.log_params({
    "learning_rate": 0.01,
    "optimizer":     "adam",
    "batch_size":    32
})

# Log a single metric per step
for i, v in enumerate([0.70, 0.80, 0.83, 0.81, 0.77]):
    exp.log_metric("val_accuracy", v, step=i)

# Log multiple metrics at once
exp.log_metrics({"val_accuracy": 0.83, "loss": 0.42}, step=3)

# End
exp.end()
```

### Context manager — auto-ends even if training crashes

```python
with Experiment("my_project", "run_002") as exp:
    exp.log_params({"learning_rate": 0.001})
    for i, v in enumerate(my_metrics):
        exp.log_metric("val_accuracy", v, step=i)
```

### Point at your deployed backend

```bash
export EXPERIMENT_AI_URL=https://your-backend.onrender.com
```

Or via `.env`:

```python
from dotenv import load_dotenv
load_dotenv()

from experiment_ai import Experiment
exp = Experiment("demo", "test_run")
```

---

## Analysis Engine

### Signal Extraction

For every experiment, the engine automatically computes:

| Signal | Description |
|---|---|
| `primary_metric` | Prefers `val_*` metrics, falls back to first logged |
| `best_score` | Max or min depending on metric direction |
| `best_epoch` | Step at which best score was achieved |
| `final_score` | Last logged value |
| `training_variance` | Population variance across all steps |

Metric direction is inferred automatically — `accuracy`, `val_accuracy`, `f1`, `auc`, `r2` are maximized; `loss`, `val_loss`, `mse`, `rmse`, `mae` are minimized.

### Diagnostics

Rule-based analysis runs on top of extracted signals:

| Issue | Detection Condition |
|---|---|
| `OVERFITTING` | Best epoch < 60% of total steps AND score dropped > 0.02 |
| `UNSTABLE_TRAINING` | Training variance > 0.08 |
| `INSUFFICIENT_DATA` | Fewer than 3 training steps logged |

Signals and diagnostics are computed once and cached in the database — subsequent requests are served instantly from cache.

### Hyperparameter Intelligence

Cross-experiment parameter analysis computes per parameter:

- **Best value** — parameter value with highest average score across all experiments
- **Best range** — range of numeric values staying within 95% of best score
- **Importance score** — variance in average scores across values (higher = more impactful)

---

## AI Copilot

The copilot is a LangGraph ReAct agent backed by Gemini 2.5 Flash with four tools:

| Tool | When it's called |
|---|---|
| `get_experiment_analysis` | User asks about a specific experiment's results |
| `get_parameter_insights` | User asks which hyperparameters work best |
| `compare_experiments` | User asks to compare two experiments |
| `retrieve_ml_knowledge` | User asks conceptual ML questions (overfitting, regularization, etc.) |

The agent decides which tool(s) to call based on the query and the experiment context sent with each request. Tool calls hit your live backend API, so answers are always grounded in real data — not hallucinated.

---

## Running Locally

### Prerequisites

- Python 3.10+
- Anaconda or virtualenv
- A Gemini API key → [Get one here](https://aistudio.google.com/app/apikey)

### Backend

```bash
git clone https://github.com/your-username/epoche.git
cd epoche

conda create -n epoche python=3.10
conda activate epoche

pip install -r requirements.txt

cp .env.example .env
# Add your GEMINI_API_KEY to .env

# Build the RAG knowledge base (first time only)
python build_rag.py

# Start the backend
bash start.sh
# or: uvicorn app.main:app --reload
```

### Dashboard

```bash
cd streamlit_app
pip install -r requirements.txt
streamlit run app.py
```

### Environment Variables

| Variable | Description |
|---|---|
| `GEMINI_API_KEY` | Your Google Gemini API key |
| `API_BASE_URL` | Backend URL — used by LangGraph agent tools internally |
| `EXPERIMENT_AI_URL` | SDK target URL — used by the Python SDK |

---

## Deployment

| Component | Platform |
|---|---|
| Backend API | [Render](https://render.com) |
| Dashboard | [Streamlit Cloud](https://streamlit.io/cloud) |

Set the following in your Render environment variables:

```
GEMINI_API_KEY  = your-gemini-key
API_BASE_URL    = https://your-app.onrender.com
```

> **Note:** `API_BASE_URL` must point to your own Render URL so the LangGraph agent's internal tool calls can reach the backend correctly. Without this, the copilot falls back to generic answers instead of using your real experiment data.

---

## Design Decisions

**Why rule-based diagnostics instead of ML-based?**
Deterministic rules are explainable and auditable. When the system says an experiment is overfitting, you can trace exactly why — best epoch was at step 3 out of 10, final score dropped 0.06. An ML classifier would produce a probability with no justification.

**Why build this instead of using MLflow or W&B?**
Those tools are excellent but carry significant infrastructure overhead and are opinionated about deployment. Epoché is designed to be entirely self-contained and understandable — every component from signal extraction to the agent's tool routing is built from scratch, which means it's also fully customizable.

**Why LangGraph for the copilot?**
The copilot needs to decide what data to fetch before answering. LangGraph's ReAct agent loop handles multi-step tool use cleanly — it can call `get_experiment_analysis`, read the result, and decide whether to also call `retrieve_ml_knowledge` for context, all within a single user query.

**Why cache signals and diagnostics?**
Signal extraction and diagnostics run the same computation every time from raw metrics. Caching the result on first computation means the dashboard loads instantly for experiments you've already viewed, and the agent's tool calls return faster.

---


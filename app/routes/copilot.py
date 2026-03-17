from fastapi import APIRouter
from pydantic import BaseModel

from app.ai.copilot_agent import ask_copilot

router = APIRouter()


class CopilotRequest(BaseModel):
    query: str


@router.post("/copilot/query/")
def copilot_query(data: dict):

    query = data.get("query")
    experiment_id = data.get("experiment_id")

    if not query:
        return {"answer": "Please enter a question."}

    answer = ask_copilot(query, experiment_id)

    return {"answer": answer}
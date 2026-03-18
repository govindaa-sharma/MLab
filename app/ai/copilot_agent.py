from langchain_core.tools import Tool

from app.ai.tools import (
    get_experiment_analysis,
    get_parameter_insights,
    compare_experiments
)

from app.ai.rag_engine import retrieve_knowledge

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from langchain.agents import create_agent
import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
tools = [

    Tool(
        name="get_experiment_analysis",
        func=get_experiment_analysis,
        description="""
Use this tool when the user asks to analyze a specific experiment.
Requires an experiment_id.
Returns experiment signals and diagnostics such as overfitting or instability.
"""
    ),

    Tool(
        name="get_parameter_insights",
        func=get_parameter_insights,
        description="""
Use this tool when the user asks about which hyperparameters work best,
which hyperparameters to try next,
or what hyperparameters performed well across experiments.
Does NOT require an experiment_id.
"""
    ),

    Tool(
        name="compare_experiments",
        func=compare_experiments,
        description="""
Use this tool when the user asks to compare two experiments
or determine which experiment performed better.
Requires two experiment ids.
"""
    ),

    Tool(
        name="retrieve_ml_knowledge",
        func=retrieve_knowledge,
        description="""
Use this tool when the user asks conceptual ML questions such as
why overfitting happens, why training is unstable, or how to fix training issues.
"""
    )

]

SYSTEM_PROMPT = """
You are an ML Experiment Copilot.

Your job is to help analyze machine learning experiments and suggest improvements.

Rules:
- If the user asks to analyze an experiment → use get_experiment_analysis.
- If the user asks which hyperparameters work best or what to try next → use get_parameter_insights.
- If the user asks to compare experiments → use compare_experiments.
- If the user asks ML theory questions → use retrieve_ml_knowledge.

Always provide practical ML recommendations.
"""

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=GEMINI_API_KEY
)

agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt=SYSTEM_PROMPT,
    checkpointer=None   
)


def ask_copilot(query, experiment_id=None):

    print("QUERY:", query)
    print("EXPERIMENT:", experiment_id)

    if not query:
        return "Please enter a question."

    if experiment_id:
        query = f"""
You are an AI assistant for ML experiment analysis.

Experiment ID: {experiment_id}

User question:
{query}

Use experiment analysis data and provide actionable ML advice.
"""

    try:
        result = agent.invoke({
            "messages": [
                {"role": "user", "content": query}
            ]
        })

        content = result["messages"][-1].content

        if isinstance(content, str):
            return content

        if isinstance(content, list):
            return "\n\n".join(
                block["text"]
                for block in content
                if isinstance(block, dict) and block.get("type") == "text" and block.get("text")
            )

        return str(content)

    except Exception as e:
        print("AI ERROR:", e)
        return f"Agent error: {e}"
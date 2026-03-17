from app.ai.rag_engine import retrieve_knowledge

docs = retrieve_knowledge("why is my model overfitting")

print(docs)
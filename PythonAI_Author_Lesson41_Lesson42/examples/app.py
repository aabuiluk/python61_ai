# file: app.py
from fastapi import FastAPI
from pydantic import BaseModel, Field
from agent_live import run_agent

app = FastAPI(title="Shop Knowledge Agent")

class AskRequest(BaseModel):
    question: str = Field(min_length=3, max_length=500)

@app.post("/ask")
def ask(request: AskRequest):
    return {"answer": run_agent(request.question)}

# Запуск: uvicorn app:app --reload
# Перевірка: відкрийте http://127.0.0.1:8000/docs
# curl -X POST http://127.0.0.1:8000/ask -H "Content-Type: application/json" -d '{"question":"Яка ціна Python?"}' 

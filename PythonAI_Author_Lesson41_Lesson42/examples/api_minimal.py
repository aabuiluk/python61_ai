# file: api_minimal.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from classifier_live import classify

app = FastAPI(title='Ukraine Store Demo')
class Request(BaseModel):
    message: str = Field(min_length=1, max_length=1000)

@app.post('/classify')
def classify_endpoint(data: Request):
    try:
        return classify(data.message, examples=True)
    except Exception as exc:
        # Не повертайте клієнту ключі чи внутрішні деталі API.
        raise HTTPException(status_code=502, detail='Помилка AI-сервісу') from exc

# Запуск: uvicorn api_minimal:app --reload
# Тест: POST /classify з JSON {"message":"Яка ціна товару?"}

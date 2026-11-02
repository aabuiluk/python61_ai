import json
import re
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

# Синтетичні правила українського магазину з того самого типу прикладів, що у 41–42.
DOCS = [
    {"id":"delivery_ua", "text":"Доставка Україною коштує 90 грн."},
    {"id":"pickup_lviv", "text":"Самовивіз у Львові безкоштовний."},
    {"id":"hours", "text":"Магазин працює з 09:00 до 18:00."},
]
def retrieve(question,k=2):
    if not isinstance(question,str) or not question.strip():
        return []
    if type(k) is not int or k < 1:
        raise ValueError("k має бути додатним цілим")
    vectorizer = TfidfVectorizer()
    matrix = vectorizer.fit_transform([d["text"] for d in DOCS])
    scores = cosine_similarity(vectorizer.transform([question]),matrix)[0]
    order = sorted(range(len(DOCS)),key=lambda i:(-scores[i],DOCS[i]["id"]))
    return [{**DOCS[i],"score":round(float(scores[i]),6)} for i in order[:k] if scores[i]>0]

def context_for(question):
    return json.dumps(retrieve(question),ensure_ascii=False)

def fixture_model(value):
    # Це ручний транспортний fixture, НЕ мовна модель і НЕ реальний API.
    text = value.to_string() if hasattr(value,"to_string") else str(value)
    match = re.search(r"<context>(.*?)</context>",text,re.S)
    docs = json.loads(match.group(1)) if match else []
    result = {"answer":docs[0]["text"] if docs else None,
              "sources":[docs[0]["id"]] if docs else []}
    return AIMessage(content=json.dumps(result,ensure_ascii=False))

def validate_answer(value,docs):
    if not isinstance(value,dict) or set(value)!={"answer","sources"}:
        return False
    answer,sources = value["answer"],value["sources"]
    if not isinstance(sources,list) or not all(isinstance(s,str) for s in sources):
        return False
    if len(sources)!=len(set(sources)) or not set(sources)<={d["id"] for d in docs}:
        return False
    return (answer is None and sources==[]) or (isinstance(answer,str) and bool(answer.strip()) and bool(sources))

def make_chain():
    prompt = ChatPromptTemplate.from_messages([
        ("system","Працюйте лише за контекстом. Поверніть answer та sources у JSON."),
        ("human","<context>{context}</context>\nПитання: {question}"),
    ])
    return ({"context":RunnableLambda(context_for),"question":RunnablePassthrough()}
            | prompt | RunnableLambda(fixture_model) | JsonOutputParser())

"""Блок 8 · альтернатива з OPENAI_API_KEY (необов'язково).

Той самий LCEL `prompt | model | parser`, але model-вузол — справжній виклик API. `invoke` робить один запит, `batch` — кілька.

Офлайн-версія: examples/example_08.py. Без ключа скрипт друкує «пропущено».
"""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from workshop import *
from live_openai import *

require_key()

prompt = ChatPromptTemplate.from_messages([("system", "Відповідайте одним коротким реченням."),
                                           ("human", "Питання: {question}")])
chain = prompt | live_model | StrOutputParser()
print(chain.invoke({"question": "Коли працює магазин, якщо графік 09:00–18:00?"}))
print(chain.batch([{"question": "Що таке LCEL?"}, {"question": "Що повертає StrOutputParser?"}]))
message = (prompt | live_model).invoke({"question": "Привіт"})
print(type(message).__name__, message.response_metadata)
print_usage()

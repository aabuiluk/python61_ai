"""Блок 8 · альтернатива з OPENAI_API_KEY (необов'язково).

Той самий LCEL `prompt | model | parser`, але model-вузол — справжній виклик API. `invoke` робить один запит, `batch` — кілька.

Офлайн-версія: examples/example_08.py. Без ключа скрипт друкує «пропущено».
"""
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from PythonAI_Author_Lesson43_Lesson44.live_openai import live_model, print_usage, require_key

require_key()

prompt = ChatPromptTemplate.from_messages([("system", "Відповідайте одним коротким реченням."),
                                           ("human", "Питання: {question}")])
chain = prompt | live_model | StrOutputParser()
print(chain.invoke({"question": "Коли працює магазин, якщо графік 09:00–18:00?"}))
print(chain.batch([{"question": "Що таке LCEL?"}, {"question": "Що повертає StrOutputParser?"}]))
message = (prompt | live_model).invoke({"question": "Привіт"})
print(type(message).__name__, message.response_metadata)
print_usage()

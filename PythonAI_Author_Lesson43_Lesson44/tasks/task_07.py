"""**Завдання 7.** Допишіть chat-шаблон: додайте повідомлення human зі змінними `{context}` і `{question}`. Запитайте, коли працює магазин, і передайте знайдений контекст.

Підказки:
1. Формат рядка як у `examples/live_07.py`: `("human", "<context>{context}</context>\nПитання: {question}")`.
2. Після TODO 1 `chat.input_variables` має показати `['context', 'question']`.

Готово, якщо: Надруковано `['context', 'question']` і одне речення з «09:00» та «18:00».

Подивіться examples/live_07.py — там той самий код без TODO. Потрібен OPENAI_API_KEY (див. README.md).
"""
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from PythonAI_Author_Lesson43_Lesson44.live_openai import live_model, require_key

require_key()

# %% Ваш код: допишіть місця TODO
chat = ChatPromptTemplate.from_messages([
    ("system", "Ви консультант магазину. Відповідайте українською одним реченням лише за контекстом."),
    # TODO 1: додайте ("human", ...) зі змінними {context} і {question}
])
print("Змінні шаблону:", chat.input_variables)
chain = chat | live_model | StrOutputParser()
question = "Коли працює магазин?"
# TODO 2: надрукуйте chain.invoke({"context": context_for(question), "question": question})

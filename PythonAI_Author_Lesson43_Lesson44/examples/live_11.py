"""Блок 11 · альтернатива з OPENAI_API_KEY (необов'язково).

Бюджет памʼяті в справжніх токенах: та сама відповідь з усією історією і з останніми чотирма повідомленнями.

Офлайн-версія: examples/example_11.py. Без ключа скрипт друкує «пропущено».
"""
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from PythonAI_Author_Lesson43_Lesson44.live_openai import live_model, print_usage, require_key

require_key()

history = []
for i in range(1, 7):
    history += [HumanMessage(content=f"Питання {i}: нагадайте правила доставки та самовивозу."),
                AIMessage(content="Доставка Україною коштує 90 грн, самовивіз у Львові безкоштовний. " * 3)]
prompt = ChatPromptTemplate.from_messages([("system", "Відповідайте одним реченням."),
                                           MessagesPlaceholder("history"), ("human", "{question}")])
for name, part in [("уся історія", history), ("останні 4", history[-4:])]:
    reply = (prompt | live_model).invoke({"history": part, "question": "Коротко: скільки коштує доставка?"})
    print(f"{name}: повідомлень {len(part)}, input_tokens {reply.response_metadata['input_tokens']}")
print_usage()

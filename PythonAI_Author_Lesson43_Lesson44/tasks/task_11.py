"""**Завдання 11.** Порівняйте ціну запиту з повною історією і з двома останніми повідомленнями. Надрукуйте `input_tokens` обох варіантів.

Підказки:
1. Додайте в список другий варіант: `("останні 2", history[-2:])`.
2. Число токенів лежить у `reply.response_metadata["input_tokens"]`.

Готово, якщо: Надруковано два числа `input_tokens`, і друге помітно менше. Відповідь в обох випадках правильна.

Подивіться examples/live_11.py — там той самий код без TODO. Потрібен OPENAI_API_KEY (див. README.md).
"""
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from PythonAI_Author_Lesson43_Lesson44.live_openai import live_model, require_key

require_key()

# %% Ваш код: допишіть місця TODO
history = []
for i in range(1, 7):
    history += [HumanMessage(content=f"Питання {i}: нагадайте правила доставки."),
                AIMessage(content="Доставка Україною коштує 90 грн. " * 3)]
prompt = ChatPromptTemplate.from_messages([("system", "Відповідайте одним реченням."),
                                           MessagesPlaceholder("history"), ("human", "{question}")])
variants = [("уся історія", history)]  # TODO: додайте ("останні 2", history[-2:])
for name, part in variants:
    reply = (prompt | live_model).invoke({"history": part, "question": "Скільки коштує доставка?"})
    print(f"{name}: повідомлень {len(part)}, input_tokens {reply.response_metadata['input_tokens']}")

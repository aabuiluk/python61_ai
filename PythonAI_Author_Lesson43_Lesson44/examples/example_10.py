"""44.4 · Memory: історія як вхідні дані та ізоляція сесій

**Факт 10. Історія належить конкретній сесії; її треба явно передати в prompt.**

MessagesPlaceholder("history") вставляє список повідомлень у визначене місце chat-шаблону.
RunnableWithMessageHistory читає та поповнює історію через get_session_history(session_id).
Параметри input_messages_key і history_messages_key узгоджують імена полів із prompt.
Без placeholder сам факт зберігання списку не означає, що модель його бачить.

Дві сесії A та B повинні мати два незалежні сховища. Інакше питання одного користувача
потрапить у prompt іншого. InMemoryChatMessageHistory зберігає дані тільки в RAM поточного
процесу: після перезапуску вони зникнуть. Це не авторизація, не довготривала пам’ять і
не готове production-сховище. Вхідний session_id потрібно прив’язувати до користувача
на рівні застосунку. Тут використовуємо синтетичні дані та локальні сесії.

Не копіюємо старі приклади ConversationBufferMemory: у новому практикумі показано
явний message history. Контроль історії агентів у сучасних графах може використовувати
інші API й checkpointers; це окреме продовження, а не прихована властивість цього wrapper.
"""
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.messages import AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableLambda
from langchain_core.runnables.history import RunnableWithMessageHistory

# %% Основний код
store = {}
def history_for(session_id):
    return store.setdefault(session_id,InMemoryChatMessageHistory())
prompt = ChatPromptTemplate.from_messages([("system","Навчальний echo-fixture."),
 MessagesPlaceholder("history"),("human","{question}")])
echo = RunnableLambda(lambda value: AIMessage(content="Отримано: "+value.to_messages()[-1].content))
chat = RunnableWithMessageHistory(prompt | echo,history_for,
 input_messages_key="question",history_messages_key="history")
print(chat.invoke({"question":"Цікавить доставка"},config={"configurable":{"session_id":"A"}}).content)
print("Повідомлень A:",len(store["A"].messages))

# %% Окрема схема
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(10, 2.3))
ax.set_xlim(0,4); ax.set_ylim(0,1); ax.axis('off')
labels = ['Session id', 'History', 'Placeholder', 'New turn']
for j,label in enumerate(labels):
    ax.text(j+0.5,0.5,label,ha='center',va='center',fontsize=11,
            bbox=dict(boxstyle='round,pad=0.65',facecolor='#eaf1ff',edgecolor='#2459be'))
    if j<3:
        ax.annotate('',xy=(j+1.08,0.5),xytext=(j+0.92,0.5),arrowprops=dict(arrowstyle='->'))
ax.set_title('Example 10: data flow, not model measurements')
fig.tight_layout()
plt.show()

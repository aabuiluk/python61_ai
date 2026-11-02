# Пари 43–44 · Від власного RAG та агента до LangChain

**Маршрут:** 30 хв переходу з 41–42 + 100 хв екосистеми фреймворків (43) +
100 хв PromptTemplate, LCEL і Memory (44). Це план на 230 навчальних хвилин;
перерви й встановлення поза часом. Тривалість проходження групою не виміряна.
Для двох пар по 80 хв: 30 хв переходу, по 65 хв основних тем; поглиблені частини
самостійних вправ і живі порівняння чатів завершуються вдома. Усі пояснення лишаються тут.

У наданих матеріалах 41 ви вже пройшли чанки, TF-IDF/cosine, top-k та відповідь з цитатами.
У 42 — tools, агентний цикл, observation, обмеження кроків і локальний застосунок.
Тепер не змінюємо бізнес-задачу: магазин у Львові відповідає про доставку та самовивіз.
Переходимо від власних функцій до стандартних компонентів і перевіряємо ті самі контракти.

**Головний результат:** запит → retrieval → ChatPromptTemplate → Runnable → parser →
валідація, а також ізольована історія двох сесій. Папка пакета містить 12 прикладів,
12 завдань і їхні критерії. Викладацькі розв’язки зберігаються в окремій версії.

## Що саме є справжнім, а що навчальним

Усі компоненти PromptTemplate, ChatPromptTemplate, RunnableLambda, JsonOutputParser та
RunnableWithMessageHistory — справжній **langchain-core 1.7.4**, а не самописний оператор `|`.
Вузол fixture_model — вручну написаний замінник відповіді моделі. Він не мислить,
не оцінює факти й не викликає API. Тому проходження локальних тестів не є оцінкою LLM.
RAG-пошук справжній локальний TF-IDF; це лексичні вектори, не семантичні embeddings.
На 41–42 у вас був live OpenAI API; тут нову архітектуру спочатку перевіряємо без витрат.
Заміна модельного вузла на провайдерський конектор — окремий подальший крок.

## Налаштування один раз

1. У студентському репозиторії `python61_ai` відкрийте папку
   `PythonAI_Author_Lesson43_Lesson44`. Файли HTML/MD/IPYNB є також у корені репозиторію.
   Без Git: [репозиторій групи](https://github.com/aabuiluk/python61_ai) → Code → Download ZIP →
   розпакуйте. Якщо новий пакет отримали окремим ZIP, його досить розпакувати у робочу папку.
2. Потрібен Python 3.10+; перевірена версія — 3.11. Відкрийте термінал у корені репозиторію.
   Якщо спільне середовище вже є, використайте його. Для нового: `python -m venv .venv`.
3. Windows: `.venv\Scripts\python -m pip install -r PythonAI_Author_Lesson43_Lesson44/requirements.txt`.
   macOS/Linux: `.venv/bin/python -m pip install -r PythonAI_Author_Lesson43_Lesson44/requirements.txt`.
   Інтернет потрібен для встановлення пакетів. Їхнє локальне використання в цьому практикумі безкоштовне.
4. Ноутбук: встановіть `python -m pip install jupyterlab ipykernel` через Python цього ж середовища,
   запустіть `python -m jupyterlab` і відкрийте `PythonAI_Author_Lesson43_Lesson44.ipynb`.
   Виконуйте згори вниз. Усі демонстрації мають власні вхідні дані; завдання пишіть у комірках із їхнім номером.
5. Окремий приклад: `python PythonAI_Author_Lesson43_Lesson44/examples/example_01.py`;
   завдання: `python PythonAI_Author_Lesson43_Lesson44/tasks/task_01.py`.
   У цих командах `python` означає Python активного середовища; без активації вкажіть повний шлях з кроку 3.
6. HTML — автономна читанка з виконаними прикладами та схемами, Python у ньому не запускається.
   Меню зліва залишається на місці при прокрутці; на телефоні воно над текстом.

Увесь обов’язковий код працює без API-ключів, Cloud-проєкту, картки, LangSmith-акаунта
та платної підписки. Не встановлюйте відразу всі фреймворки: порівняння 43 — за документацією,
реальна інсталяція потрібна тільки для langchain-core у 44.

## Додатково: той самий промпт у Gemini або ChatGPT

**Gemini:** відкрийте [gemini.google.com](https://gemini.google.com/), увійдіть, якщо потрібно,
створіть новий текстовий чат, вставте промпт із відповідного блоку та надішліть.
Альтернатива — [Google AI Studio](https://aistudio.google.com/): новий текстовий чат →
доступна безкоштовна модель без платного ключа → Run. Не активуйте Billing або trial.

**ChatGPT:** відкрийте [chatgpt.com](https://chatgpt.com/), увійдіть за потреби → звичайний Chat →
New chat / Новий чат → вставте той самий промпт → надішліть. Не купуйте підписку і не
підключайте API для цієї вправи. За регіональних, вікових обмежень або вичерпання ліміту
працюйте з локальними fixtures. Правила доступу не обходимо.

Текстова відповідь чату не виконує ваш Python і не підключає LangChain до сервісу.
Порівнюйте її за тим самим критерієм; не пишіть «модель запустила код», якщо запуску не було.
Збережіть prompt.txt, response.txt, назву сервісу, показану модель і дату. Відповідь чату
не є обов’язковим артефактом: локальні вправи забезпечують повне проходження практикуму.

## Початкові дані та спільні функції

## Порядок роботи

| Хвилини | Блок | Завдання |
|---|---|---|
| 0–15 | 41 · Переносимо retrieval і джерела | 1 |
| 15–30 | 42 · Агентний цикл і явний стан | 2 |
| 30–55 | 43.1 · Model → chain → retrieval → agent | 3 |
| 55–80 | 43.2 · LangChain, LlamaIndex та Vertex AI | 4 |
| 80–105 | 43.3 · LangGraph, CrewAI, AutoGen і Semantic Kernel | 5 |
| 105–130 | 43.4 · ADR: обрати мінімальний стек | 6 |
| 130–145 | 44.1 · PromptTemplate і ChatPromptTemplate | 7 |
| 145–165 | 44.2 · LCEL: контракт кожного Runnable | 8 |
| 165–180 | 44.3 · Parser і предметна валідація | 9 |
| 180–200 | 44.4 · Memory: історія як вхідні дані та ізоляція сесій | 10 |
| 200–215 | 44.5 · Бюджет пам’яті та межі контексту | 11 |
| 215–230 | 44.6 · Збираємо DocFlow і перевіряємо перехід | 12 |



```python
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

```
# Блок 1. 41 · Переносимо retrieval і джерела

**0–15 хв.**

**Факт 1. RAG починається з пошуку, а не з прохання моделі пригадати відповідь.**

На 41 ви ділили документи на чанки, додавали id та шукали top-k за cosine. Зараз беремо
три короткі правила магазину: доставка Україною 90 грн, самовивіз у Львові безкоштовний,
години роботи 09:00–18:00. Це синтетичні навчальні дані. Прочитайте знайдений текст перед
побудовою промпту: високий score означає схожість у цьому просторі, не істинність і не
ймовірність правильної відповіді. Нульовий збіг тут повертає порожній результат.

Три рядки не потребують окремого chunker: кожний уже є одним фрагментом. В реальному
корпусі збережіть document_id, chunk_id і шлях до джерела. Для питання без факту потрібна
відмова, а не довільний перший документ. Цей контракт переносимо в LangChain без змін.

### Приклад · основний код


```python
hits = retrieve("Доставка Україною",k=2)
print(json.dumps(hits,ensure_ascii=False,indent=2))
assert hits[0]["id"]=="delivery_ua"
```

Результат виконання:

```text
[
  {
    "id": "delivery_ua",
    "text": "Доставка Україною коштує 90 грн.",
    "score": 0.632456
  }
]

```
### Окрема графічна схема

Схема показує потік даних, а не вимірювання якості моделі.


```python
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(10, 2.3))
ax.set_xlim(0,4); ax.set_ylim(0,1); ax.axis('off')
labels = ['Question', 'TF-IDF', 'Top-k', 'Source ids']
for j,label in enumerate(labels):
    ax.text(j+0.5,0.5,label,ha='center',va='center',fontsize=11,
            bbox=dict(boxstyle='round,pad=0.65',facecolor='#eaf1ff',edgecolor='#2459be'))
    if j<3:
        ax.annotate('',xy=(j+1.08,0.5),xytext=(j+0.92,0.5),arrowprops=dict(arrowstyle='->'))
ax.set_title('Example 1: data flow, not model measurements')
fig.tight_layout()
plt.show()
```

![Схема потоку даних](figures/example_01.png)
### Промпт: Gemini або ChatGPT

**Gemini:** новий текстовий чат у Gemini/AI Studio → вставте повний текст нижче → Send/Run.

**ChatGPT — альтернатива:** chatgpt.com → Chat → New chat → той самий текст → надішліть.

За недоступності безкоштовного режиму використовуйте локальну демонстрацію. Звичайний чат не виконує LCEL автоматично.

```text
Використовуйте тільки джерело [pickup_lviv]: Самовивіз у Львові безкоштовний.
Питання: скільки коштує самовивіз у Львові? Дайте одне речення та id джерела.
Не додавайте строків, адрес чи умов, яких немає в тексті.
```


### Зараз виконайте завдання 1

Після пояснення, прикладу й схеми відкрийте `tasks/task_01.py`. Повторити демонстрацію можна в `examples/example_01.py`. У ноутбуці пишіть у наступній комірці; далі переходьте після перевірки критерію.

**Завдання 1.** Знайдіть один фрагмент про самовивіз у Львові, побудуйте JSON-контекст із id/text.
Перевірте пошук «Марсіанський телепорт» та порожній рядок. Поясніть значення score.

### Підказки

1. retrieve(question,1). 2. Виберіть id/text. 3. Невідомий словник і порожній запит мають дати [].

**Готово, якщо:** Знайдено pickup_lviv, є JSON-контекст, два порожні результати та пояснення score.

Окремі файли: `examples/example_01.py` і `tasks/task_01.py` у папці пакета.



```python
# Завдання 1: напишіть власний код за умовою.

```
# Блок 2. 42 · Агентний цикл і явний стан

**15–30 хв.**

**Факт 2. Інструмент виконує програма, а модель лише пропонує дію.**

На 42 у вас був цикл model → tool call → перевірка аргументів → Python → observation →
нова репліка моделі. Зберігайте ліміт кроків, allowlist інструментів і журнал навіть після
переходу на фреймворк. Структура {tool, arguments} сама не виконує функцію.

Нижче звичайний Python виконує дозволений пошук. Це один крок маршруту, не автономний
LLM-агент. Невідома дія повинна завершитись помилкою до виконання; порожній retrieval
повертає observation з порожнім списком. LangGraph згодом може організувати переходи стану,
але не прийме за вас бізнес-рішення, які інструменти дозволені.

### Приклад · основний код


```python
request = {"tool":"search_knowledge","arguments":{"question":"Доставка Україною"}}
if request["tool"]!="search_knowledge":
    raise ValueError("Невідомий tool")
observation = retrieve(request["arguments"]["question"],1)
trace = [{"step":1,"request":request,"observation":observation}]
print(json.dumps(trace,ensure_ascii=False,indent=2))
```

Результат виконання:

```text
[
  {
    "step": 1,
    "request": {
      "tool": "search_knowledge",
      "arguments": {
        "question": "Доставка Україною"
      }
    },
    "observation": [
      {
        "id": "delivery_ua",
        "text": "Доставка Україною коштує 90 грн.",
        "score": 0.632456
      }
    ]
  }
]

```
### Окрема графічна схема

Схема показує потік даних, а не вимірювання якості моделі.


```python
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(10, 2.3))
ax.set_xlim(0,4); ax.set_ylim(0,1); ax.axis('off')
labels = ['Request', 'Allowlist', 'Tool', 'Observation']
for j,label in enumerate(labels):
    ax.text(j+0.5,0.5,label,ha='center',va='center',fontsize=11,
            bbox=dict(boxstyle='round,pad=0.65',facecolor='#eaf1ff',edgecolor='#2459be'))
    if j<3:
        ax.annotate('',xy=(j+1.08,0.5),xytext=(j+0.92,0.5),arrowprops=dict(arrowstyle='->'))
ax.set_title('Example 2: data flow, not model measurements')
fig.tight_layout()
plt.show()
```

![Схема потоку даних](figures/example_02.png)
### Промпт: Gemini або ChatGPT

**Gemini:** новий текстовий чат у Gemini/AI Studio → вставте повний текст нижче → Send/Run.

**ChatGPT — альтернатива:** chatgpt.com → Chat → New chat → той самий текст → надішліть.

За недоступності безкоштовного режиму використовуйте локальну демонстрацію. Звичайний чат не виконує LCEL автоматично.

```text
Доступний тільки search_knowledge(question: рядок). Потрібні правила доставки Україною.
Поверніть тільки JSON {"tool":"search_knowledge","arguments":{"question":"Доставка Україною"}}.
Не вигадуйте observation. Після фактичного результату Python можна сформувати відповідь за джерелом.
```


### Зараз виконайте завдання 2

Після пояснення, прикладу й схеми відкрийте `tasks/task_02.py`. Повторити демонстрацію можна в `examples/example_02.py`. У ноутбуці пишіть у наступній комірці; далі переходьте після перевірки критерію.

**Завдання 2.** Напишіть dispatch для search_knowledge. Приймайте тільки рядкове question і жодних
зайвих аргументів. Перевірте відомий tool, невідомий delete_all та question=123.
Покажіть стан steps і max_steps до наступного кроку.

### Підказки

1. Перевірте типи та ключі. 2. Не використовуйте eval/exec. 3. steps < max_steps — умова продовження.

**Готово, якщо:** Валідний пошук працює; два некоректні запити відхилено; умова ліміту кроків явна.

Окремі файли: `examples/example_02.py` і `tasks/task_02.py` у папці пакета.



```python
# Завдання 2: напишіть власний код за умовою.

```
# Блок 3. 43.1 · Model → chain → retrieval → agent

**30–55 хв.**

**Факт 3. Фреймворк стандартизує компонування коду навколо моделі, а не замінює модель.**

Model-вузол отримує повідомлення й повертає результат. Chain задає відому послідовність:
підготувати дані → сформувати prompt → модель → parser. Retrieval знаходить документи.
Agent у циклі обирає наступну дію за станом і observation. Це ролі компонентів, а не
обов’язкова сходинка складності: RAG-chain може ніколи не бути агентом.

Сирого SDK досить для одного виклику з простим контролем. Коли з’являються повторювані
шаблони, парсери та кілька конекторів, стандартні інтерфейси економлять код. Натомість
додаються залежності, зміни API та вимога розуміти типи даних між вузлами.
Не переписуйте робочий retrieval заради модної назви: обгорніть перевірену функцію.

У прикладі карта зв’язує власні функції з компонентами майбутнього DocFlow. На 44 ми
використаємо справжні Runnable. На 43 порівнюємо архітектури; список назв не є запуском пакетів.

### Приклад · основний код


```python
layers = {"model":"fixture_model або окремий провайдерський конектор",
          "chain":"context → prompt → model → parser",
          "retrieval":"retrieve(question,k)","agent":"цикл tool/observation зі станом"}
print(json.dumps(layers,ensure_ascii=False,indent=2))
```

Результат виконання:

```text
{
  "model": "fixture_model або окремий провайдерський конектор",
  "chain": "context → prompt → model → parser",
  "retrieval": "retrieve(question,k)",
  "agent": "цикл tool/observation зі станом"
}

```
### Окрема графічна схема

Схема показує потік даних, а не вимірювання якості моделі.


```python
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(10, 2.3))
ax.set_xlim(0,4); ax.set_ylim(0,1); ax.axis('off')
labels = ['Model', 'Chain', 'Retrieval', 'Agent']
for j,label in enumerate(labels):
    ax.text(j+0.5,0.5,label,ha='center',va='center',fontsize=11,
            bbox=dict(boxstyle='round,pad=0.65',facecolor='#eaf1ff',edgecolor='#2459be'))
    if j<3:
        ax.annotate('',xy=(j+1.08,0.5),xytext=(j+0.92,0.5),arrowprops=dict(arrowstyle='->'))
ax.set_title('Example 3: data flow, not model measurements')
fig.tight_layout()
plt.show()
```

![Схема потоку даних](figures/example_03.png)
### Промпт: Gemini або ChatGPT

**Gemini:** новий текстовий чат у Gemini/AI Studio → вставте повний текст нижче → Send/Run.

**ChatGPT — альтернатива:** chatgpt.com → Chat → New chat → той самий текст → надішліть.

За недоступності безкоштовного режиму використовуйте локальну демонстрацію. Звичайний чат не виконує LCEL автоматично.

```text
Ви пояснюєте архітектуру DocFlow. Компоненти: prompt, top-k, model call, JSON parser,
tool selection, step limit. Розкладіть їх за model/chain/retrieval/agent. Для кожного
вкажіть роль і що перевіряє програма. Не стверджуйте, що chain обов’язково є агентом.
```


### Зараз виконайте завдання 3

Після пояснення, прикладу й схеми відкрийте `tasks/task_03.py`. Повторити демонстрацію можна в `examples/example_03.py`. У ноутбуці пишіть у наступній комірці; далі переходьте після перевірки критерію.

**Завдання 3.** Розкладіть шість компонентів за шарами: сформувати prompt, знайти top-k,
викликати модель, перевірити JSON, обрати наступний tool, обмежити кроки.
Позначте, які вже реалізовані у 41–42, а які винесете в LCEL.

### Підказки

1. top-k — retrieval. 2. parser — етап chain. 3. tool selection та steps належать керуванню агентом.

**Готово, якщо:** Шість компонентів розкладено за шарами; є відповідність власному коду 41–42 і компонентам 44.

Окремі файли: `examples/example_03.py` і `tasks/task_03.py` у папці пакета.



```python
# Завдання 3: напишіть власний код за умовою.

```
# Блок 4. 43.2 · LangChain, LlamaIndex та Vertex AI

**55–80 хв.**

**Факт 4. Бібліотека оркестрації та керована Cloud-платформа можуть працювати разом.**

LangChain надає компоненти й інтеграції для LLM-застосунків; у нашій 44 використовуємо
langchain-core для prompt, Runnable та parser. LlamaIndex часто розглядають першою
кандидатурою, коли головна складність — завантаження, індексація та retrieval документів.
Обидва екосистемні підходи мають перекриття: це не правило «лише агенти» проти «лише RAG».

Vertex AI у програмі — керована Google Cloud-платформа доступу до моделей та ML-сервісів.
Вона вирішує інший шар: проєкт, ідентичність, IAM, регіон, квоти, облік витрат.
Можна мати LangChain-застосунок, що використовує провайдерський сервіс у Cloud. А можна
написати звичайний SDK-клієнт без LangChain. Питання «що краще» замініть на «яку вимогу покриває».

Для трьох правил магазину спочатку лишаємо існуючий TF-IDF. Для великого неоднорідного
корпусу оцінюємо конектори, метадані, chunking, оновлення та якість retrieval.
Не встановлюйте LlamaIndex із типовими модельними провайдерами заради таблиці: це може
створити непотрібні вимоги до ключів. Огляд безкоштовний, а запуски моделей — окрема умова провайдера.

### Приклад · основний код


```python
choices = [
 {"need":"компонування prompt/model/parser","candidate":"LangChain","layer":"application"},
 {"need":"завантаження й індексація багатьох документів","candidate":"LlamaIndex","layer":"data"},
 {"need":"керований Cloud-доступ та IAM","candidate":"Vertex AI","layer":"platform"}]
print(json.dumps(choices,ensure_ascii=False,indent=2))
```

Результат виконання:

```text
[
  {
    "need": "компонування prompt/model/parser",
    "candidate": "LangChain",
    "layer": "application"
  },
  {
    "need": "завантаження й індексація багатьох документів",
    "candidate": "LlamaIndex",
    "layer": "data"
  },
  {
    "need": "керований Cloud-доступ та IAM",
    "candidate": "Vertex AI",
    "layer": "platform"
  }
]

```
### Окрема графічна схема

Схема показує потік даних, а не вимірювання якості моделі.


```python
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(10, 2.3))
ax.set_xlim(0,4); ax.set_ylim(0,1); ax.axis('off')
labels = ['Requirements', 'Data pipeline', 'Library', 'Platform']
for j,label in enumerate(labels):
    ax.text(j+0.5,0.5,label,ha='center',va='center',fontsize=11,
            bbox=dict(boxstyle='round,pad=0.65',facecolor='#eaf1ff',edgecolor='#2459be'))
    if j<3:
        ax.annotate('',xy=(j+1.08,0.5),xytext=(j+0.92,0.5),arrowprops=dict(arrowstyle='->'))
ax.set_title('Example 4: data flow, not model measurements')
fig.tight_layout()
plt.show()
```

![Схема потоку даних](figures/example_04.png)
### Промпт: Gemini або ChatGPT

**Gemini:** новий текстовий чат у Gemini/AI Studio → вставте повний текст нижче → Send/Run.

**ChatGPT — альтернатива:** chatgpt.com → Chat → New chat → той самий текст → надішліть.

За недоступності безкоштовного режиму використовуйте локальну демонстрацію. Звичайний чат не виконує LCEL автоматично.

```text
Порівняйте стек для: трьох правил магазину; тисяч PDF із метаданими; корпоративного
Cloud-доступу з IAM. Дайте таблицю: сценарій, мінімальний стек, альтернатива, перевірка.
Розрізняйте LangChain/LlamaIndex як бібліотеки та Vertex AI як платформу.
Не вигадуйте поточних тарифів, квот і гарантій якості.
```


### Зараз виконайте завдання 4

Після пояснення, прикладу й схеми відкрийте `tasks/task_04.py`. Повторити демонстрацію можна в `examples/example_04.py`. У ноутбуці пишіть у наступній комірці; далі переходьте після перевірки критерію.

**Завдання 4.** Для трьох сценаріїв запропонуйте стек і альтернативу: 1) три локальні правила;
2) тисячі PDF з метаданими; 3) корпоративні Cloud-проєкти з IAM.
Для кожного вкажіть мінімальний варіант, причину та одну перевірку до впровадження.

### Підказки

1. Малому корпусу не потрібен новий Cloud-індекс. 2. Для PDF оцініть якість витягу. 3. IAM не замінює retrieval.

**Готово, якщо:** Є три рішення, три альтернативи й перевірки; бібліотеку не названо заміною IAM/білінгу.

Окремі файли: `examples/example_04.py` і `tasks/task_04.py` у папці пакета.



```python
# Завдання 4: напишіть власний код за умовою.

```
# Блок 5. 43.3 · LangGraph, CrewAI, AutoGen і Semantic Kernel

**80–105 хв.**

**Факт 5. Цикл станів і співпраця ролей — різні способи організації роботи.**

LangGraph зручно розглядати для явного стану, вузлів, переходів, умов зупинки та
відновлення виконання. CrewAI використовує ролі/задачі в Crews і керування процесом у
Flows. Це не взаємовиключні світи: у role-based системі також потрібні стан і контроль.
Назва «редактор» не створює окрему людину чи незалежне джерело істини — це роль агента.

AutoGen історично пов’язаний із взаємодією агентів через повідомлення; Semantic Kernel —
з інтеграцією AI-функцій та інструментів у застосунки. Підтримка, рекомендовані пакети й
маршрути міграції змінюються, тому перед вибором перевіряйте офіційний статус проєкту.
На цій парі для них даємо карту ролей, не встановлення та не обіцянку переваги.
Окремо позначте Microsoft Agent Framework: це набір засобів для агентів, workflows,
модельних клієнтів та інтеграцій. Уявна карта «AutoGen — тільки чат, Semantic Kernel —
тільки плагіни» надто вузька: екосистеми розвиваються, функції перекриваються.
Для нового Microsoft-стеку перевірте [актуальний Agent Framework](https://learn.microsoft.com/en-us/agent-framework/overview/)
і рекомендації міграції, а не встановлюйте старий пакет із випадкового уроку.

Для DocFlow достатньо станів retrieve → answer → validate; при помилці одна спроба repair,
потім stop. Для процесу «дослідник → редактор → контролер» важливі артефакти кожної ролі
і критерії передачі. Навіть найсильніший framework не має права нескінченно повторювати запит.
У прикладі нижче — ручна схема переходів, не імпорт LangGraph або CrewAI.

### Приклад · основний код


```python
edges = {"retrieve":"answer","answer":"validate","validate_ok":"stop",
         "validate_error":"repair","repair":"stop"}
roles = {"researcher":"джерела","editor":"текст за джерелами","reviewer":"звіт дефектів"}
print(edges)
print(roles)
```

Результат виконання:

```text
{'retrieve': 'answer', 'answer': 'validate', 'validate_ok': 'stop', 'validate_error': 'repair', 'repair': 'stop'}
{'researcher': 'джерела', 'editor': 'текст за джерелами', 'reviewer': 'звіт дефектів'}

```
### Окрема графічна схема

Схема показує потік даних, а не вимірювання якості моделі.


```python
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(10, 2.3))
ax.set_xlim(0,4); ax.set_ylim(0,1); ax.axis('off')
labels = ['State', 'Transitions', 'Roles', 'Stop rule']
for j,label in enumerate(labels):
    ax.text(j+0.5,0.5,label,ha='center',va='center',fontsize=11,
            bbox=dict(boxstyle='round,pad=0.65',facecolor='#eaf1ff',edgecolor='#2459be'))
    if j<3:
        ax.annotate('',xy=(j+1.08,0.5),xytext=(j+0.92,0.5),arrowprops=dict(arrowstyle='->'))
ax.set_title('Example 5: data flow, not model measurements')
fig.tight_layout()
plt.show()
```

![Схема потоку даних](figures/example_05.png)
### Промпт: Gemini або ChatGPT

**Gemini:** новий текстовий чат у Gemini/AI Studio → вставте повний текст нижче → Send/Run.

**ChatGPT — альтернатива:** chatgpt.com → Chat → New chat → той самий текст → надішліть.

За недоступності безкоштовного режиму використовуйте локальну демонстрацію. Звичайний чат не виконує LCEL автоматично.

```text
Спроєктуйте DocFlow: researcher знаходить документи з id, editor пише відповідь,
reviewer звіряє її з джерелами. Дозволено один repair, після нього stop.
Дайте входи/виходи ролей і переходи станів. Поясніть вибір LangGraph або CrewAI,
не стверджуючи, що бібліотека гарантує правильність відповіді.
```


### Зараз виконайте завдання 5

Після пояснення, прикладу й схеми відкрийте `tasks/task_05.py`. Повторити демонстрацію можна в `examples/example_05.py`. У ноутбуці пишіть у наступній комірці; далі переходьте після перевірки критерію.

**Завдання 5.** Опишіть маршрут DocFlow з одним repair і трьома ролями. Для кожної ролі задайте
вхід і вихід; для процесу — max_repairs=1 та кінцевий stop. Поясніть, коли обрали б
явний граф станів, а коли організацію співпраці ролей.

### Підказки

1. Результат researcher — документи з id. 2. Editor не вигадує джерел. 3. Reviewer повертає дефекти, а не автоматичну істину.

**Готово, якщо:** Три ролі з контрактами, один repair і кінцевий stop; пояснено два стилі організації.

Окремі файли: `examples/example_05.py` і `tasks/task_05.py` у папці пакета.



```python
# Завдання 5: напишіть власний код за умовою.

```
# Блок 6. 43.4 · ADR: обрати мінімальний стек

**105–130 хв.**

**Факт 6. Архітектурне рішення має містити причину, відхилену альтернативу та ціну складності.**

ADR — короткий запис рішення: контекст, вимоги, вибір, альтернативи, наслідки та перевірка.
Для DocFlow потрібні локальний пошук, прозорий prompt, JSON-відповідь, ізоляція історії
та тести без мережі. Обираємо langchain-core для композиції, залишаємо TF-IDF і власну
предметну перевірку. LangGraph, CrewAI, LlamaIndex та Cloud не додаємо, доки немає вимоги,
яка окупить їхню складність. Це рішення для конкретної вправи, не універсальний рейтинг.

Уникайте формулювання «обрали LangChain, бо всі використовують». Поставте перевірювану
мету: той самий retrieval-id до та після обгортання; parser відхиляє поганий JSON;
сесія B не бачить історії A. Запишіть ризик: оновлення API можуть вимагати міграції,
а історія в RAM зникає після перезапуску. На 44 перевіримо саме ці наслідки.

### Приклад · основний код


```python
adr = {"context":"DocFlow: 3 локальні правила","decision":"langchain-core + existing retrieval",
       "rejected":"додавання кількох агентних фреймворків без вимоги",
       "risk":"залежність від API-версії","acceptance":"ті самі ids + parser tests + session isolation"}
print(json.dumps(adr,ensure_ascii=False,indent=2))
```

Результат виконання:

```text
{
  "context": "DocFlow: 3 локальні правила",
  "decision": "langchain-core + existing retrieval",
  "rejected": "додавання кількох агентних фреймворків без вимоги",
  "risk": "залежність від API-версії",
  "acceptance": "ті самі ids + parser tests + session isolation"
}

```
### Окрема графічна схема

Схема показує потік даних, а не вимірювання якості моделі.


```python
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(10, 2.3))
ax.set_xlim(0,4); ax.set_ylim(0,1); ax.axis('off')
labels = ['Context', 'Alternatives', 'Decision', 'Acceptance']
for j,label in enumerate(labels):
    ax.text(j+0.5,0.5,label,ha='center',va='center',fontsize=11,
            bbox=dict(boxstyle='round,pad=0.65',facecolor='#eaf1ff',edgecolor='#2459be'))
    if j<3:
        ax.annotate('',xy=(j+1.08,0.5),xytext=(j+0.92,0.5),arrowprops=dict(arrowstyle='->'))
ax.set_title('Example 6: data flow, not model measurements')
fig.tight_layout()
plt.show()
```

![Схема потоку даних](figures/example_06.png)
### Промпт: Gemini або ChatGPT

**Gemini:** новий текстовий чат у Gemini/AI Studio → вставте повний текст нижче → Send/Run.

**ChatGPT — альтернатива:** chatgpt.com → Chat → New chat → той самий текст → надішліть.

За недоступності безкоштовного режиму використовуйте локальну демонстрацію. Звичайний чат не виконує LCEL автоматично.

```text
Створіть короткий ADR для DocFlow: 3 правила, локальний TF-IDF, JSON, ізоляція сесій,
тести без мережі. Поля: context, requirements, decision, alternatives, consequences,
acceptance. Запропонуйте мінімальний стек і конкретну умову перегляду рішення.
Не активуйте Cloud і не рекомендуйте платні ресурси для цієї вправи.
```


### Зараз виконайте завдання 6

Після пояснення, прикладу й схеми відкрийте `tasks/task_06.py`. Повторити демонстрацію можна в `examples/example_06.py`. У ноутбуці пишіть у наступній комірці; далі переходьте після перевірки критерію.

**Завдання 6.** Напишіть ADR із шістьма полями context, requirements, decision, alternatives,
consequences, acceptance. Додайте умову, за якої ви переглянете рішення (наприклад,
відновлення довгого процесу після збою). Збережіть results_43_44/ADR.json.

### Підказки

1. Вимоги не мають містити назви бажаної бібліотеки. 2. Наслідки включають мінус. 3. Acceptance — спостережуваний результат.

**Готово, якщо:** Є шість полів ADR, ризик, альтернатива, умова перегляду та три критерії перевірки.

Окремі файли: `examples/example_06.py` і `tasks/task_06.py` у папці пакета.



```python
# Завдання 6: напишіть власний код за умовою.

```
# Блок 7. 44.1 · PromptTemplate і ChatPromptTemplate

**130–145 хв.**

**Факт 7. Шаблон явно оголошує вхідні змінні; chat-шаблон додатково зберігає ролі повідомлень.**

На 41 ви збирали stuffing-prompt рядком. PromptTemplate робить підстановки {context} та
{question} видимими й перевіряє відсутні значення. ChatPromptTemplate формує повідомлення
system/human/ai, а не один нерозмічений рядок. format повертає текст; invoke — PromptValue,
який можна перетворити на повідомлення. Сам шаблон нічого не генерує й не викликає API.

Використовуйте стандартне форматування рядків, не довільні сторонні template-коди.
JSON із фігурними дужками передавайте через змінну context або екрануйте {{ і }} у
літералі шаблону. Дані джерел лишаються даними; текст «ігноруй інструкції» всередині
документа не стає system-повідомленням. Ролі допомагають розділяти контекст, але не є
самодостатнім захистом від prompt injection: валідатор і межі tools залишаються потрібними.

### Приклад · основний код


```python
template = PromptTemplate.from_template("Дані: {context}\nПитання: {question}")
print(template.input_variables)
print(template.format(context="[delivery_ua] Доставка 90 грн.",question="Скільки коштує доставка?"))
chat = ChatPromptTemplate.from_messages([("system","Тільки за джерелами."),("human","{question}")])
print([m.type for m in chat.invoke({"question":"Які правила?"}).to_messages()])
```

Результат виконання:

```text
['context', 'question']
Дані: [delivery_ua] Доставка 90 грн.
Питання: Скільки коштує доставка?
['system', 'human']

```
### Окрема графічна схема

Схема показує потік даних, а не вимірювання якості моделі.


```python
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(10, 2.3))
ax.set_xlim(0,4); ax.set_ylim(0,1); ax.axis('off')
labels = ['Variables', 'Chat template', 'PromptValue', 'Messages']
for j,label in enumerate(labels):
    ax.text(j+0.5,0.5,label,ha='center',va='center',fontsize=11,
            bbox=dict(boxstyle='round,pad=0.65',facecolor='#eaf1ff',edgecolor='#2459be'))
    if j<3:
        ax.annotate('',xy=(j+1.08,0.5),xytext=(j+0.92,0.5),arrowprops=dict(arrowstyle='->'))
ax.set_title('Example 7: data flow, not model measurements')
fig.tight_layout()
plt.show()
```

![Схема потоку даних](figures/example_07.png)
### Промпт: Gemini або ChatGPT

**Gemini:** новий текстовий чат у Gemini/AI Studio → вставте повний текст нижче → Send/Run.

**ChatGPT — альтернатива:** chatgpt.com → Chat → New chat → той самий текст → надішліть.

За недоступності безкоштовного режиму використовуйте локальну демонстрацію. Звичайний чат не виконує LCEL автоматично.

```text
Ви пояснюєте шаблони Python. Покажіть різницю PromptTemplate.format та
ChatPromptTemplate.invoke(...).to_messages() на context і question.
Джерело: [pickup_lviv] Самовивіз у Львові безкоштовний. Питання: ціна самовивозу?
Не стверджуйте, що сама підстановка викликає модель або доводить істинність відповіді.
```


### Зараз виконайте завдання 7

Після пояснення, прикладу й схеми відкрийте `tasks/task_07.py`. Повторити демонстрацію можна в `examples/example_07.py`. У ноутбуці пишіть у наступній комірці; далі переходьте після перевірки критерію.

**Завдання 7.** Створіть chat-шаблон: system задає відповідь тільки за джерелом; human містить
context і question. Підставте pickup_lviv та питання про вартість самовивозу.
Перевірте типи повідомлень і поведінку за відсутності question.

### Підказки

1. ChatPromptTemplate.from_messages. 2. invoke(...).to_messages(). 3. Пропущене question має спричинити KeyError до моделі.

**Готово, якщо:** Два повідомлення system/human, context підставлено; відсутнє question відхилено до виклику моделі.

Окремі файли: `examples/example_07.py` і `tasks/task_07.py` у папці пакета.



```python
# Завдання 7: напишіть власний код за умовою.

```
# Блок 8. 44.2 · LCEL: контракт кожного Runnable

**145–165 хв.**

**Факт 8. Оператор | з’єднує вихід одного Runnable зі входом наступного.**

LCEL читається зліва направо: prompt | model | parser. Для нашого прикладу це
dict → PromptValue → AIMessage → str. RunnableLambda адаптує звичайну функцію до
інтерфейсу invoke. StrOutputParser дістає текст повідомлення, а не перевіряє його факти.
Оператор | тут належить справжньому langchain-core; ми не перевизначаємо __or__ у FakeLLM.

Помилка форми входу лишається помилкою: якщо lambda очікує повідомлення, а отримує dict,
бібліотека не вгадає правильний шлях. Спочатку запишіть таблицю типів, потім складайте chain.
Виклик invoke виконує вузли синхронно. batch приймає кілька входів; це не повторне навчання
й не гарантія, що довільна функція потокобезпечна. Наша fixture-функція локальна й детермінована.

### Приклад · основний код


```python
prompt = ChatPromptTemplate.from_messages([("human","Питання: {question}")])
model = RunnableLambda(lambda value: AIMessage(content="Навчальний fixture: "+value.to_messages()[-1].content))
chain = prompt | model | StrOutputParser()
print(chain.invoke({"question":"Коли працює магазин?"}))
print(chain.batch([{"question":"A"},{"question":"B"}]))
```

Результат виконання:

```text
Навчальний fixture: Питання: Коли працює магазин?
```

Результат виконання:

```text

['Навчальний fixture: Питання: A', 'Навчальний fixture: Питання: B']

```
### Окрема графічна схема

Схема показує потік даних, а не вимірювання якості моделі.


```python
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(10, 2.3))
ax.set_xlim(0,4); ax.set_ylim(0,1); ax.axis('off')
labels = ['Input dict', 'PromptValue', 'AIMessage', 'String']
for j,label in enumerate(labels):
    ax.text(j+0.5,0.5,label,ha='center',va='center',fontsize=11,
            bbox=dict(boxstyle='round,pad=0.65',facecolor='#eaf1ff',edgecolor='#2459be'))
    if j<3:
        ax.annotate('',xy=(j+1.08,0.5),xytext=(j+0.92,0.5),arrowprops=dict(arrowstyle='->'))
ax.set_title('Example 8: data flow, not model measurements')
fig.tight_layout()
plt.show()
```

![Схема потоку даних](figures/example_08.png)
### Промпт: Gemini або ChatGPT

**Gemini:** новий текстовий чат у Gemini/AI Studio → вставте повний текст нижче → Send/Run.

**ChatGPT — альтернатива:** chatgpt.com → Chat → New chat → той самий текст → надішліть.

За недоступності безкоштовного режиму використовуйте локальну демонстрацію. Звичайний чат не виконує LCEL автоматично.

```text
Поясніть типи даних у LCEL prompt | model | StrOutputParser:
dict → PromptValue → AIMessage → str. Наведіть мінімальний приклад із RunnableLambda,
який повертає ручний AIMessage. Позначте його fixture, не реальна LLM.
Не використовуйте застарілий LLMChain для нового прикладу.
```


### Зараз виконайте завдання 8

Після пояснення, прикладу й схеми відкрийте `tasks/task_08.py`. Повторити демонстрацію можна в `examples/example_08.py`. У ноутбуці пишіть у наступній комірці; далі переходьте після перевірки критерію.

**Завдання 8.** Побудуйте справжній LCEL prompt | RunnableLambda | StrOutputParser для питання
про самовивіз. Модельний fixture має повернути AIMessage з префіксом FIXTURE: та текстом
останнього human-повідомлення. Перевірте invoke і batch із двох різних питань.

### Підказки

1. Lambda отримує PromptValue. 2. Останнє повідомлення: to_messages()[-1].content. 3. Кінцевий результат — str.

**Готово, якщо:** Використано реальний |; вихід str; batch повертає два відповідні результати; жодного API-виклику.

Окремі файли: `examples/example_08.py` і `tasks/task_08.py` у папці пакета.



```python
# Завдання 8: напишіть власний код за умовою.

```
# Блок 9. 44.3 · Parser і предметна валідація

**165–180 хв.**

**Факт 9. Прочитаний JSON ще не означає правильний тип, джерело чи факт.**

JsonOutputParser перетворює текст на Python-об’єкт; вивід може потребувати перевірки
ключів, типів і дозволених source ids. Наша validate_answer вимагає рівно answer/sources,
відомі у переданому контексті id, відсутність дублікатів і узгоджену відмову null/[]
або непорожню відповідь з джерелом. Це контракт форми й походження, не універсальний
детектор істини. Відповідь «90 грн» і «900 грн» із тим самим id обидві можуть мати
правильну структуру, але фактично коректна тільки одна.

Не виправляйте погану відповідь мовчазно підстановкою очікуваного значення. Збережіть
помилку й статус rejected, а потім, якщо потрібно, окремий обмежений repair. Для цього
корпусу фактичну відповідність можемо додатково звірити з точним реченням джерела.

### Приклад · основний код


```python
parsed = JsonOutputParser().invoke(AIMessage(content='{"answer":"Доставка Україною коштує 90 грн.","sources":["delivery_ua"]}'))
hits = retrieve("Доставка",1)
print(parsed,validate_answer(parsed,hits))
print("Факт збігається:",parsed["answer"]==hits[0]["text"])
```

Результат виконання:

```text
{'answer': 'Доставка Україною коштує 90 грн.', 'sources': ['delivery_ua']}
```

Результат виконання:

```text
 True
Факт збігається: True

```
### Окрема графічна схема

Схема показує потік даних, а не вимірювання якості моделі.


```python
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(10, 2.3))
ax.set_xlim(0,4); ax.set_ylim(0,1); ax.axis('off')
labels = ['Raw text', 'JSON parser', 'Contract', 'Fact check']
for j,label in enumerate(labels):
    ax.text(j+0.5,0.5,label,ha='center',va='center',fontsize=11,
            bbox=dict(boxstyle='round,pad=0.65',facecolor='#eaf1ff',edgecolor='#2459be'))
    if j<3:
        ax.annotate('',xy=(j+1.08,0.5),xytext=(j+0.92,0.5),arrowprops=dict(arrowstyle='->'))
ax.set_title('Example 9: data flow, not model measurements')
fig.tight_layout()
plt.show()
```

![Схема потоку даних](figures/example_09.png)
### Промпт: Gemini або ChatGPT

**Gemini:** новий текстовий чат у Gemini/AI Studio → вставте повний текст нижче → Send/Run.

**ChatGPT — альтернатива:** chatgpt.com → Chat → New chat → той самий текст → надішліть.

За недоступності безкоштовного режиму використовуйте локальну демонстрацію. Звичайний чат не виконує LCEL автоматично.

```text
Джерело [delivery_ua]: Доставка Україною коштує 90 грн.
Поверніть тільки JSON з answer (рядок або null) і sources (список id).
Питання: вартість доставки Україною? Якщо факту немає — answer=null,sources=[].
Не додавайте інших полів, цін або умов. Python перевірить структуру та точне джерело.
```


### Зараз виконайте завдання 9

Після пояснення, прикладу й схеми відкрийте `tasks/task_09.py`. Повторити демонстрацію можна в `examples/example_09.py`. У ноутбуці пишіть у наступній комірці; далі переходьте після перевірки критерію.

**Завдання 9.** Перевірте чотири об’єкти: правильна відповідь; невідоме джерело; sources як рядок;
null із непорожнім sources. Додайте окрему точну перевірку факту для тексту про доставку
та покажіть різницю на відповіді «900 грн» із правильним id.

### Підказки

1. validate_answer для структури. 2. Для цього малого тесту зіставте answer з текстом delivery_ua. 3. Не називайте цей exact-match універсальною семантичною оцінкою.

**Готово, якщо:** Чотири перевірки дають True/False/False/False; окремо показано хибний факт із правильною структурою.

Окремі файли: `examples/example_09.py` і `tasks/task_09.py` у папці пакета.



```python
# Завдання 9: напишіть власний код за умовою.

```
# Блок 10. 44.4 · Memory: історія як вхідні дані та ізоляція сесій

**180–200 хв.**

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

### Приклад · основний код


```python
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
```

Результат виконання:

```text
Отримано: Цікавить доставка
Повідомлень A: 2

```

Результат виконання:

```text
C:\Users\Green\PycharmProjects\pet_projects\lesson_helper\python61_ai\.venv\Lib\site-packages\IPython\core\interactiveshell.py:3823: LangChainDeprecationWarning: RunnableWithMessageHistory is deprecated. Use LangGraph's built-in persistence instead.
  exec(code_obj, self.user_global_ns, self.user_ns)
C:\Users\Green\AppData\Local\Temp\ipykernel_35828\1101807922.py:3: LangChainDeprecationWarning: The class `InMemoryChatMessageHistory` was deprecated in LangChain 1.6.4 and will be removed in 2.0.0 See the short-term memory documentation for recommended alternatives: https://docs.langchain.com/oss/python/langchain/short-term-memory
  return store.setdefault(session_id,InMemoryChatMessageHistory())

```
### Окрема графічна схема

Схема показує потік даних, а не вимірювання якості моделі.


```python
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
```

![Схема потоку даних](figures/example_10.png)
### Промпт: Gemini або ChatGPT

**Gemini:** новий текстовий чат у Gemini/AI Studio → вставте повний текст нижче → Send/Run.

**ChatGPT — альтернатива:** chatgpt.com → Chat → New chat → той самий текст → надішліть.

За недоступності безкоштовного режиму використовуйте локальну демонстрацію. Звичайний чат не виконує LCEL автоматично.

```text
Поясніть MessagesPlaceholder, get_session_history та session_id у
RunnableWithMessageHistory. Є A з двома питаннями та B з одним. Скільки human/ai
повідомлень має бути в кожній історії? Не називайте InMemoryChatMessageHistory
довготривалою пам’яттю або механізмом авторизації.
```


### Зараз виконайте завдання 10

Після пояснення, прикладу й схеми відкрийте `tasks/task_10.py`. Повторити демонстрацію можна в `examples/example_10.py`. У ноутбуці пишіть у наступній комірці; далі переходьте після перевірки критерію.

**Завдання 10.** Створіть wrapper з двома сесіями. Надішліть два питання в A і одне в B.
Перевірте кількість повідомлень (4 і 2), порядок human/ai та відсутність тексту A
в історії B. Покажіть, що store є локальною пам’яттю процесу.

### Підказки

1. Новий store для вправи. 2. Окремий session_id у config. 3. Один invoke додає human та ai.

**Готово, якщо:** Сесія A має 4 повідомлення, B — 2; порядок human/ai збережено, витоку між сесіями немає.

Окремі файли: `examples/example_10.py` і `tasks/task_10.py` у папці пакета.



```python
# Завдання 10: напишіть власний код за умовою.

```
# Блок 11. 44.5 · Бюджет пам’яті та межі контексту

**200–215 хв.**

**Факт 11. Історію обмежують завершеними парами реплік, не випадковими останніми рядками.**

Безмежний список повідомлень збільшує контекст і може повернути давно неактуальні факти.
Збережіть системні правила окремо, потім додайте перевірений стан, актуальні джерела,
обмежену історію та нове питання. Якщо бюджет малий, не залишайте відповідь assistant
без її попереднього user-питання. Нижче обмежуємо кількість завершених пар, а не токени.

Дві пари довгих реплік можуть зайняти більше токенів, ніж десять коротких. Для справжнього
провайдера потрібен сумісний token counter та резерв під відповідь. Підрахунок символів
або слів — лише евристика. Обрізання повідомлень не дорівнює підсумуванню; summary може
втратити заперечення, тому вимагає перевірки та джерела. In-memory wrapper сам не задає
бюджет і не видаляє старі повідомлення за вашим бізнес-правилом.

### Приклад · основний код


```python
history = [HumanMessage(content="Q1"),AIMessage(content="A1"),
           HumanMessage(content="Q2"),AIMessage(content="A2"),
           HumanMessage(content="Q3"),AIMessage(content="A3")]
recent = history[-4:]  # тут точно дві завершені пари з підготовленого входу
print([m.content for m in recent])
print("Це ліміт реплік, не підрахунок токенів.")
```

Результат виконання:

```text
['Q2', 'A2', 'Q3', 'A3']
Це ліміт реплік, не підрахунок токенів.

```
### Окрема графічна схема

Схема показує потік даних, а не вимірювання якості моделі.


```python
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(10, 2.3))
ax.set_xlim(0,4); ax.set_ylim(0,1); ax.axis('off')
labels = ['Full turns', 'Pair budget', 'Recent turns', 'Token reserve']
for j,label in enumerate(labels):
    ax.text(j+0.5,0.5,label,ha='center',va='center',fontsize=11,
            bbox=dict(boxstyle='round,pad=0.65',facecolor='#eaf1ff',edgecolor='#2459be'))
    if j<3:
        ax.annotate('',xy=(j+1.08,0.5),xytext=(j+0.92,0.5),arrowprops=dict(arrowstyle='->'))
ax.set_title('Example 11: data flow, not model measurements')
fig.tight_layout()
plt.show()
```

![Схема потоку даних](figures/example_11.png)
### Промпт: Gemini або ChatGPT

**Gemini:** новий текстовий чат у Gemini/AI Studio → вставте повний текст нижче → Send/Run.

**ChatGPT — альтернатива:** chatgpt.com → Chat → New chat → той самий текст → надішліть.

За недоступності безкоштовного режиму використовуйте локальну демонстрацію. Звичайний чат не виконує LCEL автоматично.

```text
Є історія Q1/A1,Q2/A2,Q3/A3. Потрібно зберегти останні дві завершені пари,
system-інструкції лишаються окремо. Поясніть результат, випадок нульового бюджету
та ризик неповної пари. Не називайте кількість пар точним числом токенів.
```


### Зараз виконайте завдання 11

Після пояснення, прикладу й схеми відкрийте `tasks/task_11.py`. Повторити демонстрацію можна в `examples/example_11.py`. У ноутбуці пишіть у наступній комірці; далі переходьте після перевірки критерію.

**Завдання 11.** Напишіть keep_pairs(messages,n), яка приймає тільки завершені human/ai пари й n>=0.
Для трьох пар залиште останні дві; для n=0 поверніть []; незавершену пару відхиліть.
Не змінюйте вихідний список. Поясніть, який додатковий контроль потрібен для токенів.

### Підказки

1. Перевірте парну довжину й типи через m.type. 2. Окремий випадок n=0: slice [-0:] повернув би все. 3. Повертайте новий список.

**Готово, якщо:** Залишено дві цілі пари; n=0 і неповна пара оброблені; вихідний список не змінено; токени не переплутано з репліками.

Окремі файли: `examples/example_11.py` і `tasks/task_11.py` у папці пакета.



```python
# Завдання 11: напишіть власний код за умовою.

```
# Блок 12. 44.6 · Збираємо DocFlow і перевіряємо перехід

**215–230 хв.**

**Факт 12. Після переходу на framework мають зберегтися перевірювані бізнес-контракти.**

Остаточний ланцюжок: рядок question → паралельне формування context/question →
ChatPromptTemplate → модельний вузол → JsonOutputParser. Окремий validate_answer
перевіряє результат щодо тих самих retrieved docs. RunnablePassthrough передає вхідне
питання без змін. Словник runnable-вузлів у LCEL формує словник входів для prompt.

Ми перенесли структуру, а не довели поліпшення якості. Для відомого питання перевірте
answer і sources; для невідомого — null/[]; для зламаного контракту — rejected.
Зафіксуйте langchain-core, mode=fixture і випадки в JSON-звіті. Якщо пізніше заміните
fixture на живу модель, повторіть ці самі кейси й окремо оцініть факти, latency та витрати.
Автоматичне повторення мережевих запитів тут не додаємо.

**Exit ticket:** що лишилося від 41–42? Retrieval, джерела, allowlist, валідація, бюджет.
Що дав framework? Стандартні контракти компонентів і композицію. Де пам’ять? У сховищі
конкретної сесії, яке ми явно підставляємо в prompt. Де перечитати: блоки 1, 2, 8, 10, 11.

### Приклад · основний код


```python
chain = make_chain()
question = "Доставка Україною"
result = chain.invoke(question)
print(result)
print("Контракт:",validate_answer(result,retrieve(question)))
print("Невідомий факт:",chain.invoke("Марсіанський телепорт"))
```

Результат виконання:

```text
{'answer': 'Доставка Україною коштує 90 грн.', 'sources': ['delivery_ua']}
Контракт: True
Невідомий факт: {'answer': None, 'sources': []}

```
### Окрема графічна схема

Схема показує потік даних, а не вимірювання якості моделі.


```python
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(10, 2.3))
ax.set_xlim(0,4); ax.set_ylim(0,1); ax.axis('off')
labels = ['Retrieve', 'Prompt + fixture', 'Parser', 'Validate + log']
for j,label in enumerate(labels):
    ax.text(j+0.5,0.5,label,ha='center',va='center',fontsize=11,
            bbox=dict(boxstyle='round,pad=0.65',facecolor='#eaf1ff',edgecolor='#2459be'))
    if j<3:
        ax.annotate('',xy=(j+1.08,0.5),xytext=(j+0.92,0.5),arrowprops=dict(arrowstyle='->'))
ax.set_title('Example 12: data flow, not model measurements')
fig.tight_layout()
plt.show()
```

![Схема потоку даних](figures/example_12.png)
### Промпт: Gemini або ChatGPT

**Gemini:** новий текстовий чат у Gemini/AI Studio → вставте повний текст нижче → Send/Run.

**ChatGPT — альтернатива:** chatgpt.com → Chat → New chat → той самий текст → надішліть.

За недоступності безкоштовного режиму використовуйте локальну демонстрацію. Звичайний чат не виконує LCEL автоматично.

```text
Джерела: [delivery_ua] Доставка Україною коштує 90 грн.;
[pickup_lviv] Самовивіз у Львові безкоштовний.
Питання: скільки коштує самовивіз у Львові? Поверніть тільки JSON answer,sources.
Відповідайте лише за джерелами; невідомий факт — null і порожній список.
Не стверджуйте, що ви виконали Python/LCEL: цю перевірку проводить локальний код.
```


### Зараз виконайте завдання 12

Після пояснення, прикладу й схеми відкрийте `tasks/task_12.py`. Повторити демонстрацію можна в `examples/example_12.py`. У ноутбуці пишіть у наступній комірці; далі переходьте після перевірки критерію.

**Завдання 12.** Запустіть DocFlow для доставки, самовивозу й невідомого факту. Створіть звіт із
question, answer, sources, passed, mode. Для відомих питань перевірте точний текст
першого документа; для невідомого — null/[]. Збережіть results_43_44/report.json.
Додайте один негативний кейс невідомого source id. Напишіть два речення про межі fixtures.

### Підказки

1. Для кожного питання повторно отримайте docs. 2. passed об’єднує контракт і очікуваний факт. 3. mode завжди fixture, не live.

**Готово, якщо:** Три кейси пройшли контракт і точну перевірку; негативний id відхилено; JSON-звіт має mode=fixture й чесний висновок.

Окремі файли: `examples/example_12.py` і `tasks/task_12.py` у папці пакета.



```python
# Завдання 12: напишіть власний код за умовою.

```
# Після практикуму

Здайте власні tasks, ADR.json, report.json і короткий REPORT.md. У REPORT поясніть:
що перенесли з 41–42, що стандартизував LangChain, як розділені сесії та які межі fixture.
Ключі, .env і чужі повідомлення не включайте. Живий чат — додатковий дослід, не умова здачі.

## Домашня практика і резерв

Додайте четверте правило магазину з новим id. Покажіть незмінність контракту при
перебудові TF-IDF. Додайте два відомі й два невідомі питання, тест невідомого source id,
ізоляцію третьої сесії та перевірку нульового бюджету історії. Поглиблення: винесіть
валідацію в окремий Runnable, але збережіть доступ до retrieved docs. Не знімайте старі тести.

## Безкоштовні першоджерела

- [LangChain: призначення та співвідношення з LangGraph](https://docs.langchain.com/oss/python/langchain/overview)
- [LangGraph: стан і графи](https://reference.langchain.com/python/langgraph/overview)
- [ChatPromptTemplate](https://reference.langchain.com/python/langchain-core/prompts/chat/ChatPromptTemplate)
- [RunnableWithMessageHistory](https://reference.langchain.com/python/langchain-core/runnables/history/RunnableWithMessageHistory)
- [LlamaIndex: модульні пакети](https://developers.llamaindex.ai/python/framework/getting_started/installation/)
- [CrewAI: Crews та Flows](https://docs.crewai.com/en/introduction)
- [AutoGen: офіційний проєкт і актуальний статус](https://github.com/microsoft/autogen)
- [Semantic Kernel: офіційний огляд](https://learn.microsoft.com/en-us/semantic-kernel/overview/)
- [Microsoft Agent Framework: агенти, workflows та інтеграції](https://learn.microsoft.com/en-us/agent-framework/overview/)
- [Vertex AI: офіційний огляд платформи](https://cloud.google.com/vertex-ai/docs/start/introduction-unified-platform)

Вихідна програма та перехід звірені з наданими HTML 41–44. Перевірка посилань і
пакетів — 02.11.2026. Уточнюйте поточні назви документації, API та статус проєктів
перед виробничим впровадженням; цей практикум фіксує перевірену версію бібліотеки.



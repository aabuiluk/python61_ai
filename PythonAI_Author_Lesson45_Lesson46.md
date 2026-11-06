# Пари 45–46 · Від LCEL до Tools і перевіреного workflow

**30 хв переходу з 43–44 + 100 хв пари 45 + 100 хв пари 46 = 230 навчальних хвилин.**
Це план повного практикуму, а не виміряна тривалість групового заняття. Перерви та
встановлення поза цим часом. Якщо маєте дві пари по 80 хв, проведіть 30 хв переходу,
по 65 хв основних тем; самостійні розширення, повторні live-запуски й захист звіту — у резерві.

У 43 ви обирали framework і розділяли model/chain/retrieval/agent. У 44 склали
PromptTemplate → модель → parser і відокремили історії сесій. Тепер модельний вузол
одразу викликає **OpenAI API**. На 45 він запитує Python-tools; на 46 маршрутизатор
збирає обмежений процес і зупиняє пропозицію повернення коштів на перевірку людиною.

Використовуємо синтетичні заявки T101 (urgent), T102 (normal), T103 (low).
SLA відповідно 4, 24 та 72 години. Жодних справжніх клієнтських даних або платежів.
Фінальний результат: live tool trace, usage.jsonl, workflow JSON та рішення approve/edit/reject.
Усі приклади й заповнені завдання виконують реальні модельні запити. Без ключа скрипт
завершиться зрозумілою помилкою; автоматичної заміни відповіді моделі на fixture немає.

## Встановлення і ключ, який видає викладач

1. Відкрийте [студентський репозиторій](https://github.com/aabuiluk/python61_ai) →
   Code → Download ZIP або виконайте git pull у своєму клоні. Пакет:
   `PythonAI_Author_Lesson45_Lesson46`. Перейдіть у цю папку в терміналі.
2. Потрібен Python 3.10+, перевірка виконана на 3.11. Якщо спільне середовище вже є,
   використайте його. Інакше в корені репозиторію: `python -m venv .venv`.
3. З кореня репозиторію Windows:
   `.venv\Scripts\python -m pip install -r PythonAI_Author_Lesson45_Lesson46/requirements.txt`.
   macOS/Linux: `.venv/bin/python -m pip install -r PythonAI_Author_Lesson45_Lesson46/requirements.txt`.
4. У папці пакета скопіюйте `.env.example` у `.env`:
   Windows `Copy-Item .env.example .env`; macOS/Linux `cp .env.example .env`.
   Відкрийте .env у редакторі й локально введіть виданий викладачем ключ у OPENAI_API_KEY.
   Не вставляйте ключ у HTML, комірку ноутбука, промпт або Git. .env та results/ виключені через .gitignore.
5. OPENAI_MODEL за замовчуванням `gpt-4.1-mini`. Якщо виданий проєкт не має доступу,
   викладач задає доступну модель зі structured output і function calling. Код не
   перемикає модель мовчазно. Ключ API — це обліковий доступ; input/output tokens —
   одиниці обсягу запиту й відповіді. Це різні значення слова «токен».
6. Перейдіть у папку пакета. Запуск: `python examples/example_01.py`, потім
   `python tasks/task_01.py`. Якщо середовище не активоване, замість python використайте
   шлях до Python зі свого середовища. Кожен файл має main-блок і не викликає API при імпорті.
7. Ноутбук: встановіть jupyterlab та ipykernel у це саме середовище,
   запустіть `python -m jupyterlab`, відкрийте `PythonAI_Author_Lesson45_Lesson46.ipynb`.
   Якщо відкрили його з кореня репозиторію, перша комірка знайде папку пакета.
   Запускайте блоки по черзі: Run All надішле серію реальних запитів.

OpenAI API має власні квоти й білінг; підписка ChatGPT не замінює API-доступ.
Кожен запуск прикладу або готового завдання може витрачати виділений бюджет.
SDK має max_retries=0, timeout=30 с і max_output_tokens=800. Агент має максимум
4 модельні раунди та 6 tool calls; workflow — не більше одного repair.
Це межі виконання й виводу, а не гарантована грошова стеля. Usage записуємо для кожного запиту.

401: перевірте ключ; 403/404: доступ до моделі/проєкту; 429: квоту або частоту.
Після помилки перевірте причину, а не натискайте запуск багато разів. Status incomplete,
відмова та порожній текст не вважаються успішною відповіддю.

## Файли й навігація

У кожному блоці є пояснення → повний приклад → схема → **«Зараз виконайте завдання»** →
підказки → **«Готово, якщо»** → точні файли examples/example_NN.py і tasks/task_NN.py.
Студентська задача — практичний live-каркас із 1–2 TODO. Викладацька версія має готовий код,
очікувані інваріанти, повний промпт та пояснення до нього. Текст відповіді моделі може змінюватися.

runtime.py містить спільний клієнт API, реальні @tool, dispatcher та workflow.
Не потрібно переписувати весь runtime перед першим запуском. Після базової вправи
поглиблення — змінити потрібний контракт і додати власний локальний тест.
HTML є читанкою з кодом; Python у ньому не виконується. Меню зліва закріплене при прокрутці.

## Короткі команди підсумкової роботи

```bash
python runtime.py ask "Який SLA у заявки T101?"
python runtime.py ask "Підготуй пропозицію повернення коштів за заявкою T102"
```

Друга команда надрукує шлях results/<request_id>.json. Скопіюйте **цей реальний шлях** у:

```bash
python runtime.py review results/ВСТАВТЕ_REQUEST_ID.json approve
python runtime.py review results/ВСТАВТЕ_REQUEST_ID.json edit --answer "Відредагована пропозиція для клієнта"
python runtime.py review results/ВСТАВТЕ_REQUEST_ID.json reject
```

Для одного стану оберіть лише одне рішення. Повторне схвалення завершеного стану відхиляється.
Схвалення затверджує навчальну чернетку: код не відправляє повідомлень і не здійснює виплат.
Це локальна послідовна вправа; для багатокористувацького сервісу потрібні авторизація,
транзакційне сховище й контроль одночасних рішень.

## Порядок роботи

| Хвилини | Блок | Завдання |
|---|---|---|
| 0–15 | 43 → API · LCEL з реальною моделлю | 1 |
| 15–30 | 44 → API · Історія двох live-сесій | 2 |
| 30–55 | 45.1 · LangChain @tool і схема OpenAI | 3 |
| 55–80 | 45.2 · JSON-аргументи: parse → validate → dispatch | 4 |
| 80–105 | 45.3 · Справжній Function Calling: call_id та observation | 5 |
| 105–130 | 45.4 · ReAct-цикл: межі та помилки | 6 |
| 130–150 | 46.1 · Модельний router і локальна політика | 7 |
| 150–170 | 46.2 · Sequential workflow і незалежний validator | 8 |
| 170–185 | 46.3 · Repair і retry budget | 9 |
| 185–200 | 46.4 · HITL: зберегти стан і поставити паузу | 10 |
| 200–215 | 46.5 · Resume: approve, edit, reject | 11 |
| 215–230 | 46.6 · Повний workflow, журнал і захист | 12 |



```python
from pathlib import Path
import sys
candidates = [Path.cwd()/"PythonAI_Author_Lesson45_Lesson46", Path.cwd()/"lesson45_46_teacher", Path.cwd()]
package = next((p for p in candidates if (p/"runtime.py").is_file()),None)
if package is None:
    raise RuntimeError("Відкрийте ноутбук із папки репозиторію або пакета 45–46")
sys.path.insert(0,str(package.resolve()))
from pathlib import Path
import json
from runtime import (ClassroomAPI, ClassroomError, API_TOOLS, TOOLS, TICKETS, SLA,
    ANSWER_SCHEMA, ROUTE_SCHEMA, dispatch, validate, run_agent, route_query,
    draft_for, repair_once, run_workflow, resume, show)
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableLambda
from langchain_core.messages import AIMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

```
# Блок 1. 43 → API · LCEL з реальною моделлю

**0–15 хв.**

**Факт 1. Модельний вузол LCEL можна замінити, зберігши контракт входу й виходу.**
У 43–44 ви відокремлювали prompt від моделі. Тепер ChatPromptTemplate формує повідомлення,
RunnableLambda передає їх у ClassroomAPI.text, а StrOutputParser повертає рядок.
Усередині виконується client.responses.create; це живий API-виклик, не симуляція.
Ключ читається з локального .env пакета. Виводимо текст, фактичну модель та usage.
Перевірте призначення кожного шару: шаблон не надсилає запит сам по собі, lambda тут
викликає клієнт, parser не доводить істинність тексту. Перенесення бізнес-перевірок
залишається вашою відповідальністю.

### Приклад · реальний OpenAI API


```python
api = ClassroomAPI()
prompt = ChatPromptTemplate.from_messages([("system","Поясніть початківцю одним реченням."),("human","{question}")])
chain = prompt | RunnableLambda(api.text) | StrOutputParser()
answer = chain.invoke({"question":"Навіщо parser після моделі?"})
show(api,{"answer":answer})
```
### Схема

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 880 115" role="img" aria-label="Схема потоку даних"><title>Блок 1: потік даних</title><g><title>Chat template</title><rect x="8" y="24" width="195" height="62" rx="10" fill="#eaf1ff" stroke="#2459be"/><text x="105" y="61" text-anchor="middle" font-family="sans-serif" font-size="16" fill="#182438">Chat template</text></g><path d="M 207 55 h 17 l -5 -5 m 5 5 l -5 5" fill="none" stroke="#2459be" stroke-width="2"/><g><title>OpenAI API</title><rect x="228" y="24" width="195" height="62" rx="10" fill="#eaf1ff" stroke="#2459be"/><text x="325" y="61" text-anchor="middle" font-family="sans-serif" font-size="16" fill="#182438">OpenAI API</text></g><path d="M 427 55 h 17 l -5 -5 m 5 5 l -5 5" fill="none" stroke="#2459be" stroke-width="2"/><g><title>Parser</title><rect x="448" y="24" width="195" height="62" rx="10" fill="#eaf1ff" stroke="#2459be"/><text x="545" y="61" text-anchor="middle" font-family="sans-serif" font-size="16" fill="#182438">Parser</text></g><path d="M 647 55 h 17 l -5 -5 m 5 5 l -5 5" fill="none" stroke="#2459be" stroke-width="2"/><g><title>Usage</title><rect x="668" y="24" width="195" height="62" rx="10" fill="#eaf1ff" stroke="#2459be"/><text x="765" y="61" text-anchor="middle" font-family="sans-serif" font-size="16" fill="#182438">Usage</text></g></svg>

### Повний промпт для OpenAI API


```text
Одне коротке речення українською: чим chain відрізняється від agent? Не стверджуйте, що parser гарантує істинність.
```

Промпт передається через Python-клієнт, а не вручну через чат. Фактичні системні інструкції й JSON-схеми наведені в PROMPTS.md та runtime.py.


### Зараз виконайте завдання 1

Після прикладу відкрийте `tasks/task_01.py`, допишіть TODO і запустіть. Для порівняння — `examples/example_01.py`. Це live-код із виданим ключем OpenAI. У ноутбуці використайте наступну комірку.

**Завдання 1.** Змініть питання на різницю chain та agent. Запустіть реальний LCEL і збережіть текст відповіді разом із model та usage. Перевірте, що відбувся один API-виклик.

### Підказки

1. Скопіюйте структуру прикладу. 2. Замініть question. 3. Перевірте api.calls_used та api.records, не друкуйте ключ.

**Готово, якщо:** Є непорожня live-відповідь, один API-виклик і запис фактичних model/usage.

Окремі файли: `examples/example_01.py` і `tasks/task_01.py` у папці пакета.



```python
QUESTION = None  # TODO: власне питання про chain та agent
if not QUESTION:
    raise NotImplementedError("Заповніть QUESTION")
api = ClassroomAPI()
prompt = ChatPromptTemplate.from_messages([("system","Одне речення українською."),("human","{question}")])
chain = prompt | RunnableLambda(api.text) | StrOutputParser()
show(api,{"answer":chain.invoke({"question":QUESTION})})
```
# Блок 2. 44 → API · Історія двох live-сесій

**15–30 хв.**

**Факт 2. Модель бачить тільки ту історію, яку застосунок передав у поточному запиті.**
Зберігаємо реальний RunnableWithMessageHistory із 44, а його модельний вузол викликає
OpenAI API. Сесія A отримує кодове слово, наступна репліка просить його повторити.
Новий session_id B не має цих повідомлень. Перевіряємо і поведінку моделі, і склад
сховища; лише правдоподібна відповідь не доводить ізоляцію.
InMemoryChatMessageHistory існує в RAM поточного процесу. Store=False в API не
підміняє локальне керування історією: потрібні messages, session_id та бюджет контексту.
За нових запусків скрипта починаємо з порожнього store.
Це місток до коду 44 на зафіксованій версії: RunnableWithMessageHistory та
InMemoryChatMessageHistory уже позначені deprecated у цій лінійці LangChain. Попередження
не є помилкою запуску. Для нових виробничих агентів перегляньте short-term memory та
LangGraph persistence; у 46 ми окремо зберігаємо стан workflow, а не покладаємось на RAM.

### Приклад · реальний OpenAI API


```python
api = ClassroomAPI()
store = {}
def history_for(sid):
    return store.setdefault(sid,InMemoryChatMessageHistory())
prompt = ChatPromptTemplate.from_messages([("system","Працюйте тільки з історією цієї розмови."),MessagesPlaceholder("history"),("human","{question}")])
model = RunnableLambda(lambda value: AIMessage(content=api.text(value,stage="memory")))
chat = RunnableWithMessageHistory(prompt | model,history_for,input_messages_key="question",history_messages_key="history")
chat.invoke({"question":"Кодове слово нашої вправи — Клен."},config={"configurable":{"session_id":"A"}})
answer = chat.invoke({"question":"Яке кодове слово я назвав?"},config={"configurable":{"session_id":"A"}})
show(api,{"answer":answer.content,"messages_A":len(store["A"].messages)})
```
### Схема

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 880 115" role="img" aria-label="Схема потоку даних"><title>Блок 2: потік даних</title><g><title>Session A/B</title><rect x="8" y="24" width="195" height="62" rx="10" fill="#eaf1ff" stroke="#2459be"/><text x="105" y="61" text-anchor="middle" font-family="sans-serif" font-size="16" fill="#182438">Session A/B</text></g><path d="M 207 55 h 17 l -5 -5 m 5 5 l -5 5" fill="none" stroke="#2459be" stroke-width="2"/><g><title>Messages</title><rect x="228" y="24" width="195" height="62" rx="10" fill="#eaf1ff" stroke="#2459be"/><text x="325" y="61" text-anchor="middle" font-family="sans-serif" font-size="16" fill="#182438">Messages</text></g><path d="M 427 55 h 17 l -5 -5 m 5 5 l -5 5" fill="none" stroke="#2459be" stroke-width="2"/><g><title>OpenAI API</title><rect x="448" y="24" width="195" height="62" rx="10" fill="#eaf1ff" stroke="#2459be"/><text x="545" y="61" text-anchor="middle" font-family="sans-serif" font-size="16" fill="#182438">OpenAI API</text></g><path d="M 647 55 h 17 l -5 -5 m 5 5 l -5 5" fill="none" stroke="#2459be" stroke-width="2"/><g><title>Isolated history</title><rect x="668" y="24" width="195" height="62" rx="10" fill="#eaf1ff" stroke="#2459be"/><text x="765" y="61" text-anchor="middle" font-family="sans-serif" font-size="16" fill="#182438">Isolated history</text></g></svg>

### Повний промпт для OpenAI API


```text
Працюйте тільки з поточною історією. Якщо кодового слова там немає, так і скажіть. Не вгадуйте дані з іншої розмови.
```

Промпт передається через Python-клієнт, а не вручну через чат. Фактичні системні інструкції й JSON-схеми наведені в PROMPTS.md та runtime.py.


### Зараз виконайте завдання 2

Після прикладу відкрийте `tasks/task_02.py`, допишіть TODO і запустіть. Для порівняння — `examples/example_02.py`. Це live-код із виданим ключем OpenAI. У ноутбуці використайте наступну комірку.

**Завдання 2.** Виконайте дві live-репліки в A й одну в B. В A використайте слово «Липа», у B попросіть повторити слово, якого B не отримувала. Перевірте довжини історій 4 та 2 і відсутність повідомлень A у B.

### Підказки

1. Новий store. 2. Три invoke з двома session_id. 3. Не перевіряйте ізоляцію тільки за відповіддю моделі: перегляньте повідомлення.

**Готово, якщо:** Три реальні запити; A має 4 повідомлення, B — 2; історія B не містить приватної репліки A.

Окремі файли: `examples/example_02.py` і `tasks/task_02.py` у папці пакета.



```python
api = ClassroomAPI()
store = {}
def history_for(sid):
    return store.setdefault(sid,InMemoryChatMessageHistory())
prompt = ChatPromptTemplate.from_messages([("system","Відповідайте тільки з історії цієї сесії."),MessagesPlaceholder("history"),("human","{question}")])
model = RunnableLambda(lambda value: AIMessage(content=api.text(value,stage="memory")))
chat = RunnableWithMessageHistory(prompt | model,history_for,input_messages_key="question",history_messages_key="history")
QUERIES = []  # TODO: три пари (session_id, question) для A/A/B
if len(QUERIES)!=3:
    raise NotImplementedError("Заповніть QUERIES")
for sid,question in QUERIES:
    answer = chat.invoke({"question":question},config={"configurable":{"session_id":sid}})
show(api,{"answer":answer.content,"lengths":{k:len(v.messages) for k,v in store.items()}})
# TODO: перевірте 4/2 повідомлення та відсутність приватного тексту A в B.
```
# Блок 3. 45.1 · LangChain @tool і схема OpenAI

**30–55 хв.**

**Факт 3. Tool — це Python-функція, опис її призначення та схема аргументів.**
runtime.py оголошує lookup_ticket і get_sla через справжній декоратор @tool із
langchain-core. Docstring пояснює, коли дія доречна, а type hints задають типи.
convert_to_openai_function переносить цей контракт у function tool для Responses API.
Назва й схема не надають моделі прямого доступу до Python: виконання відбудеться
тільки через наш dispatcher. Strict schema допомагає формі аргументів, але не гарантує,
що запит до обраного інструмента доречний або що заявка існує.
У прикладі надсилаємо моделі самі схеми та просимо пояснити вибір. У наступних блоках
виконаємо справжні function calls. Два read-only tools не змінюють заявки.

### Приклад · реальний OpenAI API


```python
api = ClassroomAPI()
print(json.dumps(API_TOOLS,ensure_ascii=False,indent=2))
answer = api.text("Доступні схеми: "+json.dumps(API_TOOLS)+". Одним реченням поясніть: який tool спочатку потрібен для SLA T101 і чому?",stage="tool_schema")
show(api,{"answer":answer})
```
### Схема

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 880 115" role="img" aria-label="Схема потоку даних"><title>Блок 3: потік даних</title><g><title>Python + @tool</title><rect x="8" y="24" width="195" height="62" rx="10" fill="#eaf1ff" stroke="#2459be"/><text x="105" y="61" text-anchor="middle" font-family="sans-serif" font-size="16" fill="#182438">Python + @tool</text></g><path d="M 207 55 h 17 l -5 -5 m 5 5 l -5 5" fill="none" stroke="#2459be" stroke-width="2"/><g><title>JSON schema</title><rect x="228" y="24" width="195" height="62" rx="10" fill="#eaf1ff" stroke="#2459be"/><text x="325" y="61" text-anchor="middle" font-family="sans-serif" font-size="16" fill="#182438">JSON schema</text></g><path d="M 427 55 h 17 l -5 -5 m 5 5 l -5 5" fill="none" stroke="#2459be" stroke-width="2"/><g><title>OpenAI API</title><rect x="448" y="24" width="195" height="62" rx="10" fill="#eaf1ff" stroke="#2459be"/><text x="545" y="61" text-anchor="middle" font-family="sans-serif" font-size="16" fill="#182438">OpenAI API</text></g><path d="M 647 55 h 17 l -5 -5 m 5 5 l -5 5" fill="none" stroke="#2459be" stroke-width="2"/><g><title>Tool proposal</title><rect x="668" y="24" width="195" height="62" rx="10" fill="#eaf1ff" stroke="#2459be"/><text x="765" y="61" text-anchor="middle" font-family="sans-serif" font-size="16" fill="#182438">Tool proposal</text></g></svg>

### Повний промпт для OpenAI API


```text
Поясніть lookup_ticket(ticket_id) і get_sla(priority): перша функція повертає фактичний пріоритет заявки, друга — години за цим пріоритетом. Не плутайте опис tool із виконанням.
```

Промпт передається через Python-клієнт, а не вручну через чат. Фактичні системні інструкції й JSON-схеми наведені в PROMPTS.md та runtime.py.


### Зараз виконайте завдання 3

Після прикладу відкрийте `tasks/task_03.py`, допишіть TODO і запустіть. Для порівняння — `examples/example_03.py`. Це live-код із виданим ключем OpenAI. У ноутбуці використайте наступну комірку.

**Завдання 3.** Відкрийте Python-функцію get_sla і її JSON-схему. Збережіть перелік дозволених priority. Надішліть реальний запит пояснити різницю lookup_ticket і get_sla. Зіставте пояснення зі схемами.

### Підказки

1. TOOLS["get_sla"].args. 2. Literal задає три значення. 3. Пояснення моделі не є фактичним виконанням tool.

**Готово, якщо:** Є реальна @tool-схема, enum urgent/normal/low, strict=True та live-пояснення без твердження, що tool уже виконано.

Окремі файли: `examples/example_03.py` і `tasks/task_03.py` у папці пакета.



```python
api = ClassroomAPI()
TOOL_NAME = None  # TODO: get_sla
if TOOL_NAME not in TOOLS:
    raise NotImplementedError("Оберіть потрібний tool")
schema = next(t for t in API_TOOLS if t["name"]==TOOL_NAME)
show(api,{"schema":schema,"answer":api.text("Поясніть цю схему: "+json.dumps(schema),stage="tool_schema")})
```
# Блок 4. 45.2 · JSON-аргументи: parse → validate → dispatch

**55–80 хв.**

**Факт 4. Аргументи моделі проходять перевірку до Python-виклику.**
Зовнішній рядок спочатку читаємо json.loads, потім перевіряємо object, точний набір
ключів, типи та дозволені значення. Не використовуємо eval або getattr для довільних
назв. Dispatcher має allowlist із двох tools і повертає ok/data або ok/error.
Невідомий tool, зайвий ключ, число замість рядка й відсутня заявка — різні негативні кейси.
Приклад робить реальний API-запит на JSON-аргументи, після чого Python виконує dispatch.
Це ще не повний function-calling протокол: у ньому також є call_id та function_call_output,
які розберемо далі. Зберігайте цю різницю в назві свого результату.

### Приклад · реальний OpenAI API


```python
api = ClassroomAPI()
schema = {"type":"object","properties":{"priority":{"type":"string","enum":["urgent","normal","low"]}},"required":["priority"],"additionalProperties":False}
args = api.structured("Поверніть аргументи get_sla для priority urgent.",schema=schema,stage="arguments")
observation = dispatch("get_sla",args)
show(api,{"arguments":args,"observation":observation})
```
### Схема

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 880 115" role="img" aria-label="Схема потоку даних"><title>Блок 4: потік даних</title><g><title>Model arguments</title><rect x="8" y="24" width="195" height="62" rx="10" fill="#eaf1ff" stroke="#2459be"/><text x="105" y="61" text-anchor="middle" font-family="sans-serif" font-size="16" fill="#182438">Model arguments</text></g><path d="M 207 55 h 17 l -5 -5 m 5 5 l -5 5" fill="none" stroke="#2459be" stroke-width="2"/><g><title>JSON parse</title><rect x="228" y="24" width="195" height="62" rx="10" fill="#eaf1ff" stroke="#2459be"/><text x="325" y="61" text-anchor="middle" font-family="sans-serif" font-size="16" fill="#182438">JSON parse</text></g><path d="M 427 55 h 17 l -5 -5 m 5 5 l -5 5" fill="none" stroke="#2459be" stroke-width="2"/><g><title>Allowlist</title><rect x="448" y="24" width="195" height="62" rx="10" fill="#eaf1ff" stroke="#2459be"/><text x="545" y="61" text-anchor="middle" font-family="sans-serif" font-size="16" fill="#182438">Allowlist</text></g><path d="M 647 55 h 17 l -5 -5 m 5 5 l -5 5" fill="none" stroke="#2459be" stroke-width="2"/><g><title>Python tool</title><rect x="668" y="24" width="195" height="62" rx="10" fill="#eaf1ff" stroke="#2459be"/><text x="765" y="61" text-anchor="middle" font-family="sans-serif" font-size="16" fill="#182438">Python tool</text></g></svg>

### Повний промпт для OpenAI API


```text
Поверніть тільки аргументи get_sla для normal: JSON з одним ключем priority. Не додавайте tool name, годин чи пояснення.
```

Промпт передається через Python-клієнт, а не вручну через чат. Фактичні системні інструкції й JSON-схеми наведені в PROMPTS.md та runtime.py.


### Зараз виконайте завдання 4

Після прикладу відкрийте `tasks/task_04.py`, допишіть TODO і запустіть. Для порівняння — `examples/example_04.py`. Це live-код із виданим ключем OpenAI. У ноутбуці використайте наступну комірку.

**Завдання 4.** Отримайте від моделі аргументи для normal і виконайте get_sla. Локально перевірте unknown_tool, зламаний JSON та зайвий ключ. Виведіть різні error-коди; негативні тести не потребують додаткових API-запитів.

### Підказки

1. Schema та prompt задають normal. 2. Перевірте observation data.hours=24. 3. Викличте dispatch напряму для помилкових аргументів.

**Готово, якщо:** Live-аргументи normal дали 24 години; три негативні кейси мають окремі error-коди.

Окремі файли: `examples/example_04.py` і `tasks/task_04.py` у папці пакета.



```python
PRIORITY = None  # TODO: normal
if PRIORITY not in SLA:
    raise NotImplementedError("Заповніть PRIORITY")
api = ClassroomAPI()
schema = {"type":"object","properties":{"priority":{"type":"string","enum":list(SLA)}},"required":["priority"],"additionalProperties":False}
args = api.structured("Аргументи get_sla для "+PRIORITY,schema=schema,stage="arguments")
show(api,{"observation":dispatch("get_sla",args)})
# TODO: додайте три негативні локальні перевірки.
```
# Блок 5. 45.3 · Справжній Function Calling: call_id та observation

**80–105 хв.**

**Факт 5. Результат tool повертається моделі з тим самим call_id.**
Responses API може повернути output item type=function_call замість фінального тексту.
У ньому є name, arguments та call_id. Застосунок виконує dispatch, додає попередні output
items у діалог і надсилає function_call_output з відповідним call_id. Без цього модель
не отримала підтвердженого observation, навіть якщо ви надрукували результат у консолі.
runtime.run_agent реалізує саме цей цикл; історія передається явним input, store=False.
Перевіряємо response.status перед використанням output; incomplete не приймаємо за успіх.
У trace видно фактичні виклики й observation, а не вигадані «думки» моделі.

### Приклад · реальний OpenAI API


```python
api = ClassroomAPI()
result = run_agent(api,"Який SLA у заявки T101? Спочатку перевір заявку, потім SLA.")
show(api,result)
```
### Схема

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 880 115" role="img" aria-label="Схема потоку даних"><title>Блок 5: потік даних</title><g><title>Function call</title><rect x="8" y="24" width="195" height="62" rx="10" fill="#eaf1ff" stroke="#2459be"/><text x="105" y="61" text-anchor="middle" font-family="sans-serif" font-size="16" fill="#182438">Function call</text></g><path d="M 207 55 h 17 l -5 -5 m 5 5 l -5 5" fill="none" stroke="#2459be" stroke-width="2"/><g><title>call_id</title><rect x="228" y="24" width="195" height="62" rx="10" fill="#eaf1ff" stroke="#2459be"/><text x="325" y="61" text-anchor="middle" font-family="sans-serif" font-size="16" fill="#182438">call_id</text></g><path d="M 427 55 h 17 l -5 -5 m 5 5 l -5 5" fill="none" stroke="#2459be" stroke-width="2"/><g><title>Tool output</title><rect x="448" y="24" width="195" height="62" rx="10" fill="#eaf1ff" stroke="#2459be"/><text x="545" y="61" text-anchor="middle" font-family="sans-serif" font-size="16" fill="#182438">Tool output</text></g><path d="M 647 55 h 17 l -5 -5 m 5 5 l -5 5" fill="none" stroke="#2459be" stroke-width="2"/><g><title>Model answer</title><rect x="668" y="24" width="195" height="62" rx="10" fill="#eaf1ff" stroke="#2459be"/><text x="765" y="61" text-anchor="middle" font-family="sans-serif" font-size="16" fill="#182438">Model answer</text></g></svg>

### Повний промпт для OpenAI API


```text
Який SLA у заявки T102? Спочатку викличте lookup_ticket для T102; тільки після observation викличте get_sla за поверненим priority. Фінальний JSON має містити джерела з обох observation.
```

Промпт передається через Python-клієнт, а не вручну через чат. Фактичні системні інструкції й JSON-схеми наведені в PROMPTS.md та runtime.py.


### Зараз виконайте завдання 5

Після прикладу відкрийте `tasks/task_05.py`, допишіть TODO і запустіть. Для порівняння — `examples/example_05.py`. Це live-код із виданим ключем OpenAI. У ноутбуці використайте наступну комірку.

**Завдання 5.** Виконайте live-цикл для T102. Перевірте наявність lookup_ticket і get_sla у trace,
непорожні call_id та фінальний sla_hours=24. Перегляньте в runtime рядок function_call_output.

### Підказки

1. run_agent(api,question). 2. Перевірте множину tool names. 3. Перевірте validate на фінальному draft.

**Готово, якщо:** Є два реальні tool-виклики з call_id, observation і фінальний валідний SLA 24.

Окремі файли: `examples/example_05.py` і `tasks/task_05.py` у папці пакета.



```python
QUESTION = None  # TODO: запит про SLA T102 з вимогою перевірити ticket і policy
if not QUESTION:
    raise NotImplementedError("Заповніть QUESTION")
api = ClassroomAPI()
result = run_agent(api,QUESTION)
show(api,result)
# TODO: перевірте tool names, call_id та validate.
```
# Блок 6. 45.4 · ReAct-цикл: межі та помилки

**105–130 хв.**

**Факт 6. Кожний новий крок агента має бюджет і видимий результат попередньої дії.**
ReAct у практикумі — чергування рішення про дію, її виконання та observation.
Не вимагаємо прихованої траси міркувань. Для T103 lookup_ticket поверне low, отже
get_sla має отримати low й повернути 72 години. Бюджети max_rounds і max_tools — різні:
одна відповідь моделі може запропонувати кілька tools. Перед виконанням усієї партії
перевіряємо, чи не буде перевищено загальну межу.
Якщо модель не завершила цикл, повертаємо явну помилку budget_exhausted. Не додаємо
нескінченних повторів або «успішного» fallback із вигаданим текстом. Помилки tools є
структурованими observation, помилки API — окремими діагностичними статусами.

### Приклад · реальний OpenAI API


```python
api = ClassroomAPI(max_calls=4)
result = run_agent(api,"Перевір SLA заявки T103 через ticket і policy.",max_rounds=4,max_tools=4)
show(api,{"result":result,"remaining_calls":api.max_calls-api.calls_used})
```
### Схема

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 880 115" role="img" aria-label="Схема потоку даних"><title>Блок 6: потік даних</title><g><title>Model round</title><rect x="8" y="24" width="195" height="62" rx="10" fill="#eaf1ff" stroke="#2459be"/><text x="105" y="61" text-anchor="middle" font-family="sans-serif" font-size="16" fill="#182438">Model round</text></g><path d="M 207 55 h 17 l -5 -5 m 5 5 l -5 5" fill="none" stroke="#2459be" stroke-width="2"/><g><title>Tools</title><rect x="228" y="24" width="195" height="62" rx="10" fill="#eaf1ff" stroke="#2459be"/><text x="325" y="61" text-anchor="middle" font-family="sans-serif" font-size="16" fill="#182438">Tools</text></g><path d="M 427 55 h 17 l -5 -5 m 5 5 l -5 5" fill="none" stroke="#2459be" stroke-width="2"/><g><title>Observation</title><rect x="448" y="24" width="195" height="62" rx="10" fill="#eaf1ff" stroke="#2459be"/><text x="545" y="61" text-anchor="middle" font-family="sans-serif" font-size="16" fill="#182438">Observation</text></g><path d="M 647 55 h 17 l -5 -5 m 5 5 l -5 5" fill="none" stroke="#2459be" stroke-width="2"/><g><title>Budget / stop</title><rect x="668" y="24" width="195" height="62" rx="10" fill="#eaf1ff" stroke="#2459be"/><text x="765" y="61" text-anchor="middle" font-family="sans-serif" font-size="16" fill="#182438">Budget / stop</text></g></svg>

### Повний промпт для OpenAI API


```text
Для T101 спочатку прочитайте заявку, потім SLA за її priority. Не повторюйте той самий tool без нових даних. Якщо немає достатніх даних, повідомте це; не вигадуйте observation.
```

Промпт передається через Python-клієнт, а не вручну через чат. Фактичні системні інструкції й JSON-схеми наведені в PROMPTS.md та runtime.py.


### Зараз виконайте завдання 6

Після прикладу відкрийте `tasks/task_06.py`, допишіть TODO і запустіть. Для порівняння — `examples/example_06.py`. Це live-код із виданим ключем OpenAI. У ноутбуці використайте наступну комірку.

**Завдання 6.** Запустіть T101 з max_rounds=4, max_tools=4. Перевірте SLA=4 і бюджет api.calls_used<=4.
Окремо без мережі перевірте, що max_rounds=0 відхиляється. Поясніть різницю бюджету tools та модельних викликів.

### Підказки

1. Невалідні межі відхиляються до запиту. 2. Не провокуйте зайві платні помилки для тесту. 3. Перегляньте rounds і tool_count.

**Готово, якщо:** Live-цикл дав SLA 4, бюджети дотримані, нульовий max_rounds відхилено локально.

Окремі файли: `examples/example_06.py` і `tasks/task_06.py` у папці пакета.



```python
api = ClassroomAPI(max_calls=4)
QUESTION = None  # TODO: T101, ticket -> policy
if not QUESTION:
    raise NotImplementedError("Заповніть QUESTION")
result = run_agent(api,QUESTION,max_rounds=4,max_tools=4)
show(api,result)
# TODO: assert для SLA й бюджету.
```
# Блок 7. 46.1 · Модельний router і локальна політика

**130–150 хв.**

**Факт 7. Класифікація моделі обирає маршрут, але не скасовує обов’язкову перевірку людиною.**
Router повертає route з enum support/refund/unknown та коротку reason. Після JSON
код перевіряє enum. Запити про повернення чи компенсацію мають локальну політику review:
навіть помилковий route від LLM не може перетворити їх на автоматичну дію.
Короткий reason допомагає пояснити вибір, але не є прихованим chain-of-thought.
Для складної предметної області словникового правила недостатньо: тут воно явно
обмежене навчальними формулюваннями українською та refund англійською.
Зміна маршруту впливає на наступні кроки, тому журналюємо route окремим stage.

### Приклад · реальний OpenAI API


```python
api = ClassroomAPI()
routed = route_query(api,"Підготуй пропозицію повернення коштів за T102")
show(api,routed)
```
### Схема

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 880 115" role="img" aria-label="Схема потоку даних"><title>Блок 7: потік даних</title><g><title>Question</title><rect x="8" y="24" width="195" height="62" rx="10" fill="#eaf1ff" stroke="#2459be"/><text x="105" y="61" text-anchor="middle" font-family="sans-serif" font-size="16" fill="#182438">Question</text></g><path d="M 207 55 h 17 l -5 -5 m 5 5 l -5 5" fill="none" stroke="#2459be" stroke-width="2"/><g><title>Live router</title><rect x="228" y="24" width="195" height="62" rx="10" fill="#eaf1ff" stroke="#2459be"/><text x="325" y="61" text-anchor="middle" font-family="sans-serif" font-size="16" fill="#182438">Live router</text></g><path d="M 427 55 h 17 l -5 -5 m 5 5 l -5 5" fill="none" stroke="#2459be" stroke-width="2"/><g><title>Local policy</title><rect x="448" y="24" width="195" height="62" rx="10" fill="#eaf1ff" stroke="#2459be"/><text x="545" y="61" text-anchor="middle" font-family="sans-serif" font-size="16" fill="#182438">Local policy</text></g><path d="M 647 55 h 17 l -5 -5 m 5 5 l -5 5" fill="none" stroke="#2459be" stroke-width="2"/><g><title>Route</title><rect x="668" y="24" width="195" height="62" rx="10" fill="#eaf1ff" stroke="#2459be"/><text x="765" y="61" text-anchor="middle" font-family="sans-serif" font-size="16" fill="#182438">Route</text></g></svg>

### Повний промпт для OpenAI API


```text
Оберіть route: support для SLA заявки; refund для повернення коштів; unknown для нерелевантного питання. Поверніть route і коротку reason. Не виконуйте бізнес-дій.
```

Промпт передається через Python-клієнт, а не вручну через чат. Фактичні системні інструкції й JSON-схеми наведені в PROMPTS.md та runtime.py.


### Зараз виконайте завдання 7

Після прикладу відкрийте `tasks/task_07.py`, допишіть TODO і запустіть. Для порівняння — `examples/example_07.py`. Це live-код із виданим ключем OpenAI. У ноутбуці використайте наступну комірку.

**Завдання 7.** Класифікуйте три запити: SLA T101; повернення коштів T102; рецепт борщу.
Перевірте support/refund/unknown. Для refund поясніть роль локального правила; усі три запити мають бути справжніми API-викликами.

### Підказки

1. route_query по одному питанню. 2. Порівняйте enum. 3. Невдалу класифікацію збережіть, не підміняйте результат.

**Готово, якщо:** Три live-маршрути й записи usage; refund зберігає обов’язковий review.

Окремі файли: `examples/example_07.py` і `tasks/task_07.py` у папці пакета.



```python
api = ClassroomAPI()
QUERIES = []  # TODO: три запити support/refund/unknown
if len(QUERIES)!=3:
    raise NotImplementedError("Додайте три запити")
routes = [route_query(api,q) for q in QUERIES]
show(api,routes)
# TODO: перевірте три маршрути.
```
# Блок 8. 46.2 · Sequential workflow і незалежний validator

**150–170 хв.**

**Факт 8. Послідовність generate → validate має явний контракт на межі кожного кроку.**
Чернетка містить answer, ticket_id, sla_hours, needs_human, sources. Structured Output
контролює форму JSON, але Python звіряє SLA з локальною таблицею, перевіряє id та джерела.
Validator повертає ok і список reasons. Неправильне число не виправляється мовчазно.
Текст answer може ще потребувати змістовного перегляду: правильні структуровані поля
не гарантують відсутність суперечностей у вільному реченні. Для зовнішніх дій додавайте
предметні перевірки та review; у цій вправі ніяких зовнішніх змін немає.
Використайте результати перевірки як дані наступного вузла, а не просто print у консолі.

### Приклад · реальний OpenAI API


```python
api = ClassroomAPI()
question = "Який SLA у заявки T102?"
draft = draft_for(api,question,"support")
check = validate(draft,question,"support")
show(api,{"draft":draft,"validation":check})
```
### Схема

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 880 115" role="img" aria-label="Схема потоку даних"><title>Блок 8: потік даних</title><g><title>Live draft</title><rect x="8" y="24" width="195" height="62" rx="10" fill="#eaf1ff" stroke="#2459be"/><text x="105" y="61" text-anchor="middle" font-family="sans-serif" font-size="16" fill="#182438">Live draft</text></g><path d="M 207 55 h 17 l -5 -5 m 5 5 l -5 5" fill="none" stroke="#2459be" stroke-width="2"/><g><title>Schema</title><rect x="228" y="24" width="195" height="62" rx="10" fill="#eaf1ff" stroke="#2459be"/><text x="325" y="61" text-anchor="middle" font-family="sans-serif" font-size="16" fill="#182438">Schema</text></g><path d="M 427 55 h 17 l -5 -5 m 5 5 l -5 5" fill="none" stroke="#2459be" stroke-width="2"/><g><title>Fact validator</title><rect x="448" y="24" width="195" height="62" rx="10" fill="#eaf1ff" stroke="#2459be"/><text x="545" y="61" text-anchor="middle" font-family="sans-serif" font-size="16" fill="#182438">Fact validator</text></g><path d="M 647 55 h 17 l -5 -5 m 5 5 l -5 5" fill="none" stroke="#2459be" stroke-width="2"/><g><title>ok / reasons</title><rect x="668" y="24" width="195" height="62" rx="10" fill="#eaf1ff" stroke="#2459be"/><text x="765" y="61" text-anchor="middle" font-family="sans-serif" font-size="16" fill="#182438">ok / reasons</text></g></svg>

### Повний промпт для OpenAI API


```text
Факти: T103 має priority low; SLA low — 72 години. Поверніть answer, ticket_id=T103, sla_hours=72, needs_human=false, sources з ticket:T103 та sla:low. Не змінюйте факти.
```

Промпт передається через Python-клієнт, а не вручну через чат. Фактичні системні інструкції й JSON-схеми наведені в PROMPTS.md та runtime.py.


### Зараз виконайте завдання 8

Після прикладу відкрийте `tasks/task_08.py`, допишіть TODO і запустіть. Для порівняння — `examples/example_08.py`. Це live-код із виданим ключем OpenAI. У ноутбуці використайте наступну комірку.

**Завдання 8.** Отримайте live-чернетку для T103 та перевірте SLA=72. У копії чернетки локально змініть
sla_hours на 1, а потім sources на невідомий id. Перевірте wrong_sla й unknown_or_duplicate_source.

### Підказки

1. Не змінюйте оригінальний live-вивід. 2. Робіть копії словника. 3. Негативні перевірки без мережі.

**Готово, якщо:** Є live-чернетка T103/72, валідний контракт і два незалежні негативні кейси.

Окремі файли: `examples/example_08.py` і `tasks/task_08.py` у папці пакета.



```python
api = ClassroomAPI()
QUESTION = None  # TODO: T103
if not QUESTION:
    raise NotImplementedError("Заповніть QUESTION")
draft = draft_for(api,QUESTION,"support")
show(api,{"draft":draft,"check":validate(draft,QUESTION)})
# TODO: дві локальні копії з помилками SLA та source.
```
# Блок 9. 46.3 · Repair і retry budget

**170–185 хв.**

**Факт 9. Повтор через помилку мережі та виправлення змісту — різні механізми.**
SDK max_retries=0 прибирає приховані повтори транспорту. Бізнес-етап repair отримує
чернетку, перевірені джерела й конкретні reasons, виконує один новий модельний запит
і знову проходить validator. Якщо друга версія неправильна, workflow має rejected,
а не нескінченний цикл. Кількість repair і calls_used записуються в стан.
Щоб гарантовано побачити цей шлях, приклад починається з навмисно хибного числа
в локальній навчальній чернетці. Це дефектний вхід для досліду; виправлена відповідь
далі отримується справжнім OpenAI API, без підстановки готового результату.

### Приклад · реальний OpenAI API


```python
api = ClassroomAPI()
question = "Який SLA у заявки T101?"
broken = {"answer":"Термін 99 годин","ticket_id":"T101","sla_hours":99,"needs_human":False,"sources":["ticket:T101","sla:urgent"]}
check = validate(broken,question)
fixed,final_check = repair_once(api,question,broken,check,"support")
show(api,{"before":check,"after":fixed,"validation":final_check})
```
### Схема

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 880 115" role="img" aria-label="Схема потоку даних"><title>Блок 9: потік даних</title><g><title>Bad draft</title><rect x="8" y="24" width="195" height="62" rx="10" fill="#eaf1ff" stroke="#2459be"/><text x="105" y="61" text-anchor="middle" font-family="sans-serif" font-size="16" fill="#182438">Bad draft</text></g><path d="M 207 55 h 17 l -5 -5 m 5 5 l -5 5" fill="none" stroke="#2459be" stroke-width="2"/><g><title>Reasons</title><rect x="228" y="24" width="195" height="62" rx="10" fill="#eaf1ff" stroke="#2459be"/><text x="325" y="61" text-anchor="middle" font-family="sans-serif" font-size="16" fill="#182438">Reasons</text></g><path d="M 427 55 h 17 l -5 -5 m 5 5 l -5 5" fill="none" stroke="#2459be" stroke-width="2"/><g><title>One live repair</title><rect x="448" y="24" width="195" height="62" rx="10" fill="#eaf1ff" stroke="#2459be"/><text x="545" y="61" text-anchor="middle" font-family="sans-serif" font-size="16" fill="#182438">One live repair</text></g><path d="M 647 55 h 17 l -5 -5 m 5 5 l -5 5" fill="none" stroke="#2459be" stroke-width="2"/><g><title>Validate again</title><rect x="668" y="24" width="195" height="62" rx="10" fill="#eaf1ff" stroke="#2459be"/><text x="765" y="61" text-anchor="middle" font-family="sans-serif" font-size="16" fill="#182438">Validate again</text></g></svg>

### Повний промпт для OpenAI API


```text
Виправте чернетку T102/SLA=5 за перевіреними фактами: T102 normal, SLA normal 24. Поверніть п’ять полів за схемою. Не додавайте нових джерел. Python повторно перевірить результат.
```

Промпт передається через Python-клієнт, а не вручну через чат. Фактичні системні інструкції й JSON-схеми наведені в PROMPTS.md та runtime.py.


### Зараз виконайте завдання 9

Після прикладу відкрийте `tasks/task_09.py`, допишіть TODO і запустіть. Для порівняння — `examples/example_09.py`. Це live-код із виданим ключем OpenAI. У ноутбуці використайте наступну комірку.

**Завдання 9.** Створіть навмисно хибну чернетку T102 з SLA=5, виконайте один live-repair і перевірте
24. Перевірте calls_used=1. Якщо repair не пройшов, збережіть rejected та reasons, не запускайте нескінченний повтор.

### Підказки

1. Початкова помилка є локальним тестовим входом. 2. repair_once робить один запит. 3. Обов’язкова повторна validate.

**Готово, якщо:** Один реальний repair, повторна перевірка й SLA=24; лічильник викликів показано.

Окремі файли: `examples/example_09.py` і `tasks/task_09.py` у папці пакета.



```python
api = ClassroomAPI()
BROKEN_SLA = None  # TODO: неправильне число для T102
if type(BROKEN_SLA) is not int or BROKEN_SLA==24:
    raise NotImplementedError("Задайте навмисно неправильний SLA")
question = "Який SLA у заявки T102?"
broken = {"answer":"Навмисна помилка","ticket_id":"T102","sla_hours":BROKEN_SLA,"needs_human":False,"sources":["ticket:T102","sla:normal"]}
fixed,check = repair_once(api,question,broken,validate(broken,question),"support")
show(api,{"fixed":fixed,"check":check})
```
# Блок 10. 46.4 · HITL: зберегти стан і поставити паузу

**185–200 хв.**

**Факт 10. Пауза для людини — збережений стан, з якого можна продовжити пізніше.**
Для запиту про повернення коштів workflow виконує live-router і live-draft, перевіряє
контракт і записує JSON зі status=paused_for_human. Є request_id, revision, question,
route, draft, validation, trace, model і calls_used. Так людина бачить не лише кнопку
«ок», а перевірювану пропозицію та її походження.
Модель не отримує tool виплати. Навіть якщо текст користувача наказує «вже поверни»,
локальна політика зберігає паузу. external_action_executed=false явно позначає, що
зовнішньої дії не було. Зберігайте файл до рішення: стан має пережити завершення скрипта.

### Приклад · реальний OpenAI API


```python
api = ClassroomAPI()
state,path = run_workflow(api,"Підготуй пропозицію повернення коштів за T102")
show(api,{"state":state,"review_file":str(path)})
```
### Схема

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 880 115" role="img" aria-label="Схема потоку даних"><title>Блок 10: потік даних</title><g><title>Live proposal</title><rect x="8" y="24" width="195" height="62" rx="10" fill="#eaf1ff" stroke="#2459be"/><text x="105" y="61" text-anchor="middle" font-family="sans-serif" font-size="16" fill="#182438">Live proposal</text></g><path d="M 207 55 h 17 l -5 -5 m 5 5 l -5 5" fill="none" stroke="#2459be" stroke-width="2"/><g><title>Validate</title><rect x="228" y="24" width="195" height="62" rx="10" fill="#eaf1ff" stroke="#2459be"/><text x="325" y="61" text-anchor="middle" font-family="sans-serif" font-size="16" fill="#182438">Validate</text></g><path d="M 427 55 h 17 l -5 -5 m 5 5 l -5 5" fill="none" stroke="#2459be" stroke-width="2"/><g><title>JSON state</title><rect x="448" y="24" width="195" height="62" rx="10" fill="#eaf1ff" stroke="#2459be"/><text x="545" y="61" text-anchor="middle" font-family="sans-serif" font-size="16" fill="#182438">JSON state</text></g><path d="M 647 55 h 17 l -5 -5 m 5 5 l -5 5" fill="none" stroke="#2459be" stroke-width="2"/><g><title>Pause</title><rect x="668" y="24" width="195" height="62" rx="10" fill="#eaf1ff" stroke="#2459be"/><text x="765" y="61" text-anchor="middle" font-family="sans-serif" font-size="16" fill="#182438">Pause</text></g></svg>

### Повний промпт для OpenAI API


```text
Підготуйте пропозицію повернення коштів за T101 для розгляду людиною. Не повідомляйте, що виплату виконано. needs_human=true, sla_hours=null; фактичної дії немає.
```

Промпт передається через Python-клієнт, а не вручну через чат. Фактичні системні інструкції й JSON-схеми наведені в PROMPTS.md та runtime.py.


### Зараз виконайте завдання 10

Після прикладу відкрийте `tasks/task_10.py`, допишіть TODO і запустіть. Для порівняння — `examples/example_10.py`. Це live-код із виданим ключем OpenAI. У ноутбуці використайте наступну комірку.

**Завдання 10.** Створіть live-пропозицію повернення за T101. Перевірте paused_for_human, revision=1,
існування файла та external_action_executed=false. Прочитайте JSON заново з диска й звірте request_id.

### Підказки

1. run_workflow робить реальні запити. 2. Файл має бути в results/. 3. Пока не викликайте approve.

**Готово, якщо:** Два або більше live-виклики, файл стану з паузою, ревізією та відсутністю зовнішньої дії.

Окремі файли: `examples/example_10.py` і `tasks/task_10.py` у папці пакета.



```python
api = ClassroomAPI()
QUESTION = None  # TODO: пропозиція повернення за T101
if not QUESTION:
    raise NotImplementedError("Заповніть QUESTION")
state,path = run_workflow(api,QUESTION)
show(api,{"state":state,"path":str(path)})
# TODO: прочитайте файл і перевірте pause/revision/external_action_executed.
```
# Блок 11. 46.5 · Resume: approve, edit, reject

**200–215 хв.**

**Факт 11. Рішення людини також має правила переходу та повторну валідацію.**
Після paused_for_human можна approve, edit або reject. Edit змінює текст answer,
не довільні id чи SLA. Перед фінальним статусом знову виконується validate. Ревізія
збільшується; повторне рішення для того самого завершеного файла відхиляється.
Це локальна послідовна демонстрація, а не готовий сервіс із транзакційним блокуванням.
Для справжньої команди review потрібні авторизація, журнал рецензента й захист від
одночасного схвалення. Тут усі приклади працюють тільки з навчальними файлами.
Схвалення затверджує чернетку, але не запускає платіж чи надсилання повідомлення.

### Приклад · реальний OpenAI API


```python
api = ClassroomAPI()
state,path = run_workflow(api,"Підготуй пропозицію повернення коштів за T102")
reviewed = resume(path,"edit",edited_answer="Пропозицію передано на розгляд; повернення коштів ще не виконувалось.")
show(api,{"reviewed":reviewed})
```
### Схема

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 880 115" role="img" aria-label="Схема потоку даних"><title>Блок 11: потік даних</title><g><title>Saved pause</title><rect x="8" y="24" width="195" height="62" rx="10" fill="#eaf1ff" stroke="#2459be"/><text x="105" y="61" text-anchor="middle" font-family="sans-serif" font-size="16" fill="#182438">Saved pause</text></g><path d="M 207 55 h 17 l -5 -5 m 5 5 l -5 5" fill="none" stroke="#2459be" stroke-width="2"/><g><title>Human decision</title><rect x="228" y="24" width="195" height="62" rx="10" fill="#eaf1ff" stroke="#2459be"/><text x="325" y="61" text-anchor="middle" font-family="sans-serif" font-size="16" fill="#182438">Human decision</text></g><path d="M 427 55 h 17 l -5 -5 m 5 5 l -5 5" fill="none" stroke="#2459be" stroke-width="2"/><g><title>Revalidate</title><rect x="448" y="24" width="195" height="62" rx="10" fill="#eaf1ff" stroke="#2459be"/><text x="545" y="61" text-anchor="middle" font-family="sans-serif" font-size="16" fill="#182438">Revalidate</text></g><path d="M 647 55 h 17 l -5 -5 m 5 5 l -5 5" fill="none" stroke="#2459be" stroke-width="2"/><g><title>Approve / reject</title><rect x="668" y="24" width="195" height="62" rx="10" fill="#eaf1ff" stroke="#2459be"/><text x="765" y="61" text-anchor="middle" font-family="sans-serif" font-size="16" fill="#182438">Approve / reject</text></g></svg>

### Повний промпт для OpenAI API


```text
Підготуйте чернетку пропозиції повернення T103. Потрібен review людини; не стверджуйте, що виплату виконано. Не намагайтеся схвалити власну пропозицію.
```

Промпт передається через Python-клієнт, а не вручну через чат. Фактичні системні інструкції й JSON-схеми наведені в PROMPTS.md та runtime.py.


### Зараз виконайте завдання 11

Після прикладу відкрийте `tasks/task_11.py`, допишіть TODO і запустіть. Для порівняння — `examples/example_11.py`. Це live-код із виданим ключем OpenAI. У ноутбуці використайте наступну комірку.

**Завдання 11.** Згенеруйте live-чернетку T103 для повернення, відхиліть її через resume(...,"reject").
Перевірте status=rejected і revision=2. Повторний approve цього самого файла має завершитися ClassroomError без нового API-виклику.

### Підказки

1. Спершу має бути paused_for_human. 2. Збережіть calls_used до review. 3. Повторний виклик обгорніть try/except.

**Готово, якщо:** Є live-походження чернетки, відхилення з revision=2 і заблокований повторний approve без додаткового API-запиту.

Окремі файли: `examples/example_11.py` і `tasks/task_11.py` у папці пакета.



```python
api = ClassroomAPI()
state,path = run_workflow(api,"Підготуй пропозицію повернення коштів за T103")
DECISION = None  # TODO: reject
if DECISION not in {"approve","edit","reject"}:
    raise NotImplementedError("Оберіть рішення")
reviewed = resume(path,DECISION)
show(api,reviewed)
# TODO: перевірте revision та заблокуйте повторний review.
```
# Блок 12. 46.6 · Повний workflow, журнал і захист

**215–230 хв.**

**Факт 12. Завершення workflow доводиться станом, перевірками та журналом викликів.**
Підсумок: route → tools/draft → validate → до одного repair → completed або
paused_for_human/rejected. Клієнт моделі є залежністю ClassroomAPI, а не копією SDK-коду
в кожному вузлі. Це дозволяє тестувати транспорт локально, не підміняючи live-режим
навчальних прикладів. Дані про model, status, usage та latency потрапляють у usage.jsonl.
Ключі не записуються, текст заявки не потрібний у транспортному журналі.
Ви маєте показати живий tool trace і файл review, а локальні негативні тести позначити
окремо. Зелений транспортний тест не є фактично виконаним живим запитом.
Exit ticket: хто виконав дію; як перевірено факт; де межа повторів; який статус очікує людину?
Де перечитати: блоки 5, 8, 9, 10–11.

### Приклад · реальний OpenAI API


```python
api = ClassroomAPI(max_calls=8)
state,path = run_workflow(api,"Який SLA у заявки T101? Перевірте через інструменти.")
show(api,{"state":state,"saved_to":str(path)})
```
### Схема

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 880 115" role="img" aria-label="Схема потоку даних"><title>Блок 12: потік даних</title><g><title>Route</title><rect x="8" y="24" width="195" height="62" rx="10" fill="#eaf1ff" stroke="#2459be"/><text x="105" y="61" text-anchor="middle" font-family="sans-serif" font-size="16" fill="#182438">Route</text></g><path d="M 207 55 h 17 l -5 -5 m 5 5 l -5 5" fill="none" stroke="#2459be" stroke-width="2"/><g><title>Agent / draft</title><rect x="228" y="24" width="195" height="62" rx="10" fill="#eaf1ff" stroke="#2459be"/><text x="325" y="61" text-anchor="middle" font-family="sans-serif" font-size="16" fill="#182438">Agent / draft</text></g><path d="M 427 55 h 17 l -5 -5 m 5 5 l -5 5" fill="none" stroke="#2459be" stroke-width="2"/><g><title>Validate / repair</title><rect x="448" y="24" width="195" height="62" rx="10" fill="#eaf1ff" stroke="#2459be"/><text x="545" y="61" text-anchor="middle" font-family="sans-serif" font-size="16" fill="#182438">Validate / repair</text></g><path d="M 647 55 h 17 l -5 -5 m 5 5 l -5 5" fill="none" stroke="#2459be" stroke-width="2"/><g><title>State + log</title><rect x="668" y="24" width="195" height="62" rx="10" fill="#eaf1ff" stroke="#2459be"/><text x="765" y="61" text-anchor="middle" font-family="sans-serif" font-size="16" fill="#182438">State + log</text></g></svg>

### Повний промпт для OpenAI API


```text
Який SLA у заявки T102? Використайте lookup_ticket та get_sla, поверніть перевірювані поля й source ids. Не виконуйте жодної зовнішньої дії.
```

Промпт передається через Python-клієнт, а не вручну через чат. Фактичні системні інструкції й JSON-схеми наведені в PROMPTS.md та runtime.py.


### Зараз виконайте завдання 12

Після прикладу відкрийте `tasks/task_12.py`, допишіть TODO і запустіть. Для порівняння — `examples/example_12.py`. Це live-код із виданим ключем OpenAI. У ноутбуці використайте наступну комірку.

**Завдання 12.** Запустіть повний live-workflow для SLA T102. Перевірте completed, SLA=24, validation.ok
та наявність tools у trace. Збережіть REPORT.md: question, model, call count, usage,
валідація, межі та відмінність від запиту про повернення. Не включайте ключ.

### Підказки

1. max_calls=8 не гарантує певної ціни, але обмежує виклики. 2. completed не означає, що відбулась зовнішня дія. 3. Файл звіту зберігайте в results/.

**Готово, якщо:** Повний live-цикл completed/T102/24, tool trace, usage та REPORT.md без ключа; refund-маршрут відмежовано.

Окремі файли: `examples/example_12.py` і `tasks/task_12.py` у папці пакета.



```python
api = ClassroomAPI(max_calls=8)
QUESTION = None  # TODO: SLA T102 з перевіркою tools
if not QUESTION:
    raise NotImplementedError("Заповніть QUESTION")
state,path = run_workflow(api,QUESTION)
show(api,{"state":state,"path":str(path)})
# TODO: перевірки completed, SLA, trace та власний REPORT.md.
```
# Що здати

Заповнені tasks, JSON-файли двох workflow (SLA та refund), один завершений review,
usage.jsonl і REPORT.md. Перед здачею переконайтеся, що .env і ключа в архіві немає.
У звіті відокремте фактичні live-запуски від локальних негативних кейсів.

## Домашня практика і резерв

Додайте заявку T104 та тест її priority. Додайте новий read-only tool із точною схемою,
allowlist і негативним тестом аргументів. Перевірте, що модель його використала, а
повернення коштів як і раніше очікує людину. Поглиблення: зобразіть workflow як граф,
не змінюючи його станів і бюджетів. Нові платні запуски виконуйте в межах виданого доступу.

## Офіційні джерела

- [OpenAI: Function Calling](https://developers.openai.com/api/docs/guides/function-calling)
- [OpenAI: Structured Outputs](https://developers.openai.com/api/docs/guides/structured-outputs)
- [OpenAI: Responses API](https://developers.openai.com/api/reference/responses/overview)
- [OpenAI: керування ключами](https://platform.openai.com/api-keys)
- [LangChain: tools](https://docs.langchain.com/oss/python/langchain/tools)
- [LangChain: RunnableWithMessageHistory](https://reference.langchain.com/python/langchain-core/runnables/history/RunnableWithMessageHistory)

Програму звірено з наданими HTML 43–46. Код підготовлено 06.11.2026.
Модель задається через OPENAI_MODEL, фактична версія відповіді записується в журнал.



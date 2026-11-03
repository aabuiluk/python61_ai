# Готові розібрані приклади

Це повні приклади на окремій історії бібліотеки. Самостійні задачі про онлайн-школу лежать у tasks/.

Вставте власний токен у .env біля api_client.py. Після встановлення requirements.txt запускайте з кореня репозиторію:

## Документ → запит → реальна відповідь

python -m PythonAI_Author_Lesson41_Lesson42.examples.example_01_source_api

## Готовий міні-RAG на іншому корпусі

python -m PythonAI_Author_Lesson41_Lesson42.examples.example_02_mini_rag_api

## Реальний Function Calling у два запити

python -m PythonAI_Author_Lesson41_Lesson42.examples.example_03_function_call_api

Усі три приклади викликають реальний OpenAI API. Перші два роблять по одному запиту, третій — два. Імпорт не надсилає запити.

Основний ноутбук можна відкрити і з кореня, і з цієї папки. Файли HTML/MD/IPYNB в обох місцях ідентичні. ZIP також продубльовано.

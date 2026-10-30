# Готові розібрані приклади

Це повні приклади на окремій історії бібліотеки. Самостійні задачі про онлайн-школу лежать у tasks/.

Вставте власний токен у .env біля api_client.py. Після встановлення requirements.txt запускайте з папки практикуму:

## Документ → запит → реальна відповідь

python examples/example_01_source_api.py

## Готовий міні-RAG на іншому корпусі

python examples/example_02_mini_rag_api.py

## Реальний Function Calling у два запити

python examples/example_03_function_call_api.py

Усі три приклади викликають реальний OpenAI API. Перші два роблять по одному запиту, третій — два. Імпорт не надсилає запити.

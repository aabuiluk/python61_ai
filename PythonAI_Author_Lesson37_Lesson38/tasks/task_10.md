**Завдання 10. Звіт і наступний дослід.** Додайте case 'outside': правильну книгу b04 з непорожнім reason.
Перевірте весь набір для b02, b03 та збережіть eval_report.csv. Створіть live_protocol.json із
двома версіями промпту, однаковими case_id та статусом not_run. Перелічіть, що треба зафіксувати
для справжнього порівняння. Не записуйте вигадані результати моделі.

Підказки
1. Скопіюйте fixtures через dict та додайте outside з правильним title каталогу.
2. evaluate_fixtures повертає DataFrame; to_csv(..., index=False, encoding='utf-8-sig').
3. Для protocol використайте списки prompt_versions, case_ids та metadata_required.
4. Збережіть JSON через json.dumps(..., ensure_ascii=False, indent=2).

Готово, якщо: CSV має 6 кейсів і 1 прийнятий; протокол not_run не містить вигаданих вимірювань LLM.

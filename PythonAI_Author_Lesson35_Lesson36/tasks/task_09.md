**Завдання 9. Збережіть результат.** Отримайте top-3 для Olia, перевірте відсутність уже оцінених книг, запишіть у results/book_recommendations.csv. Прочитайте файл назад і звірте список ID. Окремо викличте рекомендацію для NewReader та поясніть reason.

Підказки
1. recommend_user уже розібрано в демонстрації; використайте його без нових формул.
2. seen визначайте за train, а не events.
3. Перетин set(result.book_id) & seen має бути порожнім.
4. OUTPUT_DIR.mkdir(parents=True,exist_ok=True); шлях OUTPUT_DIR/'book_recommendations.csv'.
5. to_csv(index=False,encoding='utf-8-sig'), потім pd.read_csv з тим самим кодуванням.

Готово, якщо: CSV існує, ID після читання збігаються, self-history відсутня, fallback підписано.

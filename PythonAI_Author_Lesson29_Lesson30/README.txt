Штучний інтелект з використанням Python · роздаток пар 29–30

Пара 28 (передумова). Word2Vec / GloVe — повторення і місток до послідовностей.
Пара 29. Мовні моделі: RNN, LSTM і Transformers.
Пара 30. Приклад seq2seq і transfer learning.

У пакеті:
- готова програма Lesson30_04_supportflow_bot.py: чат-бот на LSTM + GloVe
- models/supportflow_bot.pth — навчений seq2seq LSTM; embedding — заморожений GloVe (береться з assets/)
- assets/supportflow_qa.csv — 30 пар «запит → відповідь» служби підтримки SupportFlow
- test_data/supportflow_paraphrases.csv — 15 нових формулювань запитів з еталонними відповідями
- assets/glove/glove_100d.bin — GloVe 6B 100d, 25 тис. слів (словник пар 27–28 + слова підтримки)
- supportflow.py — спільний код: словник, Seq2Seq (RNN / LSTM / GRU, attention), TransformerSeq2Seq,
  навчання, генерація, метрики, читання GloVe без gensim
- 9 скриптів-прикладів: Lesson28_05, Lesson29_01…04, Lesson30_01…04
- Lesson29_tasks.md, Lesson30_tasks.md — по 3 практичні завдання на пару
- Lesson29_homework.md, Lesson30_homework.md — домашнє 6.3
- Lesson28_recap.md — що треба памʼятати з пари 28
- Lesson29_30_plan_180.md — план заняття на 180 хвилин
- baked HTML-презентації пар 28, 29, 30

Без GPU: усе навчається на CPU за секунди. distilGPT2 — необовʼязково (pip install transformers).
Спочатку START.txt і Lesson29_30_plan_180.md.

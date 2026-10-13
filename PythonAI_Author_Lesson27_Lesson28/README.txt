Штучний інтелект з використанням Python · роздаток пар 27–28

Пара 27. Корпуси та embeddings: Word2Vec і GloVe.
Пара 28. Word2Vec / GloVe і практичні приклади.

У пакеті:
- готова програма Lesson28_04_word_explorer.py: сусіди, схожість, аналогії, оцінка моделей
- models/reviews_w2v.bin — наш Word2Vec (Skip-gram, 100 вимірів, 15 тис. слів) на 1,4 млн слів відгуків
- assets/glove/glove_100d.bin — GloVe 6B 100d, урізаний до 25 тис. слів (оригінал 400 тис., 128 МБ)
- assets/corpus/textmind_reviews.txt — 15 відгуків для завдань 6.2.1–6.2.2
- nltk_data/ — корпуси Brown, movie_reviews, product_reviews, стоп-слова, punkt: працює без інтернету
- test_data/wordsim353.tsv — 353 пари слів з оцінками схожості від людей
- test_data/analogies.txt — 240 аналогій (столиці, родина, ступені порівняння, минулий час)
- test_data/reviews_new.csv — 20 нових відгуків про товари з мітками pos / neg
- Lesson27_tasks.md, Lesson28_tasks.md — по 2 практичні завдання на кожну пару
- 7 скриптів пар 27–28: корпуси, count-based embeddings, Word2Vec, GloVe з нуля, PCA, класифікатор
- Lesson27_28_plan_180.md — план заняття на 180 хвилин: що, коли і яким скриптом
- baked HTML-презентації студентської версії матеріалів

Без torch і без GPU: усе навчається на CPU за секунди.
Спочатку START.txt і Lesson27_28_plan_180.md.

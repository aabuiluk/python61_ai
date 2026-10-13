Штучний інтелект з використанням Python · роздаток пар 31–32

Пара 31. SVD і зниження розмірності.
Пара 32. PCA 2D і порівняння з SVD.

У пакеті:
- готова програма Lesson32_05_wine_map.py: карта вин — 13 ознак → 2 осі, сусіди, нове вино на карті
- dimred.py — спільний код: load_wine як DataFrame, StandardScaler, TruncatedSVD, PCA,
  вирівнювання знаків осей, scatter, збереження графіків, оцінка карти через kNN
- 8 скриптів-прикладів: Lesson31_01…04, Lesson32_01…04
- assets/supportflow_qa.csv — 30 запитів служби підтримки з пар 29–30 (SVD на тексті, Lesson31_04)
- Lesson31_tasks.md, Lesson32_tasks.md — по 3 практичні завдання на пару
- Lesson31_homework.md, Lesson32_homework.md — домашнє 7.1
- Lesson31_32_plan_180.md — план заняття на 180 хвилин
- baked HTML-презентації пар 31, 32

Дані wine (178 вин, 13 ознак, 3 сорти) входять у scikit-learn: інтернет і GPU не потрібні,
кожен скрипт працює кілька секунд.
Спочатку START.txt і Lesson31_32_plan_180.md.

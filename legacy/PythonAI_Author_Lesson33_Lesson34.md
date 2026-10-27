# Пари 33–34 · маршрут на 90 + 90 хвилин з повторенням пар 31–32

За два блоки по 90 хвилин ви згадаєте, як на парах 31–32 стиснули 13 ознак вина до двох осей, а потім навчитеся знаходити групи там, де ніхто не дав кольорів: поділите клієнтів ClientScope на сегменти двома алгоритмами — K-Means і DBSCAN.

| Блок | Час | Що робимо |
|---|---|---|
| **1** | 0:00–0:30 | Повторення: пара 31 → 32 і місток до кластеризації |
| | 0:30–1:30 | Пара 33 · кластеризація K-Means (практичне 7.2, завдання 1–2) |
| **2** | 0:00–1:30 | Пара 34 · DBSCAN і сегментація клієнтів (практичне 7.2, завдання 3–4) |

Час у кожному блоці йде від його початку. Усі команди запускайте **з кореня репозиторію** — з тієї папки, де лежить цей файл.

По дорозі є девʼять **міні-завдань** на 2–3 хвилини: одна змінена команда або один-два рядки коду. Їх робите ви самі, одразу після прикладу.

Маршрут є у двох формах: цей текст і ноутбук [PythonAI_Author_Lesson33_Lesson34.ipynb](PythonAI_Author_Lesson33_Lesson34.ipynb), де під кожною командою вже є її вивід і всі рисунки. Ноутбук відкривайте з кореня репозиторію, ядро — `.venv`. Комірки міні-завдань у ньому порожні: їх запускаєте ви.

Докладний варіант лише пар 33–34 на 180 хвилин: [Lesson33_34_plan_180.md](../PythonAI_Author_Lesson33_Lesson34/Lesson33_34_plan_180.md). Попередній маршрут, пари 31–32: [PythonAI_Author_Lesson31_Lesson32.md](PythonAI_Author_Lesson31_Lesson32.md).

<a id="step-0"></a>
## Підготовка

Один спільний venv у корені (Python 3.10–3.14):

```text
python -m venv .venv
.venv\Scripts\activate          (Windows)
source .venv/bin/activate        (macOS / Linux)
python -m pip install -U pip
python -m pip install -r requirements.txt
```

Перевірка — дві команди:

```bash
python PythonAI_Author_Lesson31_Lesson32/Lesson32_05_wine_map.py
python PythonAI_Author_Lesson33_Lesson34/Lesson34_05_client_segments.py
```

- [ ] перша друкує `на них 55.4% розкиду таблиці`;
- [ ] друга друкує профілі сегментів K-Means і DBSCAN.

Інтернет і GPU не потрібні. Графіки скрипти зберігають у папку `results/` своєї пари, вікна matplotlib не відкриваються.

---

# Блок 1 · 90 хвилин

<a id="step-1"></a>
## Крок 1 · 0:00–0:12 · Повторення пари 31: карта вин і SVD

```bash
python PythonAI_Author_Lesson31_Lesson32/Lesson32_05_wine_map.py
```

**Що побачите.** 178 вин, 13 ознак → 2 осі, на них 55.4% розкиду таблиці. У вин №0, №70 і №150 усі пʼять сусідів на карті — того самого сорту.

```bash
python PythonAI_Author_Lesson31_Lesson32/Lesson31_03_svd_projection.py
```

**Що побачите.** `TruncatedSVD(n_components=2)`: `(178, 13) → (178, 2)`. Без scaler перша вісь — це просто `proline` (кореляція 1.000), і сорти на карті розділяються на 70.3%. Зі scaler — на 96.6%.

**Міні-завдання 1 · 2 хв.** Виберіть три свої номери вин від 0 до 177 і перевірте, чи сусіди на карті підказують правильний сорт:

```bash
python PythonAI_Author_Lesson31_Lesson32/Lesson32_05_wine_map.py 10 100 170
```

Чи знайшлося вино, у якого серед пʼяти сусідів є чужий сорт? Де воно лежить на карті?

**Перевір себе:**
1. Навіщо перед SVD масштабувати ознаки?
2. Карта зберігає 55.4% розкиду. Чому сорти на ній все одно видно добре?

<a id="step-2"></a>
## Крок 2 · 0:12–0:22 · Повторення пари 32: PCA і скільки компонент

```bash
python PythonAI_Author_Lesson31_Lesson32/Lesson32_02_pca_by_hand.py
```

**Що побачите.** PCA руками збігається зі `sklearn`. Після scaler `TruncatedSVD` і `PCA` відрізняються лише на `9.7e-09`, без scaler — на 759.

**PCA = центрування + SVD.**

```bash
python PythonAI_Author_Lesson31_Lesson32/Lesson32_04_how_many_components.py
```

**Що побачите.** 80% розкиду зберігають 5 компонент, 90% — 8, 95% — 10. Перед класифікатором PCA стоїть у `Pipeline`, щоб не було leakage.

**Перевір себе:**
3. Чому після `StandardScaler` графіки SVD і PCA однакові?
4. Для нового вина викликають `transform`, а не `fit_transform`. Чому?

<a id="step-3"></a>
## Крок 3 · 0:22–0:30 · Місток: карта вин без кольорів

На парах 31–32 сорти на карті було видно, бо ми самі розфарбували точки за `target`. А якщо кольорів немає?

```bash
python PythonAI_Author_Lesson33_Lesson34/Lesson33_01_wine_without_colors.py
```

**Що побачите.** K-Means отримує лише 178 точок на площині і сам ділить їх на 3 групи. Лише потім ми порівнюємо групи із сортами: сорт 0 цілком в одній групі, сорт 2 — в іншій, сорт 1 майже весь у третій. Узгодженість із сортами (ARI) — 0.895. Рисунок `PythonAI_Author_Lesson33_Lesson34/results/wine_without_colors.png`: ліворуч кольори сортів, праворуч — кластерів.

**Зверніть увагу:** номери кластерів довільні. Кластер 0 не мусить бути сортом 0: важить лише, хто з ким разом.

**Міні-завдання 2 · 2 хв.** Попросіть K-Means чотири групи замість трьох:

```bash
python PythonAI_Author_Lesson33_Lesson34/Lesson33_01_wine_without_colors.py 4
```

Що сталося із сортами? Чи впала узгодженість ARI і чому?

<a id="step-4"></a>
## Крок 4 · 0:30–0:36 · Пара 33 · готова програма: сегменти клієнтів

```bash
python PythonAI_Author_Lesson33_Lesson34/Lesson34_05_client_segments.py
```

**Що побачите.** 500 клієнтів ClientScope з двома ознаками: витрати на місяць (`spend`, грн) і візити на місяць (`visits`). K-Means ділить їх на 4 сегменти по 125 клієнтів, у кожного свій профіль: хтось витрачає близько 1970 грн, хтось приходить 19 разів на місяць. DBSCAN знаходить ті самі 4 групи і ще 8 клієнтів, не схожих ні на кого. Рисунок — `PythonAI_Author_Lesson33_Lesson34/results/client_segments.png`.

**Зверніть увагу:** клієнти синтетичні, це ті самі точки, що в практичному 7.2, лише в одиницях бізнесу. Номер сегмента нічого не означає — зміст дає таблиця профілю.

**Міні-завдання 3 · 2 хв.** Додайте нового клієнта і подивіться, куди його віднесуть два алгоритми:

```bash
python PythonAI_Author_Lesson33_Lesson34/Lesson34_05_client_segments.py --new spend=900 visits=10
```

Підберіть такого клієнта, щоб DBSCAN знайшов для нього сегмент. Чим різняться відповіді K-Means і DBSCAN для «дивного» клієнта?

<a id="step-5"></a>
## Крок 5 · 0:36–0:46 · Дані ClientScope (завдання 7.2.1)

У презентації 33: «Старт: сегментація без y», «Приклад · 500 точок у 4 хмарах».

```bash
python PythonAI_Author_Lesson33_Lesson34/Lesson33_02_blobs_raw.py
```

**Що побачите.** `make_blobs(n_samples=500, centers=4, cluster_std=1.0, random_state=42)` → `DataFrame (500, 2)` з ознаками `x1`, `x2` і сирий scatter без кольорів: `results/raw_blobs.png`.

**Зверніть увагу:** справжні номери хмар лежать окремо, у таблицю не йдуть. Алгоритм бачить лише ознаки.

**Міні-завдання 4 · 2 хв.** Збільште розкид хмар (аналог 1.1):

```bash
python PythonAI_Author_Lesson33_Lesson34/Lesson33_02_blobs_raw.py 2.5
```

Відкрийте `raw_blobs.png`. Чи ще можна на око сказати, скільки тут груп?

<a id="step-6"></a>
## Крок 6 · 0:46–1:02 · KMeans і cluster_kmeans (завдання 7.2.2)

У презентації 33: «Приклад · перший fit_predict», «Що означають cluster_centers_», «Приклад · центри поверх scatter».

```bash
python PythonAI_Author_Lesson33_Lesson34/Lesson33_03_kmeans_fit.py
```

**Що побачите.** `KMeans(n_clusters=4, random_state=42)`: 4 кластери по 125 точок, чотири центри, `inertia_ = 948.9`, збіг зі справжніми хмарами (ARI) 1.000. Новим клієнтам `predict` дає найближчий центр, `transform` — відстані до всіх чотирьох. Рисунок — `results/kmeans_clusters.png`.

**Міні-завдання 5 · 2 хв.** Ті самі дані, інше `k` (аналог 2.1):

```bash
python PythonAI_Author_Lesson33_Lesson34/Lesson33_03_kmeans_fit.py 2 6
```

Де центри «розривають» справжню хмару? Чому `inertia_` за `k = 6` менша, ніж за `k = 4`, хоча розбиття гірше?

**Часта пастка:** K-Means завжди повертає рівно `k` груп. Він не скаже, що ви неправильно вгадали їх кількість.

**Напишіть самі.** Файл `PythonAI_Author_Lesson33_Lesson34/my_kmeans.py` (готовий лежить у папці пари, якщо не встигаєте набрати):

```python
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs
from sklearn.metrics import silhouette_score

X, _ = make_blobs(n_samples=500, centers=4, cluster_std=1.0, random_state=42)   # номери хмар не беремо
df = pd.DataFrame(X, columns=["x1", "x2"])

kmeans = KMeans(n_clusters=4, random_state=42)
df["cluster_kmeans"] = kmeans.fit_predict(df[["x1", "x2"]])
print(df["cluster_kmeans"].value_counts().sort_index().tolist())          # [125, 125, 125, 125]
print(round(silhouette_score(df[["x1", "x2"]], df["cluster_kmeans"]), 3))  # 0.791
# Міні-завдання 6: порахуйте silhouette для k = 3, 4, 5, 6 у циклі — яке k найкраще?

plt.scatter(df["x1"], df["x2"], c=df["cluster_kmeans"], s=12)
centers = kmeans.cluster_centers_
plt.scatter(centers[:, 0], centers[:, 1], marker="D", s=120, color="black")
plt.title("K-Means, k = 4")
plt.savefig(Path(__file__).parent / "results" / "my_kmeans.png")
```

```bash
python PythonAI_Author_Lesson33_Lesson34/my_kmeans.py
```

<a id="step-7"></a>
## Крок 7 · 1:02–1:14 · K-Means руками і чому важливий старт

У презентації 33: «За Жероном · як працює алгоритм k-means», «За Жероном · невдалий старт та ініціалізація центроїдів».

```bash
python PythonAI_Author_Lesson33_Lesson34/Lesson33_04_kmeans_by_hand.py
```

**Що побачите.**
1. Два кроки в циклі: кожну точку віддаємо найближчому центру, кожен центр переносимо в середнє своїх точок.
2. На пʼяти згустках з книжки центри перестають рухатись на 7-й ітерації, inertia 211.6.
3. З 20 випадкових стартів більшість дає inertia 212, а найгірший — 600: K-Means знаходить найближчий локальний мінімум.
4. `n_init=10` лишає найкращий із 10 стартів (211.6), розумний старт k-means++ з одного запуску дає 224.1.

Рисунок `results/kmeans_steps.png`: ліворуч шлях центрів, праворуч невдалий старт.

**Перевір себе:**
5. Чому K-Means запускають кілька разів з різних стартів?

<a id="step-8"></a>
## Крок 8 · 1:14–1:26 · Скільки кластерів і межі K-Means

У презентації 33: «За Жероном · як знайти оптимальну кількість кластерів», «За Жероном · межі k-means».

```bash
python PythonAI_Author_Lesson33_Lesson34/Lesson33_05_choose_k.py
```

**Що побачите.** inertia падає з кожним `k`, тому «лікоть» читають на око. Silhouette має максимум: на пʼяти згустках з книжки — за `k = 4` (0.689), хоча згустків пʼять: два з них дуже близько. На даних ClientScope — теж `k = 4` (0.791). На трьох витягнутих еліпсах збіг K-Means зі справжніми групами лише 0.291. Рисунок — `results/choose_k.png`.

**Зверніть увагу:** K-Means міряє відстань до центру, тому знаходить круглі групи приблизно однакового розміру.

**Міні-завдання 6 · 3 хв.** У своєму `my_kmeans.py` допишіть цикл: silhouette для `k` = 3, 4, 5, 6. Яке `k` найкраще для даних ClientScope?

**Перевір себе:**
6. inertia за `k = 9` менша, ніж за `k = 4`. Чому це не означає, що 9 кластерів кращі?

<a id="step-9"></a>
## Крок 9 · 1:26–1:30 · Перевір себе · пара 33

7. Чим кластеризація відрізняється від класифікації?
8. Що повертають `labels_` і `cluster_centers_`?
9. Що означає `inertia_`?
10. Чому K-Means погано ділить витягнуті групи?

---

# Блок 2 · 90 хвилин

<a id="step-10"></a>
## Крок 10 · 0:00–0:05 · Повернення

Шлях пари 33: `make_blobs → DataFrame → KMeans(4) → cluster_kmeans → scatter з центрами`. Кількість кластерів K-Means задаємо самі.

**Перевір себе:**
11. Що станеться, якщо в даних є клієнт, далекий від усіх груп? Куди його віднесе K-Means?

<a id="step-11"></a>
## Крок 11 · 0:05–0:22 · DBSCAN і cluster_dbscan (завдання 7.2.3)

У презентації 34: «Старт: щільність замість K», «Приклад · коло eps навколо точки», «Core, border і noise», «Приклад · скільки шуму при eps=0.8».

DBSCAN не питає кількість кластерів. Він питає, що вважати «густо»: `eps` — радіус сусідства, `min_samples` — скільки точок має бути в цьому радіусі. Точка з густим сусідством — ядрова; поруч з ядровою, але без власного густого сусідства — межова; решта — шум, мітка −1.

```bash
python PythonAI_Author_Lesson33_Lesson34/Lesson34_01_dbscan.py
```

**Що побачите.** `DBSCAN(eps=0.8, min_samples=5)`: 4 кластери і 16 точок шуму (3%); 466 ядрових, 18 межових. Стовпець `cluster_dbscan` і рисунок `results/dbscan_clusters.png`.

**Часта пастка:** мітка −1 — не пʼятий кластер, а точки, що не належать жодній густій області.

**Міні-завдання 7 · 2 хв.** Ті самі дані, інший eps (аналог 3.1):

```bash
python PythonAI_Author_Lesson33_Lesson34/Lesson34_01_dbscan.py 0.3 2.0
```

Як змінилися кількість кластерів і частка шуму? Який eps «розсипав» хмари?

<a id="step-12"></a>
## Крок 12 · 0:22–0:35 · Як вибрати eps

У презентації 34: «Як рухається eps», «Приклад · eps замалий, eps завеликий».

```bash
python PythonAI_Author_Lesson33_Lesson34/Lesson34_02_choose_eps.py
```

**Що побачите.** Для кожної точки — відстань до 5-го сусіда, відсортована. Половина точок має сусіда ближче 0.35, 95% — ближче 0.87, далі крива злітає: це шум. Таблиця eps: 0.3 → 21 кластер, 0.8 → 4 кластери і 16 точок шуму, 1.2 → 4 і 3. Якщо ознаку `x2` записати в інших одиницях (× 100), той самий `eps = 0.8` дає 500 точок шуму з 500. Рисунок — `results/k_distance.png`.

**Зверніть увагу:** DBSCAN міряє відстані, тому ознаки в різних одиницях масштабують перед ним — так само, як перед PCA на парі 31.

**Міні-завдання 8 · 2 хв.** Підберіть eps, за якого DBSCAN знаходить 4 кластери, а шуму менше 1% (менше 5 точок). Змінюйте число в команді:

```bash
python PythonAI_Author_Lesson33_Lesson34/Lesson34_01_dbscan.py 1.0
```

<a id="step-13"></a>
## Крок 13 · 0:35–0:48 · Півмісяці: де K-Means ламається

У презентації 34: «За Жероном · DBSCAN: кластери як густі області», «За Жероном · нові приклади: чому немає predict()», «За Жероном · k-means і DBSCAN на тих самих даних».

```bash
python PythonAI_Author_Lesson33_Lesson34/Lesson34_03_moons.py
```

**Що побачите.**
1. На двох півмісяцях `eps = 0.05` дає 7 кластерів і 77 точок шуму, `eps = 0.2` — рівно 2 кластери без шуму.
2. Збіг зі справжніми півмісяцями: K-Means 0.239 (ріже навпіл прямою), DBSCAN 1.000.
3. У DBSCAN немає `predict()`. Нові точки віддають kNN, навченому на ядрових точках: `[1 0 1 0]`, а з обмеженням відстані eps — `[-1 0 1 -1]`.

Рисунок — `results/moons_compare.png`.

**Перевір себе:**
12. Чому K-Means не може розділити півмісяці навіть за правильного `k = 2`?

<a id="step-14"></a>
## Крок 14 · 0:48–1:03 · K-Means і DBSCAN в одному вікні (завдання 7.2.4)

У презентації 34: «Приклад · дві панелі side-by-side», «ITSTEP Практичне 7.2 · завдання 3–4».

```bash
python PythonAI_Author_Lesson33_Lesson34/Lesson34_04_comparison.py
```

**Що побачите.**

| | K-Means | DBSCAN |
|---|---|---|
| кластерів | 4 | 4 |
| точок у шумі | 0 | 16 |
| збіг із хмарами, ARI | 1.000 | 0.956 |
| silhouette | 0.791 | 0.799 (без шуму) |

Таблиця «хто з ким разом» показує: кожен кластер K-Means — це один кластер DBSCAN плюс кілька точок шуму. Рисунок `results/clustering_comparison.png` з заголовками `K-Means Clustering` і `DBSCAN Clustering`.

**Напишіть самі.** Файл `PythonAI_Author_Lesson33_Lesson34/my_dbscan.py` (готовий лежить у папці пари):

```python
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.cluster import DBSCAN, KMeans
from sklearn.datasets import make_blobs

X, _ = make_blobs(n_samples=500, centers=4, cluster_std=1.0, random_state=42)
df = pd.DataFrame(X, columns=["x1", "x2"])
df["cluster_kmeans"] = KMeans(n_clusters=4, random_state=42).fit_predict(X)
df["cluster_dbscan"] = DBSCAN(eps=0.8, min_samples=5).fit_predict(X)

noise = int((df["cluster_dbscan"] == -1).sum())
print(df["cluster_dbscan"].nunique() - 1, noise)                           # 4 16  (кластери без шуму, шум)
# Міні-завдання 9: допишіть кількість шумових точок у заголовок правої панелі

fig = plt.figure(figsize=(11, 4.5))
plt.subplot(1, 2, 1)
plt.scatter(df["x1"], df["x2"], c=df["cluster_kmeans"], s=12)
plt.title("K-Means Clustering")
plt.subplot(1, 2, 2)
plt.scatter(df["x1"], df["x2"], c=df["cluster_dbscan"], s=12)
plt.title("DBSCAN Clustering")
fig.savefig(Path(__file__).parent / "results" / "clustering_comparison.png")
```

```bash
python PythonAI_Author_Lesson33_Lesson34/my_dbscan.py
```

**Міні-завдання 9 · 2 хв.** У `my_dbscan.py` допишіть кількість шумових точок у заголовок правої панелі (аналог 4.1), наприклад `DBSCAN Clustering · шум 16`.

**Перевір себе:**
13. Кому віддати сегментацію на круглих хмарах однакової щільності, а кому — на півмісяцях?

<a id="step-15"></a>
## Крок 15 · 1:03–1:20 · Практика

[Lesson34_tasks.md](../PythonAI_Author_Lesson33_Lesson34/Lesson34_tasks.md), завдання 3: DBSCAN на справжніх даних wine — графік k-відстаней, підбір eps, порівняння з K-Means.

Якщо важко — [Lesson33_tasks.md](../PythonAI_Author_Lesson33_Lesson34/Lesson33_tasks.md), завдання 3: скільки кластерів в ірисах.

Перед тим як показати результат, перевірте:
- [ ] ознаки масштабовано перед K-Means і DBSCAN;
- [ ] справжні мітки не потрапили в `fit`;
- [ ] надруковано кількість кластерів і шуму;
- [ ] рисунок збережено у файл.

<a id="step-16"></a>
## Крок 16 · 1:20–1:30 · Перевір себе і підсумок

14. Що означає мітка −1?
15. Чим ядрова точка відрізняється від межової?
16. Як вибрати eps?

**Підсумок.**
1. Кластеризація ділить точки на групи без правильних відповідей. Номер кластера — не клас.
2. K-Means: `k` задаємо самі; два кроки в циклі; кілька стартів; знаходить круглі групи схожого розміру.
3. Кількість кластерів підказують «лікоть» і silhouette, але вирішує задача.
4. DBSCAN: густі області замість `k`; шум −1; eps вибирають за графіком k-відстаней і лише після масштабування.
5. На круглих хмарах обидва алгоритми згодні, на півмісяцях виграє DBSCAN.

На парі 32 ви стиснули таблицю до карти, на парах 33–34 знайшли на карті групи без жодної підказки.

**Домашнє:** [Lesson33_homework.md](../PythonAI_Author_Lesson33_Lesson34/Lesson33_homework.md), [Lesson34_homework.md](../PythonAI_Author_Lesson33_Lesson34/Lesson34_homework.md).

**Наступна пара** — content-based рекомендації книг.

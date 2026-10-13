/**
 * Hover glossary — ATOMIC for student lesson folder.
 * File: Lesson2_ae_term_glossary.js (same directory as Lesson2_00_presentation.html).
 * Tooltip: English name + Ukrainian explanation. Open HTML locally; no journal required.
 */
(function () {
  "use strict";

  /** @type {{keys: string[], tip: string}[]} */
  const ENTRIES = [
    {
      keys: ["Штучний інтелект, ШІ", "Штучний інтелект", "ШІ", "Artificial Intelligence, AI", "Artificial Intelligence", "AI"],
      tip: "Artificial Intelligence\nМашинна система, яка для явних або неявних цілей виводить із вхідних даних, як згенерувати виходи: прогнози, контент, рекомендації чи рішення, що впливають на фізичне або віртуальне середовище. Системи різняться рівнем автономності й адаптивності після розгортання. (OECD AI Principles.)",
    },
    {
      keys: ["Наука про дані", "Data Science, DS", "Data Science", "DS"],
      tip: "Data Science\nМіждисциплінарний процес: бізнес-/дослідницьке питання → дані → аналіз / моделювання → інсайт або продукт. Не обовʼязково включає ML: інколи достатньо описової статистики й візуалізації.",
    },
    {
      keys: ["Машинне навчання", "Machine Learning, ML", "Machine Learning", "ML"],
      tip: "Machine Learning\nПідхід, за якого модель покращує якість прогнозу/рішення на основі досвіду (даних), а не лише за жорстко прописаними правилами. Практична рамка курсу: f(ознаки) → прогноз, параметри підбираються з прикладів.",
    },
    {
      keys: ["Глибоке навчання", "Deep Learning, DL", "Deep Learning", "DL"],
      tip: "Deep Learning\nПідмножина ML на багатошарових нейронних мережах, що вчаться складних внутрішніх представлень даних (зображення, мова, аудіо). (Goodfellow, Bengio, Courville.)",
    },
    {
      keys: ["Генеративний ШІ", "Generative AI, GenAI", "Generative AI", "AI", "GenAI"],
      tip: "Generative AI\nМоделі, що створюють новий контент (текст, зображення, код, аудіо), моделюючи розподіл даних. У дефініції OECD вихід «content» прямо включено до виходів AI-системи.",
    },
    {
      keys: ["Велика мовна модель", "Large Language Model, LLM", "Large Language Model", "LLM"],
      tip: "Large Language Model\nНейромережа (зазвичай на архітектурі Transformer), навчена на великих текстових корпусах передбачати / генерувати мову. На практиці — основа сучасних чат-ботів і кодових асистентів.",
    },
    {
      keys: ["Трансформер", "Transformer"],
      tip: "Transformer\nАрхітектура нейромереж (Vaswani et al., 2017), що спирається на механізми уваги (attention) без рекурентності й згорткових шарів як основи. Основа сучасних LLM і багатьох моделей мови / зору.",
    },
    {
      keys: ["Навчання представлень", "Representation learning"],
      tip: "Representation learning\nПідхід, коли модель сама вчить внутрішні представлення (ембедінги / ознаки) даних, замість покладатись лише на ручний feature engineering.",
    },
    {
      keys: ["Контрастивне навчання", "Contrastive learning"],
      tip: "Contrastive learning\nSelf-supervised підхід: зближувати представлення «схожих» пар і відштовхувати «несхожі» в просторі ембедінгів. Класичний приклад — SimCLR (Chen et al., 2020).",
    },
    {
      keys: ["Ембедінг / векторне представлення", "Ембедінг", "векторне представлення", "Embedding"],
      tip: "Embedding\nЧисловий вектор обʼєкта (слова, речення, клієнта, товару), у якому близькість векторів відображає семантичну / поведінкову схожість.",
    },
    {
      keys: ["Нейронна мережа", "Neural network"],
      tip: "Neural network\nМодель із шарів повʼязаних «нейронів» (лінійне перетворення + нелінійна активація), що апроксимує складні функції з даних.",
    },
    {
      keys: ["Компʼютерний зір", "Computer Vision, CV", "Computer Vision", "CV"],
      tip: "Computer Vision\nГалузь ШІ / ML про розуміння зображень і відео: класифікація, детекція, сегментація тощо.",
    },
    {
      keys: ["Обробка природної мови", "Natural Language Processing, NLP", "Natural Language Processing", "NLP"],
      tip: "Natural Language Processing\nГалузь про автоматичну обробку людської мови: токенізація, класифікація тексту, машинний переклад, діалог, витяг інформації.",
    },
    {
      keys: ["Buzzwords"],
      tip: "Buzzwords\nМодні слова без чіткого змісту. На курсі замінюємо їх на постановку: дані → ознаки → ціль → метрика → обмеження.",
    },
    {
      keys: ["Тест Тюрінга", "Turing test"],
      tip: "Turing test\nОпераційний критерій Алана Тюрінга (1950): чи може машина вести діалог так, щоб людина-суддя не відрізнила її від людини. Це імітаційна гра, не математичне визначення інтелекту.",
    },
    {
      keys: ["Дартмутський семінар", "Dartmouth Workshop, 1956", "Dartmouth Workshop", "1956"],
      tip: "Dartmouth Workshop\nПодія, з якої зазвичай ведуть відлік терміна Artificial Intelligence як назви дослідницького напряму.",
    },
    {
      keys: ["Символьний ШІ", "Symbolic AI / rule-based AI", "Symbolic AI", "AI", "rule-based AI"],
      tip: "Symbolic AI / rule-based AI\nПідхід, де знання й логіку явно кодує людина правилами / символами («якщо–то»), а не виводить закономірності з великих даних.",
    },
    {
      keys: ["Експертна система", "Expert system"],
      tip: "Expert system\nСистема на ручних правилах / базі знань експерта. Потужна у вузькій сфері, але крихка й дорога в підтримці при зміні світу.",
    },
    {
      keys: ["Статистичний / data-driven ML", "Статистичний", "data-driven ML", "Statistical / data-driven ML", "Statistical", "ML"],
      tip: "Statistical / data-driven ML\nПідхід, де закономірності оцінюють із даних (статистика, ML), а не лише з ручних правил.",
    },
    {
      keys: ["Зима ШІ", "AI winter", "AI"],
      tip: "AI winter\nПеріод спаду інтересу й фінансування через завищені обіцянки, брак даних / обчислень і крихкість ранніх систем.",
    },
    {
      keys: ["ImageNet"],
      tip: "ImageNet\nВеликий ієрархічний датасет зображень для навчання й бенчмаркінгу розпізнавання обʼєктів. Перемоги глибоких мереж на ImageNet (бл. 2012+) стали точкою вибуху DL.",
    },
    {
      keys: ["Обчислювальні ресурси", "Compute"],
      tip: "Compute\nCPU / GPU / TPU, час і вартість обчислень. Один із трьох стовпів сучасного буму ШІ разом із даними й алгоритмами представлення.",
    },
    {
      keys: ["Навчання з учителем", "Supervised learning", "supervised"],
      tip: "Supervised learning\nНавчання, де для кожного навчального прикладу відома очікувана відповідь y (мітка / ground truth). Типові оцінки: класифікатор, регресор. (scikit-learn Glossary.)",
    },
    {
      keys: ["Навчання без учителя", "Unsupervised learning", "supervised", "unsupervised"],
      tip: "Unsupervised learning\nНавчання без y: шукаємо структуру в X (кластери, аномалії, зменшення розмірності). (scikit-learn Glossary.)",
    },
    {
      keys: ["Навчання з підкріпленням", "Reinforcement Learning, RL", "Reinforcement Learning", "RL", "reinforcement"],
      tip: "Reinforcement Learning\nАгент взаємодіє із середовищем, отримує нагороди і вчиться політиці дій, що максимізує сумарну нагороду в довгостроковій перспективі. (Sutton & Barto.)",
    },
    {
      keys: ["Напівкероване навчання", "Semi-supervised learning", "supervised"],
      tip: "Semi-supervised learning\nМало міток + багато нерозмічених даних; мітки «підтягують» навчання на нерозміченій масі. У scikit-learn для нерозмічених часто використовують мітку -1.",
    },
    {
      keys: ["Самонавчання / самокероване", "Самонавчання", "самокероване", "Self-supervised learning", "supervised"],
      tip: "Self-supervised learning\nМітки створюються з самих даних (маски токенів, contrastive-пари). Основа pretraining сучасних LLM і багатьох моделей зору.",
    },
    {
      keys: ["Навчання наслідуванням", "Imitation learning"],
      tip: "Imitation learning\nНавчання поведінці експерта (демонстрації); на межі supervised і RL: копіюємо дії, а не лише оптимізуємо reward.",
    },
    {
      keys: ["Агент", "Agent"],
      tip: "Agent\nУ RL — сутність, що спостерігає стан середовища, обирає дію й отримує нагороду. У GenAI — також система, що викликає інструменти в циклі думка → дія → спостереження.",
    },
    {
      keys: ["Політика", "Policy"],
      tip: "Policy\nУ RL — правило поведінки агента: відображення стану (або розподілу) у дії. (Sutton & Barto.)",
    },
    {
      keys: ["Нагорода", "Reward"],
      tip: "Reward\nЧисловий сигнал від середовища після кроку; формалізує «що добре / погано». Мета агента — максимізувати сукупну нагороду. (Sutton & Barto.)",
    },
    {
      keys: ["Середовище", "Environment"],
      tip: "Environment\nУ RL — усе зовнішнє відносно агента: стани, переходи, видача нагород.",
    },
    {
      keys: ["Класифікація", "Classification"],
      tip: "Classification\nSupervised-задача зі скінченною дискретною множиною можливих виходів (класів). Приклади: spam / not-spam, діагноз «так/ні».",
    },
    {
      keys: ["Регресія", "Regression"],
      tip: "Regression\nSupervised-задача з числовим неперервним (або майже неперервним) y: ціна, температура, LTV.",
    },
    {
      keys: ["Кластеризація", "Clustering"],
      tip: "Clustering\nUnsupervised-задача: групування схожих обʼєктів без заздалегідь заданих міток класів. Не плутати з класифікацією.",
    },
    {
      keys: ["Зменшення розмірності", "Dimensionality reduction"],
      tip: "Dimensionality reduction\nПеретворення високо-вимірних ознак у меншу кількість координат зі збереженням головної структури / дисперсії (напр. PCA, SVD).",
    },
    {
      keys: ["Детекція аномалій", "Anomaly / outlier detection", "Anomaly", "outlier detection"],
      tip: "Anomaly / outlier detection\nПошук рідкісних або нетипових спостережень без (або з частковими) мітками.",
    },
    {
      keys: ["Моделювання тем", "Topic modeling"],
      tip: "Topic modeling\nUnsupervised-методи виділення тем у текстах (напр. LDA): документ → суміш тем.",
    },
    {
      keys: ["Детекція обʼєктів", "Object detection"],
      tip: "Object detection\nCV-задача: знайти обʼєкти на зображенні й локалізувати їх (рамки / маски).",
    },
    {
      keys: ["Сегментація", "Segmentation"],
      tip: "Segmentation\nCV-задача: попіксельна (або порегіонна) розмітка класів на зображенні.",
    },
    {
      keys: ["Рекомендаційна система", "Recommender system"],
      tip: "Recommender system\nСистема, що пропонує користувачу елементи (товари, фільми, статті) за релевантністю / уподобаннями.",
    },
    {
      keys: ["Контентні рекомендації", "Content-based filtering"],
      tip: "Content-based filtering\nРекомендації на основі схожості описів / ознак елементів із профілем користувача.",
    },
    {
      keys: ["Колаборативна фільтрація", "Collaborative filtering"],
      tip: "Collaborative filtering\nРекомендації на основі спільної поведінки користувачів / оцінок (user-based, item-based, matrix factorization).",
    },
    {
      keys: ["Багатокласова класифікація", "Multi-class classification"],
      tip: "Multi-class classification\nОдин приклад належить рівно до одного з K>2 класів.",
    },
    {
      keys: ["Мультиміткова класифікація", "Multi-label classification", "label"],
      tip: "Multi-label classification\nОдин приклад може мати кілька міток одночасно (напр. теги статті).",
    },
    {
      keys: ["Аналіз тональності", "Sentiment analysis"],
      tip: "Sentiment analysis\nКласифікація тексту за емоційним забарвленням (позитив / негатив / нейтраль тощо).",
    },
    {
      keys: ["PCA", "Principal Component Analysis"],
      tip: "Principal Component Analysis\nМетод зменшення розмірності: проєкція даних на головні компоненти з максимальною дисперсією. (scikit-learn decomposition.)",
    },
    {
      keys: ["SVD", "Singular Value Decomposition"],
      tip: "Singular Value Decomposition\nРозклад матриці на сингулярні вектори/значення. У ML — основа стиснення, латентних факторів і частини PCA.",
    },
    {
      keys: ["SVM", "Support Vector Machine"],
      tip: "Support Vector Machine\nАлгоритм, що шукає роздільну гіперплощину з максимальним запасом (margin) між класами (або регресійний аналог).",
    },
    {
      keys: ["Лінійна регресія / МНК", "Лінійна регресія", "МНК", "Ordinary Least Squares, OLS", "Ordinary Least Squares", "OLS"],
      tip: "Ordinary Least Squares\nМодель y ≈ Xw + b, де ваги мінімізують суму квадратів залишків. Аналітичний розвʼязок існує для найпростіших випадків.",
    },
    {
      keys: ["Поліноміальні ознаки", "Polynomial features", "feature"],
      tip: "Polynomial features\nРозширення простору ознак степенями й взаємодіями (x, x², xy…), щоб лінійна модель описувала нелінійні залежності.",
    },
    {
      keys: ["Ridge-регресія", "Ridge, L2 regularization", "Ridge", "L2 regularization"],
      tip: "Ridge\nЛінійна модель зі штрафом λ‖w‖²₂ за величину ваг — зменшує перенавчання при корельованих ознаках.",
    },
    {
      keys: ["Lasso-регресія", "Lasso, L1 regularization", "Lasso", "L1 regularization"],
      tip: "Lasso\nЛінійна модель зі штрафом λ‖w‖₁; схильна занулювати частину ваг (розріджений відбір ознак).",
    },
    {
      keys: ["Дерево рішень", "Decision tree"],
      tip: "Decision tree\nМодель, що ділить простір ознак порогами («питаннями») до однорідних листків із прогнозом.",
    },
    {
      keys: ["Ентропія (інформаційна)", "Ентропія", "Entropy"],
      tip: "Entropy\nМіра невизначеності розподілу класів у вузлі. Зменшення ентропії — приріст інформації при розбитті.",
    },
    {
      keys: ["Індекс Джіні", "Gini impurity"],
      tip: "Gini impurity\nАльтернативна міра «забрудненості» вузла в дереві: чим ближче до 0, тим чистіший клас.",
    },
    {
      keys: ["Приріст інформації", "Information gain"],
      tip: "Information gain\nНаскільки розбиття зменшує ентропію (або іншу домішку) порівняно з батьківським вузлом.",
    },
    {
      keys: ["Беггінг", "Bagging"],
      tip: "Bagging\nАнсамбль: навчаємо багато моделей на бутстреп-вибірках і агрегуємо прогнози (основа Random Forest).",
    },
    {
      keys: ["Бустинг", "Boosting"],
      tip: "Boosting\nАнсамбль, де наступні моделі виправляють помилки попередніх (напр. градієнтний бустинг, XGBoost).",
    },
    {
      keys: ["Випадковий ліс", "Random Forest"],
      tip: "Random Forest\nАнсамбль дерев рішень із випадковістю ознак/вибірок: багато дерев голосують → стійкіший прогноз.",
    },
    {
      keys: ["XGBoost"],
      tip: "XGBoost\nПопулярна реалізація градієнтного бустингу дерев із регуляризацією та ефективним навчанням.",
    },
    {
      keys: ["Логістична регресія", "Logistic regression"],
      tip: "Logistic regression\nЛінійний класифікатор: лінійна комбінація ознак проходить через сигмоїду → ймовірність класу; навчання мінімізує log loss.",
    },
    {
      keys: ["Сигмоїда", "Sigmoid"],
      tip: "Sigmoid\nФункція σ(z)=1/(1+e^{-z}), що стискає дійсне число в інтервал (0, 1) — зручно як ймовірність.",
    },
    {
      keys: ["Softmax"],
      tip: "Softmax\nУзагальнення сигмоїди на K класів: перетворює логіти на розподіл ймовірностей, що сумується до 1.",
    },
    {
      keys: ["K-means"],
      tip: "K-means\nКластеризація: K центроїдів; точки відносять до найближчого центроїда, центроїди оновлюють до середнього кластера. (scikit-learn.)",
    },
    {
      keys: ["K-means++"],
      tip: "K-means++\nЕвристика ініціалізації центроїдів подалі один від одного — стабільніше збігання K-means.",
    },
    {
      keys: ["DBSCAN"],
      tip: "DBSCAN\nКластеризація за щільністю: параметри eps і min_samples; знаходить кластери довільної форми і позначає шум. (Ester et al.; scikit-learn.)",
    },
    {
      keys: ["Матрична факторизація", "Matrix factorization"],
      tip: "Matrix factorization\nРозклад user–item матриці на латентні фактори користувачів і елементів для рекомендацій.",
    },
    {
      keys: ["Датасет / набір даних", "Датасет", "набір даних", "Dataset"],
      tip: "Dataset\nСтруктурований набір спостережень під конкретне питання. У табличному вигляді: рядки = обʼєкти, стовпці = ознаки / ціль.",
    },
    {
      keys: ["Спостереження / приклад / семпл", "Спостереження", "приклад", "семпл", "Observation / instance / sample", "Observation", "instance", "sample"],
      tip: "Observation / instance / sample\nОдин обʼєкт у датасеті — зазвичай один рядок. У ML n_samples = кількість рядків X. Увага: у статистиці sample часто означає вибірку (множину).",
    },
    {
      keys: ["Ознака", "Feature"],
      tip: "Feature\nХарактеристика обʼєкта, яку подаємо в модель. У матриці даних — стовпець. Також: predictor, independent variable. (scikit-learn Glossary.)",
    },
    {
      keys: ["Цільова змінна / ціль", "Цільова змінна", "ціль", "Target"],
      tip: "Target\nЗалежна змінна y у supervised: те, що передбачаємо. Синоніми: outcome, ground truth, label.",
    },
    {
      keys: ["Мітка", "Label"],
      tip: "Label\nКонкретне значення цілі для прикладу (клас «spam», число 18500).",
    },
    {
      keys: ["Матриця ознак X", "Feature matrix", "feature"],
      tip: "Feature matrix\nПрямокутна таблиця: рядки = семпли, стовпці = ознаки.",
    },
    {
      keys: ["Інженерія ознак", "Feature engineering", "feature"],
      tip: "Feature engineering\nСтворення / перетворення ознак із сирих даних (день тижня з дати, відношення, бінінг), щоб моделі було легше вчитися.",
    },
    {
      keys: ["Сховище ознак", "Feature store", "feature"],
      tip: "Feature store\nІнфраструктура повторного використання перевірених ознак (онлайн-serving + офлайн для тренування). Референсна open-source реалізація — Feast.",
    },
    {
      keys: ["Числові неперервні ознаки", "Continuous numeric features", "feature"],
      tip: "Continuous numeric features\nЗначення з плавною шкалою: площа, температура, сума чека.",
    },
    {
      keys: ["Числові дискретні / лічильні", "Числові дискретні", "лічильні", "Discrete / count features", "Discrete", "count features", "feature"],
      tip: "Discrete / count features\nЦілі або лічильні значення: кількість кімнат, кількість покупок.",
    },
    {
      keys: ["Бінарна ознака", "Binary feature", "feature"],
      tip: "Binary feature\nОзнака з двома рівнями (0/1, так/ні). Окремий випадок категоріальної.",
    },
    {
      keys: ["Категоріальні ознаки", "Categorical features", "feature"],
      tip: "Categorical features\nЯкісні значення зі скінченною множиною рівнів; часто потребують кодування перед лінійними моделями.",
    },
    {
      keys: ["Номінальні", "Nominal"],
      tip: "Nominal\nКатегорії без порядку: район, бренд, колір.",
    },
    {
      keys: ["Порядкові", "Ordinal"],
      tip: "Ordinal\nКатегорії з порядком: освіта, rating 1–5, розмір S/M/L.",
    },
    {
      keys: ["Datetime-ознаки", "Datetime features", "feature"],
      tip: "Datetime features\nДата / час; з них роблять похідні: година, день тижня, is_weekend, дні від події.",
    },
    {
      keys: ["Ідентифікатор", "ID"],
      tip: "ID\nУнікальний ключ рядка (user_id). Зазвичай не ознака для навчання — модель не повинна запамʼятовувати id.",
    },
    {
      keys: ["Токен", "Token"],
      tip: "Token\nОдиниця тексту після токенізації: слово, підслово або символ, яку бачить модель.",
    },
    {
      keys: ["RFM", "Recency, Frequency, Monetary", "Recency", "Frequency", "Monetary"],
      tip: "Recency\nКласичні маркетингові ознаки клієнта: як давно купував, як часто, на яку суму.",
    },
    {
      keys: ["User–item матриця", "User–item matrix"],
      tip: "User–item matrix\nТаблиця взаємодій користувачів з елементами (оцінки, кліки, покупки); основа collaborative filtering.",
    },
    {
      keys: ["Холодний старт", "Cold start"],
      tip: "Cold start\nПроблема рекомендацій для нового користувача / елемента без історії взаємодій.",
    },
    {
      keys: ["Словник даних", "Data dictionary"],
      tip: "Data dictionary\nПаспорт колонок для людей: тип, сенс, одиниці, допустимі значення, роль feature / target / id.",
    },
    {
      keys: ["Схема даних", "Schema"],
      tip: "Schema\nФормальний опис структури (імена, типи, обмеження, перевірки).",
    },
    {
      keys: ["Репрезентативність", "Representativeness"],
      tip: "Representativeness\nЧи відображає датасет реальний продакшен / цільову популяцію.",
    },
    {
      keys: ["Пропуски", "Missing values"],
      tip: "Missing values\nВідсутні значення. У float-масивах scikit-learn віддає перевагу NaN як позначці пропуску.",
    },
    {
      keys: ["NaN", "Not a Number"],
      tip: "Not a Number\nСпеціальне значення з IEEE floating-point; у pandas / NumPy / sklearn часто означає «немає даних».",
    },
    {
      keys: ["Дублікати", "Duplicates"],
      tip: "Duplicates\nПовторювані рядки / записи. Можуть спотворювати навчання й оцінку.",
    },
    {
      keys: ["Витік даних / витік цілі", "Витік даних", "витік цілі", "Data leakage"],
      tip: "Data leakage\nВикористання інформації, якої не буде на момент прогнозу в проді. Дає завищені метрики на валідації. (scikit-learn Common pitfalls.)",
    },
    {
      keys: ["Циркулярність ознаки", "Circularity / target leakage", "Circularity", "target leakage", "target"],
      tip: "Circularity / target leakage\nОкремий випадок leakage: ознака побудована з y (напр. price_per_m2 = rent/area при target=rent).",
    },
    {
      keys: ["Holdout / відкладена вибірка", "Holdout", "відкладена вибірка", "Holdout set"],
      tip: "Holdout set\nЧастина даних, відкладена лише для оцінки. Time split: train раніше, test пізніше.",
    },
    {
      keys: ["Train / validation / test", "Train", "validation", "test", "Train / val / test split", "val", "test split"],
      tip: "Train / val / test split\nРозбиття: train — навчання, validation — підбір гіперпараметрів, test — фінальна чесна оцінка.",
    },
    {
      keys: ["Крос-валідація", "Cross-validation, k-fold", "Cross-validation", "k-fold"],
      tip: "Cross-validation\nІтеративний поділ на train/test підмножини для стійкішої оцінки на «небаченому».",
    },
    {
      keys: ["Дрейф даних", "Data drift / covariate drift", "Data drift", "covariate drift"],
      tip: "Data drift / covariate drift\nЗміна розподілу вхідних даних P(X) у часі відносно навчання.",
    },
    {
      keys: ["Концепт-дрейф", "Concept drift"],
      tip: "Concept drift\nЗміна звʼязку P(y|X) у часі: ті самі ознаки — інша ціль. (Gama et al., 2014.)",
    },
    {
      keys: ["Дисбаланс класів", "Class imbalance"],
      tip: "Class imbalance\nОдин клас трапляється набагато рідше. Тоді accuracy часто оманлива — дивіться recall / precision / F1 / balanced accuracy.",
    },
    {
      keys: ["Перенавчання", "Overfitting"],
      tip: "Overfitting\nМодель добре на train і погано на нових даних: запамʼятала шум / специфіку вибірки.",
    },
    {
      keys: ["Недонавчання", "Underfitting"],
      tip: "Underfitting\nМодель занадто проста: погано і на train, і на test.",
    },
    {
      keys: ["Компроміс зміщення–дисперсії", "Bias–variance tradeoff"],
      tip: "Bias–variance tradeoff\nЗанадто проста модель → високе bias; занадто гнучка → висока variance. Шукаємо баланс.",
    },
    {
      keys: ["Прокляття розмірності", "Curse of dimensionality"],
      tip: "Curse of dimensionality\nУ високих вимірностях відстані й щільності поводяться контрінтуїтивно; потрібно більше даних або зменшення розмірності.",
    },
    {
      keys: ["Розрідженість", "Sparsity"],
      tip: "Sparsity\nБільшість значень нульові / відсутні (розріджені вектори BoW, user–item матриці).",
    },
    {
      keys: ["Метрика якості", "Evaluation metric / score", "Evaluation metric", "score"],
      tip: "Evaluation metric / score\nЧисловий критерій якості прогнозу (accuracy, F1, RMSE тощо).",
    },
    {
      keys: ["Accuracy / частка правильних", "Accuracy", "частка правильних"],
      tip: "Accuracy\nЧастка правильних прогнозів серед усіх. На дисбалансі може бути оманливою. Українська пастка: не плутати з precision («точність»).",
    },
    {
      keys: ["Precision"],
      tip: "Precision\nСеред спрогнозованих позитивних — яка частка справді позитивні: tp/(tp+fp).",
    },
    {
      keys: ["Recall / повнота", "Recall", "повнота", "Recall, sensitivity, TPR", "sensitivity", "TPR"],
      tip: "Recall\nСеред справжніх позитивних — яку частку знайшли: tp/(tp+fn).",
    },
    {
      keys: ["F1-міра", "F1 score"],
      tip: "F1 score\nГармонійне середнє precision і recall. Macro / micro — способи усереднення для багатьох класів.",
    },
    {
      keys: ["Істинно позитивний", "True Positive, TP", "True Positive", "TP"],
      tip: "True Positive\nМодель сказала «так», і насправді «так».",
    },
    {
      keys: ["Хибно позитивний", "False Positive, FP", "False Positive", "FP"],
      tip: "False Positive\nМодель сказала «так», а насправді «ні».",
    },
    {
      keys: ["Хибно негативний", "False Negative, FN", "False Negative", "FN"],
      tip: "False Negative\nМодель сказала «ні», а насправді «так».",
    },
    {
      keys: ["Істинно негативний", "True Negative, TN", "True Negative", "TN"],
      tip: "True Negative\nМодель сказала «ні», і насправді «ні».",
    },
    {
      keys: ["Матриця помилок", "Confusion matrix"],
      tip: "Confusion matrix\nТаблиця TP / FP / FN / TN (або багатокласовий аналог) для розбору типів помилок.",
    },
    {
      keys: ["ROC / AUC", "ROC", "AUC", "ROC curve / AUC", "ROC curve"],
      tip: "ROC curve / AUC\nROC — крива TPR проти FPR при зміні порога; AUC — площа під нею (якість ранжування класів).",
    },
    {
      keys: ["Log loss / крос-ентропія", "Log loss", "крос-ентропія", "Log loss / cross-entropy", "cross-entropy"],
      tip: "Log loss / cross-entropy\nВтрата, що штрафує за невпевнені або хибні ймовірнісні прогнози; основа логістичної регресії і багатьох нейромереж.",
    },
    {
      keys: ["MAE", "Mean Absolute Error"],
      tip: "Mean Absolute Error\nСереднє абсолютних |ŷ − y|. Робастніше до великих помилок, ніж MSE.",
    },
    {
      keys: ["MSE", "Mean Squared Error"],
      tip: "Mean Squared Error\nСереднє квадратів помилок (ŷ − y)². Сильніше штрафує великі відхилення.",
    },
    {
      keys: ["RMSE", "Root Mean Squared Error"],
      tip: "Root Mean Squared Error\nКорінь із MSE; у тих самих одиницях, що й ціль.",
    },
    {
      keys: ["R²", "Coefficient of determination"],
      tip: "Coefficient of determination\nЧастка дисперсії цілі, пояснена моделлю (1 — ідеально відносно baseline середнього).",
    },
    {
      keys: ["Baseline"],
      tip: "Baseline\nПростий орієнтир якості до «складної» моделі: константа mean/mode, правило, евристика.",
    },
    {
      keys: ["Inertia / elbow", "Inertia", "elbow", "Inertia / elbow method", "elbow method"],
      tip: "Inertia / elbow method\nInertia — сума квадратів відстаней до центроїдів у K-means; elbow — евристика вибору K.",
    },
    {
      keys: ["Силует", "Silhouette score"],
      tip: "Silhouette score\nМетрика якості кластеризації: наскільки точка ближча до свого кластера, ніж до чужих.",
    },
    {
      keys: ["Precision@k / Recall@k", "Precision@k", "Recall@k"],
      tip: "Precision@k / Recall@k\nМетрики ранжування / рекомендацій у топ-k результатах.",
    },
    {
      keys: ["EDA", "Exploratory Data Analysis"],
      tip: "Exploratory Data Analysis\nРозвідковий аналіз: розподіли, пропуски, звʼязки, аномалії перед серйозним моделюванням.",
    },
    {
      keys: ["Середнє арифметичне", "Mean"],
      tip: "Mean\nСума значень, поділена на кількість. Чутливе до викидів.",
    },
    {
      keys: ["Медіана", "Median"],
      tip: "Median\nСереднє за порядком значення; стійкіше до викидів, ніж середнє.",
    },
    {
      keys: ["Мода", "Mode"],
      tip: "Mode\nНайчастіше значення у вибірці (особливо корисно для категорій).",
    },
    {
      keys: ["Дисперсія", "Variance"],
      tip: "Variance\nСередній квадрат відхилення від середнього; міра розкиду.",
    },
    {
      keys: ["Стандартне відхилення", "Standard deviation, std", "Standard deviation", "std"],
      tip: "Standard deviation\nКорінь із дисперсії; у тих самих одиницях, що дані. Увага: NumPy `std` за замовчуванням ddof=0; для вибіркової оцінки з поправкою Бесселя ставте ddof=1.",
    },
    {
      keys: ["Викид", "Outlier"],
      tip: "Outlier\nСпостереження, що різко випадає з решти даних. Єдиної канонічної дефініції немає — на курсі завжди називайте правило виявлення (IQR fences, |z| ≥ k, DBSCAN noise тощо).",
    },
    {
      keys: ["Коваріація", "Covariance"],
      tip: "Covariance\nМіра спільної змінності двох змінних (масштаб залежить від одиниць).",
    },
    {
      keys: ["Кореляція Пірсона", "Pearson correlation"],
      tip: "Pearson correlation\nНормована коваріація в [-1, 1]: сила й напрям лінійного звʼязку. Кореляція ≠ причинність.",
    },
    {
      keys: ["Мультиколінеарність", "Multicollinearity"],
      tip: "Multicollinearity\nСильна лінійна залежність між ознаками; ускладнює інтерпретацію лінійних моделей.",
    },
    {
      keys: ["z-score"],
      tip: "Z-score\nСтандартизоване значення: (x − mean) / std. Показує, на скільки σ від середнього.",
    },
    {
      keys: ["Правило трьох сигм", "Three-sigma rule"],
      tip: "Three-sigma rule\nУ нормальному розподілі ≈99.7% маси лежить у межах mean ± 3σ; евристика для викидів.",
    },
    {
      keys: ["Гістограма", "Histogram"],
      tip: "Histogram\nГрафік розподілу: частота потраплянь у біни (інтервали).",
    },
    {
      keys: ["Box-plot / «ящик з вусами»", "Box-plot", "«ящик з вусами»", "Box plot"],
      tip: "Box plot\nВізуалізація квартилів, медіани та потенційних викидів за IQR.",
    },
    {
      keys: ["Квартилі / IQR", "Квартилі", "IQR", "Quartiles / Interquartile range", "Quartiles", "Interquartile range"],
      tip: "Quartiles / Interquartile range\nQ1/Q2/Q3 ділять розподіл на чверті; IQR = Q3 − Q1 — міра розкиду «середини».",
    },
    {
      keys: ["Діаграма розсіювання", "Scatter plot"],
      tip: "Scatter plot\nТочки (x, y) для візуального пошуку звʼязку двох змінних.",
    },
    {
      keys: ["Стандартизація / масштабування", "Стандартизація", "масштабування", "Standardization / scaling", "Standardization", "scaling"],
      tip: "Standardization / scaling\nПриведення ознак до спільного масштабу (StandardScaler, MinMaxScaler), важливо для відстаней і градієнтних методів.",
    },
    {
      keys: ["Функція втрат", "Loss function"],
      tip: "Loss function\nЧисло, яке оптимізатор зменшує під час навчання (MSE, log loss, cross-entropy…).",
    },
    {
      keys: ["Залишки", "Residuals"],
      tip: "Residuals\nРізниці ŷ − y (або y − ŷ) у регресії; показують, де модель помиляється.",
    },
    {
      keys: ["Градієнтний спуск", "Gradient descent"],
      tip: "Gradient descent\nІтеративне оновлення параметрів у напрямку антиградієнта функції втрат.",
    },
    {
      keys: ["Learning rate"],
      tip: "Learning rate\nРозмір кроку оновлення ваг. Занадто великий — розбіжність; занадто малий — повільне навчання.",
    },
    {
      keys: ["Епоха", "Epoch"],
      tip: "Epoch\nОдин повний прохід навчальної вибірки під час оптимізації.",
    },
    {
      keys: ["Батч / міні-батч", "Батч", "міні-батч", "Batch / mini-batch", "Batch", "mini-batch"],
      tip: "Batch / mini-batch\nПідмножина прикладів, на якій рахують градієнт за один крок. SGD — часто batch size = 1 або малий.",
    },
    {
      keys: ["SGD / Adam", "SGD", "Adam"],
      tip: "SGD / Adam\nSGD — стохастичний градієнтний спуск; Adam — адаптивний оптимізатор із моментами (популярний у глибокому навчанні).",
    },
    {
      keys: ["Поріг класифікації", "Decision threshold"],
      tip: "Decision threshold\nМежа ймовірності (напр. 0.5), вище якої призначаємо позитивний клас; зсув порога міняє баланс FP/FN.",
    },
    {
      keys: ["Раннє зупинення", "Early stopping"],
      tip: "Early stopping\nПрипинення навчання, коли метрика на validation перестає покращуватись (patience — терпіння в епохах).",
    },
    {
      keys: ["Інференс", "Inference (ML serving)", "ML"],
      tip: "Inference (ML serving)\nУ ML/проді: застосування вже навченої моделі для прогнозу (forward без оновлення ваг). Не плутати зі статистичним inference (висновки про популяцію з вибірки).",
    },
    {
      keys: ["Чекпойнт", "Checkpoint / state_dict", "Checkpoint", "state_dict"],
      tip: "Checkpoint / state_dict\nЗбережений знімок ваг моделі (у PyTorch часто state_dict) для відновлення / деплою.",
    },
    {
      keys: ["Персептрон", "Perceptron"],
      tip: "Perceptron\nІсторично — алгоритм / лінійний бінарний класифікатор (Rosenblatt); у сучасних текстах часто означає один нейрон (лінійний шар + активація). Не плутати з MLP (багатошарова мережа).",
    },
    {
      keys: ["Багатошаровий персептрон", "Multilayer Perceptron, MLP", "Multilayer Perceptron", "MLP"],
      tip: "Multilayer Perceptron\nНейромережа з одним або кількома прихованими шарами fully-connected + активації.",
    },
    {
      keys: ["Прихований шар", "Hidden layer"],
      tip: "Hidden layer\nШар між входом і виходом, що вчить внутрішні представлення.",
    },
    {
      keys: ["Зворотне поширення помилки", "Backpropagation"],
      tip: "Backpropagation\nАлгоритм обчислення градієнтів ваг через ланцюгове правило (forward → loss → backward).",
    },
    {
      keys: ["ReLU", "Rectified Linear Unit"],
      tip: "Rectified Linear Unit\nАктивація max(0, x): проста, зменшує затухання градієнта порівняно з сигмоїдою в глибоких мережах.",
    },
    {
      keys: ["Dropout"],
      tip: "Dropout\nРегуляризація: під час навчання випадково «вимикаємо» нейрони, щоб зменшити співзалежність.",
    },
    {
      keys: ["Weight decay"],
      tip: "Weight decay\nШтраф за величину ваг (близько до L2) під час оптимізації — боротьба з перенавчанням.",
    },
    {
      keys: ["Затухання / вибух градієнта", "Затухання", "вибух градієнта", "Vanishing / exploding gradients", "Vanishing", "exploding gradients"],
      tip: "Vanishing / exploding gradients\nГрадієнти стають надто малими або великими в глибоких / рекурентних мережах — навчання ламається.",
    },
    {
      keys: ["Ініціалізація Xavier / He", "Ініціалізація Xavier", "He", "Xavier / He initialization", "Xavier", "He initialization"],
      tip: "Xavier / He initialization\nСхеми початкових ваг, узгоджені з активаціями, щоб стабілізувати масштаб сигналу й градієнта.",
    },
    {
      keys: ["Згорткова нейромережа", "Convolutional Neural Network, CNN", "Convolutional Neural Network", "CNN"],
      tip: "Convolutional Neural Network\nАрхітектура для сіткових даних (зображення): локальні фільтри, спільні ваги, ієрархія ознак.",
    },
    {
      keys: ["Згортка / фільтр", "Згортка", "фільтр", "Convolution / kernel / filter", "Convolution", "kernel", "filter"],
      tip: "Convolution / kernel / filter\nЛокальна операція ковзання ядра по входу з отриманням карти ознак.",
    },
    {
      keys: ["Stride / padding / pooling", "Stride", "padding", "pooling"],
      tip: "Stride / padding / pooling\nStride — крок згортки; padding — обрамлення; pooling — зменшення просторового розміру (max/avg).",
    },
    {
      keys: ["BatchNorm / LayerNorm", "BatchNorm", "LayerNorm", "Batch / Layer Normalization", "Batch", "Layer Normalization"],
      tip: "Batch / Layer Normalization\nНормалізація активацій усередині мережі для стабільнішого й швидшого навчання.",
    },
    {
      keys: ["Skip-connection", "Skip / residual connection", "Skip", "residual connection"],
      tip: "Skip / residual connection\nПрямий шлях сигналу в обхід шарів (ResNet): полегшує навчання дуже глибоких мереж.",
    },
    {
      keys: ["Transfer learning"],
      tip: "Transfer learning\nПовторне використання моделі, навченої на великому датасеті, для нової задачі (часто freeze → unfreeze / fine-tuning).",
    },
    {
      keys: ["Fine-tuning"],
      tip: "Fine-tuning\nДонавчання (частини) pretrained-ваг на цільових даних під нову задачу.",
    },
    {
      keys: ["RNN / LSTM / GRU", "RNN", "LSTM", "GRU", "Recurrent networks"],
      tip: "Recurrent networks\nАрхітектури для послідовностей із прихованим станом. LSTM/GRU краще тримають довгі залежності (Hochreiter & Schmidhuber та наступники).",
    },
    {
      keys: ["Увага / Attention", "Увага", "Attention"],
      tip: "Attention\nМеханізм зважування релевантних елементів послідовності (запити/ключі/значення). Основа Transformer.",
    },
    {
      keys: ["Токенізація", "Tokenization"],
      tip: "Tokenization\nРозбиття тексту на токени (слова / підслова / символи) для подальшої обробки моделлю.",
    },
    {
      keys: ["Стоп-слова", "Stop words"],
      tip: "Stop words\nЧасті службові слова (і, the…), які інколи відкидають у класичних мішках слів.",
    },
    {
      keys: ["Стемінг", "Stemming"],
      tip: "Stemming\nГрубе обрізання закінчень евристикою до «основи» слова (швидко, менш точно).",
    },
    {
      keys: ["Лематизація", "Lemmatization"],
      tip: "Lemmatization\nПриведення слова до словникової форми (леми), зазвичай з урахуванням частини мови.",
    },
    {
      keys: ["Мішок слів", "Bag-of-words, BoW", "Bag-of-words", "BoW"],
      tip: "Bag-of-words\nПредставлення документа як підрахунків токенів без порядку слів.",
    },
    {
      keys: ["TF-IDF", "Term Frequency–Inverse Document Frequency"],
      tip: "Term Frequency–Inverse Document Frequency\nВаги токенів: часті в документі, але рідкісні в корпусі — важливіші. Класика текстового ML.",
    },
    {
      keys: ["N-грами", "N-grams"],
      tip: "N-grams\nПослідовності з n сусідніх токенів (біграми, триграми) як ознаки.",
    },
    {
      keys: ["Word2Vec", "Word2Vec (CBOW / Skip-gram)", "Word2Vec (CBOW", "CBOW", "Skip-gram)"],
      tip: "Word2Vec (CBOW / Skip-gram)\nАлгоритм навчання щільних ембедінгів слів із контексту (Mikolov et al.).",
    },
    {
      keys: ["GloVe"],
      tip: "GloVe\nГлобальні ембедінги слів на основі статистик співпояв у корпусі.",
    },
    {
      keys: ["Косинусна схожість", "Cosine similarity"],
      tip: "Cosine similarity\nСхожість векторів за кутом (не за довжиною); стандарт для ембедінгів і пошуку.",
    },
    {
      keys: ["BPE / WordPiece", "BPE", "WordPiece", "Byte-Pair Encoding / WordPiece", "Byte-Pair Encoding"],
      tip: "Byte-Pair Encoding / WordPiece\nПідсловесні токенізатори: рідкісні слова збираються з частин; основа сучасних LLM-токенайзерів.",
    },
    {
      keys: ["Спецтокени", "[CLS] / [SEP] / [PAD]", "[CLS]", "CLS", "[SEP]", "SEP", "[PAD]", "PAD"],
      tip: "[CLS] / [SEP] / [PAD]\nСлужбові токени трансформерів: класифікаційний, роздільник, паддинг; разом із attention_mask.",
    },
    {
      keys: ["Дистрибутивна гіпотеза", "Distributional hypothesis"],
      tip: "Distributional hypothesis\nСлова в схожих контекстах мають близькі значення — основа ембедінгів.",
    },
    {
      keys: ["Jupyter Notebook"],
      tip: "Jupyter Notebook\nВеб-застосунок і формат обчислювального документа: код + пояснення + результати в `.ipynb`.",
    },
    {
      keys: ["JupyterLab"],
      tip: "JupyterLab\nIDE-подібна оболонка навколо Jupyter: файли, кілька ноутбуків, термінал, розширення.",
    },
    {
      keys: ["Ядро", "Kernel"],
      tip: "Kernel\nОкремий процес мови (для Python — ipykernel), що виконує код комірок і зберігає стан.",
    },
    {
      keys: ["Комірка коду", "Code cell"],
      tip: "Code cell\nКомірка з виконуваним кодом; результат показується під коміркою.",
    },
    {
      keys: ["Комірка Markdown", "Markdown cell"],
      tip: "Markdown cell\nКомірка з розміткою для пояснень і структури документа.",
    },
    {
      keys: ["Режим редагування / командний режим", "Режим редагування", "командний режим", "Edit mode / Command mode", "Edit mode", "Command mode"],
      tip: "Edit mode / Command mode\nEdit — друкуємо в комірці; Command — керуємо комірками (додати, тип, видалити).",
    },
    {
      keys: ["IPython magic", "IPython magics"],
      tip: "IPython magics\nСпеціальні команди: % — line/cell magic, ! — shell. Приклади: %timeit, %matplotlib.",
    },
    {
      keys: ["CSV", "Comma-Separated Values"],
      tip: "Comma-Separated Values\nТекстовий табличний формат; MIME text/csv задокументовано в RFC 4180.",
    },
    {
      keys: ["ndarray", "NumPy ndarray"],
      tip: "NumPy ndarray\nN-вимірний однорідний масив NumPy — фундамент числових обчислень у Python DS/ML.",
    },
    {
      keys: ["Broadcasting"],
      tip: "Broadcasting\nПравила NumPy для поелементних операцій масивів різних, але сумісних форм без явного копіювання.",
    },
    {
      keys: ["Векторизація", "Vectorization"],
      tip: "Vectorization\nОбчислення над цілими масивами замість циклів Python — швидше завдяки низькорівневим ядрам.",
    },
    {
      keys: ["Series", "pandas Series"],
      tip: "pandas Series\nОдновимірний підписаний масив у pandas (колонка або ряд з індексом).",
    },
    {
      keys: ["DataFrame", "pandas DataFrame"],
      tip: "pandas DataFrame\nДвовимірна підписана таблиця в pandas: рядки + стовпці, основа табличного аналізу.",
    },
    {
      keys: ["groupby / split-apply-combine", "groupby", "split-apply-combine"],
      tip: "GroupBy\nПатерн: розбити на групи → застосувати функцію → зібрати результат (агрегації pandas).",
    },
    {
      keys: ["Булева маска", "Boolean mask"],
      tip: "Boolean mask\nМасив True/False для фільтрації рядків / елементів за умовою.",
    },
    {
      keys: ["One-hot кодування", "One-hot encoding"],
      tip: "One-hot encoding\nКатегорію представляють бінарними стовпцями (по одному на рівень).",
    },
    {
      keys: ["Пайплайн", "Pipeline"],
      tip: "Pipeline\nЛанцюжок кроків: дані → очищення → ознаки → модель → оцінка / деплой. У scikit-learn Pipeline також захищає від leakage у CV.",
    },
    {
      keys: ["Тензор", "Tensor (PyTorch)"],
      tip: "Tensor (PyTorch)\nБагатовимірний масив із підтримкою GPU та автодиференціювання (requires_grad).",
    },
    {
      keys: ["Autograd", "Automatic differentiation"],
      tip: "Automatic differentiation\nАвтоматичне обчислення градієнтів за графом операцій (основа backward у PyTorch).",
    },
    {
      keys: ["nn.Module", "torch.nn.Module"],
      tip: "torch.nn.Module\nБазовий клас шарів і моделей у PyTorch: параметри, forward, train/eval режими.",
    },
    {
      keys: ["DataLoader"],
      tip: "DataLoader\nІтератор батчів із Dataset: shuffle, batch size, багатопроцесорне читання.",
    },
    {
      keys: ["Промпт", "Prompt"],
      tip: "Prompt\nВхідний текст / інструкція для LLM: задача, контекст, формат відповіді, обмеження.",
    },
    {
      keys: ["Zero-shot"],
      tip: "Zero-shot\nВиконання задачі без прикладів у промпті — лише інструкція.",
    },
    {
      keys: ["Few-shot"],
      tip: "Few-shot\nКілька демонстраційних прикладів у промпті, щоб задати формат і стиль відповіді.",
    },
    {
      keys: ["Chain-of-Thought", "Chain-of-Thought, CoT", "CoT"],
      tip: "Chain-of-Thought\nТехніка: просити модель міркувати покроково перед відповіддю — часто покращує складні задачі.",
    },
    {
      keys: ["ReAct", "Reason + Act"],
      tip: "Reason + Act\nПатерн агента: чергування думки (Thought), дії (Action) і спостереження (Observation).",
    },
    {
      keys: ["Контекстне вікно", "Context window"],
      tip: "Context window\nМаксимальна кількість токенів (промпт + історія + відповідь), які модель бачить за раз.",
    },
    {
      keys: ["Галюцинація", "Hallucination"],
      tip: "Hallucination\nМодель генерує виглядає-правдоподібний, але фактично хибний або непідтверджений зміст (робоче визначення курсу: вигаданий факт без опори на джерело/контекст). Межі faithfulness / factuality у літературі розмиті.",
    },
    {
      keys: ["RAG", "Retrieval-Augmented Generation"],
      tip: "Retrieval-Augmented Generation\nСпочатку шукаємо релевантні фрагменти знань, потім підставляємо їх у промпт генерації — менше галюцинацій і актуальніші факти.",
    },
    {
      keys: ["Чанк / overlap", "Чанк", "overlap", "Chunk / overlap", "Chunk"],
      tip: "Chunk / overlap\nФрагмент документа для індексації; overlap — перекриття сусідніх чанків, щоб не різати сенс.",
    },
    {
      keys: ["Vector search / top-k", "Vector search", "top-k"],
      tip: "Vector search / top-k\nПошук найближчих ембедінгів у векторній базі; top-k — скільки фрагментів віддати в контекст.",
    },
    {
      keys: ["Function calling", "Function / tool calling", "Function", "tool calling"],
      tip: "Function / tool calling\nМодель повертає структурований виклик інструмента (імʼя + аргументи) замість «вільного» тексту.",
    },
    {
      keys: ["Prompt injection"],
      tip: "Prompt injection\nАтака / збій: шкідливий або сторонній текст у даних змушує модель порушити інструкції системи.",
    },
    {
      keys: ["PII", "Personally Identifiable Information"],
      tip: "Personally Identifiable Information\nДані, що ідентифікують особу; їх треба мінімізувати, маскувати й не світити в логах/промптах.",
    },
    {
      keys: ["Human-in-the-loop"],
      tip: "Human-in-the-loop\nЛюдина підтверджує / виправляє критичні кроки агента перед виконанням.",
    },
    {
      keys: ["Спостережуваність", "Observability (traces / spans)", "Observability (traces", "spans)"],
      tip: "Observability (traces / spans)\nТрасування викликів LLM/інструментів для дебагу якості, вартості й затримок (напр. LangSmith).",
    },
    {
      keys: ["Структурований вивід", "Structured output"],
      tip: "Structured output\nПримус відповіді моделі до схеми (JSON / tool schema) для надійної інтеграції з кодом.",
    },
    {
      keys: ["Продакшен", "Production"],
      tip: "Production\nБойове середовище продукту. Демо в ноутбуці ≠ production: потрібні тести, моніторинг, відтворюваність, обмеження latency / вартості.",
    },
    {
      keys: ["Моніторинг моделі", "Model monitoring"],
      tip: "Model monitoring\nСпостереження після запуску: якість, drift, вартість помилок, інциденти, latency.",
    },
    {
      keys: ["Затримка", "Latency"],
      tip: "Latency\nЧас відповіді системи. Модель може бути точною, але занадто повільною для продукту.",
    },
    {
      keys: ["Інтерпретованість", "Interpretability"],
      tip: "Interpretability\nНаскільки можна пояснити, чому модель так вирішила. Критично у фінансах, медицині, регуляції.",
    },
    {
      keys: ["Приватність", "Privacy"],
      tip: "Privacy\nЗахист персональних і чутливих даних протягом життєвого циклу AI-системи. (NIST AI RMF.)",
    },
    {
      keys: ["Етика ШІ", "AI ethics / responsible AI", "AI ethics", "AI", "responsible AI"],
      tip: "AI ethics / responsible AI\nСправедливість, уникнення шкоди й дискримінації, прозорість і підзвітність у рішеннях моделі.",
    },
    {
      keys: ["Proxy-дискримінація", "Proxy discrimination"],
      tip: "Proxy discrimination\nКоли «нейтральна» ознака (район, ПІБ) корелює із захищеною групою й модель дискримінує опосередковано.",
    },
    {
      keys: ["LTV", "Lifetime Value"],
      tip: "Lifetime Value\nОчікувана цінність клієнта за весь час співпраці. Часто ціль регресії в бізнесі.",
    },
    {
      keys: ["Triage"],
      tip: "Triage\nПріоритезація випадків (напр. медичних) за терміновістю / ризиком — типовий кейс класифікації.",
    },
    {
      keys: ["Decision framing"],
      tip: "Decision framing\nЯке бізнес-рішення покращуємо і хто/що діє за прогнозом.",
    },
    {
      keys: ["Label design", "label"],
      tip: "Label design\nЯк чесно визначити y: що вимірюємо, з якою затримкою, з якими помилками розмітки.",
    },
    {
      keys: ["Offline / online evaluation", "Offline", "online evaluation"],
      tip: "Offline / online evaluation\nOffline — holdout/CV до запуску; online — A/B, shadow mode, моніторинг у проді.",
    },
    {
      keys: ["Журнал", "Journal"],
      tip: "Journal\nОсновний FastAPI + React застосунок для лекційних нотаток і матеріалів тем.",
    },
    {
      keys: ["Курс", "Course"],
      tip: "Course\nФайловий Python AI курс під backend/data/courses/... (не в БД журналу).",
    },
    {
      keys: ["Пара", "Pair"],
      tip: "Pair\nОдиниця уроку mXX/pair_YY: презентація, план, ДЗ, квіз, нотатки викладача.",
    },
    {
      keys: ["Маніфест", "Manifest"],
      tip: "Manifest\nWhitelist файлів, доступних для завантаження в межах пари.",
    },
    {
      keys: ["Матеріали викладача", "Teacher materials"],
      tip: "Teacher materials\nteacher.md / teacher guides — за замовчуванням не студентський інтерфейс.",
    },
    {
      keys: ["Збірка курсу", "Course build"],
      tip: "Course build\nІдемпотентні генератори в scripts/course_build/; джерела правди — content packs.",
    },
    {
      keys: ["Дошка термінів", "Board"],
      tip: "Board\nСписок ключових термінів пари зі сценарію заняття (поле board у content packs).",
    },
    {
      keys: ["ШІ", "AI", "Artificial Intelligence", "штучний інтелект"],
      tip: "Artificial Intelligence\nМашинна система, яка для явних або неявних цілей виводить із вхідних даних, як згенерувати виходи: прогнози, контент, рекомендації чи рішення, що впливають на фізичне або віртуальне середовище. Системи різняться рівнем автономності й адаптивності після розгортання. (OECD AI Principles.)",
    },
    {
      keys: ["DS", "Data Science", "наука про дані"],
      tip: "Data Science\nМіждисциплінарний процес: бізнес-/дослідницьке питання → дані → аналіз / моделювання → інсайт або продукт. Не обовʼязково включає ML: інколи достатньо описової статистики й візуалізації.",
    },
    {
      keys: ["ML", "Machine Learning", "машинне навчання"],
      tip: "Machine Learning\nПідхід, за якого модель покращує якість прогнозу/рішення на основі досвіду (даних), а не лише за жорстко прописаними правилами. Практична рамка курсу: f(ознаки) → прогноз, параметри підбираються з прикладів.",
    },
    {
      keys: ["DL", "Deep Learning", "глибоке навчання"],
      tip: "Deep Learning\nПідмножина ML на багатошарових нейронних мережах, що вчаться складних внутрішніх представлень даних (зображення, мова, аудіо). (Goodfellow, Bengio, Courville.)",
    },
    {
      keys: ["GenAI", "Generative AI", "генеративний ШІ"],
      tip: "Generative AI\nМоделі, що створюють новий контент (текст, зображення, код, аудіо), моделюючи розподіл даних. У дефініції OECD вихід «content» прямо включено до виходів AI-системи.",
    },
    {
      keys: ["LLM", "Large Language Model"],
      tip: "Large Language Model\nНейромережа (зазвичай на архітектурі Transformer), навчена на великих текстових корпусах передбачати / генерувати мову. На практиці — основа сучасних чат-ботів і кодових асистентів.",
    },
    {
      keys: ["з учителем", "Supervised", "supervised"],
      tip: "Supervised learning\nНавчання, де для кожного навчального прикладу відома очікувана відповідь y (мітка / ground truth). Типові оцінки: класифікатор, регресор. (scikit-learn Glossary.)",
    },
    {
      keys: ["без учителя", "Unsupervised", "unsupervised"],
      tip: "Unsupervised learning\nНавчання без y: шукаємо структуру в X (кластери, аномалії, зменшення розмірності). (scikit-learn Glossary.)",
    },
    {
      keys: ["з підкріпленням", "Reinforcement", "reinforcement", "RL"],
      tip: "Reinforcement Learning\nАгент взаємодіє із середовищем, отримує нагороди і вчиться політиці дій, що максимізує сумарну нагороду в довгостроковій перспективі. (Sutton & Barto.)",
    },
    {
      keys: ["ознаки", "ознака", "features", "feature", "feature-колонки"],
      tip: "Polynomial features\nРозширення простору ознак степенями й взаємодіями (x, x², xy…), щоб лінійна модель описувала нелінійні залежності.",
    },
    {
      keys: ["цільова змінна", "цільова ознака", "target", "мітка", "мітки", "label"],
      tip: "Target\nЗалежна змінна y у supervised: те, що передбачаємо. Синоніми: outcome, ground truth, label.",
    },
    {
      keys: ["зима ШІ", "зими ШІ"],
      tip: "AI winter\nПеріод спаду інтересу й фінансування через завищені обіцянки, брак даних / обчислень і крихкість ранніх систем.",
    },
    {
      keys: ["тест Тюрінга", "тест Тюринга"],
      tip: "Turing test\nОпераційний критерій Алана Тюрінга (1950): чи може машина вести діалог так, щоб людина-суддя не відрізнила її від людини. Це імітаційна гра, не математичне визначення інтелекту.",
    },
    {
      keys: ["ноутбук", "ноутбука", "ноутбуці", "Notebook", ".ipynb"],
      tip: "Jupyter Notebook\nВеб-застосунок і формат обчислювального документа: код + пояснення + результати в `.ipynb`.",
    },
    {
      keys: ["прод", "production", "продакшен"],
      tip: "Production\nБойове середовище продукту. Демо в ноутбуці ≠ production: потрібні тести, моніторинг, відтворюваність, обмеження latency / вартості.",
    },
  /* === EXTRA_OBVIOUS_TERMS_BEGIN === */
    {
      keys: ["дані", "даних", "даними", "Data"],
      tip: "Data\nФакти, виміри чи спостереження (числа, текст, зображення тощо), з яких будують аналіз або модель. Без якісних даних жоден алгоритм не «вгадає» правду про світ.",
    },
    {
      keys: ["модель", "моделі", "моделлю", "Модель", "model"],
      tip: "Model\nСпрощене математичне/програмне представлення залежності між входами (ознаками) і виходом (прогнозом чи рішенням). Модель навчають на даних і потім застосовують до нових прикладів.",
    },
    {
      keys: ["алгоритм", "алгоритму", "алгоритми", "алгоритмів", "Алгоритм", "algorithm"],
      tip: "Algorithm\nЧітка послідовність кроків для розвʼязання задачі. У ML алгоритм навчання підбирає параметри моделі з прикладів.",
    },
    {
      keys: ["метрика", "метрики", "метрикою", "метрик", "Metric"],
      tip: "Metric\nЧисло, яким вимірюємо якість моделі або продукту (accuracy, F1, MAE, recall тощо). Метрику обирають під бізнес-ціну помилок, а не «бо так прийнято».",
    },
    {
      keys: ["прогноз", "прогнозу", "прогнози", "прогнозом", "Prediction", "prediction"],
      tip: "Prediction\nВихід моделі для нового прикладу: клас, число, рейтинг, наступна дія тощо. Прогноз — це оцінка, а не гарантія.",
    },
    {
      keys: ["навчання", "навчанні", "навчанням", "навчитись"],
      tip: "Learning\nПроцес, у якому система покращує поведінку/прогноз на основі досвіду (даних або reward), а не лише за жорстко прописаними правилами.",
    },
    {
      keys: ["параметри", "параметрів", "параметр", "Parameters", "parameters"],
      tip: "Parameters\nЧисла всередині моделі, які підбираються під час навчання (ваги нейромережі, коефіцієнти регресії). Відрізняйте від гіперпараметрів, які задає людина до навчання.",
    },
    {
      keys: ["гіперпараметри", "гіперпараметр", "Hyperparameters", "hyperparameters"],
      tip: "Hyperparameters\nНалаштування навчання/моделі, які задає людина до (або зовні) оптимізації параметрів: learning rate, глибина дерева, кількість шарів тощо.",
    },
    {
      keys: ["помилка", "помилки", "помилок", "помилкою", "Error", "error"],
      tip: "Error\nРозбіжність між прогнозом моделі і істиною (або між рішенням і бажаним результатом). У бізнесі важлива ціна помилки, не лише її кількість.",
    },
    {
      keys: ["файл", "файла", "файлі", "файлом", "File", "file"],
      tip: "File\nОдиниця збереження даних або коду на диску (CSV, .ipynb, .py). У DS/ML файли — спосіб передати відтворюваний артефакт між людьми і системами.",
    },
    {
      keys: ["таблиця", "таблиці", "таблицю", "Table", "table"],
      tip: "Table\nСтруктура даних із рядків (спостережень) і колонок (ознак/цілей). Найпоширеніший формат табличного ML.",
    },
    {
      keys: ["колонка", "колонки", "колонок", "колонках", "Column", "column", "columns"],
      tip: "Column\nПоле таблиці: одна ознака або ціль для всіх рядків. Імʼя колонки має бути стабільним і описаним у data dictionary.",
    },
    {
      keys: ["рядок", "рядка", "рядки", "рядків", "рядках", "Row", "row", "rows"],
      tip: "Row\nОдин запис таблиці = одне спостереження (клієнт, день, транзакція тощо).",
    },
    {
      keys: ["ознак", "ознаки", "ознаках", "Features", "feature-колонки", "feature-колонок"],
      tip: "Feature\nВхідні змінні моделі (X). Морфологічні форми слова «ознака»: ознак / ознаки / ознаках — той самий сенс.",
    },
    {
      keys: ["датасету", "датасеті", "датасетом", "Датасети", "датасети", "міні-датасет", "міні-датасету"],
      tip: "Dataset\nНабір спостережень для аналізу чи навчання. Форми слова: датасет / датасету / датасеті.",
    },
    {
      keys: ["цільова", "цільової", "цільову"],
      tip: "Target\nПрикметник до target-змінної: цільова ознака / цільова змінна — те, що модель вчиться передбачати (y).",
    },
    {
      keys: ["спостережень", "спостереженням"],
      tip: "Observation\nОдин приклад у датасеті (рядок). Форми: спостереження / спостережень.",
    },
    {
      keys: ["Python", "python"],
      tip: "Python\nМова програмування, де-факто стандарт для Data Science і багатьох AI-прототипів: багата екосистема (NumPy, pandas, scikit-learn, PyTorch).",
    },
    {
      keys: ["Python Core"],
      tip: "Python Core\nБазовий курс/рівень Python без DS-бібліотек: синтаксис, структури даних, функції, ООП, файли, Git — передумова цього курсу.",
    },
    {
      keys: ["GPU"],
      tip: "GPU\nGraphics Processing Unit — прискорювач паралельних обчислень. Критичний для deep learning на великих моделях і зображеннях.",
    },
    {
      keys: ["HTML"],
      tip: "HTML\nHyperText Markup Language — мова розмітки вебсторінок. Ці навчальні презентації — HTML-документи.",
    },
    {
      keys: ["API", "API keys"],
      tip: "API\nApplication Programming Interface — контракт, як програми викликають одна одну. API keys — секрети доступу; їх не кладуть у .ipynb і git.",
    },
    {
      keys: ["pip"],
      tip: "pip\nСтандартний встановлювач пакетів Python. Приклад: pip install jupyterlab.",
    },
    {
      keys: ["import", "imports", "імпорт", "імпорти"],
      tip: "import\nОператор Python, що підключає модуль/бібліотеку. У ноутбуці імпорти тримають у верхній комірці.",
    },
    {
      keys: ["pathlib"],
      tip: "pathlib\nМодуль стандартної бібліотеки для шляхів до файлів незалежно від ОС. Зручніший і безпечніший за сирі рядки шляхів.",
    },
    {
      keys: ["csv.DictReader", "csv.DictWriter", "DictReader", "DictWriter"],
      tip: "csv module\nМодуль стандартної бібліотеки для читання/запису CSV. DictReader дає рядки як словники за назвами колонок.",
    },
    {
      keys: ["Jupyter", "jupyter"],
      tip: "Jupyter\nЕкосистема інтерактивних ноутбуків (Notebook/Lab): код, текст і результат в одному документі. Зручно для навчання й EDA.",
    },
    {
      keys: ["JupyterLab"],
      tip: "JupyterLab\nСучасна оболонка Jupyter: файловий браузер, кілька вкладок, термінал. Ближче до IDE, ніж класичний Notebook.",
    },
    {
      keys: ["Google Colab", "Colab"],
      tip: "Google Colab\nХмарні Jupyter-ноутбуки від Google з безкоштовним/обмеженим GPU. Зручно стартувати без локального встановлення.",
    },
    {
      keys: ["VS Code notebooks", "VS Code"],
      tip: "VS Code notebooks\nНоутбуки всередині редактора Visual Studio Code — альтернатива JupyterLab для тих, хто вже працює в IDE.",
    },
    {
      keys: ["Markdown", "markdown", "Markdown cell", "markdown-описом"],
      tip: "Markdown\nЛегка розмітка для тексту в ноутбуках: заголовки, списки, формули. Окремий тип комірки поруч із Code.",
    },
    {
      keys: ["Code cell", "code-комірками", "code/markdown"],
      tip: "Code cell\nКомірка ноутбука з виконуваним кодом (зазвичай Python). Результат зʼявляється під коміркою.",
    },
    {
      keys: ["комірка", "комірки", "комірок", "комірках", "комірками", "комірці"],
      tip: "Cell\nОдиниця ноутбука: code або markdown. Порядок виконання комірок може відрізнятися від порядку в файлі.",
    },
    {
      keys: ["Restart Kernel", "Restart kernel", "Restart Kernel & Run All"],
      tip: "Restart Kernel\nПерезапуск ядра очищає памʼять змінних. Перед здачею: Restart Kernel & Run All — перевірка відтворюваності.",
    },
    {
      keys: ["Run All"],
      tip: "Run All\nКоманда виконати всі комірки ноутбука зверху вниз. Разом із Restart Kernel — мінімальний тест «чи запускається з нуля».",
    },
    {
      keys: ["Shift+Enter", "Ctrl/Cmd+Enter"],
      tip: "Notebook shortcuts\nТипові скорочення Jupyter: Shift+Enter — виконати й перейти далі; Esc — command mode; Enter — edit mode.",
    },
    {
      keys: ["edit mode", "command mode"],
      tip: "Notebook modes\nEdit mode — редагуєте текст комірки; command mode — керуєте структурою ноутбука (додати/видалити комірки).",
    },
    {
      keys: ["ipykernel"],
      tip: "ipykernel\nПакет, що дає Python-ядро для Jupyter. Без встановленого ядра ноутбук не виконає код.",
    },
    {
      keys: ["display_name", "display-name"],
      tip: "Kernel display name\nЛюдська назва ядра в меню Jupyter (наприклад, Python 3). Не плутати з імʼям conda/venv середовища.",
    },
    {
      keys: [".ipynb", "ipynb", "ноутбуки", "Ноутбуки", "ноутбуках"],
      tip: "Notebook (.ipynb)\nФормат файлу Jupyter Notebook (JSON). Зручний для дослідження; стабільний код краще виносити в .py.",
    },
    {
      keys: ["Jupyter magics", "%matplotlib", "%%time"],
      tip: "Jupyter magics\nСпеціальні команди ноутбука на кшталт %matplotlib inline або %%time. Це не звичайний Python — працюють у IPython/Jupyter.",
    },
    {
      keys: ["ML-задачі", "ML-задачу", "ML-задачею", "ML-продукту", "ML-продукт"],
      tip: "ML task / product\nML-задача — постановка «дані → ознаки → ціль → метрика → обмеження». ML-продукт — система в проді з моніторингом і ціною помилок.",
    },
    {
      keys: ["бінарна класифікація", "binary classification"],
      tip: "Binary classification\nЗадача з двома класами (0/1, так/ні). Метрики часто: precision, recall, F1, ROC-AUC — залежно від ціни помилок.",
    },
    {
      keys: ["багатокласова класифікація", "multiclass", "multiclass classification"],
      tip: "Multiclass classification\nКласифікація з трьома і більше класами. Часто дивляться macro/micro-F1, а не лише accuracy.",
    },
    {
      keys: ["F1", "F1-score", "macro-F1"],
      tip: "F1-score\nГармонійне середнє precision і recall. Macro-F1 — середнє F1 по класах; корисно при дисбалансі.",
    },
    {
      keys: ["false_negative", "false_positive", "False negative", "False positive"],
      tip: "False positive / negative\nFalse positive — хибна тривога; false negative — пропущений позитивний випадок. Вартість цих помилок у бізнесі різна.",
    },
    {
      keys: ["етика", "ethics"],
      tip: "Ethics\nПитання справедливості, приватності й шкоди від моделі: кого система «карає» помилкою і чи немає дискримінації через proxy-ознаки.",
    },
    {
      keys: ["loss", "Loss"],
      tip: "Loss\nФункція втрат — що саме оптимізатор мінімізує під час навчання (наприклад log-loss, MSE). Це внутрішній критерій, не завжди = бізнес-метрика.",
    },
    {
      keys: ["feedback", "feedback loop"],
      tip: "Feedback\nЗворотний звʼязок: сигнал, за яким система або людина коригує поведінку (reward у RL, правки розмітки, online-метрики).",
    },
    {
      keys: ["online evaluation", "Offline evaluation", "offline evaluation", "Online / human review"],
      tip: "Online / offline evaluation\nOffline — оцінка на історичних даних; online — у живому продукті (A/B, моніторинг). Хороший offline не гарантує online-успіх.",
    },
    {
      keys: ["Monitoring", "моніторинг"],
      tip: "Monitoring\nСпостереження за моделлю в проді: якість, drift даних, затримки, вартість помилок. Без моніторингу модель «тихо» деградує.",
    },
    {
      keys: ["drift", "Data drift", "Concept drift"],
      tip: "Drift\nЗміна розподілу даних або звʼязку X→y з часом. Через drift вчорашня модель сьогодні помиляється частіше.",
    },
    {
      keys: ["Decision framing"],
      tip: "Decision framing\nФормулювання: яке рішення людини/процесу підтримує модель. Без цього ML легко будує «точний», але непотрібний прогноз.",
    },
    {
      keys: ["Label design"],
      tip: "Label design\nЯк визначити y чесно й доступно: що вважаємо «дефолтом», «спамом», «відтоком». Погана мітка = погана модель навіть із крутим алгоритмом.",
    },
    {
      keys: ["Evaluate", "evaluation", "оцінювання"],
      tip: "Evaluation\nПеревірка якості за метриками на даних, яких модель не бачила під час навчання (holdout / time split / online).",
    },
    {
      keys: ["Anti-patterns", "anti-pattern", "антипатерн", "антипатерни"],
      tip: "Anti-pattern\nТипова шкідлива практика: test на train, accuracy при дисбалансі, ігнор ціни помилок, плутанина демо-ноутбука з production.",
    },
    {
      keys: ["Self-supervised", "self-supervised"],
      tip: "Self-supervised learning\nНавчання з мітками, які автоматично зроблено з самих даних (наприклад, передбачити наступне слово). Основа сучасних LLM.",
    },
    {
      keys: ["Semi-supervised", "semi-supervised"],
      tip: "Semi-supervised learning\nНавчання на малій частці розмічених даних + великій частці нерозмічених. Компроміс між supervised і вартістю розмітки.",
    },
    {
      keys: ["Imitation learning"],
      tip: "Imitation learning\nАгент вчиться копіювати поведінку експерта (демонстрації), а не лише з reward. Часто місток між supervised і RL.",
    },
    {
      keys: ["data-driven", "data driven"],
      tip: "Data-driven\nПідхід, коли рішення спираються на дані й вимірювані ефекти, а не лише на інтуїцію. Не означає «без експертизи домену».",
    },
    {
      keys: ["rule-based", "Rule-based"],
      tip: "Rule-based\nСистема на явних правилах «якщо–то», які написала людина. Прозора, але погано масштабується на складні патерни.",
    },
    {
      keys: ["random forest", "Random Forest"],
      tip: "Random Forest\nАнсамбль дерев рішень: багато дерев голосують разом. Сильний baseline для табличних задач.",
    },
    {
      keys: ["Transformers"],
      tip: "Transformer\nАрхітектура з attention (Vaswani et al., 2017). Основа LLM і багатьох моделей мови/зору. «Transformers» у слайдах = ця родина моделей.",
    },
    {
      keys: ["topic modeling"],
      tip: "Topic modeling\nUnsupervised аналіз текстів: знайти «теми» як розподіли слів (наприклад LDA). Не те саме, що сучасні ембедінги LLM.",
    },
    {
      keys: ["ImageNet"],
      tip: "ImageNet\nВеликий розмічений датасет зображень; історичний бенчмарк, що підштовхнув вибух deep learning у computer vision.",
    },
    {
      keys: ["LTV"],
      tip: "LTV\nLifetime-Time Value — оцінка цінності клієнта за весь час співпраці. Часта бізнес-ціль для прогнозування й сегментації.",
    },
    {
      keys: ["SVM"],
      tip: "SVM\nSupport Vector Machine — класичний алгоритм ML з роздільною гіперплощиною; важливий історично й як сильний baseline.",
    },
    {
      keys: ["PCA"],
      tip: "PCA\nPrincipal Component Analysis — метод зменшення розмірності: нові осі пояснюють максимум дисперсії даних.",
    },
    {
      keys: ["Policy", "політика агента"],
      tip: "Policy\nУ RL: стратегія агента — яку дію обрати в стані. Навчання з підкріпленням якраз і шукає хорошу policy.",
    },
    {
      keys: ["spam", "Spam", "is_spam"],
      tip: "Spam detection\nКласичний приклад binary classification: відфільтрувати небажані повідомлення. Легко пояснити false positive vs false negative.",
    },
    {
      keys: ["interpretability", "інтерпретованість"],
      tip: "Interpretability\nНаскільки людина може зрозуміти, чому модель так вирішила. Часто обмеження продукту поряд із точністю й latency.",
    },
    {
      keys: ["proxy", "proxy-дискримінації", "proxy-ознаки"],
      tip: "Proxy feature\nОзнака, що непрямо кодує чутливий атрибут (район ≈ соціально-економічний статус). Ризик прихованої дискримінації.",
    },
    {
      keys: ["human review", "human-in-the-loop"],
      tip: "Human review\nЛюдина перевіряє або затверджує рішення моделі. Часто потрібно там, де ціна помилки висока.",
    },
    {
      keys: ["senior-практики"],
      tip: "Senior practice\nІнженерний рівень: починати з decision framing і baseline, а не з «наймоднішої» моделі; думати про прод, етику й моніторинг.",
    },
    {
      keys: ["числові", "числовий", "numeric", "числова"],
      tip: "Numeric feature\nОзнака з числовим значенням (ціна, вік, години). Буває continuous (float) або discrete (лічильник).",
    },
    {
      keys: ["категоріальні", "категоріальний", "categorical", "категорія"],
      tip: "Categorical feature\nОзнака з обмеженим набором міток (район, бренд, тариф). Зазвичай потребує кодування перед лінійними/нейро моделями.",
    },
    {
      keys: ["текстові", "текстовий", "text feature", "текстові ознаки"],
      tip: "Text feature\nОзнака-текст (відгук, опис). Для класичних моделей потрібна векторизація; для LLM часто йде як сирий вхід.",
    },
    {
      keys: ["datetime", "дата/час"],
      tip: "Datetime feature\nЧасова мітка або дата. З неї роблять похідні ознаки (день тижня, місяць) і правильно ріжуть train/test у часі.",
    },
    {
      keys: ["image-ознаки", "image feature"],
      tip: "Image feature\nВхід-зображення (або ембедінг зображення). Типовий домен computer vision / multimodal моделей.",
    },
    {
      keys: ["audio feature", "аудіо-ознаки"],
      tip: "Audio feature\nВхід-звук (хвиля або спектр). Окремий домен ML зі своїми пайплайнами ознак і моделями.",
    },
    {
      keys: ["dtype"],
      tip: "dtype\nТип даних колонки (float, int, category, bool, str). Правильний dtype запобігає тихим помилкам у розрахунках.",
    },
    {
      keys: ["схема", "schema", "схему"],
      tip: "Schema\nОпис структури датасету: колонки, типи, ролі feature/target, допустимі значення. Поруч із data dictionary.",
    },
    {
      keys: ["leakage", "Leakage", "data leakage", "витік", "витоку"],
      tip: "Data leakage\nУ X потрапляє інформація з майбутнього або прямий «спойлер» y. Метрики стають завищеними й модель провалюється в проді.",
    },
    {
      keys: ["NaN", "пропусків"],
      tip: "NaN / missing\nNot a Number — маркер пропущеного значення в числових масивах. Треба рахувати частку пропусків і вирішити стратегію обробки.",
    },
    {
      keys: ["A/B", "A/B test", "A/B-тест"],
      tip: "A/B test\nЕксперимент: порівнюємо варіанти продукту на випадкових групах користувачів. Основний спосіб online-перевірки гіпотез.",
    },
    {
      keys: ["pandas", "pandas.read_csv"],
      tip: "pandas\nГоловна бібліотека табличних даних у Python. Далі на курсі CSV відкриємо через pandas.read_csv замість ручного csv.",
    },
    {
      keys: ["matplotlib"],
      tip: "matplotlib\nБазова бібліотека графіків у Python. Часто перший інструмент візуалізації в EDA.",
    },
    {
      keys: ["IDE"],
      tip: "IDE\nIntegrated Development Environment — середовище розробки (VS Code, PyCharm). JupyterLab частково виконує цю роль для DS.",
    },
    {
      keys: ["cloud notebooks", "cloud"],
      tip: "Cloud notebooks\nНоутбуки в хмарі (Colab, SageMaker тощо): менше локальної налаштування, але залежність від мережі й політики даних.",
    },
    {
      keys: ["інсайт", "інсайти", "insight"],
      tip: "Insight\nКорисний висновок із даних, який змінює рішення. Мета Data Science не в графіку самому по собі, а в інсайті.",
    },
    {
      keys: ["гіпотеза", "гіпотези", "hypothesis"],
      tip: "Hypothesis\nПеревірюване припущення. EDA і експерименти існують, щоб гіпотези підтверджувати або спростовувати.",
    },
    {
      keys: ["валідація", "validation"],
      tip: "Validation\nПеревірка моделі на окремій вибірці для вибору гіперпараметрів / ранньої зупинки. Не плутати з фінальним test.",
    },
    {
      keys: ["оптимізація", "optimization"],
      tip: "Optimization\nПроцес мінімізації loss / максимізації метрики шляхом зміни параметрів (градієнтний спуск тощо).",
    },
    {
      keys: ["градієнт", "gradient"],
      tip: "Gradient\nВектор похідних loss за параметрами. Показує напрям найшвидшого зростання; оптимізатор іде приблизно в протилежний бік.",
    },
    {
      keys: ["нейрон", "нейрони", "шар мережі", "шари мережі"],
      tip: "Neuron / layer\nНейрон — базова одиниця нейромережі (лінійне перетворення + активація). Шар — група нейронів одного рівня глибини.",
    },
    {
      keys: ["моделюванням", "моделювання", "modeling"],
      tip: "Modeling\nЕтап, коли з ознак будують і порівнюють моделі. Перед ним — розуміння даних, схеми й метрики успіху.",
    },
    {
      keys: ["середнє арифметичне", "mean baseline"],
      tip: "Mean\nСереднє арифметичне. Простий baseline для регресії: завжди передбачати середнє y на train.",
    },
    {
      keys: ["евристика", "евристики", "heuristic"],
      tip: "Heuristic\nПросте правило «на око» / досвіді домену. Часто стає baseline перед складним ML.",
    },
    {
      keys: ["дисбаланс", "дисбалансі", "class imbalance"],
      tip: "Class imbalance\nКоли один клас зустрічається набагато рідше за інший. Accuracy стає оманливою — дивіться recall/precision/F1 і вартість помилок.",
    },
    {
      keys: ["holdout", "hold-out"],
      tip: "Holdout\nВідкладена частка даних лише для оцінки. Її не використовують для підбору параметрів «до останнього».",
    },
    {
      keys: ["time split", "часовий спліт"],
      tip: "Time-based split\nTrain у минулому, test у майбутньому. Критично для задач із часовою залежністю (інакше leakage).",
    },
    {
      keys: ["продакшену", "продакшені"],
      tip: "Production\nБойове середовище продукту. Відрізняється від ноутбука: затримки, моніторинг, безпека, відтворювані пайплайни.",
    },
    {
      keys: ["обмеження", "constraints"],
      tip: "Constraints\nОбмеження продукту: latency, вартість, interpretability, етика, privacy. Вони такі ж важливі, як метрика якості.",
    },
    {
      keys: ["бізнес-ціль", "business_goal", "business goal"],
      tip: "Business goal\nНавіщо бізнесу модель: яке рішення покращуємо і яку цінність очікуємо. Без цього ML — технологія без сенсу.",
    },
    {
      keys: ["ризики", "ризик", "risks"],
      tip: "Risk\nЩо станеться при помилці моделі (збиток, втрата клієнта, шкода людині). Визначає вибір метрики й порогів.",
    },
    {
      keys: ["розмітка", "розмітки", "labeling"],
      tip: "Labeling\nПроцес створення міток y людьми або правилами. Якість розмітки часто важливіша за вибір алгоритму.",
    },
    {
      keys: ["відтворюваність", "reproducibility"],
      tip: "Reproducibility\nЗдатність отримати той самий результат при повторному запуску (Restart Kernel & Run All, фіксовані seed, зафіксовані версії).",
    },
    {
      keys: ["гігієна ноутбука", "гігієна ноутбука на парі"],
      tip: "Notebook hygiene\nПравила порядку в .ipynb: імпорти зверху, Restart & Run All, без секретів, без зайвого виводу.",
    }
  /* === EXTRA_OBVIOUS_TERMS_END === */

  ];

  const SKIP_TAGS = new Set([
    "SCRIPT", "STYLE", "CODE", "PRE", "SVG", "TEXT", "TSPAN", "TEXTAREA", "INPUT", "KBD", "CANVAS",
  ]);

  function escapeRegExp(s) {
    return s.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  }

  const pairs = [];
  ENTRIES.forEach((e) => {
    e.keys.forEach((k) => pairs.push({ key: k, tip: e.tip }));
  });
  pairs.sort((a, b) => b.key.length - a.key.length);

  const pattern = new RegExp(
    "(?<![\\p{L}\\p{N}_])(" + pairs.map((p) => escapeRegExp(p.key)).join("|") + ")(?![\\p{L}\\p{N}_])",
    "giu"
  );

  const tipByLower = new Map();
  pairs.forEach((p) => {
    const low = p.key.toLowerCase();
    if (!tipByLower.has(low)) tipByLower.set(low, p.tip);
  });

  function shouldSkip(node) {
    let el = node.parentElement;
    while (el) {
      const tag = (el.tagName || "").toUpperCase();
      if (SKIP_TAGS.has(tag)) return true;
      if (el.namespaceURI === "http://www.w3.org/2000/svg") return true;
      if (el.classList && (el.classList.contains("term") || el.classList.contains("toc") || el.classList.contains("diagram"))) {
        return true;
      }
      if (el.id === "pair-toc") return true;
      el = el.parentElement;
    }
    return false;
  }

  function wrapTextNode(textNode) {
    const text = textNode.nodeValue;
    if (!text || !pattern.test(text)) {
      pattern.lastIndex = 0;
      return;
    }
    pattern.lastIndex = 0;

    const frag = document.createDocumentFragment();
    let last = 0;
    let m;
    while ((m = pattern.exec(text)) !== null) {
      if (m.index > last) {
        frag.appendChild(document.createTextNode(text.slice(last, m.index)));
      }
      const raw = m[0];
      const tip = tipByLower.get(raw.toLowerCase());
      if (!tip) {
        frag.appendChild(document.createTextNode(raw));
      } else {
        const span = document.createElement("span");
        span.className = "term";
        span.textContent = raw;
        span.setAttribute("data-tip", tip);
        span.setAttribute("tabindex", "0");
        span.setAttribute("role", "button");
        span.setAttribute("aria-label", raw + ": " + tip.replace(/\n/g, " — "));
        frag.appendChild(span);
      }
      last = m.index + raw.length;
    }
    if (last < text.length) {
      frag.appendChild(document.createTextNode(text.slice(last)));
    }
    textNode.parentNode.replaceChild(frag, textNode);
  }

  function walk(root) {
    const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, {
      acceptNode(node) {
        if (!node.nodeValue || !node.nodeValue.trim()) return NodeFilter.FILTER_REJECT;
        if (shouldSkip(node)) return NodeFilter.FILTER_REJECT;
        return NodeFilter.FILTER_ACCEPT;
      },
    });
    const nodes = [];
    let n;
    while ((n = walker.nextNode())) nodes.push(n);
    nodes.forEach(wrapTextNode);
  }

  function ensureTipEl() {
    let tip = document.getElementById("term-tip");
    if (tip) return tip;
    tip = document.createElement("div");
    tip.id = "term-tip";
    tip.setAttribute("role", "tooltip");
    tip.hidden = true;
    document.body.appendChild(tip);
    return tip;
  }

  function placeTip(tip, anchor) {
    tip.hidden = false;
    tip.innerHTML = "";
    const parts = (tip._raw || "").split("\n");
    const en = document.createElement("div");
    en.className = "tip-en";
    en.textContent = parts[0] || "";
    tip.appendChild(en);
    if (parts.length > 1) {
      const ua = document.createElement("div");
      ua.className = "tip-ua";
      ua.textContent = parts.slice(1).join(" ");
      tip.appendChild(ua);
    }
    const r = anchor.getBoundingClientRect();
    const margin = 10;
    const tw = tip.offsetWidth;
    const th = tip.offsetHeight;
    let left = r.left + r.width / 2 - tw / 2;
    let top = r.top - th - 10;
    if (top < margin) top = r.bottom + 10;
    if (left < margin) left = margin;
    if (left + tw > window.innerWidth - margin) left = window.innerWidth - tw - margin;
    tip.style.left = Math.round(left) + "px";
    tip.style.top = Math.round(top) + "px";
  }

  function bindTips(root) {
    const tip = ensureTipEl();
    let active = null;

    function show(el) {
      active = el;
      tip._raw = el.getAttribute("data-tip") || "";
      placeTip(tip, el);
    }
    function hide(el) {
      if (el && active !== el) return;
      active = null;
      tip.hidden = true;
    }

    root.querySelectorAll(".term").forEach((el) => {
      el.addEventListener("mouseenter", () => show(el));
      el.addEventListener("mouseleave", () => hide(el));
      el.addEventListener("focus", () => show(el));
      el.addEventListener("blur", () => hide(el));
      el.addEventListener("click", (ev) => {
        if (window.matchMedia("(hover: none)").matches) {
          ev.preventDefault();
          if (active === el && !tip.hidden) hide(el);
          else show(el);
        }
      });
    });

    document.addEventListener(
      "click",
      (ev) => {
        if (!active) return;
        if (ev.target && ev.target.closest && ev.target.closest(".term")) return;
        hide(active);
      },
      true
    );

    window.addEventListener(
      "scroll",
      () => {
        if (active && !tip.hidden) placeTip(tip, active);
      },
      true
    );
  }

  function init() {
    const stage = document.querySelector(".stage");
    if (!stage) return;
    walk(stage);
    bindTips(document);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();

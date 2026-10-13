# Лабораторія пар 16–18 — один проєкт

Це **виняток**: три пари в одній папці, бо це один сюжет —
від тензора до порівняної MLP.

Звичайні роздатки курсу лишаються парами 15–16 і 17–18.

## Що тут є

| Файл | Навіщо |
|------|--------|
| `Lesson16_00_presentation.html` | Тензори, autograd, `nn.Module`, ритуал SGD, `state_dict` |
| `Lesson17_00_presentation.html` | Dropout, `train()` / `eval()`, MAE / R² |
| `Lesson18_00_presentation.html` | BatchNorm, чотири конфіги, таблиця |
| `mlp_lab/` | Спільний код: дані → навчання → метрики → таблиця |
| `LessonN_01_…` | Короткі приклади (легко → складніше) |
| `results/` | Офіційні завдання 1–N. Аналогів X.1 немає |
| `LessonN_homework.md` | Домашнє |

Словник запечений у HTML. Блоків викладача в цих файлах немає.

## Середовище

У браузерному Python немає `torch`. Працюйте з venv.

```text
python -m venv .venv
.venv\Scripts\activate
python -m pip install -U pip
python -m pip install -r requirements.txt
python -c "import torch; print(torch.__version__)"
```

Докладно: `START.txt`.

## Один прогін лабораторії

```text
python mlp_lab/run.py
```

Поруч зі скриптом з’являться `loss_curve.png`, `winner.pt` і `conclusion.txt`.
Усі чотири конфіги крутяться на тому самому seed, split, lr і числі епох.

Живі комірки в HTML:

```text
python pair_kernel.py
```

Далі відкрийте презентацію в браузері.

## Порядок пар

1. Пара 16 — зібрати цикл і зберегти ваги.
2. Пара 17 — не оцінювати Dropout у `train()`.
3. Пара 18 — порівняти чотири рядки без підкрутки lr.

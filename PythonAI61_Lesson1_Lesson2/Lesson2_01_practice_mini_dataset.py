#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Lesson 2 · Завдання 1. Зібрати міні-датасет.

Створіть CSV з ≥8 рядками. Окремо перелічіть features і target.
Тема на вибір: студенти / фільми / спорт (або своя).

Нижче вже є приклад даних (exam_pass) — скрипт запускається без помилок.
Замініть rows / FEATURES / TARGET на свої, коли будете готові.
"""

from __future__ import annotations

import csv
from pathlib import Path

# Приклад даних (≥8 рядків). TODO: замініть на власну тему за бажанням.
rows: list[dict] = [
    {"hours_study": 2, "sleep_h": 7, "practice_tasks": 1, "passed": 0},
    {"hours_study": 4, "sleep_h": 6, "practice_tasks": 3, "passed": 0},
    {"hours_study": 5, "sleep_h": 8, "practice_tasks": 4, "passed": 1},
    {"hours_study": 6, "sleep_h": 7, "practice_tasks": 5, "passed": 1},
    {"hours_study": 1, "sleep_h": 5, "practice_tasks": 0, "passed": 0},
    {"hours_study": 7, "sleep_h": 8, "practice_tasks": 6, "passed": 1},
    {"hours_study": 3, "sleep_h": 6, "practice_tasks": 2, "passed": 0},
    {"hours_study": 8, "sleep_h": 7, "practice_tasks": 7, "passed": 1},
]

FEATURES: list[str] = ["hours_study", "sleep_h", "practice_tasks"]
TARGET: str = "passed"
TASK_TYPE: str = "supervised classification"

OUT = Path(__file__).with_name("Lesson2_01_my_dataset.csv")


def main() -> None:
    assert len(rows) >= 8, "Потрібно ≥8 рядків"
    assert FEATURES, "Вкажіть FEATURES"
    assert TARGET, "Вкажіть TARGET"
    assert TASK_TYPE, "Вкажіть TASK_TYPE"
    fieldnames = list(rows[0].keys())
    for col in FEATURES + [TARGET]:
        assert col in fieldnames, f"Немає колонки {col} у rows"

    with OUT.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)

    print("saved:", OUT.resolve())
    print("features:", FEATURES)
    print("target:", TARGET)
    print("task_type:", TASK_TYPE)


if __name__ == "__main__":
    main()

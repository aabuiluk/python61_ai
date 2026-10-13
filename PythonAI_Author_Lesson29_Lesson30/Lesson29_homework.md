# Домашнє · пара 29. Корпус SupportFlow і модель LSTM (ДЗ 6.3, завдання 1–2)

Бізнес-контекст: SupportFlow AI тестує модуль автовідповідей у чаті служби підтримки.

## 1. Корпус даних

Зберіть 20–30 пар «запит → відповідь», схожих на справжні діалоги підтримки
(наприклад: "How do I change my email?" → "You can update it in your profile settings.").
Збережіть у CSV з колонками `id,topic,question,answer`, як `assets/supportflow_qa.csv`.

- Нижній регістр, без пунктуації і чисел: `supportflow.tokenize`.
- Словник token-to-index: `supportflow.prepare(rows)`.
- Максимальна довжина запиту й відповіді; padding до неї: `supportflow.make_tensors`.

## 2. Модель на LSTM

`torch.nn`: `nn.Embedding` → `nn.LSTM(hidden_size=128, num_layers=1)` → `nn.Linear` для наступного токена.
`CrossEntropyLoss`, `Adam(lr=0.001)`, 15 епох. У пакеті це `supportflow.Seq2Seq(vocab, vocab, "lstm")`.

1. Навчіть 15 епох і запишіть loss кожної епохи.
2. Навчіть ще раз до 150 епох. Порівняйте відповіді на 3 запити після 15 і після 150 епох.
3. Одним реченням: чому 15 епох на 30 парах замало?

Рубрика (100): корпус 20–30 пар з очищенням (25), словник, довжини і padding з перевірками assert (25),
модель Embedding → LSTM → Linear з параметрами з умови (25), таблиця loss і висновок про кількість епох (25).

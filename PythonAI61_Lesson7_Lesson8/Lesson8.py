import matplotlib.pyplot as plt
import numpy as np

study = np.array([1, 2, 3, 4, 5, 7], dtype=float)
scores = np.array([62, 68, 74, 79, 85, 91], dtype=float)

fig, ax = plt.subplots(figsize=(7, 4))

x = [1, 2, 3, 4, 5, 7]
y =[10, 20, 30, 40, 60, 80]
y1 = [value ** 3 for value in x]






ax.scatter(study, scores, color="green", s=80, label="студенти")
coef = np.polyfit(study, scores, 1)
xs = np.linspace(study.min(), study.max(), 50)
ax.plot(xs, coef[0] * xs + coef[1], color="orange", linestyle=":", label="тренд")
ax.plot(x, y, color="red", marker="o", linewidth=2, label="старанність")
ax.set_title("Години навчання vs підсумковий бал")
ax.set_xlabel("Години навчання")
ax.set_ylabel("Бал")
ax.grid(True, alpha=0.25)
ax.legend()
plt.show()

import matplotlib.pyplot as plt
import numpy as np

names = ["Olena", "Mark", "Nina", "Petro", "Sofia"]
test1 = [88, 76, 94, 81, 90]
test2 = [85, 80, 91, 78, 92]
x = np.arange(len(names))
width = 0.35

fig, ax = plt.subplots(figsize=(8, 4))
ax.bar(x - width / 2, test1, width, label="Тест 1", color="darkorange")
ax.bar(x + width / 2, test2, width, label="Тест 2", color="steelblue")
ax.set_title("Два тести — grouped bar")
ax.set_xlabel("Студент")
ax.set_ylabel("Бали")
ax.set_xticks(x)
ax.set_xticklabels(names, rotation=20, ha="right")
ax.legend()
plt.show()
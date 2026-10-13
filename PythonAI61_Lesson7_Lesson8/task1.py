# import matplotlib.pyplot as plt
#
# x = list(range(1, 11))
# y = [value ** 2 for value in x]
# y1 = [value ** 3 for value in x]
#
#
# fig, ax = plt.subplots(1,2,figsize=(12, 4))
# ax[0].plot(x, y, color="red", marker="o", linewidth=2)
# ax[0].plot(x, y1, color="green", marker="o", linewidth=2)
# ax[0].set_title("Графік функції y = x²")
# ax[0].set_xlabel("X")
# ax[0].set_ylabel("Y")
#
# ax[1].plot(x, y, color="red", marker="o", linewidth=2)
# ax[1].plot(x, y1, color="green", marker="o", linewidth=2)
# ax[1].set_title("Графік функції y = x²")
# ax[1].set_xlabel("X")
# ax[1].set_ylabel("Y")
#
# fig.tight_layout()
# plt.show()

# import matplotlib.pyplot as plt
#
# x = list(range(1, 11))
# y = [value ** 2 for value in x]
# y1 = [value ** 3 for value in x]
#
#
# fig, ax = plt.subplots(1,2,figsize=(12, 4))
# ax[0].plot(x, y, color="red", marker="o", linewidth=2)
# ax[0].set_title("Графік функції y = x²")
# ax[0].set_xlabel("X")
# ax[0].set_ylabel("Y")
#
# ax[1].plot(x, y1, color="green", marker="o", linewidth=2)
# ax[1].set_title("Графік функції y = x²")
# ax[1].set_xlabel("X")
# ax[1].set_ylabel("Y")
#
# fig.tight_layout()
# plt.show()

import matplotlib.pyplot as plt

months = ["Січ", "Лют", "Бер", "Кві", "Тра", "Чер", "Лип", "Сер"]
sales = [420, 380, 510, 560, 600, 580, 640, 590]
pairs = sorted(zip(months, sales), key=lambda p: p[1])
labels = [p[0] for p in pairs]
values = [p[1] for p in pairs]

fig, ax = plt.subplots(figsize=(7, 5))
bars = ax.barh(labels, values, color="sienna")
ax.set_title("Продажі кавʼярні (від менших до більших)")
ax.set_xlabel("Чашки")
for bar, val in zip(bars, values):
    ax.text(bar.get_width() + 8, bar.get_y() + bar.get_height() / 2, str(val), va="center")
plt.show()

print(list(zip(bars, values)))
import math
import matplotlib.pyplot as plt


def cosine(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(y * y for y in b))
    return dot / (norm_a * norm_b)


cat = [1.0, 0.2]
dog = [0.9, 0.3]
car = [0.1, 1.0]


print("cat ↔ dog:", cosine(cat, dog))
print("cat ↔ car:", cosine(cat, car))


# Создаём координатную плоскость
plt.figure(figsize=(7, 7))


# Рисуем векторы как стрелки из точки (0, 0)
plt.quiver(
    0, 0,
    cat[0], cat[1],
    angles="xy",
    scale_units="xy",
    scale=1,
    label="cat"
)

plt.quiver(
    0, 0,
    dog[0], dog[1],
    angles="xy",
    scale_units="xy",
    scale=1,
    label="dog"
)

plt.quiver(
    0, 0,
    car[0], car[1],
    angles="xy",
    scale_units="xy",
    scale=1,
    label="car"
)


# Подписываем концы векторов
plt.text(cat[0], cat[1], "  cat")
plt.text(dog[0], dog[1], "  dog")
plt.text(car[0], car[1], "  car")


# Настраиваем оси
plt.xlim(0, 1.2)
plt.ylim(0, 1.2)

plt.axhline(0)
plt.axvline(0)

plt.xlabel("X")
plt.ylabel("Y")

plt.grid()
plt.legend()

plt.title("Графическое представление векторов")

plt.show()
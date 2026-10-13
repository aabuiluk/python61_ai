import tkinter as tk
import torch

# ============================================================
# ДАНІ
# ============================================================

img = torch.arange(25.0).reshape(5, 5)

kernel = torch.tensor([
    [-1.0, 0.0, 1.0],
    [-1.0, 0.0, 1.0],
    [-1.0, 0.0, 1.0]
])

output = torch.zeros(3, 3)

# ============================================================
# TKINTER
# ============================================================

root = tk.Tk()
root.title("Згортка 5×5 ядром 3×3")
root.geometry("1150x650")

CELL = 65

canvas = tk.Canvas(root, width=1150, height=520, bg="white")
canvas.pack()

# Позиції трьох матриць
IMG_X = 40
IMG_Y = 100

KERNEL_X = 450
KERNEL_Y = 165

OUTPUT_X = 800
OUTPUT_Y = 165

step = 0


# ============================================================
# МАЛЮВАННЯ КЛІТИНКИ
# ============================================================

def draw_cell(x, y, value, fill="white", outline="black", width=2):
    canvas.create_rectangle(
        x, y,
        x + CELL, y + CELL,
        fill=fill,
        outline=outline,
        width=width
    )

    canvas.create_text(
        x + CELL / 2,
        y + CELL / 2,
        text=f"{value:.0f}",
        font=("Arial", 17, "bold")
    )


# ============================================================
# МАТРИЦЯ 5×5
# ============================================================

def draw_image(current_i=None, current_j=None):
    canvas.create_text(
        IMG_X + 2.5 * CELL,
        IMG_Y - 35,
        text="IMAGE 5 × 5",
        font=("Arial", 18, "bold")
    )

    for i in range(5):
        for j in range(5):

            fill = "white"
            outline = "black"
            width = 2

            # Поточна область 3×3
            if current_i is not None:
                if (
                    current_i <= i < current_i + 3
                    and
                    current_j <= j < current_j + 3
                ):
                    fill = "#ADD8E6"
                    outline = "blue"
                    width = 3

            draw_cell(
                IMG_X + j * CELL,
                IMG_Y + i * CELL,
                img[i, j],
                fill,
                outline,
                width
            )


# ============================================================
# ЯДРО 3×3
# ============================================================

def draw_kernel():
    canvas.create_text(
        KERNEL_X + 1.5 * CELL,
        KERNEL_Y - 35,
        text="KERNEL 3 × 3",
        font=("Arial", 18, "bold")
    )

    for i in range(3):
        for j in range(3):

            draw_cell(
                KERNEL_X + j * CELL,
                KERNEL_Y + i * CELL,
                kernel[i, j],
                "#FFF2B2"
            )


# ============================================================
# OUTPUT 3×3
# ============================================================

def draw_output(active_i=None, active_j=None):
    canvas.create_text(
        OUTPUT_X + 1.5 * CELL,
        OUTPUT_Y - 35,
        text="OUTPUT 3 × 3",
        font=("Arial", 18, "bold")
    )

    for i in range(3):
        for j in range(3):

            fill = "white"

            if active_i == i and active_j == j:
                fill = "#90EE90"

            # Ще не обчислені клітинки показуємо "-"
            cell_number = i * 3 + j

            if cell_number < step:
                value = f"{output[i, j]:.0f}"
            else:
                value = "-"

            x = OUTPUT_X + j * CELL
            y = OUTPUT_Y + i * CELL

            canvas.create_rectangle(
                x, y,
                x + CELL, y + CELL,
                fill=fill,
                outline="black",
                width=2
            )

            canvas.create_text(
                x + CELL / 2,
                y + CELL / 2,
                text=value,
                font=("Arial", 17, "bold")
            )


# ============================================================
# ПОЯСНЕННЯ ОБЧИСЛЕННЯ
# ============================================================

def draw_calculation(i, j, value):
    window = img[i:i+3, j:j+3]

    parts = []

    for r in range(3):
        for c in range(3):
            parts.append(
                f"{window[r,c]:.0f}×{kernel[r,c]:.0f}"
            )

    expression = " + ".join(parts)

    canvas.create_text(
        575,
        440,
        text=f"Крок {step + 1}/9   →   позиція ядра [{i}, {j}]",
        font=("Arial", 16, "bold")
    )

    canvas.create_text(
        575,
        475,
        text=expression,
        font=("Arial", 11)
    )

    canvas.create_text(
        575,
        505,
        text=f"Результат = {value:.0f}",
        font=("Arial", 17, "bold"),
        fill="green"
    )


# ============================================================
# ПЕРЕМАЛЮВАННЯ
# ============================================================

def redraw(active_i=None, active_j=None, value=None):
    canvas.delete("all")

    draw_image(active_i, active_j)
    draw_kernel()
    draw_output(active_i, active_j)

    # Стрілки
    canvas.create_text(
        390,
        260,
        text="×",
        font=("Arial", 35, "bold")
    )

    canvas.create_text(
        720,
        260,
        text="→",
        font=("Arial", 35, "bold")
    )

    if active_i is not None:
        draw_calculation(active_i, active_j, value)


# ============================================================
# ОДИН КРОК
# ============================================================

def next_step():
    global step

    if step >= 9:
        return

    # 0 -> (0,0)
    # 1 -> (0,1)
    # 2 -> (0,2)
    # 3 -> (1,0)
    # ...
    i = step // 3
    j = step % 3

    # Беремо поточне вікно 3×3
    window = img[i:i+3, j:j+3]

    # Згортка
    value = (window * kernel).sum().item()

    # Записуємо результат
    output[i, j] = value

    step += 1

    redraw(i, j, value)

    if step == 9:
        next_button.config(
            text="Готово ✓",
            state="disabled"
        )


# ============================================================
# RESET
# ============================================================

def reset():
    global step, output

    step = 0
    output = torch.zeros(3, 3)

    next_button.config(
        text="Наступний крок →",
        state="normal"
    )

    redraw()


# ============================================================
# КНОПКИ
# ============================================================

buttons = tk.Frame(root)
buttons.pack(pady=10)

next_button = tk.Button(
    buttons,
    text="Наступний крок →",
    font=("Arial", 16, "bold"),
    width=20,
    height=2,
    command=next_step
)

next_button.pack(side="left", padx=10)

reset_button = tk.Button(
    buttons,
    text="Скинути",
    font=("Arial", 16),
    width=12,
    height=2,
    command=reset
)

reset_button.pack(side="left", padx=10)


# Початковий стан
redraw()

root.mainloop()
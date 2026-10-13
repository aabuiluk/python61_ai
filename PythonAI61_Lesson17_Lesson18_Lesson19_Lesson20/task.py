# import torch
#
# x = torch.linspace(-6, 6, 13)
# s = torch.sigmoid(x)
# t = torch.tanh(x)
# grad = s * (1 - s)
# print("x sigma sigma_prime")
# for a, b, c in zip(x, s, grad):
#     print(f"{float(a):6.1f} {float(b):8.4f} {float(c):10.4f}")
# # -> найбільша похідна біля x=0
#
# import numpy as np
# import matplotlib.pyplot as plt
#
# x = np.linspace(-8, 8, 200)
# s = 1 / (1 + np.exp(-x))
# t = 1 / (1 + np.exp(-x))
# fig, ax = plt.subplots(figsize=(5.4, 3.1))
# ax.plot(x, s, color="#ffb86b", label="sigmoid")
# ax.plot(x, t, color="#6bb8ff", label="tahn")
# ax.plot(x, s * (1 - s), color="#7dffb3", label="похідна")
# ax.legend()
# ax.set_xlabel("x")
# ax.set_title("sigmoid і похідна")
# fig.tight_layout()
# plt.show()
# # -> графік з'являється після plt.show()

import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(-8, 8, 200)

# Sigmoid
s = 1 / (1 + np.exp(-x))
s_grad = s * (1 - s)

# Tanh
t = np.tanh(x)
t_grad = 1 - t ** 2

# Один графік
plt.figure(figsize=(8, 5))

plt.plot(x, s, label="sigmoid")
plt.plot(x, s_grad, label="sigmoid derivative")

plt.plot(x, t, label="tanh")
plt.plot(x, t_grad, label="tanh derivative")

plt.xlabel("x")
plt.ylabel("y")
plt.title("Sigmoid і Tanh та їх похідні")

plt.axhline(0)
plt.axvline(0)
plt.grid()
plt.legend()

plt.show()
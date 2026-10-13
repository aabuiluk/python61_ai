# import torch
#
# img = torch.arange(25.0).reshape(5, 5)
# k = torch.tensor([[-1.0, 0.0, 1.0], [-2.0, 0.0, 2.0], [-1.0, 0.0, 1.0]])
# out = torch.zeros(3, 3)
# for i in range(3):
#     for j in range(3):
#         out[i, j] = (img[i:i + 3, j:j + 3] * k).sum()
# print(out)
# # -> тензор 3×3 із результатом згортки

import torch
import torch.nn.functional as F

width = 10
height = 10

img = torch.arange(100.0).reshape(height, width)

k = torch.tensor([
    [-1.0, 0.0, 1.0],
    [-2.0, 0.0, 2.0],
    [-1.0, 0.0, 1.0]
])

# 10×10 з ядром 3×3 -> 8×8
out = torch.zeros(8, 8)

for i in range(height - 2):
    for j in range(width - 2):
        window = img[i:i + 3, j:j + 3]

        out[i, j] = (window * k).sum()


# Те саме через conv2d
auto = F.conv2d(
    img.reshape(1, 1, 10, 10),
    k.reshape(1, 1, 3, 3)
)

print(out)

print(auto[0, 0])

print(torch.allclose(auto[0, 0], out))
# True
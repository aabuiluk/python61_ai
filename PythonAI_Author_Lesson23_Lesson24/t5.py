import torch
from torch import nn

torch.manual_seed(42)
xb = torch.randn(8, 1, 28, 28)  # маленький стенд 28×28
yb = torch.randint(0, 10, (8,))  # 10 класів

def cnn_dropout_after_relu():
    return nn.Sequential(
        nn.Conv2d(1, 16, 3), nn.BatchNorm2d(16), nn.ReLU(),
        nn.Dropout(0.3), nn.MaxPool2d(2), nn.Flatten(),
        nn.Linear(16 * 13 * 13, 10),
    )

def cnn_dropout_before_relu():  # 1.1: Dropout ПЕРЕД ReLU
    return nn.Sequential(
        nn.Conv2d(1, 16, 3), nn.BatchNorm2d(16),
        nn.Dropout(0.3), nn.ReLU(),
        nn.MaxPool2d(2), nn.Flatten(),
        nn.Linear(16 * 13 * 13, 10),
    )

def train_loss(model, steps=25):
    opt = torch.optim.Adam(model.parameters(), lr=1e-3)
    loss_fn = nn.CrossEntropyLoss()
    model.train()
    last = 0.0
    for _ in range(steps):
        opt.zero_grad()
        loss = loss_fn(model(xb), yb)
        loss.backward()
        opt.step()
        last = float(loss.item())
    return last

loss_after = train_loss(cnn_dropout_after_relu())
loss_before = train_loss(cnn_dropout_before_relu())
print("Dropout після ReLU → train loss", round(loss_after, 4))
print("Dropout перед ReLU → train loss", round(loss_before, 4))
# -> два числа; місце Dropout змінює, на що саме діє маска (до/після нелінійності)
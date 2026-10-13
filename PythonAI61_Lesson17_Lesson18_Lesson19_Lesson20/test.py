import numpy as np  # зручні масиви до torch
import torch  # тензори, autograd, збереження ваг
import torch.nn as nn  # Module, Linear, ReLU, MSELoss
import torch.optim as optim  # SGD(lr=0.01), як на парі 16
import matplotlib.pyplot as plt  # крива train loss
from sklearn.datasets import make_regression  # синтетична таблиця 10 ознак
from sklearn.model_selection import train_test_split  # один чесний split
from sklearn.preprocessing import StandardScaler  # scaler.fit лише на train
torch.manual_seed(42)  # ваги Linear стартують однаково
np.random.seed(42)  # той самий датасет при повторному запуску
X_np, y_np = make_regression(n_samples=240, n_features=10, noise=8.0, random_state=42)  # стенд, не клініка
X_tr, X_te, y_tr, y_te = train_test_split(X_np, y_np, test_size=0.25, random_state=42)  # 75/25, один seed
scaler = StandardScaler()  # mean/std рахуємо нижче
X_tr = scaler.fit_transform(X_tr).astype(np.float32)  # fit тільки на train
X_te = scaler.transform(X_te).astype(np.float32)  # test лише transform — без витоку
y_tr = y_tr.reshape(-1, 1).astype(np.float32)  # Linear чекає стовпець (n, 1)
y_te = y_te.reshape(-1, 1).astype(np.float32)  # тестова ціль тієї ж форми
x = torch.from_numpy(X_tr)  # навчальний тензор ознак
y = torch.from_numpy(y_tr)  # навчальний тензор цілі
class RiskNet(nn.Module):  # клас моделі: шари в __init__, рахунок у forward
    def __init__(self):  # конструктор: тут лише оголошення шарів
        super().__init__()  # обовʼязковий виклик батька, інакше parameters() порожній
        self.hidden = nn.Linear(10, 32)  # 10→32: 10*32 ваг + 32 bias = 352
        self.act = nn.ReLU()  # нелінійність, інакше два Linear склеяться в один
        self.out = nn.Linear(32, 1)  # 32→1: 32 ваг + 1 bias = 33; разом 385
    def forward(self, batch):  # рух даних: hidden → ReLU → out
        h = self.act(self.hidden(batch))  # прихований шар + активація
        return self.out(h)  # один логіт регресії
model = RiskNet()  # екземпляр; оптимізатор побачить усі Linear
n_params = sum(p.numel() for p in model.parameters())  # 352 + 33 = 385
opt = optim.SGD(model.parameters(), lr=0.01)  # ритуал пари 16, не Adam
loss_fn = nn.MSELoss()  # регресія, не CrossEntropy
history = []  # крива, яку малюватимемо
for epoch in range(60):  # повний ритуал zero_grad → forward → loss → backward → step
    model.train()  # режим навчання (на парі 16 Dropout ще немає, але звичку ставимо)
    opt.zero_grad()  # без цього градієнт додасться до попереднього кроку
    pred = model(x)  # forward усім train-батчем
    loss = loss_fn(pred, y)  # скаляр MSE
    loss.backward()  # autograd заповнює .grad у вагах
    opt.step()  # SGD оновлює ваги
    history.append(float(loss.item()))  # точка на кривій
print("params:", n_params)  # контракт пари 16: 10→32→1 = 385
print("final train MSE:", round(history[-1], 4))  # закінчений результат навчання
weights = model.state_dict()  # знімок ваг, не pickle класу
clone = RiskNet()  # та сама архітектура
clone.load_state_dict(weights)  # відновлюємо ваги в новий екземпляр
clone.eval()  # для перевірки, що сейв спрацював
with torch.no_grad():  # граф для інференсу не потрібен
    restored = float(nn.functional.mse_loss(clone(x), y).item())  # MSE після load
print("restored MSE:", round(restored, 4))  # має збігтися з final train MSE


fig, ax = plt.subplots(figsize=(6, 4))  # вікно кривої
ax.plot(history, lw=2, color="C0")  # train loss по епохах
ax.set_xlabel("епоха")  # горизонталь — час навчання
ax.set_ylabel("MSE")  # вертикаль — помилка
ax.set_title("Кінець пари 16: MLP уже вчиться, є крива і state_dict")  # знімок уміння
fig.tight_layout()  # поля графіка
plt.show()  # показати вікно
# -> params 385; train MSE падає; restored MSE = final train MSE
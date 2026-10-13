import numpy as np  # масиви до тензорів
import torch  # тензори й режими train/eval
import torch.nn as nn  # Linear, ReLU, Dropout, MSELoss
import torch.optim as optim  # SGD зі спільним lr
import matplotlib.pyplot as plt  # дві криві: train і «як на test»
from sklearn.datasets import make_regression  # той самий стенд, що на 16–17
from sklearn.model_selection import train_test_split  # один split на всі порівняння
from sklearn.preprocessing import StandardScaler  # fit на train
from sklearn.metrics import mean_absolute_error, r2_score  # метрики на test
torch.manual_seed(42)  # ваги й Dropout-маски стартують відтворювано
np.random.seed(42)  # датасет фіксований
X_np, y_np = make_regression(n_samples=240, n_features=10, noise=12.0, random_state=42)  # трохи більше шуму, щоб був gap
X_tr, X_te, y_tr, y_te = train_test_split(X_np, y_np, test_size=0.25, random_state=42)  # спільний всесвіт
sc = StandardScaler()  # один scaler
X_tr = sc.fit_transform(X_tr).astype(np.float32)  # статистика лише з train
X_te = sc.transform(X_te).astype(np.float32)  # test не підглядає mean/std
y_tr = y_tr.reshape(-1, 1).astype(np.float32)  # форма (n, 1)
y_te = y_te.reshape(-1, 1).astype(np.float32)  # форма test
x_tr, y_tr_t = torch.from_numpy(X_tr), torch.from_numpy(y_tr)  # train тензори
x_te, y_te_t = torch.from_numpy(X_te), torch.from_numpy(y_te)  # test тензори
class DropNet(nn.Module):  # MLP кінця пари 17: Dropout після hidden
    def __init__(self):  # оголошення шарів
        super().__init__()  # реєстр параметрів nn.Module
        self.hidden = nn.Linear(10, 32)  # той самий 10→32
        self.act = nn.ReLU()  # активація перед Dropout
        self.drop = nn.Dropout(p=0.3)  # p — ймовірність ВИМКНУТИ нейрон
        self.out = nn.Linear(32, 1)  # вихід регресії
    def forward(self, batch):  # hidden → ReLU → Dropout → Linear
        h = self.act(self.hidden(batch))  # нелінійність
        h = self.drop(h)  # у train() маска випадкова; у eval() вимкнена
        return self.out(h)  # ŷ
model = DropNet()  # екземпляр з Dropout
opt = optim.SGD(model.parameters(), lr=0.01)  # той самий бюджет, що без Dropout
loss_fn = nn.MSELoss()  # порівнюємо яблука з яблуками
train_hist, test_hist = [], []  # дві криві для графіка gap
def mse_on(split_x, split_y):  # допоміжна оцінка в eval + no_grad
    model.eval()  # вимикає Dropout, інакше MAE — лотерея маски
    with torch.no_grad():  # не будуємо граф і не чіпаємо ваги
        return float(loss_fn(model(split_x), split_y).item())  # число MSE
for epoch in range(50):  # чесний короткий бюджет
    model.train()  # Dropout ПРАЦЮЄ лише тут
    opt.zero_grad()  # ритуал пари 16
    loss = loss_fn(model(x_tr), y_tr_t)  # forward + MSE на train
    loss.backward()  # градієнт
    opt.step()  # крок SGD
    train_hist.append(float(loss.item()))  # train loss цієї епохи (ще з Dropout)
    test_hist.append(mse_on(x_te, y_te_t))  # test — обовʼязково eval()
model.eval()  # фінальні метрики без маски
with torch.no_grad():  # інференс
    pred_tr = model(x_tr).numpy()  # ŷ train
    pred_te = model(x_te).numpy()  # ŷ test
mae_tr = mean_absolute_error(y_tr, pred_tr)  # MAE train
mae_te = mean_absolute_error(y_te, pred_te)  # MAE test — головне число звіту
r2_te = r2_score(y_te, pred_te)  # R² на test, не на train
gap = mae_te - mae_tr  # overfitting видно, коли gap великий
print("MAE train/test:", round(mae_tr, 3), round(mae_te, 3))  # два числа поруч
print("R2 test:", round(r2_te, 3), "gap:", round(gap, 3))  # закінчений результат пари 17


fig, ax = plt.subplots(figsize=(6, 4))  # вікно
ax.plot(train_hist, label="train MSE (з Dropout)", lw=2)  # зубріння train
ax.plot(test_hist, label="test MSE (eval)", lw=2)  # чесна крива
ax.set_xlabel("епоха")  # час
ax.set_ylabel("MSE")  # помилка
ax.set_title("Кінець пари 17: Dropout + eval(), дивимось на gap")  # знімок
ax.legend()  # підпис кривих
fig.tight_layout()  # поля
plt.show()  # показати графік
# -> MAE train і test + R²; на графіку test не зобовʼязаний падати так само, як train
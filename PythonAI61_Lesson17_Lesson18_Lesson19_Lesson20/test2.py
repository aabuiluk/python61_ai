import torch
from torch import nn
from sklearn.datasets import make_regression
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split

torch.manual_seed(42)
X, y = make_regression(200, 10, noise=10, random_state=42)
x_tr, x_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=42)
x_tr = torch.tensor(x_tr, dtype=torch.float32)
x_te = torch.tensor(x_te, dtype=torch.float32)
y_tr = torch.tensor(y_tr, dtype=torch.float32).unsqueeze(1)
y_te = y_te.reshape(-1, 1)
model = nn.Sequential(nn.Linear(10, 32),
                      nn.BatchNorm1d(32),
                      nn.ReLU(),
                      nn.Linear(32, 1))
opt = torch.optim.Adam(model.parameters(), lr=1e-3)
for _ in range(15):
    model.train()
    opt.zero_grad()
    loss = torch.nn.functional.mse_loss(model(x_tr), y_tr)
    loss.backward()
    opt.step()
model.eval()
with torch.no_grad():
    mae = mean_absolute_error(y_te, model(x_te).numpy())
path = "winner.pt"
torch.save(model.state_dict(), path)


fresh = nn.Sequential(nn.Linear(10, 32), nn.BatchNorm1d(32), nn.ReLU(), nn.Linear(32, 1))
fresh.load_state_dict(torch.load(path, weights_only=True))
fresh.eval()
with torch.no_grad():
    mae2 = mean_absolute_error(y_te, fresh(x_te).numpy())
print(round(mae, 6), round(mae2, 6), abs(mae - mae2) < 1e-6)
# -> True: той самий test MAE після load
from torch import nn

stable = nn.Sequential(
    nn.Conv2d(1, 16, 3), nn.BatchNorm2d(16), nn.ReLU(),
    nn.Dropout(0.3), nn.MaxPool2d(2), nn.Flatten(),
    nn.Linear(16 * 13 * 13, 10),
)
print(stable)
# -> модель з BN і Dropout

from torch import nn

stable = nn.Sequential(
    nn.Conv2d(1, 16, 3), nn.BatchNorm2d(16), nn.Dropout(0.3), nn.ReLU(),
    nn.MaxPool2d(2), nn.Flatten(),
    nn.Linear(16 * 13 * 13, 10),
)
print(stable)
# -> модель з BN і Dropout

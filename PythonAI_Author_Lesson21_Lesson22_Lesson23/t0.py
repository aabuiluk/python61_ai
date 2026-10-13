import torch
from torch import nn
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
from PIL import Image

# ============================================================
# 1. НАЛАШТУВАННЯ
# ============================================================

device = torch.device(
    "mps" if torch.backends.mps.is_available()
    else "cuda" if torch.cuda.is_available()
    else "cpu"
)

print("Device:", device)

# MNIST:
# картинка 28×28
# 1 канал (чорно-біла)
transform = transforms.ToTensor()


# ============================================================
# 2. ЗАВАНТАЖЕННЯ MNIST
# ============================================================

train_dataset = datasets.MNIST(
    root="./data",
    train=True,
    download=True,
    transform=transform
)

test_dataset = datasets.MNIST(
    root="./data",
    train=False,
    download=True,
    transform=transform
)

train_loader = DataLoader(
    train_dataset,
    batch_size=64,
    shuffle=True
)

test_loader = DataLoader(
    test_dataset,
    batch_size=64,
    shuffle=False
)


# ============================================================
# 3. CNN
# ============================================================

class DigitCNN(nn.Module):

    def __init__(self):
        super().__init__()

        self.conv = nn.Sequential(

            # 1×28×28 -> 16×28×28
            nn.Conv2d(
                in_channels=1,
                out_channels=16,
                kernel_size=3,
                padding=1
            ),

            nn.ReLU(),

            # 16×28×28 -> 16×14×14
            nn.MaxPool2d(2),

            # 16×14×14 -> 32×14×14
            nn.Conv2d(
                in_channels=16,
                out_channels=32,
                kernel_size=3,
                padding=1
            ),

            nn.ReLU(),

            # 32×14×14 -> 32×7×7
            nn.MaxPool2d(2)
        )

        self.classifier = nn.Sequential(

            nn.Flatten(),

            nn.Linear(
                32 * 7 * 7,
                128
            ),

            nn.ReLU(),

            nn.Linear(
                128,
                10
            )
        )

    def forward(self, x):

        x = self.conv(x)

        x = self.classifier(x)

        return x


model = DigitCNN().to(device)

print(model)


# ============================================================
# 4. LOSS + OPTIMIZER
# ============================================================

loss_function = nn.CrossEntropyLoss()

optimizer = torch.optim.Adam(
    model.parameters(),
    lr=0.001
)


# ============================================================
# 5. НАВЧАННЯ
# ============================================================

epochs = 3

for epoch in range(epochs):

    model.train()

    total_loss = 0

    for images, labels in train_loader:

        images = images.to(device)
        labels = labels.to(device)

        # -------------------------
        # Forward
        # -------------------------

        predictions = model(images)

        loss = loss_function(
            predictions,
            labels
        )

        # -------------------------
        # Backpropagation
        # -------------------------

        optimizer.zero_grad()

        loss.backward()

        optimizer.step()

        total_loss += loss.item()

    print(
        f"Epoch {epoch + 1}/{epochs}, "
        f"Loss: {total_loss / len(train_loader):.4f}"
    )


# ============================================================
# 6. ПЕРЕВІРКА ТОЧНОСТІ
# ============================================================

model.eval()

correct = 0
total = 0

with torch.no_grad():

    for images, labels in test_loader:

        images = images.to(device)
        labels = labels.to(device)

        outputs = model(images)

        predicted = outputs.argmax(dim=1)

        correct += (
            predicted == labels
        ).sum().item()

        total += labels.size(0)


accuracy = correct / total * 100

print()
print(f"Accuracy: {accuracy:.2f}%")


# ============================================================
# 7. ЗБЕРІГАЄМО МОДЕЛЬ
# ============================================================

torch.save(
    model.state_dict(),
    "mnist_cnn.pth"
)

print("Model saved: mnist_cnn.pth")


# ============================================================
# 8. ЗНАХОДИМО ПО ОДНІЙ КАРТИНЦІ КОЖНОЇ ЦИФРИ
# ============================================================

found = {}

for image, label in test_dataset:

    number = label

    if number not in found:

        found[number] = image

    if len(found) == 10:
        break


# ============================================================
# 9. РОЗПІЗНАЄМО І ЗБЕРІГАЄМО 10 КАРТИНОК
# ============================================================

model.eval()

print()
print("=" * 40)
print("РОЗПІЗНАВАННЯ")
print("=" * 40)

for real_number in range(10):

    image = found[real_number]

    # -------------------------
    # Зберігаємо PNG
    # -------------------------

    pil_image = transforms.ToPILImage()(image)

    filename = f"digit_{real_number}.png"

    pil_image.save(filename)

    # -------------------------
    # Передаємо CNN
    # -------------------------

    input_tensor = image.unsqueeze(0).to(device)

    with torch.no_grad():

        output = model(input_tensor)

        probabilities = torch.softmax(
            output,
            dim=1
        )

        predicted_number = probabilities.argmax(
            dim=1
        ).item()

        confidence = probabilities[
            0,
            predicted_number
        ].item() * 100

    print(
        f"{filename}: "
        f"справжня цифра = {real_number}, "
        f"CNN = {predicted_number}, "
        f"впевненість = {confidence:.2f}%"
    )
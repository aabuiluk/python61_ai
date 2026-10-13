from pathlib import Path
import numpy as np

ROOT = Path("assets/digits")
blob = np.load(ROOT / "digits_train.npz")
images, labels = blob["images"], blob["labels"]
print("ключі", list(blob.keys()))
print("images", images.shape, images.dtype)
print("labels", labels.shape, labels.dtype)

i = 12  # змініть: 0 .. len(labels)-1
print("елемент", i, "→ мітка", int(labels[i]))

try:
    import matplotlib.pyplot as plt
    plt.imshow(images[i], cmap="gray", vmin=0, vmax=255)
    plt.title(f"digits_train[{i}] = {int(labels[i])}")
    plt.axis("off")
    plt.show()
except ImportError:
    chars = " .:-=+*#%@"
    for row in images[i][::2, ::2]:
        print("".join(chars[min(9, int(p) * 10 // 256)] for p in row))
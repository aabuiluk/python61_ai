from pathlib import Path
import numpy as np
from PIL import Image

ROOT = Path("assets/digits")
OUT = ROOT / "from_npz"
OUT.mkdir(parents=True, exist_ok=True)

name = "test"
data_source = f"digits_{name}.npz"

blob = np.load(ROOT / data_source)
images, labels = blob["images"], blob["labels"]  # images: (N,28,28) uint8

# один кадр → один PNG
i = 42
Image.fromarray(images[i], mode="L").save(OUT / f"{name}_{i}_label{int(labels[i])}.png")
print("saved", OUT / f"{name}_{i}_label{int(labels[i])}.png")

# усі кадри з npz у PNG
for i, (img, lab) in enumerate(zip(images, labels)):
    Image.fromarray(img, mode="L").save(OUT / f"{name}_{i:04d}_label{int(lab)}.png")

print("done", len(labels), "png →", OUT.resolve())
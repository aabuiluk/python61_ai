"""Пара 18 · складніше: каркас зведеної таблиці."""

print(f"{'config':<22} {'MAE':>8} {'R2':>8}")
for name in ("ReLU", "ReLU+Dropout", "ReLU+BN", "all"):
    print(f"{name:<22} {'...':>8} {'...':>8}")

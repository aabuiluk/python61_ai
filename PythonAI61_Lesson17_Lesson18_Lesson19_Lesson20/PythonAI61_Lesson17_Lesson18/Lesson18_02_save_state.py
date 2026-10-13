"""Пара 18 · середнє: зберегти й прочитати state_dict."""

from pathlib import Path
import torch
from torch import nn

model = nn.Linear(4, 1)
path = Path(__file__).with_name("demo.pt")
torch.save(model.state_dict(), path)
model.load_state_dict(torch.load(path, weights_only=True))
print("ok", path.name)

import torch
from torch import nn

torch.manual_seed(42)
batch, seq_len, features, hidden = 2, 4, 8, 16
x = torch.randn(batch, seq_len, features)
rnn = nn.RNN(input_size=features, hidden_size=hidden, batch_first=True)
output, h_n = rnn(x)
print("x:", x.shape)           # [2, 4, 8]
print("output:", output.shape) # [2, 4, 16]
print("h_n:", h_n.shape)       # [1, 2, 16]
import torch
from DataInput import *
from Parameter import *
import torch.utils.data as Data
from torch import nn

# Mice Model
class Mice(nn.Module):
    def __init__(self):
        super(Mice, self).__init__()

        self.rnn = nn.LSTM(         
            input_size = INPUT_SIZE,
            hidden_size = UNIT_MICE,         
            num_layers = LAYER_MICE,           
            batch_first = True,       
        )

        self.out = nn.Linear(UNIT_MICE, 2)

    def forward(self, x):
        r_out, (h_n, h_c) = self.rnn(x, None)   
        out = self.out(r_out[:, -1, :])
        return out


import torch
from DataInput import *
from Parameter import *
import torch.utils.data as Data
from torch import nn
# Regress Model
class Regress(nn.Module):
    def __init__(self):
        super(Regress, self).__init__()

        self.rnn = nn.LSTM(         
            input_size = INPUT_SIZE,
            hidden_size = UNIT_REGRESS,        
            num_layers = LAYER_REGRESS,          
            batch_first = True,
        )

        self.out = nn.Linear(UNIT_REGRESS, 1)

    def forward(self, x):
        r_out, (h_n, h_c) = self.rnn(x, None)  
        out = self.out(r_out[:, -1, :]).view(-1)
        return out

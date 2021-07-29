import torch
import torch.nn.functional as F 
from DataInput import *
from Parameter import *
import torch.utils.data as Data
from torch import nn
class Net(torch.nn.Module):     
    def __init__(self, n_feature, n_hidden, n_output):
        super(Net, self).__init__()     
        self.hidden = torch.nn.Linear(n_feature, n_hidden)   
        # self.hidden1 = torch.nn.Linear(n_hidden, n_hidden)
        self.out = torch.nn.Linear(n_hidden, n_output)       

    def forward(self, x):
        # 正向传播输入值, 神经网络分析出输出值
        x = F.relu(self.hidden(x))      
        # x = F.relu(self.hidden1(x))
        x = self.out(x[:, -1, :])      
        return x
import torch
from DataInput import *
from Parameter import *
import torch.utils.data as Data
from torch import nn
from Error_Model import *
from Common import *

# model load
emodel = torch.load('emodel_sp'+ str(sp_para)+ '.pkl')
print(emodel)
# data input
(x, acc, query, is_mice) = emodel_test_input()

# mice test
for epoch in range(test_ep):
    batch_x = torch.tensor(x[epoch]).view(-1,TIME_STEP,1)
    output = emodel(batch_x)
    pred_y = output.data.numpy().tolist()
    print(pred_y[:10])
    print(query[epoch][:10])
    #(emodel_precision, normal_precision) = get_emodel_precision(acc[epoch], query[epoch], pred_y, is_mice[epoch])
    #print(emodel_precision, normal_precision)

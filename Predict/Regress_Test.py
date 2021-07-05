import torch
from DataInput import *
from Parameter import *
import torch.utils.data as Data
from torch import nn
from Mice_Model import *
from Regress_Model import *
from Common import *

# model load
regress = torch.load('regress_sp'+ str(sp_para)+ '.pkl')
# data input
(x, acc, query, is_mice) = regress_test_input()

# mice test
with open("../data/predict/regress_test_sp"+str(sp_para)+".txt", 'w')as f:
    for epoch in range(test_ep):
        batch_x = torch.tensor(x[epoch]).view(-1,TIME_STEP,1)
        output = regress(batch_x)
        pred_y = output.data.numpy().tolist()
        (regress_precision, normal_precision) = get_regress_precision_predict(acc[epoch], query[epoch], pred_y, is_mice[epoch])
        print(regress_precision, normal_precision)
        f.write(str(regress_precision)+' '+str(normal_precision)+'\n')

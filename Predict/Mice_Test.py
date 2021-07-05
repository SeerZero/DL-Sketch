import torch
from DataInput import *
from Parameter import *
import torch.utils.data as Data
from torch import nn
from Common import *
from Mice_Model import *
sk_name = ["cmsk", "cusk", "psk"]
# model load
mice_t = torch.load('mice_sp'+str(sp_para) + '.pkl')
# data input
(x,y) = mice_test_input()
# test
with open('../data/predict/'+str(sp_para)+".txt","w")as f:
    for epoch in range(test_ep):
        output = mice_t(x[epoch])
        pred_y = torch.max(output, 1)[1].data.numpy().tolist()
        (acc, precision, recall, tp, fp, tn, fn) = get_mice_precision(y[epoch], pred_y)
        print("epoch",epoch,"|acc %.4f" % acc,"|precision %.4f" % precision,"|recall %.4f" % recall,"|tp:" ,tp, "|fp:",fp, "|tn:", tn, "|fn:", fn)
        f.write(str(acc)+' '+str(precision)+' '+str(recall)+'\n')

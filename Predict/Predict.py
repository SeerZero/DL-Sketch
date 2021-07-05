import torch
from DataInput import *
from Parameter import *
import torch.utils.data as Data
from torch import nn
from Mice_Model import *
from Regress_Model import *
from Common import *

regress = torch.load('regress_sp'+ str(sp_para)+ '.pkl')
mice = torch.load('mice_sp'+str(sp_para) + '.pkl')
print("sampling_para:",sp_para)
(x, y, query, back, is_mice) = predict_input()

with open("../data/predict/predict_test_mice_sp"+str(sp_para)+".txt", 'w')as f:
    for i in range(TestEpoch):
        test_x = x[i]
        test_y = y[i]
        test_query = query[i]
        test_back = back[i]
        test_is_mice = is_mice[i]

        tensorx = torch.tensor(test_x).float().view(-1, TIME_STEP, 1)
        output = mice(tensorx)
        pred_is_mice = torch.max(output, 1)[1].data.numpy().tolist()
        (acc, precision, recall, tp, fp, tn, fn) = get_mice_precision(test_is_mice, pred_is_mice)
        
        pred_y = []
        p_x = []
        p_y = []
        p_is_mice = []
        p_query = []
        p_back = []
        for k in range(len(test_x)):
            if pred_is_mice[k] == 1:
                p_is_mice.append(1)
                p_y.append(test_y[k])
                p_query.append(test_query[k])
                p_x.append(test_x[k])
                p_back.append(test_back[k])
                
        tensorx = torch.tensor(p_x).view(-1, TIME_STEP, 1)
        output = regress(tensorx)
        pred_y =output.data.numpy().tolist()
        (regress_precision, normal_precision) = get_regress_precision_predict(p_y, p_query, pred_y, p_is_mice)
        print("mice_flow | normal: %.6f" % normal_precision," predict %.6f"% regress_precision)
        f.write(str(tp+fp)+' '+str(regress_precision)+' '+str(normal_precision)+'\n')

print()

(x, y, query, back, is_mice) = predict_input()
with open("../data/predict/predict_test_all_sp"+str(sp_para)+".txt", 'w')as f:
    for i in range(TestEpoch):
        test_x = x[i]
        test_y = y[i]
        test_query = query[i]
        test_back = back[i]
        test_is_mice = is_mice[i]

        tensorx = torch.tensor(test_x).float().view(-1, TIME_STEP, 1)
        output = mice(tensorx)
        pred_is_mice = torch.max(output, 1)[1].data.numpy().tolist()
        (acc, precision, recall, tp, fp, tn, fn) = get_mice_precision(test_is_mice, pred_is_mice)
        
        pred_y = []
        for k in range(len(test_x)):
            if pred_is_mice[k] == 1:
                tensorx = torch.tensor(test_x[k]).view(-1, TIME_STEP, 1)        
                output = regress(tensorx)
                pred_y.append(output.data.numpy().tolist()[0])
            else:
                pred_y.append(test_query[k]) 
        (regress_precision, normal_precision) = get_regress_precision_predict(test_y, test_query, pred_y, test_is_mice)
        print("all_flow | normal: %.6f" % normal_precision," predict %.6f"% regress_precision)
        f.write(str(regress_precision)+' '+str(normal_precision)+'\n')
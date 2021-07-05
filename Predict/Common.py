def get_regress_precision(sw_y, sw_query, pred_y, is_mice):
    regress_precision = 0
    normal_precision = 0
    cnt = 0
    for i in range(len(is_mice)):
        if is_mice[i] == 1:
            if pred_y[i] < 0:
                pred_y[i] = - pred_y[i]
            if sw_y[i] > pred_y[i]:
                t = (1 - (sw_y[i] - pred_y[i]) / sw_y[i])
                if t < 0:
                    regress_precision = regress_precision + (1 - (sw_y[i] - pred_y[i]) / sw_y[i])
            else:
                t = (1 - (pred_y[i] - sw_y[i]) / pred_y[i])
                if t < 0:
                    regress_precision = regress_precision + (1 - (pred_y[i] - sw_y[i]) / pred_y[i])
        else:
            if sw_y[i] > sw_query[i]:
                regress_precision = regress_precision + (1 - (sw_y[i] - sw_query[i]) / sw_y[i])
            else:
                regress_precision = regress_precision + (1 - (sw_query[i] - sw_y[i]) / sw_query[i])
        if sw_y[i] > sw_query[i]:
            normal_precision = normal_precision + (1 - (sw_y[i] - sw_query[i]) / sw_y[i])
        else:
            normal_precision = normal_precision + (1 - (sw_query[i] - sw_y[i]) / sw_query[i])
    regress_precision = regress_precision / len(is_mice)
    normal_precision = normal_precision / len(is_mice)
    return (regress_precision, normal_precision) 


def get_mice_precision(record_y, pre_y):
    tp = 0
    fn = 0
    tn = 0
    fp = 0
    for i in range(len(pre_y)): 
        if record_y[i] == 1:
            if pre_y[i] == 1:
                tp = tp + 1
            else:
                fn = fn + 1
        else:
            if pre_y[i] == 1:
                fp = fp + 1
            else:
                tn = tn + 1
    if tp + fp != 0:
        precision = tp / (tp + fp)
    else:
        precision = 1
    if tp + fn != 0:
        recall = tp / (tp + fn) 
    else:
        recall = 1
    acc = (tp + tn)/ len(pre_y)
    return (acc,precision, recall,tp,fp,tn,fn)

def get_regress_precision_predict(sw_y, sw_query, pred_y, is_mice):
    regress_precision = 0
    normal_precision = 0
    cnt = 0
    for i in range(len(is_mice)):
        rgp = 0
        if is_mice[i] == 1:
            if pred_y[i] < 0:
                pred_y[i] = - pred_y[i]
            if sw_y[i] > pred_y[i]:
                rgp = (1 - (sw_y[i] - pred_y[i]) / sw_y[i])
            else:
                rgp = (1 - (pred_y[i] - sw_y[i]) / pred_y[i])
        else:
            if sw_y[i] > sw_query[i]:
                rgp = (1 - (sw_y[i] - sw_query[i]) / sw_y[i])
            else:
                rgp = (1 - (sw_query[i] - sw_y[i]) / sw_query[i])
        nmp = 0
        if sw_y[i] > sw_query[i]:
            nmp =  (1 - (sw_y[i] - sw_query[i]) / sw_y[i])
        else:
            nmp = (1 - (sw_query[i] - sw_y[i]) / sw_query[i])
        if nmp > rgp:
            rgp = nmp
        normal_precision = normal_precision + nmp
        regress_precision = regress_precision + rgp
    regress_precision = regress_precision / len(is_mice)
    normal_precision = normal_precision / len(is_mice)
    return (regress_precision, normal_precision) 

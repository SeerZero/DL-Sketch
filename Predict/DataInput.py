from Parameter import *


# Read Sketch
def data_input(file_name, is_sampling):
    record_x = []
    record_y = []
    record_query = []
    record_back = []
    record_is_mice = []
    with open("../data/predict/mice_loss_sp" + str(sp_para) + "_mices.txt", 'w')as f1:
        with open(file_name, "r") as f:
            s = f.readlines()
            max = 0
            for line in s:
                line = list(map(float, line.strip().split()))
                for x in line:
                    if x > max:
                        max = x

            min_ratio = 1 / max
            left = 0.00025
            right = 1

            for line in s:
                line1 = line
                line = list(map(float, line.strip().split()))
                k = line
                for i in range(len(k)):
                    k[i] = k[i] / max
                    k[i] = left + (k[i] - min_ratio) / (1 - min_ratio) * (right - left)
                line = k
                if line[0] / line[1] <= Train_Precision:
                    record_is_mice.append(1)
                    f1.write(str(line1) + "\n")
                else:
                    record_is_mice.append(0)
                record_back.append(max)
                record_x.append(list(reversed(line[2:])))
                # print(record_x)
                # print('\n')
                record_y.append(line[0])
                record_query.append(line[1])
        # print(''record_is_mice)
        return (record_x, record_y, record_query, record_back, record_is_mice)


def mice_train_input():
    sk_name = ["cmsk", "cusk", "psk"]

    # training dataset
    x = []
    y = []
    test_x = []
    test_y = []
    for epoch in range(train_ep - 1):
        server_file_name = "../data/sketch/sp" + str(sp_para) + "_ep" + str(epoch) + "_" + sk_name[sk_type] + "_" + str(
            sk_r) + "_5.sketch"

        (input_x, _, _, _, input_y) = data_input(server_file_name, 1)
        x += input_x
        y += input_y
    min = 10 * BATCH_SIZE_MICE
    if len(x) - (len(x) % BATCH_SIZE_MICE) < min:
        min = len(x) - (len(x) % BATCH_SIZE_MICE)
    x = torch.tensor(x[:min]).float().view(-1, TIME_STEP, 1)
    y = torch.tensor(y[:min]).long().view(-1)

    # validation dataset
    # server_file_name = "../data/sketch/sp" + str(sp_para) + "_ep" + str(train_ep - 1) + "_" + sk_name[sk_type] + "_" + str(sk_r) + ".sketch"
    # server_file_name = "../data/sketch/sp1" + "_ep" + str(train_ep + 1) + "_" + sk_name[sk_type] + "_" + str(sk_r) + ".sketch"
    for epoch in range(1):
        server_file_name = "../data/sketch/sp" + str(sp_para) + "_ep" + str(epoch + 3) + "_" + sk_name[
            sk_type] + "_" + str(sk_r) + "_5.sketch"

        (test_x0, _, _, _, test_y0) = data_input(server_file_name, 0)
        test_x += test_x0
        test_y += test_y0
    min = BATCH_SIZE_MICE
    if min > len(test_x):
        min = len(test_x)
    test_x = torch.tensor(test_x[:min]).float().view(-1, TIME_STEP, 1)
    test_y = torch.tensor(test_y[:min]).long().view(-1)

    return x, y, test_x, test_y


def mice_test_input():
    sk_name = ["cmsk", "cusk", "psk"]

    # Test dataset
    x = []
    y = []
    for epoch in range(TestEpoch):
        server_file_name = "../data/sketch/sp1" + "_ep" + str(epoch) + "_" + sk_name[sk_type] + "_" + str(
            sk_r) + ".sketch"
        (input_x, _, _, _, input_y) = data_input(server_file_name, 0)
        x.append(torch.tensor(input_x).float().view(-1, TIME_STEP, 1))
        y.append(input_y)
    return x, y


def regress_train_input():
    sk_name = ["cmsk", "cusk", "psk"]

    # training dataset
    x = []
    y = []
    test_x = []
    test_y = []
    for epoch in range(train_ep - 1):
        server_file_name = "../data/sketch/sp" + str(sp_para) + "_ep" + str(epoch) + "_" + sk_name[sk_type] + "_" + str(
            sk_r) + "_5.sketch"
        (input_x, input_y, _, _, _) = data_input(server_file_name, 1)
        x += input_x
        y += input_y
    x = torch.tensor(x[:len(x) - (len(x) % BATCH_SIZE_MICE)]).float().view(-1, TIME_STEP, 1)
    y = torch.tensor(y[:len(x) - (len(x) % BATCH_SIZE_MICE)]).float().view(-1)

    #  validation dataset
    # server_file_name = "../data/sketch/sp" + str(sp_para) + "_ep" + str(train_ep - 1) + "_"  + sk_name[sk_type] + "_" + str(sk_r) + ".sketch"
    for epoch in range(1):
        server_file_name = "../data/sketch/sp1" + "_ep" + str(epoch + 3) + "_" + sk_name[sk_type] + "_" + str(
            sk_r) + "_5.sketch"
        (test_x0, test_y0, _, _, _) = data_input(server_file_name, 0)
        test_x += test_x0
        test_y += test_y0
    test_x = torch.tensor(test_x).float().view(-1, TIME_STEP, 1)
    test_y = torch.tensor(test_y).float().view(-1)

    return x, y, test_x, test_y


def regress_test_input():
    sk_name = ["cmsk", "cusk", "psk"]

    # Test dataset
    x = []
    y = []
    is_mice = []
    query = []
    for epoch in range(TestEpoch):
        server_file_name = "../data/sketch/sp1" + "_ep" + str(epoch) + "_" + sk_name[sk_type] + "_" + str(
            sk_r) + ".sketch"
        (input_x, input_y, input_query, _, mice) = data_input(server_file_name, 0)
        test_x = []
        test_y = []
        test_mice = []
        test_input_query = []
        for i in range(len(mice)):
            if mice[i] == 1:
                test_x.append(input_x[i])
                test_y.append(input_y[i])
                test_mice.append(1)
                test_input_query.append(input_query[i])
        x.append(test_x)
        y.append(test_y)
        is_mice.append(test_mice)
        query.append(test_input_query)
    return x, y, query, is_mice


def predict_input():
    sk_name = ["cmsk", "cusk", "psk"]

    # Test dataset
    x = []
    y = []
    is_mice = []
    query = []
    back = []
    for epoch in range(TestEpoch):
        server_file_name = "../data/sketch/sp1" + "_ep" + str(epoch) + "_" + sk_name[sk_type] + "_" + str(
            sk_r) + ".sketch"
        (input_x, input_y, input_query, input_back, input_mice) = data_input(server_file_name, 0)
        x.append(input_x)
        y.append(input_y)
        is_mice.append(input_mice)
        query.append(input_query)
        back.append(input_back)
    return x, y, query, back, is_mice


def emodel_train_input():
    sk_name = ["cmsk", "cusk", "psk"]

    # training dataset
    x = []
    y = []
    for epoch in range(train_ep - 1):
        server_file_name = "../data/sketch/sp" + str(sp_para) + "_ep" + str(epoch) + "_" + sk_name[sk_type] + "_" + str(
            sk_r) + ".sketch"
        (input_x, input_y, _, _, _) = data_input(server_file_name, 1)
        x += input_x
        k = []
        for i, j in zip(input_x, input_y):
            k.append(j / i[0])
        y += k
    x = torch.tensor(x[:len(x) - (len(x) % BATCH_SIZE_MICE)]).float().view(-1, TIME_STEP, 1)
    y = torch.tensor(y[:len(x) - (len(x) % BATCH_SIZE_MICE)]).float().view(-1)

    # validation dataset
    # server_file_name = "../data/sketch/sp" + str(sp_para) + "_ep" + str(train_ep - 1) + "_"  + sk_name[sk_type] + "_" + str(sk_r) + ".sketch"
    server_file_name = "../data/sketch/sp1" + "_ep" + str(train_ep + 1) + "_" + sk_name[sk_type] + "_" + str(
        sk_r) + ".sketch"
    (test_x, test_y, _, _, _) = data_input(server_file_name, 0)
    k = []
    for i, j in zip(test_x, test_y):
        k.append(j / i[0])
    test_x = torch.tensor(test_x).float().view(-1, TIME_STEP, 1)
    test_y = torch.tensor(k).float().view(-1)

    return x, y, test_x, test_y


def emodel_test_input():
    sk_name = ["cmsk", "cusk", "psk"]

    # Test dataset
    x = []
    y = []
    is_mice = []
    query = []
    for epoch in range(TestEpoch):
        server_file_name = "../data/sketch/sp1" + "_ep" + str(epoch) + "_" + sk_name[sk_type] + "_" + str(
            sk_r) + ".sketch"
        (input_x, input_y, input_query, _, mice) = data_input(server_file_name, 0)
        k = []
        for i, j in zip(input_y, input_query):
            k.append(i / j)
        input_query = k

        test_x = []
        test_y = []
        test_mice = []
        test_input_query = []
        for i in range(len(mice)):
            if mice[i] == 1:
                test_x.append(input_x[i])
                test_y.append(input_y[i])
                test_mice.append(1)
                test_input_query.append(input_query[i])
        x.append(test_x)
        y.append(test_y)
        is_mice.append(test_mice)
        query.append(test_input_query)
    return x, y, query, is_mice
import torch
from DataInput import *
from Parameter import *
import torch.utils.data as Data
from torch import nn
from Mice_Model import *
from Mice_Model_L import *
(x, y, test_x, test_y) = mice_train_input()
torch_dataset = Data.TensorDataset(x, y)
net = Net(n_feature=INPUT_SIZE,n_hidden=100,n_output=2)
optimizer_mice = torch.optim.Adam(net.parameters(), lr = LR_MICE)
loss_func_mice = nn.CrossEntropyLoss()

min_test_loss = 1e10
end_train = 60000
min_count = 0
with open("../data/predict/mice_loss_sp"+str(sp_para)+".txt", 'w')as f:
    for epoch in range(EPOCH_MICE):
        output = net(x)
        print(output[:20])
        loss = loss_func_mice(output, y) 
        optimizer_mice.zero_grad()                         
        loss.backward()                                
        optimizer_mice.step()
        test_loss = loss_func_mice(net(test_x), test_y).data.numpy()
        pred_y = torch.max(output[:20], 1)[1].data.numpy().tolist() 
        print('prediction number',pred_y)
        print('real number', y[:20])
        # pred_y = torch.max(output[:20], 1)[1].data.numpy().tolist() 
        # print('prediction number',pred_y)
        # print('real number', y[:20])   
        if min_test_loss > test_loss:
            min_test_loss = test_loss
            torch.save(net, "mice_sp"+str(sp_para)+"_L.pkl")
        else:
            min_count = min_count + 1
            if min_count == end_train:
                exit(0)
        print('Epoch: ', epoch, '| train loss: %.6f' % loss.data.numpy(), '| test loss: %.6f' % test_loss)
        f.write(str(loss.data.numpy())+" "+ str(test_loss)+"\n")



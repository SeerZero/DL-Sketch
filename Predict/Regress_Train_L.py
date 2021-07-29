import torch
from DataInput import *
from Parameter import *
import torch.utils.data as Data
from torch import nn
from Regress_Model import *
from Regress_Model_L import *
# data_loader, input train data and test data
(x, y, test_x, test_y) = regress_train_input()
torch_dataset = Data.TensorDataset(x, y)
loader = Data.DataLoader(
    dataset = torch_dataset,
    batch_size = BATCH_SIZE_REGRESS,
    shuffle = True,
)

# Regress Parameter
regress = Regress()
net = Net(n_feature=INPUT_SIZE, n_hidden=100, n_output=1)
optimizer_regress = torch.optim.Adam(net.parameters(), lr = LR_REGRESS)
loss_func_regress = nn.L1Loss()


# Training
min_test_loss = 1e10
end_point = 15000
edp = 0
with open("../data/predict/regress_loss_sp"+str(sp_para)+".txt", 'w')as f:
    for epoch in range(EPOCH_REGRESS):
        for step, (batch_x, batch_y) in enumerate(loader):
            output = net(batch_x)
            loss = loss_func_regress(output, batch_y) 
            optimizer_regress.zero_grad()                         
            loss.backward()                                
            optimizer_regress.step()
            output2 = net(test_x)
            test_loss = loss_func_regress(output2, test_y).data.numpy()
            print('Epoch: ', epoch, 'Step:',step,'| train loss: %.10f' % loss.data.numpy(), '| test loss: %.10f' % test_loss)
            edp = edp+1
            if min_test_loss > test_loss:
                min_test_loss = test_loss
                torch.save(net, "regress_sp"+str(sp_para)+"_L1.pkl")
            else:
                if edp >= end_point:
                    exit(0)
            f.write(str(loss.data.numpy())+" "+ str(test_loss)+"\n")

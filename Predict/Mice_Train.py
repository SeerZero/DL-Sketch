import torch
from DataInput import *
from Parameter import *
import torch.utils.data as Data
from torch import nn
from Mice_Model import *

# data_loader, input train data and test data
(x, y, test_x, test_y) = mice_train_input()
torch_dataset = Data.TensorDataset(x, y)
loader = Data.DataLoader(
    dataset = torch_dataset,
    batch_size = BATCH_SIZE_MICE,
    shuffle = True,
)

# Mice Parameter
mice = Mice()
optimizer_mice = torch.optim.Adam(mice.parameters(), lr = LR_MICE)
loss_func_mice = nn.CrossEntropyLoss()


# Training
min_test_loss = 1e10
end_train = 6000
min_count = 0
with open("../data/predict/mice_loss_sp"+str(sp_para)+".txt", 'w')as f:
    for epoch in range(EPOCH_MICE):
        for step, (batch_x, batch_y) in enumerate(loader):
            output = mice(x)
            loss = loss_func_mice(output, y) 
            optimizer_mice.zero_grad()                         
            loss.backward()                                
            optimizer_mice.step()
            test_loss = loss_func_mice(mice(test_x), test_y).data.numpy()
                
            if min_test_loss > test_loss:
                min_test_loss = test_loss
                torch.save(mice, "mice_sp"+str(sp_para)+".pkl")
            else:
                min_count = min_count + 1
                if min_count == end_train:
                    exit(0)
            print('Epoch: ', epoch, 'Step:',step,'| train loss: %.6f' % loss.data.numpy(), '| test loss: %.6f' % test_loss)
            f.write(str(loss.data.numpy())+" "+ str(test_loss)+"\n")



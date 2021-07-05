import torch
from DataInput import *
from Parameter import *
import torch.utils.data as Data
from torch import nn
from Error_Model import *

# data_loader, input train data and test data
(x, y, test_x, test_y) = emodel_train_input()
torch_dataset = Data.TensorDataset(x, y)
loader = Data.DataLoader(
    dataset = torch_dataset,
    batch_size = BATCH_SIZE_REGRESS,
    shuffle = True,
)

# Regress Parameter
emodel = EModel()
optimizer_emodel = torch.optim.Adam(emodel.parameters(), lr = LR_REGRESS)
loss_func_emodel = nn.L1Loss()


# Training
min_test_loss = 1e10
end_point = 3000
edp = 0
for epoch in range(EPOCH_REGRESS):
    for step, (batch_x, batch_y) in enumerate(loader):
        output = emodel(batch_x)
        loss = loss_func_emodel(output, batch_y) 
        optimizer_emodel.zero_grad()                         
        loss.backward()                                
        optimizer_emodel.step()
        output2 = emodel(test_x)
        test_loss = loss_func_emodel(output2, test_y).data.numpy()
        print('Epoch: ', epoch, 'Step:',step,'| train loss: %.10f' % loss.data.numpy(), '| test loss: %.10f' % test_loss)
        if min_test_loss > test_loss:
            min_test_loss = test_loss
            edp = 0
            torch.save(emodel, "emodel_sp"+str(sp_para)+".pkl")
        else:
            edp = edp + 1
            if edp >= end_point:
                exit(0)

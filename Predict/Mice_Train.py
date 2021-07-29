import torch
from DataInput import *
from Parameter import *
import torch.utils.data as Data
from torch import nn
from Mice_Model import *

# data_loader, input train data and test data
(x, y, test_x, test_y) = mice_train_input()
torch_dataset = Data.TensorDataset(x, y)
# loader = Data.DataLoader(
#     dataset = torch_dataset,
#     batch_size = BATCH_SIZE_MICE,
#     shuffle = True,
# )

# Mice Parameter
mice = Mice()
optimizer_mice = torch.optim.Adam(mice.parameters(), lr = LR_MICE)
loss_func_mice = nn.CrossEntropyLoss()


# Training
min_test_loss = 1e10
end_train = 60000
min_count = 0
with open("../data/predict/mice_loss_sp"+str(sp_para)+".txt", 'w')as f:
    for epoch in range(EPOCH_MICE):
        # loader = torch_dataset[(epoch-1)*5000:epoch*5000]
        # print(loader)
        # for step, (batch_x, batch_y) in enumerate(loader):
            # print(batch_x)
        #print(mice(batch_x))
            # print(batch_y)
        output = mice(x)
        print(output[:20])
        loss = loss_func_mice(output, y)
        optimizer_mice.zero_grad()
        loss.backward()
        optimizer_mice.step()
        # print(test_x)
        # print(mice(test_x))
        # print(test_y)
        test_loss = loss_func_mice(mice(test_x), test_y).data.numpy()
        pred_y = torch.max(output[:20], 1)[1].data.numpy().tolist()
        print('prediction number',pred_y)
        print('real number', y[:20])
        if min_test_loss > test_loss:
            min_test_loss = test_loss
            torch.save(mice, "mice_sp"+str(sp_para)+".pkl")
        else:
            min_count = min_count + 1
            if min_count == end_train:
                exit(0)
        print('Epoch: ', epoch, '| train loss: %.6f' % loss.data.numpy(), '| test loss: %.6f' % test_loss)
        f.write(str(loss.data.numpy())+" "+ str(test_loss)+"\n")



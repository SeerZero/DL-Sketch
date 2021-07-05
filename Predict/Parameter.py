import torch


# Sketch Parameter
sk_type = 2             # 0 cmsketch 1 cusketch 2 psketch
sk_r = 3                # sketch row
sk_c = 40000            # sketch column
max_epoch = 10          # max emperiment epoch 
sp_para = 10             # sampling parameter

TestEpoch = 100

# Train Parameter
Minimum_Precision = 0.9 # train data filter precision < Minimum_precision
Train_Precision = 0.9
train_ep = 10           # end epoch for train if alltime = 0

# Train Parameter
Train_Precision = 0.9  # train data filter precision < Minimum_precision
train_ep = 8           # end epoch for train if alltime = 0

# Test Parameter
Test_Precision = 0.9     # train data filter precision < Minimum_precision
test_ep = 100             # end epoch for train if alltime = 0


# Hyper Parameters
torch.manual_seed(1)    # reproducible
TIME_STEP = sk_r         
INPUT_SIZE = 1        

# Mice Hyper Parameters
EPOCH_MICE = 30000        
BATCH_SIZE_MICE = 5000
LR_MICE = 0.0003
UNIT_MICE = 5
LAYER_MICE = 1

# Regress Hyper Parameters
EPOCH_REGRESS = 10000        
BATCH_SIZE_REGRESS = 5000        
LR_REGRESS = 0.00003
UNIT_REGRESS = 30
LAYER_REGRESS = 1
import torch.nn as nn
import torch


use_cuda = torch.cuda.is_available()
device = torch.device("cuda:0" if use_cuda else "cpu")
Tensor = torch.cuda.FloatTensor if use_cuda else torch.FloatTensor


class Net(nn.Module):
    def __init__(self, nZones):
        super(Net, self).__init__()

        self.model = nn.Sequential(
            nn.Linear((nZones * nZones), 512),
            nn.ReLU(),

            nn.Linear(512, 128),
            nn.ReLU(),

            nn.Linear(128, 1)
        )

    def forward(self, x):
        return self.model(x).view(-1)

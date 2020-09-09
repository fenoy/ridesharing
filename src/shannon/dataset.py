import torch
from torch.utils import data
import json


class RidesharingDataset(data.Dataset):
    def __init__(self, reqPath, setSize):
        self.setSize = setSize
        with open(reqPath, "r") as f:
            self.req = [torch.Tensor(r) for r in json.load(f)]

    def __len__(self):
        return len(self.req)

    def __getitem__(self, item):
        return self.req[item].repeat(self.setSize, 1, 1)

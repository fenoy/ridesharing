import torch
from torch.utils import data
import json

class RidesharingDataset(data.Dataset):
    def __init__(self, candidatesPath, nZones):
        with open(candidatesPath, "r") as f:
            candidates = json.load(f)

        self.coalitions = [
            {
                'coalition': torch.sum(torch.Tensor([[
                    1 if int(a) == i else 0
                    for i in range(nZones * nZones)
                ] for a in c['coalition']]), dim=0),
                'value': float(c['value'])
            } for c in candidates
        ]

    def __len__(self):
        return len(self.coalitions)

    def __getitem__(self, item):
        return self.coalitions[item]


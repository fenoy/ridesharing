import matplotlib
matplotlib.use('Agg')


### PARAMETERS ###

params = {
    'candidatesTrainPath': '../../data/cache/coalitions/regression_train.json',
    'candidatesTestPath': '../../data/cache/coalitions/regression_test.json',
    'fakeReqPath': '../../data/cache/req/fakeFile.csv',
    'outputPath': '../../data/cache/gan/regressor.pth',
    'batchSize': 64,
    'nZones': 63,
    'lr': 0.0001,
    'betas': (0.9, 0.999),
    'nEpochs': 100
}


### TORCH ###

import torch


use_cuda = torch.cuda.is_available()
device = torch.device("cuda:0" if use_cuda else "cpu")
Tensor = torch.cuda.FloatTensor if use_cuda else torch.FloatTensor

print("Using GPU:" + str(use_cuda))


### VISDOM ###

from visdom import Visdom

viz = Visdom(port=8097)
viz.close()

optsLossTrain = {
    'title': 'Loss Train',
    'xlabel': 'Epoch',
    'width': 800,
    'height': 400,
}

winLossTrain = viz.line(
    Y=Tensor([0]),
    X=Tensor([0]),
    opts=optsLossTrain
)

optsLossTest = {
    'title': 'Loss Test',
    'xlabel': 'Epoch',
    'width': 800,
    'height': 400,
}

winLossTest = viz.line(
    Y=Tensor([0]),
    X=Tensor([0]),
    opts=optsLossTest
)

### LOAD DATA ###

from torch.utils import data
from dataset import RidesharingDataset


dataset = {
    'train': RidesharingDataset(params['candidatesTrainPath'], params['nZones']),
    'test': RidesharingDataset(params['candidatesTestPath'], params['nZones'])
}

loader = {x: data.DataLoader(dataset[x], params['batchSize'], shuffle=True, num_workers=4) for x in ['train', 'test']}


### CREATE GAN ###

from model import Net


net = Net(params['nZones']).to(device)
loss_func = torch.nn.MSELoss()
optimizer = torch.optim.Adam(net.parameters(), params['lr'], params['betas'])


### TRAIN THE GAN ###

history = []
for epoch in range(params['nEpochs']):
    cumLossTrain = 0
    for i, data in enumerate(loader['train']):
        net.train()

        coalition, value = data['coalition'].to(device), data['value'].float().to(device)
        prediction = net(coalition)

        loss = loss_func(prediction, value)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        cumLossTrain += loss.item()
        print("[Epoch {0}/{1}] [Batch {2}/{3}] [Loss: {4}]".format(
            epoch, params['nEpochs'], i, len(loader['train']), loss.item()
        ))

    cumLossTest = 0
    for i, data in enumerate(loader['test']):
        net.eval()

        coalition, value = data['coalition'].to(device), data['value'].float().to(device)
        prediction = net(coalition)
        loss = loss_func(prediction, value)

        cumLossTest += loss.item()

    history += [
        {
            'lossTrain': cumLossTrain / len(loader['train']),
            'lossTest': cumLossTest / len(loader['test'])
        }
    ]

    viz.line(
        Y=Tensor([history[i]['lossTrain'] for i in range(epoch + 1)]),
        X=Tensor([i for i in range(epoch + 1)]),
        win=winLossTrain,
        update='replace'
    )

    viz.line(
        Y=Tensor([history[i]['lossTest'] for i in range(epoch + 1)]),
        X=Tensor([i for i in range(epoch + 1)]),
        win=winLossTest,
        update='replace'
    )

torch.save(net.state_dict(), params['outputPath'])

### GRAPH ###

import matplotlib.pyplot as plt

values, predictions = [], []
for i, data in enumerate(loader['test']):
    net.eval()

    coalition, value = data['coalition'].to(device), data['value'].float().to(device)
    prediction = net(coalition)
    for v, p in zip(value, prediction):
        values.append(v.item())
        predictions.append(p.item())

real_values = []
for i, data in enumerate(loader['train']):
    value = data['value'].float().to(device)
    for v in value:
        real_values.append(v.item())

mean = sum(real_values) / len(real_values)
mse = sum((v - p)**2 for v, p in zip(values, predictions)) / len(values)
dumb_mse = sum((v - mean)**2 for v in values) / len(values)

plt.scatter(values, predictions, s=0.25)
plt.title('NEURAL NETWORK REGRESSION (PYTORCH)')
plt.xlim([-5, 0.5])
plt.ylim([-5, 0.5])
plt.xlabel('Value')
plt.ylabel('Prediction')
plt.text(-1.5, 0, 'MODEL MSE: ' + str(mse)[:5])
plt.text(-1.5, -0.5,   'MEAN MSE:   ' + str(dumb_mse)[:5])
plt.savefig('../../data/output/plot.png')

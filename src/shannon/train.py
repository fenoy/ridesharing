### PARAMETERS ###

params = {
    'requestsPath': '../../data/cache/req/trips_20161201_modified.json',
    'outputPath': '../../data/cache/gan/generator.pth',
    'fakeReqPath': '../../data/cache/req/fakeFile.csv',
    'oraclePath': '../../src/oracle/',
    'regressorPath': '../../data/cache/gan/regressor.pth',
    'nZones': 63,                   # Number of zones of the problem (Cannot be modified)
    'setSize': 64,                  # Number of elements in the output set of coalitions
    'latentSize': 100,              # Size of the latent vector
    'lr': 0.0001,                   # Learning rate for Adam optimizer
    'betas': (0.5, 0.999),          # Beta parameters for the Adam optimizer
    't0': 0.9,                      # Starting temperature for the Gumble Softmax
    'nEpochs': 500,                 # Number of epochs for training
    'tInf': 0.1                     # Limit of convergence for the tempeerature for the Gumble Softmax
}


### TORCH ###

import torch


use_cuda = torch.cuda.is_available()
device = torch.device("cuda:0" if use_cuda else "cpu")
Tensor = torch.cuda.FloatTensor if use_cuda else torch.FloatTensor

print("Using GPU:" + str(use_cuda))


### LOAD DATA ###

from torch.utils import data
from dataset import RidesharingDataset


dataset = {
    'train': RidesharingDataset(params['requestsPath'], params['setSize']),
    'test': RidesharingDataset(params['requestsPath'], params['setSize'])
}

loader = {x: data.DataLoader(dataset[x], None, num_workers=4) for x in ['train', 'test']}


### CREATE MODEL ###

from model import Generator, Regressor


netG = Generator(params['latentSize'], params['nZones']).to(device)
netR = Regressor(params['nZones']).to(device)
netR.load_state_dict(torch.load(params['regressorPath']))

optimizerG = torch.optim.Adam(netG.parameters(), params['lr'], params['betas'])
optimizerR = torch.optim.Adam(netR.parameters(), params['lr'], params['betas'])

regression_loss = torch.nn.MSELoss()

### DEFINE LOSSES ###

import math


def computeShannonEntropy(x_fake):
    '''
    b, m, _ = x_fake.size()
    n = params['nZones']
    x = x_fake[:, :, 1:].view(b, m, n, n).sum(dim=1)
    reqPen = torch.relu(x - req).sum(dim=(1, 2)) ** 2
    valid = (reqPen == 0).bool()
    '''

    setO = x_fake[:, :, 1:].sum(dim=1)
    setF = setO#[valid]
    setX, inverse_indices = torch.unique(
        setF,
        return_inverse=True,
        dim=0
    )

    H = torch.Tensor([0]).to(device)
    for i, x in enumerate(setX):
        pi = sum(
            torch.mean(1 - (x.detach() - o) ** 2)
            for o in setF[inverse_indices == i]
        ) / setO.size(0)
        H += - pi * torch.log2(pi) / math.log2(setO.size(0))

    return H

def computeImprovedShannonEntropy(x_fake):
    '''
    b, m, _ = x_fake.size()
    n = params['nZones']
    x = x_fake[:, :, 1:].view(b, m, n, n).sum(dim=1)
    reqPen = torch.relu(x - req).sum(dim=(1, 2)) ** 2
    valid = (reqPen == 0).bool()
    '''

    setO = x_fake[:, :, 1:].sum(dim=1)
    setF = setO#[valid]
    setX = torch.unique(setF, dim=0)

    H = torch.Tensor([0]).to(device)
    for i, x in enumerate(setX):
        pi = sum(
            torch.prod(1 - (x.detach() - o) ** 2)
            for o in setF
        ) / setO.size(0)
        H += - pi * torch.log2(pi) / math.log2(setO.size(0))

    return H

def computeCollapse(x_fake, z):
    C = torch.Tensor([0]).to(device)
    for i, (g1, z1) in enumerate(zip(x_fake[:-1], z[:-1])):
        for g2, z2 in zip(x_fake[i+1:], z[i+1:]):
            C += torch.sum(torch.abs(g2 - g1)) / max(0.1, torch.sum(torch.abs(z2 - z1)))
    return C


def computeQuality(x_fake):
    coalition = x_fake.sum(dim=1)[:, 1:]
    return netR(coalition)

def computeValidPenalty(x_fake, req):
    b, m, _ = x_fake.size()
    n = params['nZones']
    x = x_fake[:, :, 1:].view(b, m, n, n).sum(dim=1)

    # Req coherence
    reqPen = torch.relu(x - req).sum(dim=(1, 2)) ** 2

    return (
        reqPen.mean(),
        (reqPen == 0).float().mean()
    )


### VALUE ###

import subprocess


def value(x_fake):
    b, n, _ = x_fake.size()
    z = params['nZones']
    agents = x_fake[:, :, 0].view(b, n).bool()
    coalition = x_fake[:, :, 1:].view(b, n, z, z)

    v = []
    for a, c in zip(agents, coalition):
        c_reduced = c[~a, :, :]
        c_trip = c_reduced.sum(dim=2).argmax(dim=1) * params['nZones'] + c_reduced.sum(dim=1).argmax(dim=1)
        val = subprocess.run(
            ['./oracle'] +
            [params['fakeReqPath']] +
            [str(a.item()) for a in c_trip],
            stdout=subprocess.PIPE,
            cwd=params['oraclePath']
        ).stdout.decode('utf-8').strip('\n')
        v.append(float(val))
    return Tensor(v)


### TRAIN THE MODEL ###

with open("./train.txt", "a") as f:
    f.write('loss,entropy,quality,value,validity\n')

history = []
t = params['t0']
for epoch in range(params['nEpochs']):
    if epoch % 10 == 9: t *= 0.9
    for i, data in enumerate(loader['train']):
        netG.train()
        netR.train()
        req = data.to(device)

        z = torch.randn(req.size(0), params['latentSize'], device=device)
        x_fake = netG(z, req, t=t + params['tInf'])

        entropy = computeShannonEntropy(x_fake)
        quality = computeQuality(x_fake)
        validPenalty, reqPercentage = computeValidPenalty(x_fake, req)
        lossG = - torch.mean(quality) - entropy + validPenalty

        lossG.backward()
        if i % 16 == 15:
            optimizerG.step()
            optimizerG.zero_grad()

        x_fake = netG(z, req, t=t + params['tInf'])
        quality = computeQuality(x_fake.detach())
        val = value(x_fake.detach())
        lossR = regression_loss(quality, val)
        lossR.backward()
        optimizerR.step()
        optimizerR.zero_grad()

        print("[Epoch {0}/{1}] [Batch {2}/{3}] [G loss: {4}] [% Entropy: {5}] [% Quality: {6}] [% Validity: {7}]".format(
            epoch, params['nEpochs'], i, len(loader['train']), lossG.item(), entropy.item(), torch.mean(quality).item(), reqPercentage.item()
        ))


### EVALUATION ###

    cumLoss, cumEntropy, cumQuality, cumReqPercentage, cumValue = 0, 0, 0, 0, 0
    for i, data in enumerate(loader['test']):
        netG.eval()
        netR.eval()
        req = data.to(device)

        z = torch.randn(req.size(0), params['latentSize'], device=device)
        x_fake = netG(z, req, t=t + params['tInf'])

        entropy = computeShannonEntropy(x_fake)
        quality = computeQuality(x_fake)
        validPenalty, reqPercentage = computeValidPenalty(x_fake, req)
        lossG = - torch.mean(quality) - entropy + validPenalty
        val = value(x_fake.detach())

        cumValue += val.mean().item()
        cumLoss += lossG.item()
        cumReqPercentage += reqPercentage.item()
        cumQuality += torch.mean(quality).item()
        cumEntropy += entropy.item()

        print("[Epoch {0}/{1}] [Batch {2}/{3}] [G loss: {4}] [% Entropy: {5}] [% Quality: {6}] [% Validity: {7}]".format(
            epoch, params['nEpochs'], i, len(loader['train']), lossG.item(), entropy.item(), torch.mean(quality).item(), reqPercentage.item()
        ))

### WRITE RESULTS ###

    torch.save(netG.state_dict(), params['outputPath'])
    history += [
        {
            'loss': cumLoss / len(loader['test']),
            'entropy': cumEntropy / len(loader['test']),
            'quality': cumQuality / len(loader['test']),
            'value': cumValue / len(loader['test']),
            'reqPercentage': cumReqPercentage / len(loader['test'])
        }
    ]

    with open("./train.txt", "a") as f:
        f.write(
            str(cumLoss / len(loader['test'])) + ',' +
            str(cumEntropy / len(loader['test'])) + ',' +
            str(cumQuality / len(loader['test'])) + ',' +
            str(cumValue / len(loader['test'])) + ',' +
            str(cumReqPercentage / len(loader['test'])) + '\n'
        )

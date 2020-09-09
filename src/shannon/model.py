### PYTORCH ###
"""
Import useful PyTorch libraries.
Check availability of CUDA device and declare tensor object accordingly.

See PyTorch docs for more information:
    - https://pytorch.org/docs/stable/index.html
"""

import torch.nn as nn
import torch.nn.functional as F
import torch


use_cuda = torch.cuda.is_available()
device = torch.device("cuda:0" if use_cuda else "cpu")
Tensor = torch.cuda.FloatTensor if use_cuda else torch.FloatTensor


### GUMBEL SOFTMAX ###
"""
The next functions implement gumble softmax approximation.

Code was obtained from:
    - Repo: https://github.com/dev4488/VAE_gumble_softmax
    - File: vae_gumble_softmax.py
    - Line: 52-73
"""

def sample_gumbel(shape, eps=1e-20):
    U = torch.rand(shape, device=device)
    return -torch.log(-torch.log(U + eps) + eps)

def gumbel_softmax_sample(logits, temperature):
    y = F.log_softmax(logits, dim=-1) + sample_gumbel(logits.size())
    return F.softmax(y / temperature, dim=-1)

def gumbel_softmax(logits, temperature):
    y = gumbel_softmax_sample(logits, temperature)
    shape = y.size()
    _, ind = y.max(dim=-1)
    y_hard = torch.zeros_like(y).view(-1, shape[-1])
    y_hard.scatter_(1, ind.view(-1, 1), 1)
    y_hard = y_hard.view(*shape)
    return (y_hard - y).detach() + y


### GAN ###
"""
Implementation of a conditional GAN,
with fully connected layers,
and gumble-softmax output layer.

Generative Adversarial Network (GAN):
    Goodfellow, Ian, et al.
    "Generative adversarial nets."
    Advances in neural information processing systems.
    2014.

GAN, conditional GAN, and many other GAN implementations in PyTorch:
    - https://github.com/eriklindernoren/PyTorch-GAN
"""

class Generator(nn.Module):
    def __init__(self, latent_size, nZones):
        super(Generator, self).__init__()
        self.model = nn.Sequential(
            nn.Linear(latent_size + nZones * nZones, 512),
            nn.LeakyReLU(0.2, inplace=True),

            nn.Linear(512, 512),
            nn.LeakyReLU(0.2, inplace=True),

            nn.Linear(512, 512),
            nn.LeakyReLU(0.2, inplace=True),

            nn.Linear(512, 5 * nZones * nZones + 5)
        )

    def forward(self, z, req, t=1):
        b, s, _ = req.size()
        n = 5

        r = req.view(b, -1)
        input = torch.cat((z, r), dim=1)

        model = self.model(input).view(b, n, s * s + 1)
        return gumbel_softmax(model, t)


class Regressor(nn.Module):
    def __init__(self, nZones):
        super(Regressor, self).__init__()

        self.model = nn.Sequential(
            nn.Linear((nZones * nZones), 512),
            nn.ReLU(),

            nn.Linear(512, 128),
            nn.ReLU(),

            nn.Linear(128, 1)
        )

    def forward(self, x):
        return self.model(x).view(-1)

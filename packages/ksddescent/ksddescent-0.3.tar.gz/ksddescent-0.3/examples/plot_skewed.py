"""
==============================
Unbalanced mixture of Gaussian
==============================
"""  # noqa

# Author: Pierre Ablin <pierre.ablin@ens.fr>
#
# License: MIT

import torch
from ksddescent import ksdd_lbfgs
import matplotlib.pyplot as plt
import numpy as np


def make_mog(centers, vars, weights):
    weights = torch.tensor(weights)
    weights /= weights.sum()

    def score(x):
        den = 0
        top = 0
        for center, var, weight in zip(centers, vars, weights):
            exp = torch.exp(-0.5 * ((x - center) ** 2).sum(axis=1) / var)
            den += weight * exp
            top += weight * exp[:, None] * (x - center) / var
        return -top / den[:, None]

    def potential(x):
        op = 0.0
        for center, var, weight in zip(centers, vars, weights):
            exp = torch.exp(-0.5 * ((x - center) ** 2).sum(axis=1) / var)
            op += weight * exp
        return torch.log(op)

    def sampler(n_samples):
        x = []
        for c, v, w in zip(centers, vars, weights):
            z = torch.randn(int(n_samples * w), 2)
            z *= np.sqrt(v)
            z += c
            x.append(z.clone())
        return torch.cat(x)

    return score, potential, sampler


fac = 1
centers = [
    torch.tensor([-3, 0]),
    torch.tensor([3, 0.0]),
    torch.tensor([0.0, 3.0]),
]
# centers = [torch.tensor([0., 1.]), torch.tensor([0., -1])]
variances = [0.5, 0.3, 0.1]
weights = [0.5, 0.5, 0.5]
score, potential, sampler = make_mog(centers, variances, weights)

n_samples = 200
p = 2


x = 0.5 * torch.randn(n_samples, p)
bw = 0.1
x_ksd0, ksd_traj0, _ = ksdd_lbfgs(x.clone(), score, bw=bw, store=True)
labels = ["KSD", "KSD", "KSD"]
methods = ["init1", "init2", "init3"]
colors = ["blue", "blue", "blue"]
for x_final, x_init, label, color, method in zip(
    [
        x_ksd0,
    ],
    [
        x,
    ],
    labels,
    colors,
    methods,
):
    plt.figure(figsize=(3, 2))
    # plt.plot(traj[:, :, 0], traj[:, :, 1], c='k', alpha=.2, linewidth=.5)
    s = 2
    plt.scatter(x_init[:, 0], x_init[:, 1], s=0.3, color="green", marker="x")

    x_final = x_final.detach()
    plt.scatter(x_final[:, 0], x_final[:, 1], label=label, s=s, c=color)
    # plt.legend()

    x_ = np.linspace(-7, 7)
    y_ = np.linspace(-5, 5)
    X, Y = np.meshgrid(x_, y_)
    XX = torch.tensor(np.array([X.ravel(), Y.ravel()]).T)
    Z = potential(XX).reshape(X.shape).detach().numpy()
    plt.contour(X, Y, Z, levels=5, colors="k", alpha=0.6)

    x_ = np.linspace(min(x_), max(x_), 20)
    y_ = np.linspace(min(y_), max(y_), 20)
    X, Y = np.meshgrid(x_, y_)
    XX = torch.tensor(np.array([X.ravel(), Y.ravel()]).T)
    score_z = score(XX)
    u = score_z[:, 0].reshape(X.shape).detach().numpy()
    v = score_z[:, 1].reshape(X.shape).detach().numpy()
    plt.quiver(X, Y, u, v, color="red", alpha=0.2)

    plt.tick_params(
        axis="both",
        which="both",
        bottom=False,
        top=False,
        labelbottom=False,
        left=False,
        right=False,
        labelleft=False,
    )
    plt.xlim(min(x_), max(x_))
    plt.ylim(min(y_), max(y_))
plt.show()

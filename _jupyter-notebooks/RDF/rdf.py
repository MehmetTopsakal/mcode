""" calculate the radial distribution function around Ti atoms
"""

from os import path
import numpy as np
from ase.io import read
from ase.neighborlist import NeighborList

subset = np.load("subset.npz")["subset"]

gr = np.zeros(81)
counter = 0
for poscar in subset:
    atoms = read(path.join(poscar[0], "POSCAR"), format="vasp")
    neigh_list = NeighborList([4]*len(atoms), skin=0, sorted=False,
                              bothways=True, self_interaction=False)
    neigh_list.build(atoms)

    for i, atom in enumerate(atoms):
        if atom.symbol == "Ti":
            counter += 1

            neighbor, offset = neigh_list.get_neighbors(i)
            shift = np.dot(offset, atoms.cell)
            xij = (atoms.positions[neighbor, :] + shift) - atom.position
            bins = (np.linalg.norm(xij, axis=1)/0.1).astype(int)

            for bin in bins:
                gr[bin] += 1

import matplotlib.pyplot as plt
from scipy.signal import argrelextrema
r = np.linspace(0, 8, 81)
gr = gr/(r**2)
extr = argrelextrema(gr, np.greater)[0]

plt.plot(r, gr)

for ext in extr:
    plt.text(r[ext], gr[ext], r[ext])
plt.savefig("rdf.pdf")

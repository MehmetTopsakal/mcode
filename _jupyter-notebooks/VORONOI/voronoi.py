





# /home/mt/software/anaconda3/pkgs/pymatgen-2017.11.30-py36_0/lib/python3.6/site-packages/pymatgen/analysis/local_env.py


import pymatgen 
from pymatgen.symmetry.analyzer import *
#structure = pymatgen.Structure.from_file("./mvc-11115/CONTCAR")
#structure = pymatgen.Structure.from_file("./mp-5229_STO/CONTCAR")
#structure = pymatgen.Structure.from_file("./mp-656850/CONTCAR")
#structure = pymatgen.Structure.from_file("./mvc-4715/CONTCAR")
#structure = pymatgen.Structure.from_file("./mp-636827/CONTCAR")
#structure = pymatgen.Structure.from_file("./mp-553432/CONTCAR")
#structure = pymatgen.Structure.from_file("./mp-572822/CONTCAR")
#structure = pymatgen.Structure.from_file("./mp-655656/CONTCAR")
structure = pymatgen.Structure.from_file("./mvc-2169/CONTCAR")
finder = SpacegroupAnalyzer(structure)
symmetrized_structure = finder.get_symmetrized_structure()
[sites, indices]  = symmetrized_structure.equivalent_sites, symmetrized_structure.equivalent_indices
print(indices)
#print(sites)





"""
Uses a Voronoi algorithm to determine near neighbors for each site in a
structure.

Args:
    tol (float): tolerance parameter for near-neighbor finding
        (default: 0).
    targets (Element or list of Elements): target element(s).
    cutoff (float): cutoff radius in Angstrom to look for near-neighbor
        atoms. Defaults to 10.0.
    allow_pathological (bool): whether to allow infinite vertices in
        determination of Voronoi coordination.
"""
from pymatgen.analysis.local_env import VoronoiNN
vnn = VoronoiNN(tol=0, targets=None, cutoff=5)
vcn = vnn.get_cn(symmetrized_structure, 0, use_weights=True)
print(vcn)
















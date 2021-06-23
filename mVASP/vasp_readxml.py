#!/usr/bin/env python


import numpy as np

from mVASP import readvasprunxml



params, kpoints, kpoints_path, klines_path, poscar0, bands_up, bands_dw, efermi, Edos, tdos_up, tdos_dw, pdos_up, pdos_dw = readvasprunxml('vasprun.xml')



np.savez('vasprun', params=params, kpoints=kpoints, kpoints_path=kpoints_path, klines_path=klines_path, poscar0=poscar0, bands_up=bands_up, bands_dw=bands_dw, Edos=Edos, tdos_up=tdos_up, tdos_dw=tdos_dw, pdos_up=pdos_up, pdos_dw=pdos_dw, efermi=efermi)






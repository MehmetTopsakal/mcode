#!/usr/bin/python

import os
import sys
from   pylab import sqrt
import numpy as np
import scipy.io as sio

#### ========================================================  NOTE: DNR




def readQEXML(file):
    
    with open(file) as f:
        lines = f.readlines()
    
    POSITIONS = []
    LATTICE = []
    NSPIN = 1
    CELL_DIMENSIONS = []
    
    for i, line in enumerate(lines):

        if line.startswith('    <LATTICE_PARAMETER type='):
            LATTICE_PARAMETER = float(lines[i+1])

        if line.startswith('    <CELL_DIMENSIONS type='):
            for a in range(6):
                CELL_DIMENSIONS.append(float(lines[i+1+a]))
            CELL_DIMENSIONS = np.array(CELL_DIMENSIONS, np.float)
 
        if line.startswith('  </CELL>'):
            NATOMS = int(lines[i+3].split()[0])
            NTYPES = int(lines[i+6].split()[0])             
 
        if line.startswith('    <WFC_CUTOFF'):                   
            ECUTWFC  = float(lines[i+1].split()[0])
            ECUTRHO  = float(lines[i+4].split()[0])

        if line.startswith('    <LSDA'):                   
            if lines[i+1].split()[0] == 'T': NSPIN = 2
            LNONCOL = lines[i+4].split()[0]     
            LSORBIT = lines[i+7].split()[0]
                                 
        if line.startswith('    <UNITS_FOR_ATOMIC_POSITIONS UNITS='):
            for a in range(NATOMS):
                POSITIONS.append(lines[i+1+a].strip().split('"')[5].split()[0:3])
            POSITIONS = np.array(POSITIONS, np.float)
            
        if line.startswith('      <UNITS_FOR_DIRECT_LATTICE_VECTORS UNITS='):
            LATTICE.append(lines[i+2].split()[0:3]) 
            LATTICE.append(lines[i+5].split()[0:3]) 
            LATTICE.append(lines[i+8].split()[0:3])
            LATTICE = np.array(LATTICE, np.float)
            
            


    params = []
    params.append(NATOMS)
    params.append(NTYPES)
    params.append(ECUTWFC)  
    params.append(ECUTRHO)
    params.append(NSPIN) 
    params.append(LNONCOL)  
    params.append(LSORBIT)
    
    lattice = LATTICE/1.88972612456506
    positions = POSITIONS/1.88972612456506 
    
    qe_alat = LATTICE_PARAMETER
    qe_cell = CELL_DIMENSIONS   
    
    return params, lattice, positions, qe_alat, qe_cell





params, lattice, positions, qe_alat, qe_cell = readQEXML('data-file.xml')




#np.savez('vasprun', params=params, kpoints=kpointsDir, kpoints_path=kpoints_path, klines_path=klines_path, bands_up=bands_up, bands_dw=bands_dw, Edos=Edos, tdos_up=tdos_up, tdos_dw=tdos_dw, pdos_up=pdos_up, pdos_dw=pdos_dw, efermi=efermi)






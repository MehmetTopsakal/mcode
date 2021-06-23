#!/usr/bin/env python

import numpy as np


### USAGE:
### import mPOSCAR,numpy
### data = np.loadtxt('ev.in', usecols=(0, 1))
### v0, e0, b0, bp, res, vd, ed, vf, ef, pf = mBM.makefit(data,1,1)
### 
### 
### 
#### ========================================================
def read_poscar(file):
  lattice = []; positions = []; labels = []
  with open(file, mode='r') as f:
    lines = [line for line in f.readlines()]
    
    alat =  float(lines[1].split()[0]); 
    lattice.append(lines[2].split());  
    lattice.append(lines[3].split());   
    lattice.append(lines[4].split());
    labels = lines[5].split();
    natoms = lines[6].split(); natoms = np.array(natoms); natoms = natoms.astype(np.int); 
    
    line8 = lines[7].split();
    line9 = lines[8].split();
    
    if (line8[0][0] == 'S') or  (line8[0][0] == 's'):
        pfmtline = line9
        for a in range(sum(natoms)):
            positions.append(lines[a+9].split()[0:3])
    else:
        pfmtline = line8
        for a in range(sum(natoms)):
            positions.append(lines[a+8].split()[0:3])
        
        
    lattice   = np.array(lattice); lattice = lattice.astype(np.float); lattice = lattice*alat
    positions = np.array(positions); positions = positions.astype(np.float); positions = positions*alat  

    
    if (pfmtline[0][0] == 'D') or  (pfmtline[0][0] == 'd'):
        positions_cart = []; pnew = [] 
        for p in range(len(positions)):
            pnew.append( positions[p][0]*lattice[0][0] + positions[p][1]*lattice[1][0] + positions[p][2]*lattice[2][0] ); 
            pnew.append( positions[p][0]*lattice[0][1] + positions[p][1]*lattice[1][1] + positions[p][2]*lattice[2][1] );
            pnew.append( positions[p][0]*lattice[0][2] + positions[p][1]*lattice[1][2] + positions[p][2]*lattice[2][2] );
            positions_cart.append(pnew); pnew = []
            
        positions_cart = np.array(positions_cart); 
        positions_cart = positions_cart.reshape(len(positions),3,order='F').copy()
        positions_cart = positions_cart/alat 
        positions_dir = positions/alat        
    else:
        #input positions are in cartesian format !
        positions_cart = positions
        positions_dir = [] 
        print('direct positions are not implemented for input POSCAR in cartesian')
        
  return labels, natoms, lattice, positions_cart, positions_dir




      
#labels, natoms, lattice, positions = read_poscar(file)

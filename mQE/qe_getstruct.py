#!/usr/bin/python

import mQE
import os
import sys
import numpy as np


#### ========================================================  NOTE:


params, lattice, positions, qe_alat, qe_cell = mQE.readxml()


f = open('./qetmp/pwscf.struct', 'w')
f.write(' \n')
f.write('CELL_PARAMETERS (angstrom) \n')

print('%12.8f' %(lattice[0][0]),  '%12.8f' %(lattice[0][1]),  '%12.8f' %(lattice[0][2]), file=f)
print('%12.8f' %(lattice[1][0]),  '%12.8f' %(lattice[1][1]),  '%12.8f' %(lattice[1][2]), file=f) 
print('%12.8f' %(lattice[2][0]),  '%12.8f' %(lattice[2][1]),  '%12.8f' %(lattice[2][2]), file=f) 

f.write(' \n')
f.write('ATOMIC_POSITIONS (angstrom) \n')

for p in range(len(positions)):
    print('%s' %(params[9][p]), '%12.8f' %(positions[p][0]),  '%12.8f' %(positions[p][1]),  '%12.8f' %(positions[p][2]), file=f)
    
    
f.close() 


















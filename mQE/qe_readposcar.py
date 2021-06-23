#!/usr/bin/python2

import numpy as np
from   pylab import *
import scipy.io as sio


#inputs = sys.argv
#ilen   = len(inputs)

#if ilen == 1:
  #file = 'scf.out'; 
#else:
  #file = sys.argv[1];
  

inputs = sys.argv
ilen   = len(inputs)

if ilen == 1:
  inputs.append('scf.out'); #inputs.append(45); inputs.append(45); 
#if ilen == 2:
  #inputs.append(45); inputs.append(45);
#if ilen == 3:
  #inputs.append(10);

file = inputs[1]
#azi = int(inputs[2])
#ele = int(inputs[3])  
  


def read_cell(file):
  lattice = []; positions = [];
  with open(file, mode='r') as f:
    lines = [line for line in f.readlines()]
    for i, line in enumerate(lines):
      if 'lattice parameter (alat)  =' in line:
	alat= lines[i].split()[4]; alat = float(alat)/1.88972612456506
      if 'number of atoms/cell      = ' in line:   
	natom = lines[i].split()[4]; natom = int(natom)	
      if 'celldm(1)=' in line:
	#cell1= lines[i].split()[1]
	lattice.append(lines[i+4].split()[3:6])
	lattice.append(lines[i+5].split()[3:6])
	lattice.append(lines[i+6].split()[3:6])	
	lattice = np.array(lattice); lattice = lattice.astype(np.float); lattice = lattice*alat
      if 'site n.     atom                  positions (alat units)' in line: 
	for e in range(natom):	
	 positions.append(lines[i+1].split()[6:9])
	 i += 1 
	positions = np.array(positions); positions = positions.astype(np.float); positions = positions*alat 	
        break
  return lattice, positions
      
lattice, positions = read_cell(file)
print(lattice)
print(positions)
sio.savemat('.POSCAR.mat', dict(lattice=lattice, positions=positions)) #http://docs.scipy.org/doc/scipy-0.14.0/reference/tutorial/io.html





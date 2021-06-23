#!/usr/bin/python2

import numpy as np
from   pylab import *
import scipy.io as sio
from   matplotlib import gridspec
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

inputs = sys.argv
ilen   = len(inputs)

if ilen == 1:
  inputs.append('scf.out'); inputs.append(45); inputs.append(45); 
if ilen == 2:
  inputs.append(45); inputs.append(45);
if ilen == 3:
  inputs.append(10);

file = inputs[1]
azi = int(inputs[2])
ele = int(inputs[3])



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
#print lattice
#print positions
##sio.savemat('POSCAR.mat', dict(lattice=lattice, positions=positions)) #http://docs.scipy.org/doc/scipy-0.14.0/reference/tutorial/io.html





gs = gridspec.GridSpec(1, 1,
                       ) #height_ratios=[3,2] )    
gs.update(top=0.95, bottom=0.08, left=0.07, right=0.98, hspace=0.3, wspace=0.2)






ax = plt.subplot(gs[0], projection='3d')

x1 = [ 0.,  lattice[0,0]]; y1 = [ 0.,  0.]; z1 = [ 0.,  0.]
x2 = [ 0.,  0.]; y2 = [ 0.,  lattice[1,1]]; z2 = [ 0.,  0.]
x3 = [ 0.,  0.]; y3 = [ 0.,  0.]; z3 = [ 0.,  lattice[2,2]]

for i in range(1, 2):
    ax.plot(x1[i-1:i+1], y1[i-1:i+1], z1[i-1:i+1], 'r-', linewidth=2)
    ax.plot(x2[i-1:i+1], y2[i-1:i+1], z2[i-1:i+1], 'g-', linewidth=2)
    ax.plot(x3[i-1:i+1], y3[i-1:i+1], z3[i-1:i+1], 'b-', linewidth=2)  

ax.plot(positions[:,0], positions[:,1], positions[:,2], 'ko')    
    
ax.set_xlim3d(0, lattice[0,0]); ax.set_ylim3d(0, lattice[1,1]); ax.set_zlim3d(0, lattice[2,2])


#for ii in xrange(0,360,10):
    #ax.view_init(elev=10., azim=ii)
    #savefig("tmp"%ii+".png")


ax.view_init(elev=ele, azim=azi)
savefig("POSCAR.png")



plt.show()





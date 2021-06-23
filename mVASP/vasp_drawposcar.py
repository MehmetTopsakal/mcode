#!/usr/bin/python2

import matplotlib
matplotlib.use('Agg') # see http://matplotlib.org/faq/usage_faq.html#what-is-a-backend

import numpy as np
from   pylab import *
import scipy.io as sio

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d import proj3d

matplotlib.rcParams['backend'] = 'Qt4Agg'


#font = {'size':8}
#matplotlib.rc('font', **font)
#savefig('plot.png', format='png', dpi=200) 
#### ========================================================  NOTE: DNR




inputs = sys.argv
ilen   = len(inputs)

if ilen == 1:
  inputs.extend(['POSCAR',45,45,10]); 
if ilen == 2:
  inputs.extend([45,45,10]); 
if ilen == 3:
  inputs.extend([45,10]); 
if ilen == 4:
  inputs.extend([10]);  
  
  
file = inputs[1]
azi = float(inputs[2])
ele = float(inputs[3])
ms  = float(inputs[4])



#### ========================================================  NOTE: defs
# http://choorucode.com/2014/11/13/how-to-get-orthographic-projection-in-3d-plot-of-matplotlib/ 
def orthogonal_proj(zfront, zback):
    a = (zfront+zback)/(zfront-zback)
    b = -2*(zfront*zback)/(zfront-zback)
    # -0.0001 added for numerical stability as suggested in:
    # http://stackoverflow.com/questions/23840756
    return np.array([[1,0,0,0],
                        [0,1,0,0],
                        [0,0,a,b],
                        [0,0,-0.0001,zback]])
proj3d.persp_transformation = orthogonal_proj # workaround #ax.invert_zaxis() 




  
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
        positions = positions_cart/alat    
        
  return labels, natoms, lattice, positions   
      
labels, natoms, lattice, positions = read_poscar(file)



#supercell = []; pnew=[]; p=positions; l=lattice

#for s in range(len(p)):
    #pnew.append(p[s][0]); pnew.append(p[s][1]); pnew.append(p[s][2]); supercell.append(pnew); pnew=[]
    
    #pnew.append(p[s][0]+l[0][0]); pnew.append(p[s][1]+l[0][1]); pnew.append(p[s][2]+l[0][2]); supercell.append(pnew); pnew=[] # +x
    #pnew.append(p[s][0]-l[0][0]); pnew.append(p[s][1]-l[0][1]); pnew.append(p[s][2]-l[0][2]); supercell.append(pnew); pnew=[] # -x
    #pnew.append(p[s][0]+l[1][0]); pnew.append(p[s][1]+l[1][1]); pnew.append(p[s][2]+l[1][2]); supercell.append(pnew); pnew=[] # +y
    #pnew.append(p[s][0]-l[1][0]); pnew.append(p[s][1]-l[1][1]); pnew.append(p[s][2]-l[1][2]); supercell.append(pnew); pnew=[] # -y
    #pnew.append(p[s][0]+l[2][0]); pnew.append(p[s][1]+l[2][1]); pnew.append(p[s][2]+l[2][2]); supercell.append(pnew); pnew=[] # +z
    #pnew.append(p[s][0]-l[2][0]); pnew.append(p[s][1]-l[2][1]); pnew.append(p[s][2]-l[2][2]); supercell.append(pnew); pnew=[] # -z
    
    #pnew.append(p[s][0]+l[0][0]+l[1][0]); pnew.append(p[s][1]+l[0][1]+l[1][1]); pnew.append(p[s][2]+l[0][2]+l[1][2]); supercell.append(pnew); pnew=[] # +x+y
    #pnew.append(p[s][0]+l[0][0]-l[1][0]); pnew.append(p[s][1]+l[0][1]-l[1][1]); pnew.append(p[s][2]+l[0][2]-l[1][2]); supercell.append(pnew); pnew=[] # +x-y
    #pnew.append(p[s][0]-l[0][0]+l[1][0]); pnew.append(p[s][1]-l[0][1]+l[1][1]); pnew.append(p[s][2]-l[0][2]+l[1][2]); supercell.append(pnew); pnew=[] # -x+y
    #pnew.append(p[s][0]-l[0][0]-l[1][0]); pnew.append(p[s][1]-l[0][1]-l[1][1]); pnew.append(p[s][2]-l[0][2]-l[1][2]); supercell.append(pnew); pnew=[] # -x-y
    #pnew.append(p[s][0]+l[2][0]+l[0][0]); pnew.append(p[s][1]+l[2][1]+l[0][1]); pnew.append(p[s][2]+l[2][2]+l[0][2]); supercell.append(pnew); pnew=[] # +z+x
    #pnew.append(p[s][0]+l[2][0]-l[0][0]); pnew.append(p[s][1]+l[2][1]-l[0][1]); pnew.append(p[s][2]+l[2][2]-l[0][2]); supercell.append(pnew); pnew=[] # +z-x
    #pnew.append(p[s][0]-l[2][0]+l[0][0]); pnew.append(p[s][1]-l[2][1]+l[0][1]); pnew.append(p[s][2]-l[2][2]+l[0][2]); supercell.append(pnew); pnew=[] # -z+x
    #pnew.append(p[s][0]-l[2][0]-l[0][0]); pnew.append(p[s][1]-l[2][1]-l[0][1]); pnew.append(p[s][2]-l[2][2]-l[0][2]); supercell.append(pnew); pnew=[] # -z-x
    #pnew.append(p[s][0]+l[2][0]+l[1][0]); pnew.append(p[s][1]+l[2][1]+l[1][1]); pnew.append(p[s][2]+l[2][2]+l[1][2]); supercell.append(pnew); pnew=[] # +z+y
    #pnew.append(p[s][0]+l[2][0]-l[1][0]); pnew.append(p[s][1]+l[2][1]-l[1][1]); pnew.append(p[s][2]+l[2][2]-l[1][2]); supercell.append(pnew); pnew=[] # +z-y
    #pnew.append(p[s][0]-l[2][0]+l[1][0]); pnew.append(p[s][1]-l[2][1]+l[1][1]); pnew.append(p[s][2]-l[2][2]+l[1][2]); supercell.append(pnew); pnew=[] # -z+y
    #pnew.append(p[s][0]-l[2][0]-l[1][0]); pnew.append(p[s][1]-l[2][1]-l[1][1]); pnew.append(p[s][2]-l[2][2]-l[1][2]); supercell.append(pnew); pnew=[] # -z-y
    
    #pnew.append(p[s][0]+l[2][0]+l[0][0]+l[1][0]); pnew.append(p[s][1]+l[2][1]+l[0][1]+l[1][1]); pnew.append(p[s][2]+l[2][2]+l[0][2]+l[1][2]); supercell.append(pnew); pnew=[] # +z+x+y
    #pnew.append(p[s][0]+l[2][0]+l[0][0]-l[1][0]); pnew.append(p[s][1]+l[2][1]+l[0][1]-l[1][1]); pnew.append(p[s][2]+l[2][2]+l[0][2]-l[1][2]); supercell.append(pnew); pnew=[] # +z+x-y
    #pnew.append(p[s][0]+l[2][0]-l[0][0]-l[1][0]); pnew.append(p[s][1]+l[2][1]-l[0][1]-l[1][1]); pnew.append(p[s][2]+l[2][2]-l[0][2]-l[1][2]); supercell.append(pnew); pnew=[] # +z-x-y
    #pnew.append(p[s][0]+l[2][0]-l[0][0]+l[1][0]); pnew.append(p[s][1]+l[2][1]-l[0][1]+l[1][1]); pnew.append(p[s][2]+l[2][2]-l[0][2]+l[1][2]); supercell.append(pnew); pnew=[] # +z-x+y
    #pnew.append(p[s][0]-l[2][0]+l[0][0]+l[1][0]); pnew.append(p[s][1]-l[2][1]+l[0][1]+l[1][1]); pnew.append(p[s][2]-l[2][2]+l[0][2]+l[1][2]); supercell.append(pnew); pnew=[] # -z+x+y
    #pnew.append(p[s][0]-l[2][0]+l[0][0]-l[1][0]); pnew.append(p[s][1]-l[2][1]+l[0][1]-l[1][1]); pnew.append(p[s][2]-l[2][2]+l[0][2]-l[1][2]); supercell.append(pnew); pnew=[] # -z+x-y
    #pnew.append(p[s][0]-l[2][0]-l[0][0]-l[1][0]); pnew.append(p[s][1]-l[2][1]-l[0][1]-l[1][1]); pnew.append(p[s][2]-l[2][2]-l[0][2]-l[1][2]); supercell.append(pnew); pnew=[] # -z-x-y
    #pnew.append(p[s][0]-l[2][0]-l[0][0]+l[1][0]); pnew.append(p[s][1]-l[2][1]-l[0][1]+l[1][1]); pnew.append(p[s][2]-l[2][2]-l[0][2]+l[1][2]); supercell.append(pnew); pnew=[] # -z-x+y

#supercell = np.array(supercell) ;
#supercell = supercell.reshape(len(p)*27,3,order='F').copy()
#positions = supercell


#reduced_positions = []

#for p in range(len(positions)):
    
    ##if (positions[p,0]<0):
        ##continue
    
    ##if (positions[p,1]<0):
        ##continue    

    ##if (positions[p,2]<0):
        ##continue 
    
    ##if (positions[p,0]>lattice[0,0]):
        ##continue
    
    ##if (positions[p,1]>lattice[0,0]):
        ##continue    

    ##if (positions[p,2]>lattice[0,0]):
        ##continue     
    
    #reduced_positions.append(positions[p][:])

    ##ax.plot(positions[p][:], 'ko', ms=10)

#reduced_positions = np.array(reduced_positions); reduced_positions = reduced_positions.astype(np.float); 
#positions = reduced_positions
 
 
 




#### ========================================================  NOTE: plot
plt.close('all')
fig = plt.figure()







ax1 = fig.add_subplot(321, projection='3d')
x1=[0,1]; x1[0]=array([0, 0, 0]); x1[1]=lattice[0,:];
x1 = np.array(x1); x1 = x1.astype(np.float); ax1.plot3D(x1[:,0], x1[:,1], x1[:,2], 'r-', lw=2) 
x2=[0,1]; x2[0]=array([0, 0, 0]); x2[1]=lattice[1,:];
x2 = np.array(x2); x2 = x2.astype(np.float); ax1.plot3D(x2[:,0], x2[:,1], x2[:,2], 'g-', lw=2) 
x3=[0,1]; x3[0]=array([0, 0, 0]); x3[1]=lattice[2,:];
x3 = np.array(x3); x3 = x3.astype(np.float); ax1.plot3D(x3[:,0], x3[:,1], x3[:,2], 'b-', lw=2) 
ax1.plot3D(positions[:,0], positions[:,1], positions[:,2], 'ko', ms=ms/3, zdir='z') 
axis('tight'); axis('equal'); ax1._axis3don = False # box off
ax1.view_init(elev=90, azim=-90)
title('azi= -90, ele= 90', fontsize=8)

ax1 = fig.add_subplot(323, projection='3d')
x1=[0,1]; x1[0]=array([0, 0, 0]); x1[1]=lattice[0,:];
x1 = np.array(x1); x1 = x1.astype(np.float); ax1.plot3D(x1[:,0], x1[:,1], x1[:,2], 'r-', lw=2) 
x2=[0,1]; x2[0]=array([0, 0, 0]); x2[1]=lattice[1,:];
x2 = np.array(x2); x2 = x2.astype(np.float); ax1.plot3D(x2[:,0], x2[:,1], x2[:,2], 'g-', lw=2) 
x3=[0,1]; x3[0]=array([0, 0, 0]); x3[1]=lattice[2,:];
x3 = np.array(x3); x3 = x3.astype(np.float); ax1.plot3D(x3[:,0], x3[:,1], x3[:,2], 'b-', lw=2)  
ax1.plot3D(positions[:,0], positions[:,1], positions[:,2], 'ko', ms=ms/3, zdir='z') 
axis('tight'); axis('equal'); ax1._axis3don = False # box off
ax1.view_init(elev=0, azim=-90)
title('azi= -90, ele= 0', fontsize=8)

ax1 = fig.add_subplot(325, projection='3d')
x1=[0,1]; x1[0]=array([0, 0, 0]); x1[1]=lattice[0,:];
x1 = np.array(x1); x1 = x1.astype(np.float); ax1.plot3D(x1[:,0], x1[:,1], x1[:,2], 'r-', lw=2) 
x2=[0,1]; x2[0]=array([0, 0, 0]); x2[1]=lattice[1,:];
x2 = np.array(x2); x2 = x2.astype(np.float); ax1.plot3D(x2[:,0], x2[:,1], x2[:,2], 'g-', lw=2) 
x3=[0,1]; x3[0]=array([0, 0, 0]); x3[1]=lattice[2,:];
x3 = np.array(x3); x3 = x3.astype(np.float); ax1.plot3D(x3[:,0], x3[:,1], x3[:,2], 'b-', lw=2) 
ax1.plot3D(positions[:,0], positions[:,1], positions[:,2], 'ko', ms=ms/3, zdir='z') 
axis('tight'); axis('equal'); ax1._axis3don = False # box off
ax1.view_init(elev=0, azim=0)
title('azi= 0, ele= 0', fontsize=8)





ax1 = fig.add_subplot(122, projection='3d')
x1=[0,1]; x1[0]=array([0, 0, 0]); x1[1]=lattice[0,:];
x1 = np.array(x1); x1 = x1.astype(np.float); ax1.plot3D(x1[:,0], x1[:,1], x1[:,2], 'r-', lw=2) 
x2=[0,1]; x2[0]=array([0, 0, 0]); x2[1]=lattice[1,:];
x2 = np.array(x2); x2 = x2.astype(np.float); ax1.plot3D(x2[:,0], x2[:,1], x2[:,2], 'g-', lw=2) 
x3=[0,1]; x3[0]=array([0, 0, 0]); x3[1]=lattice[2,:];
x3 = np.array(x3); x3 = x3.astype(np.float); ax1.plot3D(x3[:,0], x3[:,1], x3[:,2], 'b-', lw=2) 
ax1.plot3D(positions[:,0], positions[:,1], positions[:,2], 'ko', ms=ms/1.5, zdir='z') 
axis('tight'); axis('equal'); #ax1._axis3don = False # box off
ax1.view_init(elev=ele, azim=azi)
title('azi= '+str(azi)+ ' ele= '+str(ele), fontsize=8)





plt.tight_layout()




# CAUTION: Duplication is needed here !!!! ------------- ###
plt.savefig('structure.png', format='png') 
plt.savefig('structure.png', format='png', dpi=300) 
# ------------------------------------------------------ ###
#plt.show()




 

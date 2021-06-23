#!/usr/bin/python3

import mPOSCAR
import subprocess 
import numpy as np
import math
import sys


inputs = sys.argv
for a in range(len(inputs)):
    s=inputs[a].split('=')
    if s[0] == 'target' or s[0] == 't' : target = int(s[1])
    elif s[0] == 'dmax' or s[0] == 'd' : dmax = float(s[1]) 
    elif s[0] == 'supercell' or s[0] == 's' : supercell = int(s[1])
    elif s[0] == 'poscar' or s[0] == 'p' : poscar = s[1]
    
try:
    target
except:
    ef = open('_ERROR', 'w')
    ef.write('\n ERROR: target atom is not given  !! Exiting.... \n')
    sys.exit('\n >> ERROR: target atom is not given  !! Exiting.... \n') 

try:
    dmax
except:
    dmax=15.0

try:
    supercell
except:
    supercell=4

try:
    poscar
except:
    poscar='POSCAR'





labels, natoms, lattice, positions_cart, positions_dir = mPOSCAR.read_poscar(poscar)

labels_all = []
c = 0
for i in range(len(natoms)):
    for j in range(natoms[i]):
        labels_all.append(labels[i])
        c =+ 1
target_atom_label = labels_all[target-1]



#{{{{{{{{{{{{{{{{{{{{{}}}}}}}}}}}}}}}}}} shift adsorbing atom to origin
postions_shiftedx = []; postions_shiftedy = []; postions_shiftedz = []

for s in range(len(positions_dir)):
    postions_shiftedx.append(positions_dir[s][0]-positions_dir[target-1][0])
    postions_shiftedy.append(positions_dir[s][1]-positions_dir[target-1][1])    
    postions_shiftedz.append(positions_dir[s][2]-positions_dir[target-1][2])  
postions_shiftedx  = np.array(postions_shiftedx, np.float)
postions_shiftedy  = np.array(postions_shiftedy, np.float)
postions_shiftedz  = np.array(postions_shiftedz, np.float)

positions_shifted = np.column_stack( (postions_shiftedx,postions_shiftedy,postions_shiftedz) )

f = open('POSCAR_shifted', 'w')
f.write('shifted poscar         \n')
f.write('1.000000              \n')

for p in range(len(lattice)):
    f.write(str(format(lattice[p][0],'.8f'))+'  '+str(format(lattice[p][1],'.8f'))+'  '+str(format(lattice[p][2],'.8f'))+'   \n')
  
for l in range(len(labels)):
    f.write(str(labels[l])+' ')       
f.write('\n ')

for n in range(len(natoms)):
    f.write(str(natoms[n])+' ')       
f.write('\nDirect \n')

for p in range(len(positions_shifted)):
    f.write(str(format(positions_shifted[p][0],'.8f'))+'  '+str(format(positions_shifted[p][1],'.8f'))+'  '+str(format(positions_shifted[p][2],'.8f'))+'   \n')

f.close()
labels, natoms, lattice, positions_cart, positions_dir = mPOSCAR.read_poscar('POSCAR_shifted')


#{{{{{{{{{{{{{{{{{{{{{}}}}}}}}}}}}}}}}}} make supercell-1
subprocess.call(' msupercell POSCAR_shifted '+str(int(supercell))+' '+str(int(supercell))+' '+str(int(supercell))+' > /dev/null ', shell=True)
labels, natoms, lattice, positions_cart, positions_dir = mPOSCAR.read_poscar('sPOSCAR_shifted')

# BOZUK !!!!!!
#import ase.io.vasp
#cell = ase.io.vasp.read_vasp("POSCAR_shifted")
#ase.io.vasp.write_vasp("POSCAR_ase",cell*(supercell,supercell,supercell), label='supercell',direct=True,sort=False)
#subprocess.call(' awk "NR<6" POSCAR_ase > sPOSCAR_shifted ', shell=True)
#subprocess.call(' awk "NR==6" POSCAR_shifted >> sPOSCAR_shifted ', shell=True)
#subprocess.call(' awk "NR>5" POSCAR_ase >> sPOSCAR_shifted ', shell=True)
#labels, natoms, lattice, positions_cart, positions_dir = mPOSCAR.read_poscar('sPOSCAR_shifted')



z = np.zeros((len(positions_cart), 1), dtype=positions_cart.dtype)   
positions_cart = np.column_stack( (positions_cart,z) )

a=0
for l in range(len(labels)):
    nl = natoms[l]
    for i in range(nl):
        positions_cart[a][3] = l+1
        a += 1


#{{{{{{{{{{{{{{{{{{{{{}}}}}}}}}}}}}}}}}} make supercell-2
supercell = []; pnew=[]; p=positions_cart; l=lattice

for s in range(len(p)):
    pnew.append(p[s][0]); pnew.append(p[s][1]); pnew.append(p[s][2]); pnew.append(p[s][3]); supercell.append(pnew); pnew=[]
    
    pnew.append(p[s][0]+l[0][0]); pnew.append(p[s][1]+l[0][1]); pnew.append(p[s][2]+l[0][2]); pnew.append(p[s][3]); supercell.append(pnew); pnew=[] # +x
    pnew.append(p[s][0]-l[0][0]); pnew.append(p[s][1]-l[0][1]); pnew.append(p[s][2]-l[0][2]); pnew.append(p[s][3]); supercell.append(pnew); pnew=[] # -x
    pnew.append(p[s][0]+l[1][0]); pnew.append(p[s][1]+l[1][1]); pnew.append(p[s][2]+l[1][2]); pnew.append(p[s][3]); supercell.append(pnew); pnew=[] # +y
    pnew.append(p[s][0]-l[1][0]); pnew.append(p[s][1]-l[1][1]); pnew.append(p[s][2]-l[1][2]); pnew.append(p[s][3]); supercell.append(pnew); pnew=[] # -y
    pnew.append(p[s][0]+l[2][0]); pnew.append(p[s][1]+l[2][1]); pnew.append(p[s][2]+l[2][2]); pnew.append(p[s][3]); supercell.append(pnew); pnew=[] # +z
    pnew.append(p[s][0]-l[2][0]); pnew.append(p[s][1]-l[2][1]); pnew.append(p[s][2]-l[2][2]); pnew.append(p[s][3]); supercell.append(pnew); pnew=[] # -z
    
    pnew.append(p[s][0]+l[0][0]+l[1][0]); pnew.append(p[s][1]+l[0][1]+l[1][1]); pnew.append(p[s][2]+l[0][2]+l[1][2]); pnew.append(p[s][3]); supercell.append(pnew); pnew=[] # +x+y
    pnew.append(p[s][0]+l[0][0]-l[1][0]); pnew.append(p[s][1]+l[0][1]-l[1][1]); pnew.append(p[s][2]+l[0][2]-l[1][2]); pnew.append(p[s][3]); supercell.append(pnew); pnew=[] # +x-y
    pnew.append(p[s][0]-l[0][0]+l[1][0]); pnew.append(p[s][1]-l[0][1]+l[1][1]); pnew.append(p[s][2]-l[0][2]+l[1][2]); pnew.append(p[s][3]); supercell.append(pnew); pnew=[] # -x+y
    pnew.append(p[s][0]-l[0][0]-l[1][0]); pnew.append(p[s][1]-l[0][1]-l[1][1]); pnew.append(p[s][2]-l[0][2]-l[1][2]); pnew.append(p[s][3]); supercell.append(pnew); pnew=[] # -x-y
    pnew.append(p[s][0]+l[2][0]+l[0][0]); pnew.append(p[s][1]+l[2][1]+l[0][1]); pnew.append(p[s][2]+l[2][2]+l[0][2]); pnew.append(p[s][3]); supercell.append(pnew); pnew=[] # +z+x
    pnew.append(p[s][0]+l[2][0]-l[0][0]); pnew.append(p[s][1]+l[2][1]-l[0][1]); pnew.append(p[s][2]+l[2][2]-l[0][2]); pnew.append(p[s][3]); supercell.append(pnew); pnew=[] # +z-x
    pnew.append(p[s][0]-l[2][0]+l[0][0]); pnew.append(p[s][1]-l[2][1]+l[0][1]); pnew.append(p[s][2]-l[2][2]+l[0][2]); pnew.append(p[s][3]); supercell.append(pnew); pnew=[] # -z+x
    pnew.append(p[s][0]-l[2][0]-l[0][0]); pnew.append(p[s][1]-l[2][1]-l[0][1]); pnew.append(p[s][2]-l[2][2]-l[0][2]); pnew.append(p[s][3]); supercell.append(pnew); pnew=[] # -z-x
    pnew.append(p[s][0]+l[2][0]+l[1][0]); pnew.append(p[s][1]+l[2][1]+l[1][1]); pnew.append(p[s][2]+l[2][2]+l[1][2]); pnew.append(p[s][3]); supercell.append(pnew); pnew=[] # +z+y
    pnew.append(p[s][0]+l[2][0]-l[1][0]); pnew.append(p[s][1]+l[2][1]-l[1][1]); pnew.append(p[s][2]+l[2][2]-l[1][2]); pnew.append(p[s][3]); supercell.append(pnew); pnew=[] # +z-y
    pnew.append(p[s][0]-l[2][0]+l[1][0]); pnew.append(p[s][1]-l[2][1]+l[1][1]); pnew.append(p[s][2]-l[2][2]+l[1][2]); pnew.append(p[s][3]); supercell.append(pnew); pnew=[] # -z+y
    pnew.append(p[s][0]-l[2][0]-l[1][0]); pnew.append(p[s][1]-l[2][1]-l[1][1]); pnew.append(p[s][2]-l[2][2]-l[1][2]); pnew.append(p[s][3]); supercell.append(pnew); pnew=[] # -z-y
    
    pnew.append(p[s][0]+l[2][0]+l[0][0]+l[1][0]); pnew.append(p[s][1]+l[2][1]+l[0][1]+l[1][1]); pnew.append(p[s][2]+l[2][2]+l[0][2]+l[1][2]); pnew.append(p[s][3]); supercell.append(pnew); pnew=[] # +z+x+y
    pnew.append(p[s][0]+l[2][0]+l[0][0]-l[1][0]); pnew.append(p[s][1]+l[2][1]+l[0][1]-l[1][1]); pnew.append(p[s][2]+l[2][2]+l[0][2]-l[1][2]); pnew.append(p[s][3]); supercell.append(pnew); pnew=[] # +z+x-y
    pnew.append(p[s][0]+l[2][0]-l[0][0]-l[1][0]); pnew.append(p[s][1]+l[2][1]-l[0][1]-l[1][1]); pnew.append(p[s][2]+l[2][2]-l[0][2]-l[1][2]); pnew.append(p[s][3]); supercell.append(pnew); pnew=[] # +z-x-y
    pnew.append(p[s][0]+l[2][0]-l[0][0]+l[1][0]); pnew.append(p[s][1]+l[2][1]-l[0][1]+l[1][1]); pnew.append(p[s][2]+l[2][2]-l[0][2]+l[1][2]); pnew.append(p[s][3]); supercell.append(pnew); pnew=[] # +z-x+y
    pnew.append(p[s][0]-l[2][0]+l[0][0]+l[1][0]); pnew.append(p[s][1]-l[2][1]+l[0][1]+l[1][1]); pnew.append(p[s][2]-l[2][2]+l[0][2]+l[1][2]); pnew.append(p[s][3]); supercell.append(pnew); pnew=[] # -z+x+y
    pnew.append(p[s][0]-l[2][0]+l[0][0]-l[1][0]); pnew.append(p[s][1]-l[2][1]+l[0][1]-l[1][1]); pnew.append(p[s][2]-l[2][2]+l[0][2]-l[1][2]); pnew.append(p[s][3]); supercell.append(pnew); pnew=[] # -z+x-y
    pnew.append(p[s][0]-l[2][0]-l[0][0]-l[1][0]); pnew.append(p[s][1]-l[2][1]-l[0][1]-l[1][1]); pnew.append(p[s][2]-l[2][2]-l[0][2]-l[1][2]); pnew.append(p[s][3]); supercell.append(pnew); pnew=[] # -z-x-y
    pnew.append(p[s][0]-l[2][0]-l[0][0]+l[1][0]); pnew.append(p[s][1]-l[2][1]-l[0][1]+l[1][1]); pnew.append(p[s][2]-l[2][2]-l[0][2]+l[1][2]); pnew.append(p[s][3]); supercell.append(pnew); pnew=[] # -z-x+y

supercell = np.array(supercell) ;
supercell = supercell.reshape(len(p)*27,4,order='F').copy()
positions_supercell = supercell


#{{{{{{{{{{{{{{{{{{{{{}}}}}}}}}}}}}}}}}} trim atoms    
z = np.zeros((len(positions_supercell), 1), dtype=positions_supercell.dtype)   
positions_supercell = np.column_stack( (positions_supercell,z) )
     

positions_trimmed = []; d = []
for i in range(len(positions_supercell)):
    ds = positions_supercell[i][0]*positions_supercell[i][0] + positions_supercell[i][1]*positions_supercell[i][1] + positions_supercell[i][2]*positions_supercell[i][2]
    d = math.sqrt(ds)    
    if d < dmax and d != 0:
        positions_supercell[i][4]=d
        positions_trimmed.append(positions_supercell[i])    

#print((len(positions_trimmed)))
#{{{{{{{{{{{{{{{{{{{{{}}}}}}}}}}}}}}}}}} write atoms.dat 
f = open('tmp.dat', 'w')
f.write('  0.00000000   0.00000000   0.00000000     0    0.0000 \n')
for i in range(len(positions_trimmed)):
    f.write('%12.8f %12.8f %12.8f     %d    %6.4f \n' %(positions_trimmed[i][0],positions_trimmed[i][1],positions_trimmed[i][2],positions_trimmed[i][3],positions_trimmed[i][4]))
f.close()
subprocess.call(' echo ATOMS > atoms.dat ', shell=True)
subprocess.call(' sort -nk 5,5  tmp.dat >> atoms.dat ', shell=True)
subprocess.call(' echo END >> atoms.dat ', shell=True)


#{{{{{{{{{{{{{{{{{{{{{}}}}}}}}}}}}}}}}}} write atoms.xyz 
f = open('tmp.xyz', 'w')
for i in range(len(positions_trimmed)):
    f.write('%s %12.8f %12.8f %12.8f  %12.8f  \n' %( labels[int(positions_trimmed[i][3])-1],positions_trimmed[i][0],positions_trimmed[i][1],positions_trimmed[i][2],positions_trimmed[i][4] ) )
f.close()
subprocess.call(' echo '+str(len(positions_trimmed)+1)+' > atoms.xyz ', shell=True)
subprocess.call(' echo C >> atoms.xyz ', shell=True)
subprocess.call(' echo '+target_atom_label+' 0 0 0 >> atoms.xyz ', shell=True)
subprocess.call(' sort -nk 5,5  tmp.xyz >> atoms.xyz ', shell=True)


subprocess.call(' rm -f tmp.dat tmp.xyz POSCAR_ase POSCAR_shifted  POSCAR_supercell  sPOSCAR_shifted ', shell=True)

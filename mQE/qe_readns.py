#!/usr/bin/python2

from   sys   import stdin
import numpy as np
from   pylab import *
import scipy.io as sio

print()
#print 'USAGE: qe_readns.py file iatom iwrite (be careful with iatom)'
print()

inputs = sys.argv
ilen   = len(inputs)

if ilen == 1:
  inputs.append('scf.out'); inputs.append(1); inputs.append(1); 
if ilen == 2:
  inputs.append(1); inputs.append(1);
if ilen == 3:
  inputs.append(10);

nsfile = inputs[1]
iatom = int(inputs[2])
iwrite = int(inputs[3])

#print iatom
#print iwrite

def read_ns_nm(nsfile,iatom,iwrite):
  c=0
  evec = []; occup = [];
  s = 'atom ' + str(iatom).rjust(4) + '   Tr[ns(na)] =' ;
  with open(nsfile, mode='r') as f:
    lines = [line for line in f.readlines()]
    for i, line in enumerate(lines):
      if s in line:
	c=c+1
	if (c is iwrite):
	  eval = lines[i+2].split()
	  nssize=len(eval)
	  for e in range(nssize):
	    evec.append(lines[i+4].split());
	    occup.append(lines[i+5+nssize].split());
	    i += 1 
	  eval = np.array(eval); evec = np.array(evec); occup = np.array(occup);
	  eval = eval.astype(np.float); evec = evec.astype(np.float);
          break
  return eval, evec 




def read_ns_mag(nsfile,iatom,iwrite):
  c=0
  evec_up = []; occup_up = []; evec_dw = []; occup_dw = []; 
  s = 'atom ' + str(iatom).rjust(4) + '   Tr[ns(na)] (up, down, total) =' ;
  with open(nsfile, mode='r') as f:
    lines = [line for line in f.readlines()]
    for i, line in enumerate(lines):
      if s in line:
	c=c+1
	if (c is iwrite):
	  eval_up = lines[i+3].split()
	  nssize=len(eval_up); 
	  eval_dw = lines[i+8+2*nssize].split()
	  for e in range(nssize):
	    evec_up.append(lines[i+5].split()); evec_dw.append(lines[i+10+2*nssize].split())
	    occup_up.append(lines[i+6+nssize].split()); occup_dw.append(lines[i+11+3*nssize].split())
	    i += 1 
	  eval_up = np.array(eval_up); eval_dw = np.array(eval_dw); evec_up = np.array(evec_up); occup_up = np.array(occup_up); evec_dw = np.array(evec_dw); occup_dw = np.array(occup_dw);
	  eval_up = eval_up.astype(np.float); evec_up = evec_up.astype(np.float); eval_dw = eval_dw.astype(np.float); evec_dw = evec_dw.astype(np.float);
          break
  return eval_up, eval_dw, evec_up, evec_dw  



s1 = 'Tr[ns(na)] (up, down, total) ='
s2 = 'Tr[ns(na)] ='

with open(nsfile, mode='r') as f:
  lines = [line for line in f.readlines()]
  for i, line in enumerate(lines):
    if s1 in line:
      #print 'qe_readns.py: This is a magnetic system'
      eval_up, eval_dw, evec_up, evec_dw = read_ns_mag(nsfile,iatom,iwrite)
      sio.savemat('.ns.mat', dict(eval_up=eval_up, eval_dw=eval_dw, evec_up=evec_up, evec_dw=evec_dw)) #http://docs.scipy.org/doc/scipy-0.14.0/reference/tutorial/io.html
      break
    else:
      if s2 in line:
	#print 'qe_readns.py: This is a non-magnetic system'
	eval, evec = read_ns_nm(nsfile,iatom,iwrite)
	sio.savemat('.ns.mat', dict(eval=eval, evec=evec)) #http://docs.scipy.org/doc/scipy-0.14.0/reference/tutorial/io.html
	break





#def read_cell(nsfile):
  #lattice = []; positions = [];
  #with open(nsfile, mode='r') as f:
    #lines = [line for line in f.readlines()]
    #for i, line in enumerate(lines):
      #if 'lattice parameter (alat)  =' in line:
	#alat= lines[i].split()[4]; alat = float(alat)/1.88972612456506
      #if 'number of atoms/cell      = ' in line:   
	#natom = lines[i].split()[4]; natom = int(natom)	
      #if 'celldm(1)=' in line:
	##cell1= lines[i].split()[1]
	#lattice.append(lines[i+4].split()[3:6])
	#lattice.append(lines[i+5].split()[3:6])
	#lattice.append(lines[i+6].split()[3:6])	
	#lattice = np.array(lattice); lattice = lattice.astype(np.float); lattice = lattice*alat
      #if 'site n.     atom                  positions (alat units)' in line: 
	#for e in range(natom):	
	 #positions.append(lines[i+1].split()[6:9])
	 #i += 1 
	#positions = np.array(positions); positions = positions.astype(np.float); positions = positions*alat 	
        #break
  #return lattice, positions
      
##lattice, positions = read_cell('scf1.out')
##print lattice
##sio.savemat('lattice.mat', {'lattice':lattice}) #http://docs.scipy.org/doc/scipy-0.14.0/reference/tutorial/io.html




#def read_positions_alat(nsfile):
  #positions_alat = [];
  #with open(nsfile, mode='r') as f:
    #lines = [line for line in f.readlines()]
    #for i, line in enumerate(lines):
      #if 'number of atoms/cell      = ' in line:   
	#natom = lines[i].split()[4]; natom = int(natom)
      #if 'site n.     atom                  positions (alat units)' in line: 
	#for e in range(natom):	
	 #positions_alat.append(lines[i+1].split()[6:9])
	 #i += 1 
	#positions_alat = np.array(positions_alat) 
	#break
  #return positions_alat

##positions_alat = read_positions_alat('scf1.out')
##print positions_alat



#def read_ipositions_cryst(nsfile):
  #ipositions_cryst = [];
  #with open(nsfile, mode='r') as f:
    #lines = [line for line in f.readlines()]
    #for i, line in enumerate(lines):
      #if 'number of atoms/cell      = ' in line:   
	#natom = lines[i].split()[4]; natom = int(natom)
      #if 'site n.     atom                  positions (cryst. coord.)' in line: 
	#for e in range(natom):	
	 #ipositions_cryst.append(lines[i+1].split()[6:9])
	 #i += 1 
	#ipositions_cryst = np.array(ipositions_cryst) 
	#break
  #return ipositions_cryst

##ipositions_cryst = read_ipositions_cryst('scf1.out')
##print ipositions_cryst



### pipe to ase
##from ase import Atoms, units
##from ase.io import write

##lattice, positions = read_cell('scf1.out')
##ipositions_cryst = read_ipositions_cryst('scf1.out')

##atoms = Atoms(symbols='Pr4Co4O12',positions=ipositions_cryst)
##atoms.set_cell(lattice, scale_atoms=False)
##c1 = atoms.get_cell()
##print c1
##c2 = atoms.get_positions()
##print c2 # yanlis okuyo



### draw lattice -------------------------------------------------------------- ###

#lattice, positions = read_cell('scf4.out')
##center_atom = positions[0]


##gs = gridspec.GridSpec(2, 2,
                       ##height_ratios=[3,2] )    
##gs.update(top=0.95, bottom=0.08, left=0.07, right=0.98, hspace=0.3, wspace=0.2)



##ax = plt.subplot(gs[0], projection='3d')

##x1 = [ 0.,  lattice[0,0]]; y1 = [ 0.,  0.]; z1 = [ 0.,  0.]
##x2 = [ 0.,  0.]; y2 = [ 0.,  lattice[1,1]]; z2 = [ 0.,  0.]
##x3 = [ 0.,  0.]; y3 = [ 0.,  0.]; z3 = [ 0.,  lattice[2,2]]

##for i in range(1, 2):
    ##ax.plot(x1[i-1:i+1], y1[i-1:i+1], z1[i-1:i+1], 'r-', linewidth=2)
    ##ax.plot(x2[i-1:i+1], y2[i-1:i+1], z2[i-1:i+1], 'g-', linewidth=2)
    ##ax.plot(x3[i-1:i+1], y3[i-1:i+1], z3[i-1:i+1], 'b-', linewidth=2)  

##ax.plot(positions[:,0], positions[:,1], positions[:,2], 'ko')    
    
##ax.set_xlim3d(0, lattice[0,0]); ax.set_ylim3d(0, lattice[1,1]); ax.set_zlim3d(0, lattice[2,2])




##ax = plt.subplot(gs[1], projection='3d')

##x1 = [ -lattice[0,0]/2,  lattice[0,0]/2]; y1 = [ 0.,  0.]; z1 = [ 0.,  0.]
##x2 = [ 0.,  0.]; y2 = [ -lattice[1,1]/2,  lattice[1,1]/2]; z2 = [ 0.,  0.]
##x3 = [ 0.,  0.]; y3 = [ 0.,  0.]; z3 = [ -lattice[2,2]/2,  lattice[2,2]/2]

##for i in range(1, 2):
    ##ax.plot(x1[i-1:i+1], y1[i-1:i+1], z1[i-1:i+1], 'r-', linewidth=2)
    ##ax.plot(x2[i-1:i+1], y2[i-1:i+1], z2[i-1:i+1], 'g-', linewidth=2)
    ##ax.plot(x3[i-1:i+1], y3[i-1:i+1], z3[i-1:i+1], 'b-', linewidth=2)  

##ax.plot(positions[:,0]-center_atom[0], positions[:,1]-center_atom[1], positions[:,2]-center_atom[2], 'ko')    
    
##ax.set_xlim3d(-lattice[0,0]/2, lattice[0,0]/2); ax.set_ylim3d(-lattice[1,1]/2, lattice[1,1]/2); ax.set_zlim3d(-lattice[2,2]/2, lattice[2,2]/2)





## draw charge -------------------------------------------------------------- ###
#x = np.arange(-lattice[0,0]/2, lattice[0,0]/2, 0.1);
#y = np.arange(-lattice[1,1]/2, lattice[1,1]/2, 0.1);
#z = np.arange(-lattice[2,2]/2, lattice[2,2]/2, 0.1);

#print len(x)

#[X,Y,Z] = np.meshgrid(x,y,z) #(, sparse=True)#http://stackoverflow.com/questions/2460627/memoryerror-when-running-numpy-meshgrid
#Rsq = X**2 + Y**2 + Z**2; R = sqrt(Rsq);
#xx=X/R; yy = Y/R; zz = Z/R;

#rcst=2
#psi_rad = Rsq*rcst*exp(-rcst*R/1);

##  http://en.wikipedia.org/wiki/Table_of_spherical_harmonics
#orb1 = 0.5*(zz*(5*zz**2-3));
#orb2 = -sqrt(3/2)*0.5*xx*(5*zz**2-1); # The negative sign is crucial
#orb3 = -sqrt(3/2)*0.5*yy*(5*zz**2-1); # The negative sign is crucial
#orb4 = 0.5*sqrt(15)*zz*(xx**2-yy**2);
#orb5 = sqrt(15)*xx*yy*zz;
#orb6 = -0.5*sqrt(5/2)*xx*(xx**2-3*yy**2);         #negative sign
#orb7 = -0.5*sqrt(5/2)*yy*(3*xx**2-yy**2);         #negative sigh


##[evalues1,evectors1]=qe_readns(file,atom1,ns1); Lamda1=evalues1; C1 = evectors1;
#eval_up, eval_dw, evec_up, evec_dw  = read_ns_mag('scf4.out',1,1)

##occ_orb1{1} = (C1(1,1)*orb1+C1(2,1)*orb2+C1(3,1)*orb3+C1(4,1)*orb4+C1(5,1)*orb5+C1(6,1)*orb6+C1(7,1)*orb7).*psi_rad;

#occ_orb1 = (evec_up[0,0]*orb1+evec_up[1,0]*orb2+evec_up[2,0]*orb3+evec_up[3,0]*orb4+evec_up[4,0]*orb5+evec_up[5,0]*orb6+evec_up[6,0]*orb7)*psi_rad;
#occ_orb2 = (evec_up[0,1]*orb1+evec_up[1,1]*orb2+evec_up[2,1]*orb3+evec_up[3,1]*orb4+evec_up[4,1]*orb5+evec_up[5,1]*orb6+evec_up[6,1]*orb7)*psi_rad;
#occ_orb3 = (evec_up[0,2]*orb1+evec_up[1,2]*orb2+evec_up[2,2]*orb3+evec_up[3,2]*orb4+evec_up[4,2]*orb5+evec_up[5,2]*orb6+evec_up[6,2]*orb7)*psi_rad;
#occ_orb4 = (evec_up[0,3]*orb1+evec_up[1,3]*orb2+evec_up[2,3]*orb3+evec_up[3,3]*orb4+evec_up[4,3]*orb5+evec_up[5,3]*orb6+evec_up[6,3]*orb7)*psi_rad;
#occ_orb5 = (evec_up[0,4]*orb1+evec_up[1,4]*orb2+evec_up[2,4]*orb3+evec_up[3,4]*orb4+evec_up[4,4]*orb5+evec_up[5,4]*orb6+evec_up[6,4]*orb7)*psi_rad;
#occ_orb6 = (evec_up[0,5]*orb1+evec_up[1,5]*orb2+evec_up[2,5]*orb3+evec_up[3,5]*orb4+evec_up[4,5]*orb5+evec_up[5,5]*orb6+evec_up[6,5]*orb7)*psi_rad;
#occ_orb7 = (evec_up[0,6]*orb1+evec_up[1,6]*orb2+evec_up[2,6]*orb3+evec_up[3,6]*orb4+evec_up[4,6]*orb5+evec_up[5,6]*orb6+evec_up[6,6]*orb7)*psi_rad;



#black = (0,0,0)
#white = (1,1,1)
#mlab.figure(bgcolor=white)
#mlab.plot3d([0, 155], [0, 0], [0, 0], color=black, tube_radius=1.)
#mlab.plot3d([0, 0], [0, 155], [0, 0], color=black, tube_radius=1.)
#mlab.plot3d([0, 0], [0, 0], [0, 155], color=black, tube_radius=1.)
##mlab.text3d(1050, -50, +50, 'X', color=black, scale=100.)
##mlab.text3d(0, 1550, +50, 'Y', color=black, scale=100.)
##mlab.text3d(0, -50, 1550, 'Z', color=black, scale=100.)


## http://stackoverflow.com/questions/24768179/combining-mayavi-and-matplotlib-in-the-same-figure
#mlab.contour3d(occ_orb1**2, contours=[.5])
#mlab.outline()
#mlab.show()

##fig = plt.figure()
##ax = fig.add_subplot(111, projection='3d')


##ax.plot_surface(X,Y,Z,occ_orb5**2)
##plt.show() 

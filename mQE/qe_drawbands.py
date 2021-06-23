#!/usr/bin/python2

import matplotlib
matplotlib.use('Agg') # see http://matplotlib.org/faq/usage_faq.html#what-is-a-backend

import os
import numpy as np
from   pylab import *
import scipy.io as sio
from   matplotlib import gridspec
import mQE


#font = {'family' : 'serif',
        #'weight' : 'bold',
        #'size'   : 12}
font = {'size'   : 8}
matplotlib.rc('font', **font)


#### inputs ><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><> ### |
inputs = sys.argv
ilen   = len(inputs)

if ilen == 1:
  print()
  print("USAGE:    qe_drawbands.py file     ymin ymax custom_shift inputfermi_if_missing ")
  print("DEFAULTS: qe_drawbands.py scf.out -6    6    0            0                     ")  
  print("using DEFAULTS")
  print()  
  inputs.append('scf.out'); inputs.append(-6); inputs.append(6); inputs.append(0); inputs.append(0);   
if ilen == 2:
  inputs.append(-6); inputs.append(6); inputs.append(0); inputs.append(0); 
if ilen == 3:
  inputs.append(6); inputs.append(0); inputs.append(0);
if ilen == 4:
  inputs.append(0); inputs.append(0)
if ilen == 5:
  inputs.append(0)


file   = inputs[1]
ymin   = float(inputs[2])
ymax   = float(inputs[3])
cshift = float(inputs[4])
inpfermi = float(inputs[5])




##### reader ><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><> ### |
#def bands_reader(file):
  #os.system("qe_readscf.py " + file)
  #qe_data = sio.loadmat('.readqe.mat')
  ##os.remove('.readqe.mat')
   
  #efermi = qe_data['efermi']; 
  #params = qe_data['params'];
  #gap_data = qe_data['gap_data']; 
  
  #if not efermi:
    #print("E-fermi from .readqe.mat is empty !!!")
    #print("setting efermi as inputfermi      !!!")
    #print(inpfermi)
    #efermi = inpfermi
    
  #shift=float(efermi+cshift)
  
  #kpoints = qe_data['kpoints']
  #bands_up = qe_data['bands_up']
  #bands_dw = qe_data['bands_dw']
  
  
  #### generate kpts path
  #kpoints_path = []
  #kpoints_path.append(0) 
  
  #for k in range(len(kpoints)-1):
    #k0=kpoints[k];
    #k1=kpoints[k+1];
    #dx=k0[0]-k1[0]; dy=k0[1]-k1[1]; dz=k0[2]-k1[2];
    #newk=kpoints_path[k]+sqrt(dx*dx+dy*dy+dz*dz);
    #kpoints_path.append(newk) 
    
  #return kpoints_path, shift, params, efermi, bands_up, bands_dw, gap_data
  
#kpoints_path, shift, params, efermi, bands_up, bands_dw, gap_data  = bands_reader(file)




if os.path.isfile('qerun.npz') == False:
    mQE.readqe()

readnpz = np.load('qerun.npz')
efermi = readnpz['efermi']
bands_up = readnpz['bands_up']
bands_dw = readnpz['bands_dw']
kpoints = readnpz['kpoints']
qe_params = readnpz['qe_params']


print(qe_params)


### generate kpts path
kpoints_path = []
kpoints_path.append(0) 

for k in range(len(kpoints)-1):
  k0=kpoints[k];
  k1=kpoints[k+1];
  dx=k0[0]-k1[0]; dy=k0[1]-k1[1]; dz=k0[2]-k1[2];
  newk=kpoints_path[k]+sqrt(dx*dx+dy*dy+dz*dz);
  kpoints_path.append(newk) 
  
shift=efermi





#### plot1 ><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><> ### |
gs = gridspec.GridSpec(1, 2,
                       width_ratios=[1,2] )    
gs.update(top=0.97, bottom=0.1, left=0.1, right=0.99, wspace=0.15)


ax1 = plt.subplot(gs[0])
ax1.tick_params(top="off", right="off", direction="out" )


for b in range(len(bands_up)):
  ax1.plot(kpoints_path,bands_up[b]-shift, 'r-', lw=0.5);
  if qe_params[7] == 2.0: 
    ax1.plot(kpoints_path,bands_dw[b]-shift, 'b--', lw=0.5);
  
ax1.plot([ 0, max(kpoints_path) ], [ 0, 0 ], 'k-.',linewidth=0.4)
plt.xticks([]); plt.ylabel('Energy [eV]') 
xlim( (0, max(kpoints_path)) )
ylim( (min(bands_up[0]-shift-1), max(bands_up[len(bands_up)-1]-shift+1)) )
 

#### plot2 ><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><> ### |
ax1 = plt.subplot(gs[1])
ax1.tick_params(top="off", right="off", direction="out" )

for b in range(len(bands_up)):
  ax1.plot(kpoints_path,bands_up[b]-shift, 'r.-', lw=1, mfc='k', ms=3)
  if qe_params[7] == 2.0: 
    ax1.plot(kpoints_path,bands_dw[b]-shift, 'b.-', lw=1, mfc='k', ms=0)
 
ax1.plot([ 0, max(kpoints_path) ], [ 0, 0 ], 'k-.',linewidth=0.4)
plt.xticks([]); plt.ylabel('Energy [eV]') 
xlim( (0, max(kpoints_path)) )
ylim( ymin, ymax )  



#### bandgaps ><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><> ### |
#bandgapstr1 = '$E_{gap}=%.4f$\t$(up)$\n$E_{gap}=%.4f$\t$(dw)$'%(gap_data[0][0], gap_data[0][1])
#bandgapstr2 = '$E_{gap}=%.4f$\t$(%s,up)$\n$E_{gap}=%.4f$\t$(%s,dw)$'%(gap_data[0][2], int(gap_data[0][4]), gap_data[0][3], int(gap_data[0][5]))
#props1 = dict(boxstyle='round', facecolor='red', alpha=0.5)
#ax1.text(0.15, -0.04, bandgapstr1, transform=ax1.transAxes, fontsize=8,
        #verticalalignment='top', bbox=props1)
#props2 = dict(boxstyle='round', facecolor='green', alpha=0.5)
#ax1.text(0.55, -0.04, bandgapstr2, transform=ax1.transAxes, fontsize=8,
        #verticalalignment='top', bbox=props2)



#### export ><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><> ### |
plt.savefig('bands.png', format='png', dpi=200) 
#plt.savefig('bands.eps', format='eps', dpi=200) 





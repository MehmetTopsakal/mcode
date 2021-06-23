#!/home/mt/software/anaconda3/bin/python

import matplotlib
matplotlib.use('Agg') 

from mVASP import readvasp
import os
import numpy as np
from   pylab import *
import scipy.io as sio
from   matplotlib import gridspec
import sys

rcParams['figure.figsize'] =6,6


font = {'size':9}
matplotlib.rc('font', **font)
#savefig('plot.png', format='png', dpi=200) 
#### ========================================================  NOTE: DNR



inputs = sys.argv



for a in range(1,len(inputs)):
    s=inputs[a].split('=')
    if s[0] == 'lr' or 'rl': lr = s[1]
    if s[0] == 'ymin': ymin = float(s[1]) 
    if s[0] == 'ymax': ymax = float(s[1])   
    if s[0] == 'bshift' or s[0] == 'shift' : bshift = float(s[1]) 
    if s[0] == 'lr' : lr = s[1]
    if s[0] == 'file' : file = s[1]    
try:
    ymin
except:
    ymin=-10

try:
    ymax
except:
    ymax=10

try:
    bshift
except:
    bshift=0    

try:
    lr
except:
    lr='r'     

try:
    file
except:
    file='vasprun.xml'      
    
    
    

fig, (ax1) = plt.subplots(1,1)   
subplots_adjust(hspace=0.05)
subplots_adjust(wspace=0.08)
subplots_adjust(top=0.98)
subplots_adjust(bottom=0.07)
subplots_adjust(right=0.95)
subplots_adjust(left=0.12)


ax=ax1
plt.setp( ax.get_xticklabels(), visible=False)
ax.tick_params(top="off", left="on", right="off", direction="out")


#### ========================================================  NOTE: bands
ax.tick_params(top="off", right="on", direction="out" )

# read data


vasp_params, kpoints, kpoints_path, klines_path, poscar0, bands_up, bands_dw,     dos_info, efermi, Edos, tdos, pdos_up, pdos_dw = readvasp(file=file)

# draw vertical lines band structure
for kl in range(1,len(klines_path)-1):
    plt.plot([ klines_path[kl],  klines_path[kl]  ], [ ymin, ymax ], 'k-', linewidth=0.1) 

# draw bands
for b in range(len(bands_up)):
  ax.plot(kpoints_path,bands_up[b]+bshift, 'k-', lw=2, mfc='k', ms=3)
  if vasp_params[2] == 2: 
    ax.plot(kpoints_path,bands_dw[b]+bshift, 'b--', lw=1, mfc='k', ms=0)

## shade band gap
#vband=int(vasp_params[8]/2)
#cband=int((vasp_params[8]/2)+1)
#ax.fill_between(kpoints_path, bands_up[vband-1]-efermi+bshift, 0, lw=0, facecolor='y')
#ax.fill_between(kpoints_path, 0, bands_up[cband-1]-efermi+bshift, lw=0, facecolor='y')



# arrange limits
ax.plot([ 0, max(kpoints_path) ], [ 0, 0 ], 'k-.',linewidth=0.4)
plt.xticks([]); plt.ylabel('Energy (eV)', fontsize=12) 
xlim( (0, max(kpoints_path)) ); ylim( ymin, ymax ) 
#plt.xlabel('( KPOINTS PATH : $\Gamma$  ->   X  ->   S  ->   $\Gamma$  ->   Y )')

#### ========================================================  NOTE: text
test = '$E_{gap}$=%.3f (%.3f) [%.3f (%.3f)]; dir/indir=%d (%d); NSPIN=%d; fermi-cor=%.2f '%(vasp_params[11], vasp_params[12], vasp_params[13], vasp_params[14], vasp_params[15], vasp_params[16], vasp_params[2], vasp_params[17])
props = dict(boxstyle='round', facecolor='silver', alpha=0.5)
ax.text(-0.1, -0.03, test, transform=ax.transAxes, fontsize=10,
        verticalalignment='top', bbox=props)


 
 
 
 

##### ========================================================  NOTE: dos
#ax = plt.subplot(gs1[1])
#ax.tick_params(top="off", right="off", direction="out" )


#ax.fill(tdos_up,Edos,'silver', lw=0, label='tot.')
#if params[2] == 2:
    #ax.fill(tdos_dw,Edos,'silver', lw=0)
#ax.plot([ 0, -6 ], [ 0, 0 ], 'k-.',linewidth=0.4)

## arrange limits
#ax.plot([ -6, 6 ], [ 0, 0 ], 'k-.',linewidth=0.4)
#plt.yticks([]); plt.xlabel('States/eV') 
#xlim( -6, 6 ); ylim( ymin, ymax )  



##### ========================================================  NOTE: pdos
#if len(pdos_up) != 0:

    #Epdos, sumdos, sdos, pdos, ddos, fdos = mVASP.arrangepdos(params,Edos,tdos_up,tdos_dw,pdos_up,pdos_dw,sigma,-1)

    #ax.plot(  sdos[0],Edos-dshift,'m', lw=0.8, label='s')
    #ax.plot(  pdos[0],Edos-dshift,'r', lw=1.0, label='p')
    #ax.plot(  ddos[0],Edos-dshift,'b', lw=1.3, label='d')
    #ax.plot(  fdos[0],Edos-dshift,'c', lw=1.5, label='f')
    #ax.plot(sumdos[0],Edos-dshift,'k', lw=0.4, label='sum')    
    #legend = plt.legend(loc='upper right',fontsize='small', bbox_to_anchor=(1, 0.99))


    #if params[2] == 2:
        #ax.plot(  sdos[1],Edos-dshift,'m', lw=0.8, label='s')
        #ax.plot(  pdos[1],Edos-dshift,'r', lw=1.0, label='p')
        #ax.plot(  ddos[1],Edos-dshift,'b', lw=1.3, label='d')
        #ax.plot(  fdos[1],Edos-dshift,'c', lw=1.5, label='f')
        #ax.plot(sumdos[1],Edos-dshift,'k', lw=0.4, label='sum')

    #xlim( dxmin, dxmax ); ylim( ymin, ymax ) 





#### ========================================================  NOTE: export
plt.savefig('bands.eps', format='eps', dpi=200) 





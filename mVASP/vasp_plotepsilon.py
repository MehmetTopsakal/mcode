#!/usr/bin/python2

import matplotlib
matplotlib.use('Agg') # see http://matplotlib.org/faq/usage_faq.html#what-is-a-backend

import numpy as np
from   pylab import *
from   matplotlib import gridspec
import operator
import scipy.io as sio
import numpy as np


font = {'size':10}
matplotlib.rc('font', **font)
#savefig('plot.png', format='png', dpi=200) 
#### ========================================================  NOTE: DNR




#### ========================================================  NOTE: inputs
inputs = sys.argv
ilen   = len(inputs)

if ilen == 1:
  inputs.append('1'); inputs.append(10); inputs.append(20); inputs.append('vasprun.xml'); 
if ilen == 2:
  inputs.append(10); inputs.append(20); inputs.append('vasprun.xml');
if ilen == 3:
  inputs.append(20); inputs.append('vasprun.xml');
if ilen == 4:
  inputs.append('vasprun.xml');  

key  = int(inputs[1])
maxx = float(inputs[2])
maxy = float(inputs[3])
file = inputs[4]




#### ========================================================  NOTE: defs
def readvasprun(file,text_to_search):
  E  = []; imag = [];  real = [];
  with open(file, mode='r') as f:
    lines = [line for line in f.readlines()]
    for i, line in enumerate(lines):
      
      if text_to_search in line:
	while True:
	    t = lines[i+12].split(); #print t
	    if len(t) == 1: break	    
	    imag.append(lines[i+12].split()[2:5])
	    E.append(lines[i+12].split()[1])
	    i = i+1

	while True:
	    t = lines[i+12+14].split(); #print t
	    if len(t) == 1: break	    
	    real.append(lines[i+12+14].split()[2:5])
	    i = i+1

    E = np.array(E).astype(np.float); imag = np.array(imag).astype(np.float); real = np.array(real).astype(np.float) 	 
    return E, imag, real



  	 
#### ========================================================  NOTE: read

if key == 1:
  text_to_search='<dielectricfunction>'
  title='(independent particle, no local field effects)'  
  
if key == 2:
  text_to_search='HEAD OF MICROSCOPIC DIELECTRIC TENSOR (INDEPENDENT PARTICLE)'  
  title='( HEAD OF MICROSCOPIC DIELECTRIC TENSOR (INDEPENDENT PARTICLE) )'   
  
if key == 3:
  text_to_search='1 + v P,  with REDUCIBLE POLARIZABILTY P=P_0 (1 -(v+f) P_0)^-1'  
  title='( 1 + v P,  with REDUCIBLE POLARIZABILTY P=P_0 (1 -(v+f) P_0)^-1 )' 
  
if key == 4:
  text_to_search='INVERSE MACROSCOPIC DIELECTRIC TENSOR (including local field effects in RPA (Hartree)'  
  title='( INVERSE MACROSCOPIC DIELECTRIC TENSOR (including local field effects in RPA (Hartree) )' 
  
if key == 5:
  text_to_search='INVERSE MACROSCOPIC DIELECTRIC TENSOR (test charge-test charge, local field effects in DFT)'  
  title='( INVERSE MACROSCOPIC DIELECTRIC TENSOR (test charge-test charge, local field effects in DFT) )'   
  
  
E, imag, real = readvasprun(file,text_to_search)


if len(E) == 0:
  print('ERROR !!!! Unable to read dielectric constant information....', file=sys.stderr)
  print("Exception: %s" % str(1), file=sys.stderr)
  sys.exit(1)
  
  
de=float(E[1])-float(E[0]);
print('Energy grid size is '+str(de)+' eV')



#### ========================================================  NOTE: plot  
gs = gridspec.GridSpec(2, 1 )    
gs.update(top=0.95, bottom=0.13, left=0.1, right=0.98, hspace=0.15)



ax1 = plt.subplot(gs[0]); ax1.tick_params(top="off", right="off", direction="out" ); ax1.grid(True) 
plt.title(title, fontsize=10)


ax1.plot(E,real[:,0], 'r-', ms=6, lw=3, label='x')
ax1.plot(E,real[:,1], 'g-', ms=5, lw=2, label='y')
ax1.plot(E,real[:,2], 'b-', ms=5, lw=2, label='z')
ax1.plot(E,np.sum(real,axis=1)/3, 'k--', ms=5, lw=2, label='(x+y+z)/3')

legend = plt.legend(loc='upper right')
plt.ylabel(r'$\epsilon^{(1)} (\omega)$')
xlim( (0, maxx) ); #ylim( float(min(peaks)), float(max(peaks)) )

ax1 = plt.subplot(gs[1]); ax1.tick_params(top="off", right="off", direction="out" ); ax1.grid(True) 


ax1.plot(E,imag[:,0], 'r-', ms=6, lw=3, label='x')
ax1.plot(E,imag[:,1], 'g-', ms=5, lw=2, label='y')
ax1.plot(E,imag[:,2], 'b-', ms=5, lw=2, label='z')
ax1.fill(E,np.sum(imag,axis=1), 'y--', lw=0.5, label='(x+y+z)')
plt.xticks(np.arange(0,55,maxx/10)) ; plt.yticks(np.arange(0,100,maxy/10)) ; 

legend = plt.legend(loc='upper right')
plt.xlabel(r'$\omega$ [eV]')
plt.ylabel(r'$\epsilon^{(2)} (\omega)$')
xlim( (0, maxx) ); ylim( (0, maxy) )


plt.savefig('epsilon_'+str(key)+'.pdf', format='pdf', dpi=600) 

sio.savemat('dielectric.mat', dict(E=E, real=real, imag=imag)) #http://docs.scipy.org/doc/scipy-0.14.0/reference/tutorial/io.html

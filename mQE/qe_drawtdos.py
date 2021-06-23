#!/usr/bin/python2

import os    
import sys
import scipy.io as sio
import pylab as pyl
import numpy as np
import itertools as it 
from   io import StringIO
from   pylab import *
from   matplotlib import gridspec
from   matplotlib.widgets import MultiCursor

import mQE
import mSMOOTH

#font = {'family' : 'serif',
        #'weight' : 'bold',
        #'size'   : 12}
font = {'size'   : 8}
matplotlib.rc('font', **font)




### inputs ------------------------------------------------------------- |
inputs = sys.argv
ilen   = len(inputs)

if ilen == 1:
  inputs.append('r'); inputs.append("-6"); inputs.append("6"); inputs.append("-6"); inputs.append("6"); inputs.append("0.1"); inputs.append("0");
if ilen == 2:
  inputs.append("-6"); inputs.append("6"); inputs.append("-6"); inputs.append("6"); inputs.append("0.1"); inputs.append("0");
if ilen == 3:
  inputs.append("6"); inputs.append("-6"); inputs.append("6"); inputs.append("0.1"); inputs.append("0");  
if ilen == 4:
  inputs.append("-6"); inputs.append("6"); inputs.append("0.1"); inputs.append("0");  
if ilen == 5:
  inputs.append("6"); inputs.append("0.1"); inputs.append("0");  
if ilen == 6:
  inputs.append("0.1"); inputs.append("0");    
if ilen == 7:
  inputs.append("0");  

lr      = inputs[1]
minx    = float(inputs[2])
maxx    = float(inputs[3])
miny    = float(inputs[4])
maxy    = float(inputs[5])
sigma   = float(inputs[6])
shift   = float(inputs[7])






if os.path.isfile('qerun.npz') == False:
    mQE.readqe()

readnpz = np.load('qerun.npz')
efermi = readnpz['efermi']
Etdos = readnpz['Etdos']

tdos = readnpz['tdos']
#E = tdos[0]
tu = tdos[0]
td = tdos[1]

print(Etdos)





  
  
### plot ------------------------------------------------------------- |   
gs = gridspec.GridSpec(2, 1,
                       height_ratios=[1,3] )    
gs.update(top=0.98, bottom=0.08, left=0.1, right=0.98, hspace=0.14)


x1 = Etdos-efermi-shift ; x2 = x1
y1 = tu ; y2 = -td 
x1s, y1s = mSMOOTH.Gaussian_old(x1,y1,sigma,0) ; y1s[0]=0 ; y1s[len(y1s)-1]=0
x2s, y2s = mSMOOTH.Gaussian_old(x2,y2,sigma,0) ; y2s[0]=0 ; y2s[len(y2s)-1]=0
 
ax1 = plt.subplot(gs[0])
ax1.tick_params(top="off", right="off", direction="out" )
ax1.plot(x1,y1, 'r.-')
ax1.plot(x2,y2, 'r.-')
ax1.plot(x1s,y1s, 'b-')
ax1.plot(x2s,y2s, 'b-')
ax1.plot([ -200, 100 ], [ 0, 0 ], 'k-')
ax1.plot([ 0, 0 ], [ -800, 800 ], 'k-')
xlim( (min(x1s), max(x1s)) )
ylim( (min(y2s), max(y1s)) )
plt.ylabel('States/eV')


ax2 = plt.subplot(gs[1])
ax2.tick_params(top="off", right="off", direction="out" )  
#ax2.plot(x1,y1, 'r.-')
#ax2.plot(x2,y2, 'r.-')
ax2.fill(x1s,y1s,'silver')
ax2.fill(x2s,y2s,'silver')
ax2.grid(True)  
ax2.plot([ -200, 100 ], [ 0, 0 ], 'k-', linewidth=1.2)
ax2.plot([ 0, 0 ], [ -800, 800 ], 'k-', linewidth=1.2)
xlim( (minx, maxx) )
ylim( (miny, maxy) )
plt.xlabel('Energy (eV)')
plt.ylabel('States/eV')
  
savefig('dos.png', format='png', dpi=300)
  








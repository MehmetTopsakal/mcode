import matplotlib
matplotlib.use('Agg')

import numpy as np
import os,sys
import subprocess as sp 

from pylab import *
from matplotlib import gridspec
from matplotlib import pyplot as plt



# =================================================================== 
inputs = sys.argv

for a in range(len(inputs)):
    s=inputs[a].split('=')
    if s[0]   == 'lr  '   or s[0] == 'RL'   : lr = s[1]
    elif s[0] == 'xmin'   or s[0] == 'min'  : xmin  = float(s[1]) 
    elif s[0] == 'xmax'   or s[0] == 'max'  : xmax  = float(s[1]) 



try:
    lr
except:
    lr = 'r'
    
    


file='exciting.npz'
if not os.path.exists(file):
    sp.call(' mpy exciting_readdosagr.py ', shell=True)
elif lr == 'r':
    sp.call(' mpy exciting_readdosagr.py ', shell=True)
    
    

readnpz = np.load(file)
E = readnpz['E']; E=E*2*13.605698066
tdos = readnpz['tdos']
intdos = readnpz['intdos']
pdoss = readnpz['pdoss']

print(E[-1]-E[0])

try:
    xmin
except:
    xmin = E[0]

try:
    xmax
except:
    xmax = E[-1]



sel = (E > xmin) & (E < xmax)
E = E[sel]
tdos = tdos[sel]
intdos = intdos[sel]





from matplotlib import gridspec
fig = plt.figure(figsize=(6,6))
gs = gridspec.GridSpec(2, 1, width_ratios=[1] )
gs.update(top=0.97, bottom=0.04, left=0.1, right=0.98, wspace=0.0, hspace=0.0)




ax = fig.add_subplot(gs[0])
ax.plot(E, tdos, 'rs-', lw=1, ms=2, alpha=0.6, label='total')
ax.plot(E, intdos, 'bo-', lw=1, ms=2, alpha=0.6, label='interstitial')
ax.plot([0,0],[0,max(tdos)*1.05], 'k:', lw=0.5)


ax.set_xlim([xmin,xmax])
ax.set_ylim([0,max(tdos)*1.05])


savefig('dos.png', format='png', dpi=300)

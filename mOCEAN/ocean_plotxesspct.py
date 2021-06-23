#!/usr/bin/python

import matplotlib
matplotlib.use('Agg') # see http://matplotlib.org/faq/usage_faq.html#what-is-a-backend
import numpy as np
from pylab import *

import mOCEAN


from pylab import rcParams
rcParams['figure.figsize'] =6,8

font = {\
    'weight' : 'bold',
    'size'   : 8
    }
matplotlib.rc('font', **font)


     





 
fig, (ax1,ax2) = plt.subplots(2,1,sharex=False)   
subplots_adjust(hspace=0.2)
subplots_adjust(wspace=0.2)
subplots_adjust(top=0.98)
subplots_adjust(bottom=0.11)
subplots_adjust(right=0.95)
subplots_adjust(left=0.2)



E, Itot, Iatom, Iall = mOCEAN.read_xesspct(xesfile='ocean_xesspcts.dat')


## ============================================================================
ax = ax1
plt.setp( ax.get_yticklabels(), visible=False)
ax.tick_params(top="off", left="off", right="off", direction="out")

ax.plot(E, Itot, 'r-', lw=3, ms=2, alpha=0.6, label='tot')
ax.set_xlabel('Energy [eV]', fontsize=15)
ax.set_ylabel('XAS', fontsize=15)
ax.legend(loc='upper center', bbox_to_anchor=(0.85, 0.8), ncol=1, fontsize='large', fancybox=True, shadow=True)



## ============================================================================
ax = ax2
plt.setp( ax.get_yticklabels(), visible=False)
ax.tick_params(top="off", left="off", right="off", direction="out")

for i in range(len(Iatom)):
    ax.plot(E, Iatom[i], label='atom #'+str(i+1))
    
ax.set_xlabel('Energy [eV]', fontsize=15)
ax.set_ylabel('XAS', fontsize=15)
ax.legend(loc='upper center', bbox_to_anchor=(0.8, 0.95), ncol=1, fontsize='large', fancybox=True, shadow=True)



savefig('xesspct.png', format='png', dpi=300)


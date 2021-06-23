#!/usr/bin/python

import matplotlib
matplotlib.use('Agg') # see http://matplotlib.org/faq/usage_faq.html#what-is-a-backend
import numpy as np
from pylab import *

import mFEFF

from pylab import rcParams
rcParams['figure.figsize'] =8,12

font = {\
    'weight' : 'bold',
    'size'   : 8
    }
matplotlib.rc('font', **font)








 
fig, (ax1,ax2,ax3) = plt.subplots(3,1,sharex=False)   
subplots_adjust(hspace=0.20)
subplots_adjust(wspace=0.05)
subplots_adjust(top=0.98)
subplots_adjust(bottom=0.11)
subplots_adjust(right=0.95)
subplots_adjust(left=0.08)


plt.setp( ax1.get_yticklabels(), visible=False)
ax1.tick_params(top="off", left="off", right="off", direction="out")





## ============================================================================
ax = ax1
Ef, mu = mFEFF.read_xmu('xmu.dat')
ax.plot(Ef, mu, 'ko-', lw=3, ms=2, alpha=0.6)
ax.set_xlabel('Energy [eV]', fontsize=15)
ax.set_ylabel('XANES', fontsize=15)





## ============================================================================
ax = ax2
Ed, sd, pd, dd, fd = mFEFF.read_ldos('ldos00.dat')
ax.plot(Ed, sd, 'r-', lw=3, alpha=0.6)
ax.plot(Ed, pd, 'g-', lw=3, alpha=0.6)
#ax.plot(Ed, dd, 'b-', lw=3, alpha=0.6)
#ax.set_xlabel('Energy [eV]', fontsize=15)
ax.set_ylabel('ldos00', fontsize=15)




## ============================================================================
ax = ax3
Ed, sd, pd, dd, fd = mFEFF.read_ldos('ldos02.dat')
ax.plot(Ed, sd, 'r-', lw=3, alpha=0.6)
ax.plot(Ed, pd, 'g-', lw=3, alpha=0.6)
#ax.plot(Ed, dd, 'b-', lw=3, alpha=0.6)
ax.set_xlabel('Energy [eV]', fontsize=15)
ax.set_ylabel('ldos01', fontsize=15)








savefig('xmu+ldos.png', format='png', dpi=300)


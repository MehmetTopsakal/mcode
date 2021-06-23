#!/usr/bin/python

import matplotlib
matplotlib.use('Agg') # see http://matplotlib.org/faq/usage_faq.html#what-is-a-backend

import os
import sys
from   pylab import *
import numpy as np
import mFIT



font = {'size':5,'weight':'bold'}
matplotlib.rc('font', **font)

from pylab import rcParams
rcParams['figure.figsize'] = 4, 3







#### ========================================================  NOTE: inputs
inputs = sys.argv
ilen   = len(inputs)

if ilen == 1:
    print('Error: input file is not given !!!')
    exit()   
if ilen == 2:
    inputs.extend([1,2,1])
if ilen == 3:
    inputs.extend([2,1])
if ilen == 4:
    inputs.extend([1])
      
    
ifile   = inputs[1]
colx    = int(inputs[2])
coly    = int(inputs[3])
savekey = int(inputs[4])






#### ========================================================  NOTE: readdata
values = np.loadtxt(ifile, unpack=True, comments='%', usecols=(colx-1,coly-1), skiprows=0)

   
#### ========================================================  NOTE: plot
xd, yd, x0, y0, res, xf, yf = mFIT.polyfit3(values,savekey)
dx=(max(xd)-min(xd))/15; dy1=(max(yd)-min(yd))/15; dy2=(max(yd-y0)-min(yd-y0))/15

fig, ax1 = plt.subplots()
ax1.plot(xf,yf,'r-' )
ax1.plot(xd,yd,'ro', )
ax1.plot(x0,y0,'b.', ms=6 )
ax1.set_ylim(min(yd)-dy1, max(yd)+dy1);

ax2 = ax1.twinx()
ax2.plot(xf,yf-x0,'r-' )
ax2.plot(xd,yd-x0,'ro', )
ax2.plot(x0,y0-x0,'b.', ms=6 )
ax2.set_xlim(min(xd)-dx, max(xd)+dx);
ax2.set_ylim(min(yd-y0)-dy2, max(yd-y0)+dy2);
ax2.plot([ min(xd)-dx,  max(xd)+dx ], [ 0, 0 ], 'k-',linewidth=0.4)

text = 'x$_{min}$=%.6f ; y$_{min}$=%.6f  ; res=%.4f ' %(x0, y0, res)
props = dict(boxstyle='round', facecolor='red', alpha=0.5)
ax2.text(0.22, 1.07, text, transform=ax1.transAxes, fontsize=5,
        verticalalignment='top', bbox=props)

savefig('mfit.png', format='png', dpi=300)

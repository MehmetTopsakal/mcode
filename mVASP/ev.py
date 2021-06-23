#!/usr/bin/python

import matplotlib
matplotlib.use('Agg') # see http://matplotlib.org/faq/usage_faq.html#what-is-a-backend

import sys
import numpy as np
from sys import argv
from pylab import *
import os


#font = {'size':8}
#matplotlib.rc('font', **font)
#savefig('plot.png', format='png', dpi=200) 
#### ========================================================  NOTE: DNR





#!/usr/bin/env python

import numpy as np


### USAGE:
### import mBM,numpy
### data = np.loadtxt('ev.in', usecols=(0, 1))
### v0, e0, b0, bp, res, vd, ed, vf, ef, pf = mBM.makefit(data,1,1)
### 
### 
### 
#### ========================================================
def makefit(data,formatkey,savekey):

    if formatkey == 0:
        VV = data[:,0]/6.7483330416152265
        EE = data[:,1]*13.605698066 
    else:
        VV = data[:,0]
        EE = data[:,1]
        print('Attention : NOT converting "a.u.^3 > A^3"  "Ry > eV" ')

    fitdata = np.polyfit(VV**(-2./3.), EE, 3, full=True)

    ssr = fitdata[1]
    sst = np.sum((EE - np.average(EE))**2.)
    residuals0 = ssr/sst
    deriv0 = np.poly1d(fitdata[0])
    deriv1 = np.polyder(deriv0, 1)
    deriv2 = np.polyder(deriv1, 1)
    deriv3 = np.polyder(deriv2, 1)

    volume0 = 0
    x = 0
    for x in np.roots(deriv1):
        if x > 0 and deriv2(x) > 0:
            volume0 = x**(-3./2.)
            energy0 = fitdata[0][0]*x*x*x + fitdata[0][1]*x*x + fitdata[0][2]*x + fitdata[0][3]
            break

    if volume0 == 0:
        print('Error: No minimum could be found')
        exit()

    derivV2 = 4./9. * x**5. * deriv2(x)
    derivV3 = (-20./9. * x**(13./2.) * deriv2(x) -
        8./27. * x**(15./2.) * deriv3(x))
    
    echarge = 1.60217733e-19 ; unitconv = echarge * 1.0e21
    
    bulk_modulus0 = unitconv * derivV2 / x**(3./2.)
    bulk_deriv0 = -1 - x**(-3./2.) * derivV3 / derivV2
    
    vfit = np.linspace(min(VV),max(VV),500); 
    vv = (volume0 / vfit) ** (2. / 3)
    ff = vv - 1.0
    efit = energy0 + 9. * (bulk_modulus0 / unitconv) * volume0 / 16.0 * (ff ** 3 * bulk_deriv0+ (6.0 - 4.0 * vv) * ff ** 2)
    pfit = 3. * (bulk_modulus0) / 2. * ((volume0 / vfit) ** (7. / 3) - (volume0 / vfit) ** (5. / 3)) * (1 + 3. * ff * (bulk_deriv0 - 4) / 4.)

    v0, e0, b0, bp, res, vd, ed, vf, ef, pf =  volume0, energy0, bulk_modulus0, bulk_deriv0, residuals0, VV, EE, vfit, efit, pfit
    
    if savekey == 1:
        out = open('ev.out',"w")
        print('#   Vo       Eo                 Bo            Bp        res.  \n', end=' ', file=out) 
        print('%12.5f' %(v0),  '%12.5f' %(e0),  '%12.3f' %(b0),  '%12.3f' %(bp),  '%12.6f' %(res), file=out)
        out.close()
        
    if savekey == 2:
        np.savez('ev.npz', v0=v0, e0=e0, b0=b0, bp=bp, res=res, vd=vd, ed=ed, vf=vf, ef=ef, pf=pf)
        
    print('%12.5f' %(v0),  '%12.5f' %(e0),  '%12.3f' %(b0),  '%12.3f' %(bp),  '%12.6f' %(res), '# Vo Eo Bo Bp res.')
    return v0, e0, b0, bp, res, vd, ed, vf, ef, pf















os.remove('ev.npz') if os.path.exists('ev.npz') else None
os.remove('ev.eps') if os.path.exists('ev.eps') else None
os.remove('ev.out') if os.path.exists('ev.out') else None



# ### inputs  ^
inputs = sys.argv
ilen   = len(inputs)

if ilen == 1:
    inputs.extend(['ev.in',0,1])
if ilen == 2:
    inputs.extend([0,1])
if ilen == 3:
    inputs.extend([1])
    
evin      = inputs[1]
formatkey = int(inputs[2])
savekey   = int(inputs[3])





data = np.loadtxt(evin, usecols=(0, 1))
v0, e0, b0, bp, res, vd, ed, vf, ef, pf = makefit(data,formatkey,savekey)






#### ========================================================  NOTE: plot and savefig
ax1 = subplot(211); ax1.tick_params(top="off", right="off", direction="out"); ax1.grid(True)

ax1.plot(vf, ef - e0 , 'r-', lw=1.5, label='B-M fit')
ax1.plot(vd, ed - e0 , 'go', ms=6,   label='calc.')
ax1.plot(v0, 0, 'bo', markersize=4)

dx = (max(vf) - min(vf)) / 15; dy = (max(ef) - min(ef)) / 15
xlim((min(vf) - dx, max(vf) + dx)) ; ylim((min(ef- e0) - dy, max(ef- e0) + dy))
xlabel(r'Volume [$\AA^3 $]'); ylabel(r'$E-E_0 $ [eV]')

legend(loc='upper center', fontsize='small')


text = '$V_{min}$=%.4f $\AA^3$ (%.4f $a.u.^3$) ; $E_{min}$=%.6f eV (%.6f Ry) ; $B_{0}$=%.2f GPa ; $B^{,}$=%.2f ; res=%.6f  '%(v0,v0*6.74833449394997,e0,e0/13.60569253,b0,bp,res)
props = dict(boxstyle='round', facecolor='red', alpha=0.3)
ax1.text(-0.10, 1.15, text, transform=ax1.transAxes, fontsize=6, verticalalignment='top', bbox=props)




# --------------------------------------------------
ax2 = subplot(325); ax2.tick_params(top="off", right="off", direction="out"); ax2.grid(True)

ax2.plot(ef - e0 , vf, 'r-', label='B-M fit')
ax2.plot(ed - e0 , vd, 'go', markersize=4, label='calc.')
ax2.plot(0, v0, 'bo', markersize=3)

dy = (max(vf) - min(vf)) / 15; dx = (max(ef) - min(ef)) / 15
ylim((min(vf) - dy, max(vf) + dy)) ; xlim((min(ef- e0) - dx, max(ef- e0) + dx))
ylabel(r'Volume [$\AA^3$]'); 
xlabel(r'$E-E_0 $ [eV]')
tick_params(labelsize=8)


# -------------------------------------------------
ax3 = subplot(326, sharey=ax2); setp( ax3.get_yticklabels(), visible=False)
ax3.tick_params(top="off", right="off", direction="out"); ax3.grid(True)

ax3.plot( pf , vf, 'b-', label='B-M fit')
ax3.plot(0, v0, 'ro', markersize=3)

dy = (max(vf) - min(vf)) / 15; dx = (max(pf) - min(pf)) / 15
ylim((min(vf) - dy, max(vf) + dy)) ; xlim((min(pf) - dx, max(pf) + dx))
xlabel(r'$P $ [GPa]')
tick_params(labelsize=8)



#subplots_adjust(hspace=0)
#subplots_adjust(wspace=0.1)


# -------------------------------------------------
savefig('ev.png', format='png', dpi=200) 



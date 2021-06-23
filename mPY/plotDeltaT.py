#!/usr/bin/python2

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




#### ========================================================  NOTE: inputs
inputs = sys.argv
ilen   = len(inputs)

if ilen == 1:
    print('USAGE : plotDelta.py 4 ../WIEN 0.78 1.06')
    inputs.extend([4,'../WIEN',0.78,1.06])
if ilen == 2:
    inputs.extend(['../WIEN',0.78,1.06])
if ilen == 3:
    inputs.extend([0.78,1.06])
if ilen == 4:
    inputs.extend([1.06])

here          = os.getcwd()
folderp       = os.getcwd()
natom         = int(inputs[1])  
folderw       = inputs[2]
range_min     = float(inputs[3])
range_max     = float(inputs[4])

if ilen == 1:
    print('      : using default inputs : '+str(inputs))   

#### ========================================================  NOTE:  defs
# adapted from Delta_v3-0 package off Ugent
def BM(data,formatkey,savekey,natom):

    if formatkey == 0:
        VV = data[:,0]/(natom*6.74833449394997)
        EE = data[:,1]*13.60569253/natom
    else:
        VV = data[:,0]/natom
        EE = data[:,1]/natom
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
    
    vfit = np.linspace(min(VV),max(VV),400); 
    vv = (volume0 / vfit) ** (2. / 3)
    ff = vv - 1.0
    efit = energy0 + 9. * (bulk_modulus0 / unitconv) * volume0 / 16.0 * (ff ** 3 * bulk_deriv0+ (6.0 - 4.0 * vv) * ff ** 2)
    pfit = 3. * (bulk_modulus0) / 2. * ((volume0 / vfit) ** (7. / 3) - (volume0 / vfit) ** (5. / 3)) * (1 + 3. * ff * (bulk_deriv0 - 4) / 4.)

    v0, e0, b0, b1, res, vd, ed, vf, ef, pf =  volume0, energy0, bulk_modulus0, bulk_deriv0, round(residuals0,7), VV, EE, vfit, efit, pfit
    
    if savekey == 1:
        np.savez('ev.npz', v0=v0, e0=e0, b0=b0, b1=b1, res=res, vd=vd, ed=ed, vf=vf, ef=ef, pf=pf)

    return v0, e0, b0, b1, res, vd, ed, vf, ef, pf



def calcDelta(v0w,b0w,b1w,v0p,b0p,b1p,range_min,range_max):


    b0w = b0w * 10.**9. / 1.602176565e-19 / 10.**30.0
    b0p = b0p * 10.**9. / 1.602176565e-19 / 10.**30.0   
    
    # ATTENTION: KL default is False !!!!!
    useasymm  = True     

    vref = 30.
    bref = 100. * 10.**9. / 1.602176565e-19 / 10.**30.

    if useasymm:
        Vi = range_min * v0w
        Vf = range_max * v0w
    else:
        Vi = range_min * (v0w + v0p) / 2.
        Vf = range_max * (v0w + v0p) / 2.

    a3f = 9. * v0p**3. * b0p / 16. * (b1p - 4.)
    a2f = 9. * v0p**(7./3.) * b0p / 16. * (14. - 3. * b1p)
    a1f = 9. * v0p**(5./3.) * b0p / 16. * (3. * b1p - 16.)
    a0f = 9. * v0p * b0p / 16. * (6. - b1p)

    a3w = 9. * v0w**3. * b0w / 16. * (b1w - 4.)
    a2w = 9. * v0w**(7./3.) * b0w / 16. * (14. - 3. * b1w)
    a1w = 9. * v0w**(5./3.) * b0w / 16. * (3. * b1w - 16.)
    a0w = 9. * v0w * b0w / 16. * (6. - b1w)

    x = [0, 0, 0, 0, 0, 0, 0]

    x[0] = (a0f - a0w)**2
    x[1] = 6. * (a1f - a1w) * (a0f - a0w)
    x[2] = -3. * (2. * (a2f - a2w) * (a0f - a0w) + (a1f - a1w)**2.)
    x[3] = -2. * (a3f - a3w) * (a0f - a0w) - 2. * (a2f - a2w) * (a1f - a1w)
    x[4] = -3./5. * (2. * (a3f - a3w) * (a1f - a1w) + (a2f - a2w)**2.)
    x[5] = -6./7. * (a3f - a3w) * (a2f - a2w)
    x[6] = -1./3. * (a3f - a3w)**2.

    y = [0, 0, 0, 0, 0, 0, 0]

    y[0] = (a0f + a0w)**2 / 4.
    y[1] = 3. * (a1f + a1w) * (a0f + a0w) / 2.
    y[2] = -3. * (2. * (a2f + a2w) * (a0f + a0w) + (a1f + a1w)**2.) / 4.
    y[3] = -(a3f + a3w) * (a0f + a0w) / 2. - (a2f + a2w) * (a1f + a1w) / 2.
    y[4] = -3./20. * (2. * (a3f + a3w) * (a1f + a1w) + (a2f + a2w)**2.)
    y[5] = -3./14. * (a3f + a3w) * (a2f + a2w)
    y[6] = -1./12. * (a3f + a3w)**2.

    Fi = np.zeros_like(Vi)
    Ff = np.zeros_like(Vf)

    Gi = np.zeros_like(Vi)
    Gf = np.zeros_like(Vf)

    for n in range(7):
        Fi = Fi + x[n] * Vi**(-(2.*n-3.)/3.)
        Ff = Ff + x[n] * Vf**(-(2.*n-3.)/3.)

        Gi = Gi + y[n] * Vi**(-(2.*n-3.)/3.)
        Gf = Gf + y[n] * Vf**(-(2.*n-3.)/3.)

    Delta = 1000. * np.sqrt((Ff - Fi) / (Vf - Vi))
    Deltarel = 100. * np.sqrt((Ff - Fi) / (Gf - Gi))
    if useasymm:
        Delta1 = 1000. * np.sqrt((Ff - Fi) / (Vf - Vi)) \
                 / v0w / b0w * vref * bref
    else: 
        Delta1 = 1000. * np.sqrt((Ff - Fi) / (Vf - Vi)) \
                 / (v0w + v0p) / (b0w + b0p) * 4. * vref * bref

    return Delta, Deltarel, Delta1 # from left to right: Delta [meV/atom] - relative Delta [%] - Delta1 [meV/atom]








#### ========================================================  NOTE: read
os.chdir(folderw)
data = np.loadtxt('ev.in', usecols=(0, 1))
v0w, e0w, b0w, b1w, resw, vdw, edw, vfw, efw, pfw = BM(data,0,0,natom)
os.chdir(here)


os.chdir(folderp)
data = np.loadtxt('ev.in', usecols=(0, 1))
v0p, e0p, b0p, b1p, resp, vdp, edp, vfp, efp, pfp = BM(data,0,0,natom)
os.chdir(here)







#### ========================================================  NOTE: calc. delta

# My delta -----------------------------------
diff = (efw - e0w)-(efp - e0p)

area = 0; dV = vfw[1]-vfw[0]
for i in range(len(vfw)):
    area = (area + dV*abs(diff[i]))

delta = 1000*area/((max(vfw)-min(vfw)))


# Ugent delta -----------------------------------
Delta, Deltarel, Delta1 = calcDelta(v0w,b0w,b1w,v0p,b0p,b1p,range_min,range_max)



print()
print('delta = '+str(delta)+' ; Delta = '+str(Delta))
print()


#### ========================================================  NOTE: plots

# ----------------------------------------------
ax1 = subplot(211); 
ax1.tick_params(top="off", right="off", direction="out"); ax1.grid(True)
setp( ax1.get_xticklabels(), visible=False)

ax1.plot(vfw, efw - e0w, 'r-', lw=1.5, label='WIEN2K')
ax1.plot(vfp, efp - e0p, 'b-', lw=1.5, label='pseudo')
legend(loc='upper right', fontsize='small')
ylabel(r'Energy [eV/atom]')
dx = (max(vfw) - min(vfw)) / 15; xlim((min(vfw) - dx, max(vfw) + dx)); 
dy = (max(efw - e0w) - min(efw - e0w)) / 15; ylim((min(efw - e0w) - dy, max(efw - e0w) + dy));


ax2 = subplot(212, sharex=ax1); 
ax2.tick_params(top="off", right="off", direction="out"); ax2.grid(True)
ax2.fill_between(vfw, diff*1000 , 0 ,  lw=0.1, facecolor='y')
ylabel(r'WIEN2k-pseudo [meV]')
xlabel(r'Volume [$\AA^3$/atom]');
dx = (max(vfw) - min(vfw)) / 15; xlim((min(vfw) - dx, max(vfw) + dx)); 
dy = (max(diff*1000) - min(diff*1000)) / 15; ylim((min(diff*1000) - dy, max(diff*1000) + dy));


subplots_adjust(hspace=0.1)
subplots_adjust(wspace=0.1)




# ----------------------------------------------
text1 = 'WIEN2K : $V_{min}$=%.4f $\AA^3$ $B_{0}$=%.2f GPa $B^{,}$=%.2f ; res=%.6f \n pseudo : $V_{min}$=%.4f $\AA^3$ $B_{0}$=%.2f GPa $B^{,}$=%.2f ; res=%.6f '%(v0w,b0w,b1w,resw,v0p,b0p,b1p,resp)
props = dict(boxstyle='round', facecolor='red', alpha=0.3)
ax1.text(-0.10, 1.235, text1, transform=ax1.transAxes, fontsize=8, verticalalignment='top', bbox=props)

text2 = ' Area = %.1f ($meV\\times\AA^3$) '%(area*1000)
props = dict(boxstyle='round', facecolor='yellow', alpha=0.8)
ax1.text(0.55, 1.23, text2, transform=ax1.transAxes, fontsize=8, verticalalignment='top', bbox=props)

text3 = ' $\Delta_{MT}$ = %.2f ($meV/at.$) '%(delta)
props = dict(boxstyle='round', facecolor='magenta', alpha=0.5)
ax1.text(0.80, 1.23, text3, transform=ax1.transAxes, fontsize=8, verticalalignment='top', bbox=props)

text4 = ' $\Delta_{KL}$ = %.2f ($meV/at.$) ( for %.2f - %.2f ) '%(Delta, range_min, range_max)
props = dict(boxstyle='round', facecolor='cyan', alpha=0.5)
ax1.text(0.58, 1.10, text4, transform=ax1.transAxes, fontsize=8, verticalalignment='top', bbox=props)






savefig('deltaT.png', format='png', dpi=200) 



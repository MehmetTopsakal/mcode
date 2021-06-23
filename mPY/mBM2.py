#!/usr/bin/env python

import numpy as np


### USAGE:
### import mBM,numpy
### data = np.loadtxt('ev.in', usecols=(0, 1))
### v0, e0, b0, bp, res, vd, ed, vf, ef, pf = mBM2.makefit(data,1,1)
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
    
        
    electron_charge = 1.602176565e-19
    bohr_radius = 5.2917721092e-11
    unitconv = electron_charge / (1e9 * bohr_radius ** 3) * 1
    hf = []
    for h in range(len(vf)):
        hf.append( float( ef[h] + pf[h]*(vf[h]*6.7483330416152265)/unitconv) )
    hf = np.array(hf, np.float)
    
    return v0, e0, b0, bp, res, vd, ed, vf, ef, pf, hf
















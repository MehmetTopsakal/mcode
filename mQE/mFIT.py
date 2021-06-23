#!/usr/bin/env python

import numpy as np


### USAGE:
### import mFIT,numpy
### data = numpy.loadtxt('ev.in', unpack=True, comments='%', usecols=(1-1,2-1), skiprows=0)
### xd, yd, x0, y0, res, xf, yf = mFIT.polyfit3(data)
### 
### 
### 
#### ========================================================
def polyfit3(values,savekey):
    xd=values[0]; yd=values[1]; 
    fit3 = np.polyfit(xd**(-2./3.), yd, 3, full=True)
    ssr = fit3[1]; sst = np.sum((yd - np.average(yd))**2.); res = ssr/sst
    deriv0 = np.poly1d(fit3[0]); deriv1 = np.polyder(deriv0, 1); deriv2 = np.polyder(deriv1, 1)
    x0 = 0; x = 0
    for x in np.roots(deriv1):
        if x > 0 and deriv2(x) > 0:
            x0 = x**(-3./2.)
            y0 = np.polyval(fit3[0],x)
            break
    
    if x0 == 0:
        print('ERROR: Minimum could not be found')
        exit()
    
    x = 0; xf = []; yf = []
    for x in np.linspace(min(xd),max(xd),500):
        xf.append(x)
        yf.append(np.polyval(fit3[0],x**(-2./3.)))
        
    if savekey == 1:
        out = open('fit.out',"w")
        print('%12.6f' %(x0),  '%12.6f' %(y0),  '%12.6f' %(res),'  # x0 y0 res', file=out)
        #out.write(str(x0)+'   '+str(y0)+'   '+str(res[0])+'   # x0 y0 res' ) # this line works with python2       
        out.close()
        
    return xd, yd, x0, y0, res, xf, yf 


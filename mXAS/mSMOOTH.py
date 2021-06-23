#!/usr/bin/env python

import numpy as np
import os
import shutil
import mWIEN
import subprocess
import time

from scipy import interpolate
from scipy.interpolate import InterpolatedUnivariateSpline

### USAGE:
### import mSMOOTH
### 
### mSMOOTH.Gaussian(Edos,tdos_up,sigma,1); 
### 
### 
### 
#### ========================================================




# <><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><> ###
# adapted from http://www.swharden.com/blog/2008-11-17-linear-data-smoothing-in-python/
# Better way of smoothing should be done using interpolation. I'm lazy to implement it here...
def Gaussian_old(X,Y,sigma,vkey=None):
        
    dE = float(X[1]-X[0])
    nsigma = round(sigma/(dE/2))    
   
    if (nsigma == 0.0) or (nsigma == 1.0): 
        nsigma = 1
        #if vkey==2: print('Input Gaussian sigma is less than dE !!!')
    else:
        nsigma = int(nsigma)
    
    window=nsigma*2-1  
    weight=np.array([1.0]*window)  
    weightGauss=[]  
    for i in range(window):  
        i=i-nsigma+1  
        frac=i/float(window)  
        gauss=1/(np.exp((4*(frac))**2))  
        weightGauss.append(gauss)  
    weight=np.array(weightGauss)*weight  
    Ys=[0.0]*(len(Y)-window)    
    for i in range(len(Ys)):  
        Ys[i]=sum(np.array(Y[i:i+window])*weight)/sum(weight) 
    Xs=X[nsigma-1:len(X)-nsigma] 
    #print('Effective Gaussian sigma is ' + str(round(float(nsigma*(X[2]-X[1])/2),5)) + ' eV; dE is ' + str(round(dE,6)) + ' eV.')
    Xs = np.array(Xs) ; Ys = np.array(Ys) 
    return Xs, Ys 




# works with uniform X grid
def Gaussian(xin,yin,sigma):
    
    #fwhm = sigma * 2.354820    
    delta = xin[1]-xin[0]
    
    if sigma == 0: sigma = delta
    
    xout = xin
    yout = xin*0
    
    carpan1 = ( delta/( np.sqrt(2*3.14159265359) * sigma) )
    carpan2 = (-2*sigma**2)   
    
    for i in range(len(xin)):
        for j in range(len(xin)):
            yout[i]=yout[i]+yin[j]*carpan1*np.exp ( ((xin[i]-xin[j])**2)/carpan2 )
            
    return xout, yout





# with interpolation
def Gaussian_fast(xin,yin,sigma):
    
    #fwhm = sigma * 2.354820    
    delta = xin[1]-xin[0]
    
    if sigma == 0: sigma = delta
    
    f  = InterpolatedUnivariateSpline(xin,yin)
    xin = np.arange(min(xin), max(xin), sigma/4)
    yin = f(xin)
    
    xout = xin
    yout = xin*0
    
    carpan1 = ( delta/( np.sqrt(2*3.14159265359) * sigma) )
    carpan2 = (-2*sigma**2)   
    
    for i in range(len(xin)):
        for j in range(len(xin)):
            yout[i]=yout[i]+yin[j]*carpan1*np.exp ( ((xin[i]-xin[j])**2)/carpan2 )
            
    return xout, yout






## works with uniform X grid
#def Gaussian2(xin,yin,sigma):
    
    ##fwhm = sigma * 2.354820    
    #delta = xin[1]-xin[0]
    
    #if sigma == 0: sigma = delta
    
    #bx, by = np.loadtxt('/home/mt/mBOX/scripts/python/mpy/ebroadening.dat', unpack=True, comments='#', usecols=(0,1), skiprows=0)
    ##bx = np.arange(0, 100, 0.1); by = (bx/10)+0.025
    ##bx, by = np.loadtxt('spinel-sigma.dat', unpack=True, comments='#', usecols=(0,1), skiprows=0) 
    
    #b  = interpolate.interp1d(bx,by)
    
    #xout = xin
    #yout = xin*0
    #for i in range(len(xin)):
        #sigma = b(xin[i])
        #for j in range(len(xin)):
            ##yout[i]=yout[i]+yin[j]*delta/(np.sqrt(2*3.14159265359) * sigma)*np.exp ( ((xin[i]-xin[j])**2)/(-2*sigma**2) )
            #yout[i]=yout[i]+yin[j]*delta/( 2.5066282746310828 * sigma)*np.exp ( ((xin[i]-xin[j])**2)/(-2*sigma**2) )
            
    #return xout, yout




# see http://www.tcm.phy.cam.ac.uk/castep/documentation/WebHelp/content/modules/castep/thcastepeels.htm
# works with uniform X grid
def Lorentzian(xin,yin,gamma=None,bonset=None,bmethod=None,gamma_ev=None):
    
    if bmethod is None: bmethod = 2
    
    if gamma is None:  

        if bmethod == 0:
            #by Edgerton 2003 =================================
            bx, by = np.loadtxt('/home/mt/mBOX/scripts/python/mpy/ebroadening.dat', unpack=True, comments='#', usecols=(0,1), skiprows=0)
            if gamma_ev is None: gamma_ev = 1.0
            by = (by*0)+gamma_ev
            if bonset is None: bonset = 0
            xadd = np.arange(0, bonset, 0.1)
            yadd = (xadd*0)+0.025        
            bx = bx+bonset
            bx = np.append(xadd,bx)
            by = np.append(yadd,by)
            b  = interpolate.interp1d(bx,by)        
            out = np.column_stack( (bx, by) );  np.savetxt('b.dat', out, delimiter=" ", fmt="%12.6f %12.6f")

        
        if bmethod == 1:
            #by Edgerton 2003 =================================
            bx, by = np.loadtxt('/home/mt/mBOX/scripts/python/mpy/ebroadening.dat', unpack=True, comments='#', usecols=(0,1), skiprows=0)        
            if bonset is None: bonset = 0
            xadd = np.arange(0, bonset, 0.1)
            yadd = (xadd*0)+0.025        
            bx = bx+bonset
            bx = np.append(xadd,bx)
            by = np.append(yadd,by)
            b  = interpolate.interp1d(bx,by)        
            # out = np.column_stack( (bx, by) );  np.savetxt('b.dat', out, delimiter=" ", fmt="%12.6f %12.6f")
        
        if bmethod == 12:
            #by Edgerton 2003 =================================
            bx, by = np.loadtxt('/home/mt/mBOX/scripts/python/mpy/ebroadening.dat', unpack=True, comments='#', usecols=(0,1), skiprows=0)        
            if bonset is None: bonset = 0
            xadd = np.arange(0, bonset, 0.1)
            yadd = (xadd*0)+0.025        
            bx = bx+bonset
            bx = np.append(xadd,bx)
            by = np.append(yadd,by*2)
            b  = interpolate.interp1d(bx,by)        
            # out = np.column_stack( (bx, by) );  np.savetxt('b.dat', out, delimiter=" ", fmt="%12.6f %12.6f")
        
        if bmethod == 2:
            # by E/10  ==========================================               
            bx = np.arange(0, 100, 0.1)
            by = (bx/10)+0.025
            
            if bonset is None: bonset = 0
            xadd = np.arange(0, bonset, 0.1)
            yadd = (xadd*0)+0.025
            
            bx = bx+bonset
            bx = np.append(xadd,bx)
            by = np.append(yadd,by)
            
            b  = interpolate.interp1d(bx,by)
            # out = np.column_stack( (bx, by) );  np.savetxt('b.dat', out, delimiter=" ", fmt="%12.6f %12.6f")
        
        if bmethod == 3:
            # by E/5  ==========================================               
            bx = np.arange(0, 100, 0.1)
            by = (bx/5)+0.025
            
            if bonset is None: bonset = 0
            xadd = np.arange(0, bonset, 0.1)
            yadd = (xadd*0)+0.025
            
            bx = bx+bonset
            bx = np.append(xadd,bx)
            by = np.append(yadd,by)
            
            b  = interpolate.interp1d(bx,by)
            # out = np.column_stack( (bx, by) );  np.savetxt('b.dat', out, delimiter=" ", fmt="%12.6f %12.6f")
        
        if bmethod == 'spinel':
            #by Edgerton 2003 =================================
            bx, by = np.loadtxt('spinel-sigma.dat', unpack=True, comments='#', usecols=(0,1), skiprows=0)        
            b  = interpolate.interp1d(bx,by)        
            # out = np.column_stack( (bx, by) );  np.savetxt('b.dat', out, delimiter=" ", fmt="%12.6f %12.6f")
        
        if bmethod == 'rocksalt':
            #by Edgerton 2003 =================================
            bx, by = np.loadtxt('rocksalt-sigma.dat', unpack=True, comments='#', usecols=(0,1), skiprows=0)        
            b  = interpolate.interp1d(bx,by)        
            # out = np.column_stack( (bx, by) );  np.savetxt('b.dat', out, delimiter=" ", fmt="%12.6f %12.6f")


        
        vbflag = 1
    else: vbflag = 0
   
    delta = xin[1]-xin[0]
    
    xout = xin
    yout = xin*0
    for i in range(len(xin)):
        if vbflag == 1: gamma = b(xin[i]/2.354820)
        for j in range(len(xin)):
            yout[j]=yout[j]+yin[i]/3.14159265359*(np.arctan((xin[i]-xin[j]+delta)/gamma)-(np.arctan((xin[i]-xin[j]-delta)/gamma)))
    
    yout = yout/2
    
    return xout, yout
    










def wien_broad_elnes(dx,dy,clifetime=None,sigma_spec_Ry=None):
    if clifetime is None: clifetime=0.155864
    if sigma_spec_Ry is None: sigma_spec_Ry=0.007349861764895055 #  ATTENTION in Ry; =0.1 eV
    #sigma_specRy=sigma_spec*13.605698066
    if not os.path.exists('wbroadtmp'):
        os.mkdir('wbroadtmp')        

    os.chdir('wbroadtmp')   
    
    out = np.column_stack( (dx,dy) )
    np.savetxt('wbroadtmp.elnes', out, delimiter=" ", fmt="%10.5f %13.5e")
        
    f = open('wbroadtmp.inb', 'w');
    f.write('wbroad-elnes                                                                           \n')
    f.write('ELNES               #  We broaden case.elnes .                                         \n')
    f.write('  1  1  0           #  We use spectrum 1 out of 1                                      \n')
    f.write('  0  1  1           # split energy, weights of spectra                                 \n')
    f.write('  '+str(clifetime)+' 0        # core hole lifetime of two edges                                  \n')
    f.write('  1   0             # select linearly energy dependent valence broadening; edge offset \n')
    f.write('  '+str(sigma_spec_Ry)+'            # default spectrometer broadening - Gaussian FWHM                  \n')
    f.close()
    mWIEN.x(1,'broadening')
    broadW = np.loadtxt('wbroadtmp.broadspec', unpack=True, comments='#', usecols=(0,1), skiprows=0)    
    os.chdir('..')    
    shutil.rmtree('wbroadtmp',ignore_errors=True)
    return broadW[0], broadW[1]







def wien(dx,dy,Sbroad=None,Cbroad=None,Vswitch=None,edgeoffset=None,code_call=None):
    
    if code_call is None: code_call=' /home/mt/mBOX/programs/wien2k-broadening-module/broadening wbroadening.def '
    if Sbroad is None: Sbroad=0.5       # Gaussian spectrometer broadening with FWHM in eV; multiplied by 1.62 for wien units
    if Cbroad is None: Cbroad=0.1       # has no effect if Sbroad=0
    if edgeoffset is None: edgeoffset=0 # edge offset    
    if Vswitch is None: Vswitch=0       # switch for valence broadening with W=E/10; 0 or 1 or 2 (not implemented yet)

    inp = np.column_stack( (dx, dy) )
    np.savetxt('wdata0.dat', inp, delimiter=" ", fmt="%10.5f %13.5e"); time.sleep(1)
    #
    f = open('wbroadening.def', 'w')
    f.write(' 5,\'wbroadening.in\',\'old\',\'formatted\',0       \n')
    f.write(' 6,\'wbroadening.out\',\'unknown\',\'formatted\',0  \n')
    f.write('46,\'wdata1.dat\',\'unknown\',\'formatted\',0       \n')
    f.write('47,\'wdata0.dat\',\'old\',\'formatted\',0           \n')
    f.close();
    #
    f = open('wbroadening.in', 'w')
    f.write('edge              # Title (of no consequence for the calculation) \n')
    f.write('ABS               # Type of input spectrum                        \n')
    f.write('1 1 0             # We use spectrum 1 out of 1                    \n')
    f.write(str(Cbroad)+' 0.0           # core-hole widths in eV  (only first one is effective) \n')
    f.write(str(Vswitch)+'    '+str(str(edgeoffset))+'          # Valence-broadening-modus and edge offset in eV \n')
    f.write(str(Sbroad*1.62)+'              # S ; Spectrometer FWHM resolution in eV   \n')
    f.close();
    #
    subprocess.call(code_call, shell=True); #time.sleep(1)
    #
    wout  = np.loadtxt('wdata1.dat',  unpack=True, comments='#', usecols=(0,1), skiprows=0)
    subprocess.call(' rm  wdata0.dat wdata1.dat wbroadening.def wbroadening.in wbroadening.error wbroadening.out', shell=True)  
    
    return wout[0], wout[1]

# USAGE:  wx,wy = mSMOOTH.wien(wien[0],wien[1],Sbroad=0.2,Cbroad=0.2,Vswitch=0,edgeoffset=0)






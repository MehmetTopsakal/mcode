#!/usr/bin/python2

import matplotlib
matplotlib.use('Agg') # see http://matplotlib.org/faq/usage_faq.html#what-is-a-backend

import os
import numpy as np
from   pylab import *
import scipy.io as sio
from   matplotlib import gridspec


font = {'size':8}
matplotlib.rc('font', **font)
#savefig('plot.png', format='png', dpi=200) 
#### ========================================================  NOTE: DNR




#### ========================================================  NOTE: inputs
inputs = sys.argv
ilen   = len(inputs)

if ilen == 1:
    bf = os.getcwd(); df = os.getcwd(); cf = os.getcwd()
    inputs.extend(['l',bf,df,-6,6,0,10,0.05,0,0,cf]); 
if ilen == 2:
    bf = os.getcwd(); df = os.getcwd(); cf = os.getcwd()
    inputs.extend([bf,df,-6,6,0,10,0.05,0,0,cf]);
if ilen == 3:
    df = os.getcwd(); cf = os.getcwd()
    inputs.extend([df,-6,6,0,10,0.05,0,0,cf]);
if ilen == 4:
    cf = os.getcwd()
    inputs.extend([-6,6,0,10,0.05,0,0,cf]);
if ilen == 5:
    cf = os.getcwd()
    inputs.extend([6,0,10,0.05,0,0,cf]);
if ilen == 6:
    cf = os.getcwd()
    inputs.extend([0,10,0.05,0,0,cf]);
if ilen == 7:
    cf = os.getcwd()
    inputs.extend([10,0.05,0,0,cf]);
if ilen == 8:
    cf = os.getcwd()
    inputs.extend([0.05,0,0,cf]);
if ilen == 9:
    cf = os.getcwd()
    inputs.extend([0,0,cf]);
if ilen == 10:
    cf = os.getcwd()
    inputs.extend([0,cf]);    
if ilen == 11:
    cf = os.getcwd()
    inputs.extend([cf]);     
   
    
lr = inputs[1]
bf = inputs[2]
df = inputs[3]
ymin = float(inputs[4])
ymax = float(inputs[5])    
dxmin = float(inputs[6])
dxmax = float(inputs[7]) 
sigma = float(inputs[8])
bshift = float(inputs[9])
dshift = float(inputs[10])    
cf = inputs[11]




#### ========================================================  NOTE: smoother
# adapted from http://www.swharden.com/blog/2008-11-17-linear-data-smoothing-in-python/
# Better way of smoothing should be done using interpolation. I'm lazy to implement it here...
def smoothGaussian(X,Y,sigma,vkey):
    
    dE = float(X[1]-X[0])
    nsigma = round(sigma/(dE/2))
    
    if nsigma == 0.0: 
        nsigma = 1
        if vkey==2: print 'Input Gaussian sigma is less than dE !!!'
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
    if vkey==2: print 'Effective Gaussian sigma is ' + str(float(nsigma*(X[2]-X[1])/2)) + ' eV'
    Xs = np.array(Xs) ; Ys = np.array(Ys) 
    return Xs, Ys 




#### ========================================================  NOTE: reader
def readvasprunnpz(lr,sigma):
    if lr == 'r':
      if os.path.isfile('vasprun.xml') == False:
        print >> sys.stderr, 'vasprun.xml DOES NOT exist !!!'
        print >> sys.stderr, "Exception: %s" % str(1)
        sys.exit(1)
      print  
      print 'reading available vasprun.xml....'  
      os.popen("vasp_readxml.py")
      print

    if lr == 'l':
        if os.path.isfile('vasprun.npz') == False:
            print >> sys.stderr, 'vasprun.npz DOES NOT exist !!!'
            print 'reading available vasprun.xml....'
            os.popen("vasp_readxml.py")
        else:
            print 'reading available vasprun.xml....'

      
    readdata = np.load('vasprun.npz')
    
    params = readdata['params']; nspin  = int(params[2]); natom  = int(params[6]); ndos   = int(params[5]); nelect   = int(params[8]);
    Edos = readdata['Edos']; tdos_up = readdata['tdos_up']; tdos_dw = readdata['tdos_dw']; 
    pdos_up = readdata['pdos_up']; pdos_dw = readdata['pdos_dw']; efermi = readdata['efermi']
    kpoints_path=readdata['kpoints_path']; klines_path=readdata['klines_path'];
    bands_up=readdata['bands_up']; bands_dw=readdata['bands_dw']
    
    Edos = Edos-efermi;
    
    Etdos, tdos_ups = smoothGaussian(Edos,tdos_up,sigma,1); tdos_ups[0]=0; tdos_ups[len(tdos_ups)-1]=0;
    Etdos, tdos_dws = smoothGaussian(Edos,tdos_dw,sigma,1); tdos_dws[0]=0; tdos_dws[len(tdos_dws)-1]=0;
    tdos = np.vstack((tdos_ups,-tdos_dws));
    
    return params, kpoints_path, klines_path, bands_up, bands_dw, Etdos, tdos, Edos, pdos_up, pdos_dw, efermi   


#### ========================================================  NOTE: arrange PDOS
def arrangepdos(params,Edos,pdos_up,pdos_dw,sigma,sel):
    ndos = params[5]
    natom = params[6]
    if sel==-1:
        s_up = pdos_up[:,0]                    ; s_up = s_up.reshape(ndos,natom,order='F').copy(); s_up = np.sum(s_up, axis=1);
        p_up = np.sum(pdos_up[:,1:4], axis=1)  ; p_up = p_up.reshape(ndos,natom,order='F').copy(); p_up = np.sum(p_up, axis=1);
        d_up = np.sum(pdos_up[:,4:9], axis=1)  ; d_up = d_up.reshape(ndos,natom,order='F').copy(); d_up = np.sum(d_up, axis=1);
        f_up = np.sum(pdos_up[:,9:16],axis=1)  ; f_up = f_up.reshape(ndos,natom,order='F').copy(); f_up = np.sum(f_up, axis=1);
        
        s_dw = pdos_dw[:,0]                    ; s_dw = s_dw.reshape(ndos,natom,order='F').copy(); s_dw = np.sum(s_dw, axis=1); 
        p_dw = np.sum(pdos_dw[:,1:4], axis=1)  ; p_dw = p_dw.reshape(ndos,natom,order='F').copy(); p_dw = np.sum(p_dw, axis=1); 
        d_dw = np.sum(pdos_dw[:,4:9], axis=1)  ; d_dw = d_dw.reshape(ndos,natom,order='F').copy(); d_dw = np.sum(d_dw, axis=1); 
        f_dw = np.sum(pdos_dw[:,9:16],axis=1)  ; f_dw = f_dw.reshape(ndos,natom,order='F').copy(); f_dw = np.sum(f_dw, axis=1); 

        sp_sumup = np.add(s_up,p_up); df_sumup = np.add(d_up,f_up); spdf_sumup = np.add(sp_sumup,df_sumup);
        sp_sumdw = np.add(s_dw,p_dw); df_sumdw = np.add(d_dw,f_dw); spdf_sumdw = np.add(sp_sumdw,df_sumdw);
    else:        
        al = len(sel);
        start=(sel[0]-1)*ndos; stop=(sel[-1])*ndos;
        s_up = pdos_up[start:stop,0]                  ; s_up = s_up.reshape(ndos,al,order='F').copy(); s_up = np.sum(s_up, axis=1); 
        p_up = np.sum(pdos_up[start:stop,1:4], axis=1)  ; p_up = p_up.reshape(ndos,al,order='F').copy(); p_up = np.sum(p_up, axis=1);
        d_up = np.sum(pdos_up[start:stop,4:9], axis=1)  ; d_up = d_up.reshape(ndos,al,order='F').copy(); d_up = np.sum(d_up, axis=1);
        f_up = np.sum(pdos_up[start:stop,9:16],axis=1)  ; f_up = f_up.reshape(ndos,al,order='F').copy(); f_up = np.sum(f_up, axis=1);
        
        s_dw = pdos_dw[start:stop,0]                    ; s_dw = s_dw.reshape(ndos,al,order='F').copy(); s_dw = np.sum(s_dw, axis=1); 
        p_dw = np.sum(pdos_dw[start:stop,1:4], axis=1)  ; p_dw = p_dw.reshape(ndos,al,order='F').copy(); p_dw = np.sum(p_dw, axis=1); 
        d_dw = np.sum(pdos_dw[start:stop,4:9], axis=1)  ; d_dw = d_dw.reshape(ndos,al,order='F').copy(); d_dw = np.sum(d_dw, axis=1); 
        f_dw = np.sum(pdos_dw[start:stop,9:16],axis=1)  ; f_dw = f_dw.reshape(ndos,al,order='F').copy(); f_dw = np.sum(f_dw, axis=1); 

        sp_sumup = np.add(s_up,p_up); df_sumup = np.add(d_up,f_up); spdf_sumup = np.add(sp_sumup,df_sumup);
        sp_sumdw = np.add(s_dw,p_dw); df_sumdw = np.add(d_dw,f_dw); spdf_sumdw = np.add(sp_sumdw,df_sumdw);        
        
    Edoss, sdos_ups = smoothGaussian(Edos,s_up,sigma,1); sdos_ups[0]=0; sdos_ups[len(sdos_ups)-1]=0;    
    Edoss, pdos_ups = smoothGaussian(Edos,p_up,sigma,1); pdos_ups[0]=0; pdos_ups[len(pdos_ups)-1]=0;
    Edoss, ddos_ups = smoothGaussian(Edos,d_up,sigma,1); ddos_ups[0]=0; ddos_ups[len(ddos_ups)-1]=0;    
    Edoss, fdos_ups = smoothGaussian(Edos,f_up,sigma,1); fdos_ups[0]=0; fdos_ups[len(fdos_ups)-1]=0;    

    Edoss, sdos_dws = smoothGaussian(Edos,s_dw,sigma,1); sdos_dws[0]=0; sdos_dws[len(sdos_dws)-1]=0;
    Edoss, pdos_dws = smoothGaussian(Edos,p_dw,sigma,1); pdos_dws[0]=0; pdos_dws[len(pdos_dws)-1]=0;
    Edoss, ddos_dws = smoothGaussian(Edos,d_dw,sigma,1); ddos_dws[0]=0; ddos_dws[len(ddos_dws)-1]=0;    
    Edoss, fdos_dws = smoothGaussian(Edos,f_dw,sigma,1); fdos_dws[0]=0; fdos_dws[len(fdos_dws)-1]=0;    
    
    Edoss, spdf_sumups = smoothGaussian(Edos,spdf_sumup,sigma,1); spdf_sumups[0]=0; spdf_sumups[len(spdf_sumups)-1]=0; 
    Edoss, spdf_sumdws = smoothGaussian(Edos,spdf_sumdw,sigma,2); spdf_sumdws[0]=0; spdf_sumdws[len(spdf_sumdws)-1]=0;     
    
    sumdos = np.vstack((spdf_sumups,-spdf_sumdws)); 
    sdos = np.vstack((sdos_ups,-sdos_dws)); pdos = np.vstack((pdos_ups,-pdos_dws)); 
    ddos = np.vstack((ddos_ups,-ddos_dws)); fdos = np.vstack((fdos_ups,-fdos_dws));
    
    Epdos = Edoss
    
    return Epdos, sumdos, sdos, pdos, ddos, fdos










#### ========================================================  NOTE: grid
gs1 = gridspec.GridSpec(1, 2,
                       width_ratios=[3,1] )    
gs1.update(top=0.97, bottom=0.1, left=0.1, right=0.99, wspace=0.05)

 
 
 
 
 
 

#### ========================================================  NOTE: bands
ax1 = plt.subplot(gs1[0])
ax1.tick_params(top="off", right="on", direction="out" )

# read data
os.chdir(bf)  
params, kpoints_path, klines_path, bands_up, bands_dw, Etdos, tdos, Edos, pdos_up, pdos_dw, efermi = readvasprunnpz(lr,sigma)
os.chdir(cf)

# draw vertical lines band structure
for kl in range(1,len(klines_path)-1):
    plt.plot([ klines_path[kl],  klines_path[kl]  ], [ ymin, ymax ], 'k-', linewidth=0.1) 

# draw bands
for b in range(len(bands_up)):
  ax1.plot(kpoints_path,bands_up[b]-efermi+bshift, 'k-', lw=2, mfc='k', ms=3)
  if params[2] == 2: 
    ax1.plot(kpoints_path,bands_dw[b]-efermi+bshift, 'b--', lw=1, mfc='k', ms=0)

# shade band gap
vband=params[8]/2
cband=(params[8]/2)+1
ax1.fill_between(kpoints_path, bands_up[vband-1]-efermi+bshift, 0, lw=0, facecolor='y')
ax1.fill_between(kpoints_path, 0, bands_up[cband-1]-efermi+bshift, lw=0, facecolor='y')



# arrange limits
ax1.plot([ 0, max(kpoints_path) ], [ 0, 0 ], 'k-.',linewidth=0.4)
plt.xticks([]); plt.ylabel('Energy (eV)', fontsize=12) 
xlim( (0, max(kpoints_path)) ); ylim( ymin, ymax ) 
#plt.xlabel('( KPOINTS PATH : $\Gamma$  ->   X  ->   S  ->   $\Gamma$  ->   Y )')

#### ========================================================  NOTE: text
test = '$E_{gap}$=%.3f (%.3f) [%.3f (%.3f)]; dir/indir=%d (%d); NSPIN=%d; fermi-cor=%.2f; ISMEAR=%.3f '%(params[11], params[12], params[13], params[14], params[15], params[16], params[2], params[17], sigma)
props = dict(boxstyle='round', facecolor='red', alpha=0.5)
ax1.text(-0.12, -0.05, test, transform=ax1.transAxes, fontsize=9,
        verticalalignment='top', bbox=props)


 
 
 
 

#### ========================================================  NOTE: dos
ax1 = plt.subplot(gs1[1])
ax1.tick_params(top="off", right="off", direction="out" )

os.chdir(df)  
params, kpoints_path, klines_path, bands_up, bands_dw, Etdos, tdos, Edos, pdos_up, pdos_dw, efermi = readvasprunnpz(lr,sigma)
os.chdir(cf)

ax1.fill(tdos[0],Etdos-dshift,'silver', lw=0, label='tot.')
if params[2] == 2:
    ax1.fill(tdos[1],Etdos-dshift,'silver', lw=0)
ax1.plot([ 0, dxmax ], [ 0, 0 ], 'k-.',linewidth=0.4)

# arrange limits
ax1.plot([ dxmin, dxmax ], [ 0, 0 ], 'k-.',linewidth=0.4)
plt.yticks([]); plt.xlabel('States/eV') 
xlim( dxmin, dxmax ); ylim( ymin, ymax )  



#### ========================================================  NOTE: pdos
if len(pdos_up) != 0:

    Epdos, sumdos, sdos, pdos, ddos, fdos = arrangepdos(params,Edos,pdos_up,pdos_dw,sigma,-1)

    ax1.plot(  sdos[0],Epdos-dshift,'m', lw=0.8, label='s')
    ax1.plot(  pdos[0],Epdos-dshift,'r', lw=1.0, label='p')
    ax1.plot(  ddos[0],Epdos-dshift,'b', lw=1.3, label='d')
    ax1.plot(  fdos[0],Epdos-dshift,'c', lw=1.5, label='f')
    ax1.plot(sumdos[0],Epdos-dshift,'k', lw=0.4, label='sum')    
    legend = plt.legend(loc='upper right',fontsize='small', bbox_to_anchor=(1, 0.99))


    if params[2] == 2:
        ax1.plot(  sdos[1],Epdos-dshift,'m', lw=0.8, label='s')
        ax1.plot(  pdos[1],Epdos-dshift,'r', lw=1.0, label='p')
        ax1.plot(  ddos[1],Epdos-dshift,'b', lw=1.3, label='d')
        ax1.plot(  fdos[1],Epdos-dshift,'c', lw=1.5, label='f')
        ax1.plot(sumdos[1],Epdos-dshift,'k', lw=0.4, label='sum')

    xlim( dxmin, dxmax ); ylim( ymin, ymax ) 





#### ========================================================  NOTE: export
plt.savefig('bands.eps', format='eps', dpi=200) 





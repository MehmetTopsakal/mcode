#!/usr/bin/python2

import os    
import sys
import scipy.io as sio
import pylab as pyl
import numpy as np
import itertools as it 
from   io import StringIO
from   pylab import *
from   matplotlib import gridspec
from   matplotlib.widgets import MultiCursor

#font = {'family' : 'serif',
        #'weight' : 'bold',
        #'size'   : 12}
font = {'size'   : 8}
matplotlib.rc('font', **font)


### inputs ------------------------------------------------------------- |
inps = sys.argv
ilen   = len(inps)

if ilen == 1:
  inps.append('r'); inps.append("-6"); inps.append("6"); inps.append("-6"); inps.append("6"); inps.append("4"); inps.append("0");
if ilen == 2:
  inps.append("-6"); inps.append("6"); inps.append("-6"); inps.append("6"); inps.append("4"); inps.append("0");
if ilen == 3:
  inps.append("6"); inps.append("-6"); inps.append("6"); inps.append("10"); inps.append("0");  
if ilen == 4:
  inps.append("-6"); inps.append("6"); inps.append("10"); inps.append("0");  
if ilen == 5:
  inps.append("6"); inps.append("10"); inps.append("0");  
if ilen == 6:
  inps.append("10"); inps.append("0");    
if ilen == 7:
  inps.append("0");  

lr      = inps[1]                 #lr      = 'l'
minx    = float(inps[2])          #minx    = float(-6)
maxx    = float(inps[3])          #maxx    = float(6)
miny    = float(inps[4])          #miny    = float(-30)
maxy    = float(inps[5])          #maxy    = float(30)
sigma   = int(inps[6])            #sigma   = int(3)
shift   = float(inps[7])          #shift   = float(0)


### smooth function ------------------------------------------------------------- | 	
# adapted from http://www.swharden.com/blog/2008-11-17-linear-data-smoothing-in-python/
def smoothGaussian(X,Y,sigma):  
    window=sigma*2-1  
    weight=np.array([1.0]*window)  
    weightGauss=[]  
    for i in range(window):  
        i=i-sigma+1  
        frac=i/float(window)  
        gauss=1/(np.exp((4*(frac))**2))  
        weightGauss.append(gauss)  
    weight=np.array(weightGauss)*weight  
    Ys=[0.0]*(len(Y)-window)   
    for i in range(len(Ys)):  
        Ys[i]=sum(np.array(Y[i:i+window])*weight)/sum(weight) 
    Xs=X[sigma-1:len(X)-sigma]
    print('gaussian sigma is ' + str(float(sigma*(X[2]-X[1])/2)) + ' eV')
    Xs = np.array(Xs) ; Ys = np.array(Ys) 
    return Xs, Ys 


### pdos.mat reader ------------------------------------------------------------- |
def readpdosmat(lr,sigma,shift):
    if lr == 'r':
      if os.path.isfile('pdos.dos') == False:
        print('pdos.dos DO NOT exists !!!', file=sys.stderr)
        print("Exception: %s" % str(1), file=sys.stderr)
        sys.exit(1)
      print()  
      print('reading available pdos.dos....')  
      os.popen("octave -q --eval qe_readpdos")      

    if lr == 'l': 
      print()
      print('loading available pdos.mat....')
      print()
      
    mat_contents = sio.loadmat('pdos.mat')
    
    dim = mat_contents['dim']
    fermi = mat_contents['fermi']
    
    nspin  = int(dim[0][0])
    natom  = int(dim[0][1])
    ndos   = int(dim[0][2])
    nstate = int(dim[0][3]) 
    
    Efp = mat_contents['Ep'];  Efp = np.asarray(Efp); tdosfp = mat_contents['tdosp']; # tdos from projwfc.x
    Eft = mat_contents['Et'];  Eft = np.asarray(Eft); tdosft = mat_contents['tdost']; # tdos from dos.x     
    pdos_all = mat_contents['pdos_all']
    
    tup  = tdosfp[:,0]; tdp = tdosfp[:,1]   ; tut = tdosft[:,0]; tdt = tdosft[:,1];
    s_up = pdos_all[:,0]                    ; s_up = s_up.reshape(ndos,natom,order='F').copy(); s_up = np.sum(s_up, axis=1);
    p_up = np.sum(pdos_all[:,1:3], axis=1)  ; p_up = p_up.reshape(ndos,natom,order='F').copy(); p_up = np.sum(p_up, axis=1);
    d_up = np.sum(pdos_all[:,4:8], axis=1)  ; d_up = d_up.reshape(ndos,natom,order='F').copy(); d_up = np.sum(d_up, axis=1);
    f_up = np.sum(pdos_all[:,9:15],axis=1)  ; f_up = f_up.reshape(ndos,natom,order='F').copy(); f_up = np.sum(f_up, axis=1);
    s_dw = pdos_all[:,16]                   ; s_dw = s_dw.reshape(ndos,natom,order='F').copy(); s_dw = np.sum(s_dw, axis=1);
    p_dw = np.sum(pdos_all[:,17:19],axis=1) ; p_dw = p_dw.reshape(ndos,natom,order='F').copy(); p_dw = np.sum(p_dw, axis=1);
    d_dw = np.sum(pdos_all[:,20:24],axis=1) ; d_dw = d_dw.reshape(ndos,natom,order='F').copy(); d_dw = np.sum(d_dw, axis=1);
    f_dw = np.sum(pdos_all[:,25:31],axis=1) ; f_dw = f_dw.reshape(ndos,natom,order='F').copy(); f_dw = np.sum(f_dw, axis=1);
    
    sp_sumu = np.add(s_up,p_up); df_sumu = np.add(d_up,f_up); spdf_sumu = np.add(sp_sumu,df_sumu);
    sp_sumd = np.add(s_dw,p_dw); df_sumd = np.add(d_dw,f_dw); spdf_sumd = np.add(sp_sumd,df_sumd);
    
    xp = Efp-fermi-shift; xt = Eft-fermi-shift; 
    
    xts, tuts = smoothGaussian(xt,tut,sigma)  ; tuts[0]=0 ; tuts[len(tuts)-1]=0
    xts, tdts = smoothGaussian(xt,tdt,sigma)  ; tdts[0]=0 ; tdts[len(tdts)-1]=0
    xps, tups = smoothGaussian(xp,tup,sigma)  ; tups[0]=0 ; tups[len(tups)-1]=0
    xps, tdps = smoothGaussian(xp,tdp,sigma)  ; tdps[0]=0 ; tdps[len(tdps)-1]=0
    xps, sus = smoothGaussian(xp,s_up,sigma)  ; sus[0]=0  ; sus[len(sus)-1]=0
    xps, pus = smoothGaussian(xp,p_up,sigma)  ; pus[0]=0  ; pus[len(pus)-1]=0
    xps, dus = smoothGaussian(xp,d_up,sigma)  ; dus[0]=0  ; dus[len(dus)-1]=0
    xps, fus = smoothGaussian(xp,f_up,sigma)  ; fus[0]=0  ; fus[len(fus)-1]=0
    xps, sds = smoothGaussian(xp,s_dw,sigma)  ; sds[0]=0  ; sds[len(sds)-1]=0
    xps, pds = smoothGaussian(xp,p_dw,sigma)  ; pds[0]=0  ; pds[len(pds)-1]=0
    xps, dds = smoothGaussian(xp,d_dw,sigma)  ; dds[0]=0  ; dds[len(dds)-1]=0
    xps, fds = smoothGaussian(xp,f_dw,sigma)  ; fds[0]=0  ; fds[len(fds)-1]=0
    xps, spdf_sumus = smoothGaussian(xp,spdf_sumu,sigma)  ; spdf_sumus[0]=0 ; spdf_sumus[len(spdf_sumus)-1]=0
    xps, spdf_sumds = smoothGaussian(xp,spdf_sumd,sigma)  ; spdf_sumds[0]=0 ; spdf_sumds[len(spdf_sumds)-1]=0
    
    Ep = xps; Et = xts; tp = np.vstack((tups,-tdps)); tt = np.vstack((tuts,-tdts)); sp = np.vstack((spdf_sumus,-spdf_sumds));
    s = np.vstack((sus,-sds)); p = np.vstack((pus,-pds));  d = np.vstack((dus,-dds));  f = np.vstack((fus,-fds)); 
    return Ep, tp, sp, Et, tt, s, p, d, f



Ep, tp, sp, Et, tt, s, p, d, f = readpdosmat(lr,sigma,shift)



### plot ------------------------------------------------------------- |
gs1 = gridspec.GridSpec(2, 2,
                       width_ratios=[8,1], height_ratios=[1,4] )    
gs1.update(top=0.98, bottom=0.08, left=0.1, right=0.98, hspace=0.14)

gs2 = gridspec.GridSpec(2, 1,
                       height_ratios=[1,4] )    
gs2.update(top=0.98, bottom=0.08, left=0.1, right=0.98, hspace=0.14)




fig = plt.figure()

ax = fig.add_subplot(gs1[0])
ax.tick_params(top="off", right="off", direction="out" )  
ax.fill(Et,tt[0],'silver')
ax.fill(Et,tt[1],'silver')
 
ax.grid(True)  
ax.plot([ -200, 100 ], [ 0, 0 ], 'k-', linewidth=1.2)
ax.plot([ 0, 0 ], [ -800, 800 ], 'k-', linewidth=1.2)
xlim( (min(Ep), max(Ep)) )
ylim( (min(tp[1]), max(tp[0])) )
plt.ylabel('States/eV')



ax = fig.add_subplot(gs2[1])
ax.tick_params(top="off", right="off", direction="out" )  

#ax.fill(Et,tt[0],'silver', lw=0, label='tot-dos')
ax.plot(Ep,s[0],'m', lw=0.5, label='s-dos')
ax.plot(Ep,p[0],'g', lw=1.0, label='p-dos')
ax.plot(Ep,d[0],'b', lw=1.3, label='d-dos')
ax.fill(Ep,f[0],'r', lw=0,   label='f-dos')
ax.plot(Ep,sp[0],'k', lw=0.2, label='s+p+d+f')
legend = plt.legend(loc='upper right', bbox_to_anchor=(1, 1.35))

#ax.fill(Et,tt[1],'silver', lw=0)
ax.plot(Ep,sp[1],'k', lw=0.2)
ax.plot(Ep,s[1],'m', lw=0.5)
ax.plot(Ep,p[1],'g', lw=1.0)
ax.plot(Ep,d[1],'b', lw=1.3)
ax.fill(Ep,f[1],'r', lw=0)



ax.grid(True)  
ax.plot([ -200, 100 ], [ 0, 0 ], 'k-', linewidth=1.2)
ax.plot([ 0, 0 ], [ -800, 800 ], 'k-', linewidth=1.2)
xlim( (minx, maxx) )
ylim( (miny, maxy) )
plt.xlabel('Energy (eV)')
plt.ylabel('States/eV')
  
savefig('pdos.eps')
  

#plt.show() 







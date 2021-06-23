#!/usr/bin/python2

import matplotlib
matplotlib.use('Agg') # see http://matplotlib.org/faq/usage_faq.html#what-is-a-backend

import os    
import sys
import numpy as np
from   pylab import *
from   matplotlib import gridspec


font = {'size':8}
matplotlib.rc('font', **font)
#savefig('plot.png', format='png', dpi=200) 
#### ========================================================  NOTE: DNR





#### ========================================================  NOTE: inputs
inps = sys.argv
ilen   = len(inps)

if ilen == 1:
  inps.append('r'); inps.append("-6"); inps.append("6"); inps.append("-6"); inps.append("6"); inps.append("1"); inps.append("0");
if ilen == 2:
  inps.append("-6"); inps.append("6"); inps.append("-6"); inps.append("6"); inps.append("1"); inps.append("0");
if ilen == 3:
  inps.append("6"); inps.append("-6"); inps.append("6"); inps.append("1"); inps.append("0"); 
if ilen == 4:
  inps.append("-6"); inps.append("6"); inps.append("1"); inps.append("0");
if ilen == 5:
  inps.append("6"); inps.append("1"); inps.append("0");
if ilen == 6:
  inps.append("1"); inps.append("0");
if ilen == 7:
  inps.append("0");


lr      = inps[1]              
minx    = float(inps[2])       
maxx    = float(inps[3])       
miny    = float(inps[4])       
maxy    = float(inps[5])       
sigma   = int(inps[6])         
shift   = float(inps[7])       


# adapted from http://www.swharden.com/blog/2008-11-17-linear-data-smoothing-in-python/
def smoothGaussian(X,Y,sigma,vkey):  
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
    if vkey==2: print 'gaussian sigma is ' + str(float(sigma*(X[2]-X[1])/2)) + ' eV'
    Xs = np.array(Xs) ; Ys = np.array(Ys) 
    return Xs, Ys 


def readvasprunnpz(lr,sigma,shift):
    if lr == 'r':
      if os.path.isfile('vasprun.xml') == False:
        print >> sys.stderr, 'vasprun.xml DO NOT exists !!!'
        print >> sys.stderr, "Exception: %s" % str(1)
        sys.exit(1)
      print  
      print 'reading available vasprun.xml....'  
      os.popen("old_vasp_readxml.py")
      print

    if lr == 'l': 
      print
      print 'loading available vasprun.npz....'
      print
      
    mat_contents = np.load('vasprun.npz')
    
    dim = mat_contents['params']; nspin  = int(dim[2]); natom  = int(dim[6]); ndos   = int(dim[5]);  
    Edos = mat_contents['Edos']; tdos_up = mat_contents['tdos_up']; tdos_dw = mat_contents['tdos_dw']; 
    pdos_up = mat_contents['pdos_up']; pdos_dw = mat_contents['pdos_dw']; efermi = mat_contents['efermi']
    
    Edos = Edos-efermi-shift;
    
    Etdos, tdos_ups = smoothGaussian(Edos,tdos_up,sigma,1); tdos_ups[0]=0; tdos_ups[len(tdos_ups)-1]=0;
    Etdos, tdos_dws = smoothGaussian(Edos,tdos_dw,sigma,1); tdos_dws[0]=0; tdos_dws[len(tdos_dws)-1]=0;
    tdos = np.vstack((tdos_ups,-tdos_dws)); 
    
    params = nspin, natom, ndos
    
    return params, Etdos, tdos, Edos, pdos_up, pdos_dw


def arrangepdos(params,Edos,pdos_up,pdos_dw,sigma,sel):
    ndos = params[2]
    natom = params[1]
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
        al = (sel[1]-sel[0]+1)
        
        s_up = pdos_up[start:stop,0]                    ; s_up = s_up.reshape(ndos,al,order='F').copy(); s_up = np.sum(s_up, axis=1); 
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
gs1 = gridspec.GridSpec(2, 2,
                       width_ratios=[8,1], height_ratios=[1,4] )    
gs1.update(top=0.98, bottom=0.08, left=0.1, right=0.98, hspace=0.14)

gs2 = gridspec.GridSpec(2, 1,
                       height_ratios=[1,4] )    
gs2.update(top=0.98, bottom=0.08, left=0.1, right=0.98, hspace=0.14)

fig = plt.figure()




#### ========================================================  NOTE: plot bands
params, Etdos, tdos, Edos, pdos_up, pdos_dw  = readvasprunnpz(lr,sigma,shift)

ax = fig.add_subplot(gs1[0]); ax.tick_params(top="off", right="off", direction="out" )  
ax.fill(Etdos,tdos[0],'silver')
ax.fill(Etdos,tdos[1],'silver')

ax.plot([ -200, 100 ], [ 0, 0 ], 'k-', linewidth=1.2)
ax.plot([ 0, 0 ], [ -800, 800 ], 'k-', linewidth=1.2)
xlim( (min(Etdos), max(Etdos)) ); ylim( (min(tdos[1]), max(tdos[0])) )
plt.ylabel('States/eV'); ax.grid(True)  


ax = fig.add_subplot(gs2[1]); ax.tick_params(top="off", right="off", direction="out" )  
ax.fill(Etdos,tdos[0],'silver', lw=0, label='tot-dos')
ax.fill(Etdos,tdos[1],'silver', lw=0)

ax.plot([ -200, 100 ], [ 0, 0 ], 'k-', linewidth=1.2)
ax.plot([ 0, 0 ], [ -800, 800 ], 'k-', linewidth=1.2)
xlim( (minx, maxx) ); ylim( (miny, maxy) )
plt.xlabel('Energy (eV)'); plt.ylabel('States/eV'); ax.grid(True)
legend = plt.legend(loc='upper right', bbox_to_anchor=(1, 1.36))  
  




#### ========================================================  NOTE: plot dos
if len(pdos_up) != 0:

    Epdos, sumdos, sdos, pdos, ddos, fdos        = arrangepdos(params,Edos,pdos_up,pdos_dw,sigma,-1)

    ax.plot(Epdos,sumdos[0],'k', lw=0.2, label='sum-dos')
    ax.plot(Epdos,sdos[0],'m', lw=0.5, label='s-dos')
    ax.plot(Epdos,pdos[0],'g', lw=1.0, label='p-dos')
    ax.plot(Epdos,ddos[0],'b', lw=1.3, label='d-dos')
    ax.fill(Epdos,fdos[0],'r', lw=0,   label='f-dos')
    legend = plt.legend(loc='upper right', bbox_to_anchor=(1, 1.36))

    ax.plot(Epdos,sumdos[1],'k', lw=0.2)
    ax.plot(Epdos,sdos[1],'m', lw=0.5)
    ax.plot(Epdos,pdos[1],'g', lw=1.0)
    ax.plot(Epdos,ddos[1],'b', lw=1.3)
    ax.fill(Epdos,fdos[1],'r', lw=0)

    ax.plot([ -200, 100 ], [ 0, 0 ], 'k-', linewidth=1.2)
    ax.plot([ 0, 0 ], [ -800, 800 ], 'k-', linewidth=1.2)
    xlim( (minx, maxx) ); ylim( (miny, maxy) )
    plt.xlabel('Energy (eV)'); plt.ylabel('States/eV'); ax.grid(True)
    legend = plt.legend(loc='upper right', bbox_to_anchor=(1, 1.36))  
  



#### ========================================================  NOTE: export fig
plt.savefig('pdos.eps', format='eps', dpi=200) 






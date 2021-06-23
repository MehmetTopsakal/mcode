#!/usr/bin/env python

import numpy as np
import os


### USAGE:
### import mVASP
### 
### mVASP.readvasprunnpz(lr,sigma,shift)
### 
### 
### 
#### ========================================================



wienroot='~/software/wien2k/main'



    
def change_de(case_in1_file,newde):   
    import shutil
    
    with open(case_in1_file, mode='r') as f:
        lines = [line for line in f.readlines()]
          
    lastline = lines[-1].split()     
    lastline[4] = float(newde)   

    nf = open(case_in1_file+'.new', 'w' ) 
    
    for j in range(len(lines)-1):        
        nf.write(lines[j])       
     
    for i in range(0,3):
        nf.write(str(lastline[i])+' ')

    nf.write(' '+str(lastline[3])+'   ')         
    nf.write('    '+str(lastline[4])+'   ') 
    nf.write('    '+str(lastline[5])+'  ')    
        
    for i in range(6,len(lastline)):
        nf.write(str(lastline[i])+' ')  
    nf.write('\n')    
      
    nf.close()
    
    shutil.move(case_in1_file+'.new',case_in1_file)
    return    
    
    


def change_RKMAX(case_in1_file,newRKMAX):    
    import shutil
    
    with open(case_in1_file, mode='r') as f:
        lines = [line for line in f.readlines()]
          
    line2 = lines[1].split()     
    line2[0] = float(newRKMAX)   

    nf = open(case_in1_file+'.new', 'w' )
   
    nf.write(lines[0])    
    for i in range(0,3):
        nf.write(str(line2[i])+'    ')        
    for i in range(3,len(line2)):
        nf.write(str(line2[i])+' ')  
    nf.write('\n') 
    
    for j in range(2,len(lines)):        
        nf.write(lines[j])        
 
    nf.write('\n') 
    
    nf.close()
    
    shutil.move(case_in1_file+'.new',case_in1_file)
    return


def gen_machines(ncores=None):    
    if ncores is None: ncores=8   
    mf = open('.machines', 'w' )
    for i in range(ncores):
        mf.write('1:localhost \n')
    mf.write('granularity:1 \n') 
    mf.write('extrafine:1 \n')    
    mf.close()
    return

def run_lapw(numthreads=None,cc=None,ec=None,ni=None,extra=None):
    if numthreads is None: numthreads=1
    if cc is None: cc=0.0001 
    if ec is None: ec=0.0001
    if ni is None: ni=50
    if extra is None: extra=' '
    import subprocess
    print('Running "run_lapw  '+extra+' -ec '+str(cc)+' -cc '+str(ec)+' -i '+str(ni)+' -NI" (nthreads='+str(numthreads)+')\n' )
    subprocess.call(' export WIENROOT='+wienroot+' ; PATH=$PATH:$WIENROOT; export OMP_NUM_THREADS='+str(int(numthreads))+'; run_lapw  '+extra+' -ec '+str(cc)+' -cc '+str(ec)+' -i '+str(ni)+' -NI > /dev/null', shell=True)
    return
def run_lapw_p(numthreads=None,ncores=None,cc=None,ec=None,ni=None,extra=None):
    if ncores is None: ncores=8    
    gen_machines(ncores) 
    if numthreads is None: numthreads=1
    if cc is None: cc=0.0001 
    if ec is None: ec=0.0001
    if ni is None: ni=50
    if extra is None: extra=' '
    import subprocess
    print('Running "run_lapw -p '+extra+' -ec '+str(cc)+' -cc '+str(ec)+' -i '+str(ni)+' -NI" (nthreads='+str(numthreads)+')\n' )
    subprocess.call(' export WIENROOT='+wienroot+' ; PATH=$PATH:$WIENROOT; export OMP_NUM_THREADS='+str(int(numthreads))+'; run_lapw -p '+extra+' -ec '+str(cc)+' -cc '+str(ec)+' -i '+str(ni)+' -NI > /dev/null', shell=True)
    return


def runsp_lapw(numthreads=None,cc=None,ec=None,ni=None,extra=None):
    if numthreads is None: numthreads=1
    if cc is None: cc=0.0001 
    if ec is None: ec=0.0001
    if ni is None: ni=50
    if extra is None: extra=' '
    import subprocess
    print('Running "runsp_lapw  '+extra+' -ec '+str(cc)+' -cc '+str(ec)+' -i '+str(ni)+' -NI" (nthreads='+str(numthreads)+')\n' )
    subprocess.call(' export WIENROOT='+wienroot+' ; PATH=$PATH:$WIENROOT; export OMP_NUM_THREADS='+str(int(numthreads))+'; runsp_lapw '+extra+' -ec '+str(cc)+' -cc '+str(ec)+' -i '+str(ni)+' -NI > /dev/null', shell=True)
    return
def runsp_lapw_p(numthreads=None,ncores=None,cc=None,ec=None,ni=None,extra=None):
    if ncores is None: ncores=8
    gen_machines(ncores) 
    if numthreads is None: numthreads=1
    if cc is None: cc=0.0001 
    if ec is None: ec=0.0001
    if ni is None: ni=50
    if extra is None: extra=' '
    import subprocess
    print('Running "runsp_lapw -p '+extra+' -ec '+str(cc)+' -cc '+str(ec)+' -i '+str(ni)+' -NI" (nthreads='+str(numthreads)+')\n' )
    subprocess.call(' export WIENROOT='+wienroot+' ; PATH=$PATH:$WIENROOT; export OMP_NUM_THREADS='+str(int(numthreads))+'; runsp_lapw -p '+extra+' -ec '+str(cc)+' -cc '+str(ec)+' -i '+str(ni)+' -NI > /dev/null', shell=True)
    return



def x(numthreads,command):    
    import subprocess
    print('Running "x '+command+'   " (nthread='+str(numthreads)+')\n' )
    subprocess.call(' export WIENROOT='+wienroot+' ; PATH=$PATH:$WIENROOT; export OMP_NUM_THREADS='+str(int(numthreads))+'; x '+command+'   > /dev/null', shell=True)
    return
def x_p(numthreads,ncores,command): 
    gen_machines(ncores) 
    import subprocess
    print('Running "x '+command+' -p  " (nthread='+str(numthreads)+'; ncores='+str(ncores)+')\n' )
    subprocess.call(' export WIENROOT='+wienroot+' ; PATH=$PATH:$WIENROOT; export OMP_NUM_THREADS='+str(int(numthreads))+'; x '+command+' -p   > /dev/null', shell=True)
    return








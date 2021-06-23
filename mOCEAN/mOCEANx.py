#!/usr/bin/env python

import numpy as np
import os
import subprocess as sp 
import time
from functools import reduce
import operator
import subprocess
import shutil

import glob
import os





# ============================================================================================= 
def get_absspct(path=None):
    
    if path is None: path=os.getcwd()  
    
    if os.path.isdir(path+'/CNBSE') == True:
        #print(' Found CNBSE folder !! Reading absspct files in there' )
        os.chdir(path+'/CNBSE')
        subprocess.call(' ls -l absspct* | awk \'{print \"# \" $9}\' > .otmpx', shell=True)
        subprocess.call(' cat .otmpx |  wc -l > .otmpxs', shell=True)        
        subprocess.call(' echo \"# natom=`cat .otmpx |  cut -c 14-17 | uniq | wc -l` nphoton=`cat .otmpx |  cut -c 22-23 | sort | uniq | wc -l`\" >> .otmpx; echo \" \" >> .otmpx', shell=True)
        subprocess.call(' size=`cat .otmpxs`; for i in `seq 1 $size`; do  file=`awk \"NR==$i\" .otmpx | awk \'{print $2}\'`; echo "########### $file "         >> .otmpx; cat $file | awk \'{print $1\"  \"$2}\' >> .otmpx ; echo \"  \"  >> .otmpx ; done ', shell=True)
        subprocess.call(' mv .otmpx ../ocean_absspcts.dat', shell=True)  
    os.chdir('..')

    return



# ============================================================================================= 
def get_xesspct(path=None):
    
    if path is None: path=os.getcwd()  
    
    if os.path.isdir(path+'/CNBSE') == True:
        #print(' Found CNBSE folder !! Reading xesspct files in there' )
        os.chdir(path+'/CNBSE')
        subprocess.call(' ls -l xesspct* | awk \'{print \"# \" $9}\' > .otmpx', shell=True)
        subprocess.call(' cat .otmpx |  wc -l > .otmpxs', shell=True)        
        subprocess.call(' echo \"# natom=`cat .otmpx |  cut -c 14-17 | uniq | wc -l` nphoton=`cat .otmpx |  cut -c 22-23 | sort | uniq | wc -l`\" >> .otmpx; echo \" \" >> .otmpx', shell=True)
        subprocess.call(' size=`cat .otmpxs`; for i in `seq 1 $size`; do  file=`awk \"NR==$i\" .otmpx | awk \'{print $2}\'`; echo "########### $file "         >> .otmpx; cat $file | awk \'{print $1\"  \"$2}\' >> .otmpx ; echo \"  \"  >> .otmpx ; done ', shell=True)
        subprocess.call(' mv .otmpx ../ocean_xesspcts.dat', shell=True)  
    os.chdir('..')

    return




# ============================================================================================= 
def get_cores(path=None):
    
    if path is None: path=os.getcwd()  
    
    if os.path.isdir(path+'/Common') == True:    
        os.chdir(path+'/Common')    
           
        f = open('core_offset', 'r')
        co = f.readline().split(); co = co[0] 
        
        f = open('cnbse.rad', 'r')
        cr = f.readline().split(); cr = float(cr[0]) 
        
        f = open('nedges', 'r')
        ne = f.readline().split(); ne = int(ne[0]) 
        
        os.chdir('../')
        
    if co == '.false.' :
        cores = []        
    elif co == '.true.' :
        os.chdir(path+'/SCREEN')
                
        cores = []
        
        if os.path.isfile('core_shift_new.log') == True: 
            logfile='core_shift_new.log' 
        else: logfile='core_shift.log'
        
        with open(logfile) as f:
            lines = f.readlines()
        
        ls = """Radius = %(cr)1.2f Bohr""" % vars()
        
        for i, line in enumerate(lines):
            if ls in line:
                for a in range(ne):
                    cores.append(lines[i+4].split()[2:4])
                    i += 1
        np.save('_cores', cores)
        np.save('_offset', []) 
        print(cores)
        os.chdir('..') 
    else:
        os.chdir(path+'/SCREEN')
                
        cores = []

        if os.path.isfile('core_shift_new.log') == True: 
            logfile='core_shift_new.log' 
        else: logfile='core_shift.log'
        
        with open(logfile) as f:
            lines = f.readlines()
        
        ls = """Radius = %(cr)1.2f Bohr""" % vars()
        
        for i, line in enumerate(lines):
            if ls in line:
                for a in range(ne):
                    cores.append(lines[i+3].split()[1:3])
                    i += 1
        np.save('_cores', cores)
        np.save('_offset', []) 
        print(cores)
        os.chdir('..') 

    return cores



# ============================================================================================= 
def read_absspct(absfile=None,savekey=None):
 
    if absfile is None: absfile='ocean_absspcts.dat' 
    if savekey is None: savekey=0  
    
    if os.path.isfile(absfile) == False:
        print(' ocean_absspcts.dat not found. Exiting.... ' )
        return
    
    abslist = []
    with open(absfile, mode='r') as f:
        lines = [line for line in f.readlines()]
        for i, line in enumerate(lines):
            if '# natom=' in line:
                natom= int(lines[i].split()[1].split('=')[1]);
                nphoton= int(lines[i].split()[2].split('=')[1]); 
            
            if '###########' in line:
                abslist.append(lines[i].split()[1])
            
    d0x,d0y = np.loadtxt(absfile, unpack=True, comments='#', usecols=(0,1), skiprows=0)
    
    ne = int(len(d0x)/(natom*nphoton)) 
    E = d0x.reshape(ne,(natom*nphoton),order='F').copy()
    E = E[:,0]
    
    Iall = d0y.reshape(ne,(natom*nphoton),order='F').copy()
    Itot = np.sum(Iall, axis=1);
    
    Iatom = []
    for a in range(natom):
        start = a*nphoton
        stop  = a*nphoton+nphoton
        tmp = np.sum(Iall[:,start:stop], axis=1);
        Iatom.append(tmp)

    if savekey == 1:
        np.save('_E', E)
        np.save('_Itot', Itot)
        np.save('_Iatom', Iatom)   
        np.save('_Iall', Iall)    
       
    return E, Itot, Iatom, Iall 









# ============================================================================================= 
def read_xesspct(xesfile=None,savekey=None):
 
    if xesfile is None: xesfile='ocean_xesspcts.dat' 
    if savekey is None: savekey=0  
    
    if os.path.isfile(xesfile) == False:
        print(' ocean_xesspcts.dat not found. Exiting.... ' )
        return
    
    xeslist = []
    with open(xesfile, mode='r') as f:
        lines = [line for line in f.readlines()]
        for i, line in enumerate(lines):
            if '# natom=' in line:
                natom= int(lines[i].split()[1].split('=')[1]);
                nphoton= int(lines[i].split()[2].split('=')[1]); 
            
            if '###########' in line:
                xeslist.append(lines[i].split()[1])
            
    d0x,d0y = np.loadtxt(xesfile, unpack=True, comments='#', usecols=(0,1), skiprows=0)
    
    ne = int(len(d0x)/(natom*nphoton)) 
    E = d0x.reshape(ne,(natom*nphoton),order='F').copy()
    E = E[:,0]
    
    Iall = d0y.reshape(ne,(natom*nphoton),order='F').copy()
    Itot = np.sum(Iall, axis=1);
    
    Iatom = []
    for a in range(natom):
        start = a*nphoton
        stop  = a*nphoton+nphoton
        tmp = np.sum(Iall[:,start:stop], axis=1);
        Iatom.append(tmp)

    if savekey == 1:
        np.save('_E', E)
        np.save('_Itot', Itot)
        np.save('_Iatom', Iatom)   
        np.save('_Iall', Iall)    
       
    return E, Itot, Iatom, Iall 








# ============================================================================================= 
def readocean(cleankey=None,plotkey=None,mode=None): 
    
    if cleankey is None: cleankey=0    
    if plotkey is None: plotkey=0 
    if mode is None: mode=0   # 0 for xas 1 for xes
    
    # first create ocean.save folder        
    try:
        os.stat('ocean.save')
    except:
        os.mkdir('ocean.save')           


    if mode == 1:
        if os.path.isdir('CNBSE') == True:    
            get_xesspct()
            shutil.copyfile('ocean_xesspcts.dat', './ocean.save/ocean_xesspcts.dat') 
            subprocess.call('cp ./CNBSE/xesspct_*  ./ocean.save/', shell=True)
            if cleankey == 2: print('yes'); shutil.rmtree('./CNBSE',ignore_errors=True) 
        
        read_xesspct(savekey=1)
        subprocess.call(' mv *.npy ocean.save ', shell=True)
        
        subprocess.call(' mpy ocean_plotxesspct.py ', shell=True)
        shutil.copyfile('xesspct.png', './ocean.save/xesspct.png')
        shutil.copyfile('ocean_xesspcts.dat', './ocean.save/ocean_xesspcts.dat')


    if mode == 0:
        if os.path.isdir('CNBSE') == True:    
            get_absspct()
            shutil.copyfile('ocean_absspcts.dat', './ocean.save/ocean_absspcts.dat') 
            subprocess.call('cp ./CNBSE/absspct_*  ./ocean.save/', shell=True)
            subprocess.call('cp ./CNBSE/mode  ./ocean.save/', shell=True)            
            if cleankey == 2: print('yes'); shutil.rmtree('./CNBSE',ignore_errors=True) 
        
        read_absspct(savekey=1)
        subprocess.call(' mv *.npy ocean.save ', shell=True)
        
        subprocess.call(' mpy ocean_plotabsspct.py ', shell=True)
        shutil.copyfile('absspct.png', './ocean.save/absspct.png')
        shutil.copyfile('ocean_absspcts.dat', './ocean.save/ocean_absspcts.dat')

    
    if os.path.isdir('DFT') == True:    
        os.chdir('DFT')
        if plotkey == 1: 
            subprocess.call(' mpy qe_drawbands.py ', shell=True); 
            shutil.copyfile('bands.png', '../ocean.save/bands_DFT.png')
        shutil.copyfile('scf.in', '../ocean.save/scf_DFT.in')
        shutil.copyfile('scf.out', '../ocean.save/scf_DFT.out')        
        dirs = next(os.walk('.'))[1] ; 
        if 'Out' in dirs: dirs.remove('Out')

        for i in range(len(dirs)):
            os.chdir(dirs[i])
            if plotkey == 1:
                subprocess.call(' mpy qe_drawbands.py ', shell=True)
                shutil.copyfile('bands.png', '../../ocean.save/bands_'+dirs[i]+'.png')
            shutil.copyfile('nscf.in', '../../ocean.save/nscf_'+dirs[i]+'.in')
            shutil.copyfile('nscf.out', '../../ocean.save/nscf_'+dirs[i]+'.out')            
            os.chdir('..')        
        os.chdir('..')
        if cleankey == 2: shutil.rmtree('./DFT',ignore_errors=True)

    if os.path.isfile('./SCREEN/core_shift.log') == True:
        get_cores()
        subprocess.call(' mv ./SCREEN/*.npy ./ocean.save ', shell=True)
        subprocess.call(' cp ./SCREEN/core_* ./ocean.save ', shell=True)
    else:
        np.save('./ocean.save/_cores', 0)
        np.save('./ocean.save/_offset', 0)  
        
    subprocess.call(' rm -rf ocean.npz; cp *.in *.out photon* *.fhi *.UPF *.fill *.opts ocean.save ', shell=True)    
    subprocess.call(' cd ocean.save; mkdir ocean_inputs; mv *.fhi *.UPF photon* *.fill *.opts mode* ocean_inputs; cp *.in ocean_inputs; rm -rf ./ocean_inputs/scf*; rm -rf ./ocean_inputs/nscf* ', shell=True)
    subprocess.call(' cd ocean.save; mkdir dft_part; mv scf* nscf* dft_part', shell=True)  
    subprocess.call(' cd ocean.save; mkdir spects; mv absspct_* xesspct_* spects 2> /dev/null', shell=True)       
    subprocess.call(' cd ocean.save; zip -qr ../ocean.npz *; sleep 2 ; cd ..; rm -rf ocean.save ', shell=True) 
    #shutil.rmtree('ocean.save',ignore_errors=True)


    if cleankey == 1: subprocess.call(' rm -rf *.UPF *.fhi photon* *.fill *.opts 2> /dev/null', shell=True) 
    
    if cleankey == 2: shutil.rmtree('./Common',ignore_errors=True)
    if cleankey == 2: shutil.rmtree('./PAW',ignore_errors=True)
    if cleankey == 2: shutil.rmtree('./PREP',ignore_errors=True)    
    if cleankey == 2: shutil.rmtree('./SCREEN',ignore_errors=True) 
    if cleankey == 2: shutil.rmtree('./zWFN',ignore_errors=True)     
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

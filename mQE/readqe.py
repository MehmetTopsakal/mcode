#!/usr/bin/env python

import numpy as np
from functools import reduce
import operator
import os
import subprocess as sp 
import time

from .readqeout import readqeout
from .readpdos import readpdos
from .readtdos import readtdos



def readqe(scffile=None,tmpfolder=None,cleankey=None): 
    
  
    
    if cleankey == 2:
        if os.path.isfile('qerun.npz') == True:
            print('  qerun.npz exists !!!. Remove it first.')
            return

    if cleankey is None: cleankey=0
    
    if scffile is None: 
        if os.path.isfile('bands.out') == True:
            scffile='bands.out'
        elif os.path.isfile('nscf_bands.out') == True:
            scffile='nscf_bands.out'   
        elif os.path.isfile('nscf_dos.out') == True:
            scffile='nscf_dos.out'               
        elif os.path.isfile('nscf.out') == True:
            scffile='nscf.out'            
        elif os.path.isfile('scf.out') == True:
            scffile='scf.out' 
            
    print(scffile)
            
    if tmpfolder is None: tmpfolder='qetmp'    
              
    if os.path.isfile('pdos.dos') == True:
        #sp.call(' sed -n \'/Charges/,/Spilling/p\' pdos.out  > lowdin.dat ', shell=True)
        sp.call(' echo "not implemented"  > lowdin.dat ', shell=True)
        dos_info, efermi, Edos, tdos, pdos_up, pdos_dw = readpdos()
    else:
        print('NO DOS here !!!')
        dos_info = []
        
    #if os.path.isfile('pwscf.dos') == True:
        #readtdos(savekey=1)
    #else: 
        #if os.path.isfile('pwscf.pdos_tot') == True:
            #readtdos(savekey=1)
        
    if os.path.isfile(scffile) == True:
        qe_params, efermi, kpoints, bands_up, bands_dw, lattice, recipro, positions, positions_d, etot, tmag, alabels, atypes = readqeout(file=scffile)
    print(qe_params)

    #if os.path.isdir(tmpfolder) == True:
        #print('reading qetmp folder')
        #readxml(tmpfolder=tmpfolder,savekey=1)

   
    #if cleankey == 1:
        #if os.path.isfile('qerun.npz') == True:
            #print('  qerun.npz exists !!!. Remove it first.')
        #else:    
            #sp.call(' rm -f pdos.dos pwscf.dos pwscf.pdos_tot pdos.out pdos.mat', shell=True)
            #sp.call(' zip pseudos.zip *.UPF *.upf ', shell=True)
            #sp.call(' rm -f *.upf *.UPF pdos.* pwscf.pdos_* dos.*', shell=True) 
            #sp.call(' zip -q qerun.npz *.npy pseudos.zip tdos_*.dat scf.out nscf.out scf.in nscf.in nscf_bands.in nscf_dos.out nscf_dos.out lowdin.dat ', shell=True)
            #time.sleep(1)
            #sp.call('  rm -f *.npy pseudos.zip tdos_*.dat lowdin.dat', shell=True)
    #else:
        #sp.call(' rm -rf qerun.npz ', shell=True)        
        #sp.call(' zip -q qerun.npz *.npy  tdos_*.dat scf.out nscf.out scf.in nscf.in nscf_bands.in nscf_dos.out nscf_dos.out lowdin.dat ', shell=True)
        #time.sleep(1)
        #sp.call(' rm -f *.npy tdos_*.dat lowdin.dat supportInfo.kpath kpts.pwscf', shell=True)
    
    if not dos_info:
        np.savez('qerun', qe_params=qe_params, efermi=efermi, kpoints=kpoints, bands_up=bands_up, bands_dw=bands_dw, lattice=lattice, recipro=recipro, positions=positions, positions_d=positions_d, etot=etot, tmag=tmag, alabels=alabels, atypes=atypes)    
    else:
        np.savez('qerun', dos_info=dos_info, Edos=(Edos-efermi), tdos=tdos, pdos_up=pdos_up, pdos_dw=pdos_dw,   qe_params=qe_params, efermi=efermi, kpoints=kpoints, bands_up=bands_up, bands_dw=bands_dw, lattice=lattice, recipro=recipro, positions=positions, positions_d=positions_d, etot=etot, tmag=tmag, alabels=alabels, atypes=atypes)    
    time.sleep(1)
    sp.call('  zip -rq qerun.npz scf.in* pdos.in* nscf.in* nscf_bands.in* nscf_dos.in* scf.out* nscf.out* nscf_bands.out* nscf_dos.out* *.UPF *.upf *.vdb lowdin.dat*', shell=True)
    
    if cleankey == 1: sp.call('  rm -f  lowdin.dat* pdos.dos*  pwscf.pdos_tot', shell=True)
    if cleankey == 2: sp.call('  rm -f  scf.in* pdos.in* nscf.in* nscf_bands.in* nscf_dos.in* scf.out* nscf.out* nscf_bands.out* nscf_dos.out* *.UPF *.upf *.vdb lowdin.dat* pdos.dos*  pwscf.pdos_tot', shell=True)    
    return

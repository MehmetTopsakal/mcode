#!/usr/bin/env python

import numpy as np
import os, time
import subprocess as sp
from .readvasprunxml import readvasprunxml
from .readdoscar import readdoscar


def readvasp(cleankey=None):
    
    
    if cleankey == 2:
        if os.path.isfile('vasprun.npz') == True:
            print('  vasprun.npz exists !!!. Remove it first.')
            return

    if cleankey is None: cleankey=0
    

    vasp_params  = []
    kpoints      = []
    kpoints_path = []
    klines_path  = []
    poscar0      = []
    bands_up     = []
    bands_dw     = []
    
    dos_info     = []
    Edos         = [] 
    efermi       = []    
    tdos         = []
    pdos_up      = []
    pdos_dw      = []
    
    

    
    
    #Read vasprun.xml
    if os.path.isfile('vasprun.xml') == True: 
        print('\nReading vasprun.xml...')
        vasp_params, kpoints, kpoints_path, klines_path, poscar0, bands_up, bands_dw, efermi = readvasprunxml()     
    
    #Read DOSCAR      
    if os.path.isfile('DOSCAR') == True:
        print('Reading DOSCAR...')
        dsize = os.path.getsize('DOSCAR')
        print(dsize)            
        dos_info, efermi, Edos, tdos, pdos_up, pdos_dw = readdoscar() 
    print()
    
    
    
    np.savez('vasprun', vasp_params=vasp_params, kpoints=kpoints, kpoints_path=kpoints_path, klines_path=klines_path, poscar0=poscar0, bands_up=bands_up, bands_dw=bands_dw,    dos_info=dos_info, efermi=efermi, Edos=(Edos-efermi), tdos=tdos, pdos_up=pdos_up, pdos_dw=pdos_dw)
    time.sleep(1)
    sp.call('  zip -rq vasprun.npz INCAR KPOINTS POTCAR CONTCAR POSCAR OUTCAR OSZICAR DOSCAR', shell=True)
    
    if cleankey == 1: sp.call(' rm -f DOSCAR vasprun.xml ', shell=True)     
    if cleankey == 2: sp.call(' rm -f INCAR KPOINTS POTCAR POSCAR OUTCAR DOSCAR vasprun.xml CHG  EIGENVAL  IBZKPT  PCDAT  REPORT  XDATCAR', shell=True) 
    
    return vasp_params, kpoints, kpoints_path, klines_path, poscar0, bands_up, bands_dw,     dos_info, efermi, Edos, tdos, pdos_up, pdos_dw    
  

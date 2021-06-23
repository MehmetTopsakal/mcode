#!/usr/bin/env python

import numpy as np
import os
import subprocess as sp 
import fnmatch
import shutil



def cleanup(level=None): 
    
    if level is None: level=1
    
    save_list = ['EFERMI.OUT','STATE.OUT','INFO.OUT','INFOXS.OUT','EQATOMS.OUT',
                'BONDLENGTH.OUT','EVALCORE.OUT','TOTENERGY.OUT','KPOINTS.OUT','LATTICE.OUT']
    
    for file in os.listdir('.'):
        if fnmatch.fnmatch(file, 'EPSILON_BSE*.OUT'):
            save_list.append(file)  
        if fnmatch.fnmatch(file, 'LOSS_BSE*.OUT'):
            save_list.append(file)              
        if fnmatch.fnmatch(file, 'SIGMA_BSE*.OUT'):
            save_list.append(file)             
        if fnmatch.fnmatch(file, '*.xml'):
            save_list.append(file)    

    ignore_list = ['atoms.xml','geometry_QMT001.xml','geometry_SCR.xml','info_QMT001.xml','info_SCR.xml']
    
    

    for file in os.listdir('.'):
        
        if fnmatch.fnmatch(file, '*.OUT'):
            if file not in save_list: os.remove(file)
            
        if fnmatch.fnmatch(file, '*.xml'):     
            if file in ignore_list: os.remove(file)
            
        if fnmatch.fnmatch(file, '*_scf.xml'):     
            os.remove(file)            

        if fnmatch.fnmatch(file, 'EPSILON_*'):     
            os.remove(file)    
        if fnmatch.fnmatch(file, 'LOSS_*'):     
            os.remove(file)    
        if fnmatch.fnmatch(file, 'SIGMA_*'):     
            os.remove(file)   
            
    return

#!/usr/bin/env python

import numpy as np
import os





def readtdos(file=None,savekey=None):
    
    if file is None: file='pwscf.dos'
    if savekey is None: savekey=0
    
    if os.path.isfile(file) == False:
        if os.path.isfile('pwscf.pdos_tot') == True:
            file='pwscf.pdos_tot'  
            
    readtdos = np.loadtxt(file, unpack=True, comments='#', skiprows=0)       
                
    tdos = []    
    if len(readtdos) == 3: 
        Etdos = readtdos[0]
        tdos_up = readtdos[1]
        tdos_up = np.array(tdos_up, np.float)/2; 
        tdos_dw = tdos_up
    if len(readtdos) == 4 or len(readtdos) == 5: 
        Etdos = readtdos[0]
        tdos_up = readtdos[1]
        tdos_dw = readtdos[2]        
        tdos_up = np.array(tdos_up, np.float); 
        tdos_dw = np.array(tdos_dw, np.float);            
    tdos.append(tdos_up); tdos.append(tdos_dw) 
    
    if savekey == 1: 
        np.save('Etdos', Etdos)
        np.save('tdos', tdos) 
        out = np.column_stack( (Etdos,tdos[0]) ); np.savetxt('tdos_up.dat', out, delimiter=" ", fmt="%4.5f %12.6f")
        if len(readtdos) == 4: out = np.column_stack( (Etdos,tdos[1]) ); np.savetxt('tdos_dw.dat', out, delimiter=" ", fmt="%4.5f %12.6f")
        
    return Etdos, tdos
 
 

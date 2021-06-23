#!/usr/bin/env python

import numpy as np
#from .readqe import readqe

import mSMOOTH



def loadpdos(file=None):
    
    if file is None: file='qerun.npz'; print('reading pdos from qerun.npz')
            
    readnpz = np.load(file)
    efermi = readnpz['efermi']
    dos_info = readnpz['dos_info']
    Edos = readnpz['Edos']      
    tdos = readnpz['tdos']  
    pdos_up = readnpz['pdos_up']
    pdos_dw = readnpz['pdos_dw']      
   
    return dos_info, efermi, Edos, tdos, pdos_up, pdos_dw
 
 
 
 
 
 
 
 
def getpdos(pdosin,sel,sigma):
    
    dos_info, efermi, Edos, tdos, pdos_up, pdos_dw = pdosin

    
    atom_part = sel.split('|')[0]
    atoms = []
    if len(atom_part.split(',')) == 1: 
        a = atom_part.split(',')[0]
        if ':' in a:
            start = int(a.split(':')[0])
            stop  = int(a.split(':')[1])+1
            for j in range(start,stop,1):
                atoms.append(j)
        else:
            atoms.append(int(a))
    else:
        for i in range(len(atom_part.split(','))):
            a = atom_part.split(',')[i]
            if ':' in a:
                start = int(a.split(':')[0])
                stop  = int(a.split(':')[1])+1
                for j in range(start,stop,1):
                    atoms.append(j)
            else:
                atoms.append(int(a))
    
    orb_part = sel.split('|')[1]
    orbs = []
    for o in range(len(orb_part)):
        if orb_part[o] == 's':   orbs.append(1)
        elif orb_part[o] == 'p': orbs.append(2) 
        elif orb_part[o] == 'd': orbs.append(3)
        elif orb_part[o] == 'f': orbs.append(4) 
        elif orb_part[o] == 't': orbs=[1,2,3,4]
        else: orbs=[1,2,3,4] 
    orbs = sorted(orbs)    
    
    if len(sel) < 3: spin=[1]
    elif sel.split('|')[2][0] == 'u': spin=1
    elif sel.split('|')[2][0] == 'd': spin=2
    elif sel.split('|')[2][0] == 'a': spin=3   
    else: spin=1
    
    nedos = int(dos_info[1])
    nspin = int(dos_info[0])

    
    if spin == 1: pdos_sel = pdos_up; tsel = tdos[0]
    elif nspin == 1: pdos_sel= pdos_up; tsel = tdos[0]
    elif nspin == 2: pdos_sel= pdos_dw; tsel = tdos[1]    
    elif nspin == 3: pdos_sel= (pdos_up+pdos_dw)/2; tsel = (tdos[0]+tdos[1])/2 

    
    if len(pdos_up) == 0: 
        print('\nPDOS is empty !!!\n')
        
    else:    
        out = Edos*0
        for a in range(len(atoms)):
            tmp = []
            for i in range(nedos):
                current_line = pdos_sel[(nedos*(atoms[a]-1))+i]
                if orbs == [1,2,3,4]: tmp.append(np.sum(current_line))
                elif orbs == [1]: tmp.append(current_line[0])  
                elif orbs == [2]: tmp.append(np.sum(current_line[1:4]))
                elif orbs == [3]: tmp.append(np.sum(current_line[4:9])) 
                elif orbs == [4]: tmp.append(np.sum(current_line[9:16])) 
                elif orbs == [1,2]: tmp.append(np.sum(current_line[0:4]))
                elif orbs == [1,2,3]: tmp.append(np.sum(current_line[0:9]))
                elif orbs == [2,3]: tmp.append(np.sum(current_line[1:9]))    
                elif orbs == [2,3,4]: tmp.append(np.sum(current_line[1:16]))  
                elif orbs == [3,4]: tmp.append(np.sum(current_line[4:16]))    
                elif orbs == [1,3]: tmp.append( current_line[0]+np.sum(current_line[4:9]) )     
                elif orbs == [1,4]: tmp.append( current_line[0]+np.sum(current_line[9:16]) )    
                elif orbs == [2,4]: tmp.append( np.sum(current_line[1:4])+np.sum(current_line[9:16]) )     
                elif orbs == [1,2,4]: tmp.append( current_line[0]+np.sum(current_line[1:4])+np.sum(current_line[9:16]) )     
                elif orbs == [1,3,4]: tmp.append( current_line[0]+np.sum(current_line[4:9])+np.sum(current_line[9:16]) )  
            out  = np.array(tmp, np.float) + out 


    
    Esel, tsel = mSMOOTH.Gaussian_old(Edos,tsel,sigma)
    
    if len(pdos_up) == 0:
        Esel, psel = Esel, tsel
    else:
        Esel, psel = mSMOOTH.Gaussian_old(Edos,out,sigma)    
        if nspin == 2: psel = psel/2
        if nspin == 3: psel = psel/2    

    
    return Esel, tsel, psel

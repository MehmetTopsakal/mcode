#!/usr/bin/env python

import numpy as np






def readpdos(file=None,savekey=None):
    
    if file is None: file='pdos.dos'
    if savekey is None: savekey=0
    
    d = []
    with open(file) as f:
        lines = f.readlines()
        
    natom = int(lines[0].split()[0])
    nedos = int(lines[0].split()[1])
    efermi = 0
    nspin = int(lines[0].split()[2])+1
    nstate = int(lines[0].split()[3]) 
    
    atom_list = []    
    state_list = []
    for s in range(nstate):
        l = lines[s+1].split()
        atom_list.append(l[0])
        state_list.append(l[1])
    atom_list = np.array(atom_list, np.int)    
    state_list = np.array(state_list, np.int) 
    

    Edos = []
    for i in range(nedos):
        l = lines[i+1+len(state_list)].split()
        Edos.append(l[0])
    Edos = np.array(Edos, np.float) 

    if max(state_list) == 1:  pdos_up = np.zeros((natom*nedos, 4))
    if max(state_list) == 2:  pdos_up = np.zeros((natom*nedos, 9))
    if max(state_list) == 3:  pdos_up = np.zeros((natom*nedos, 16))
    
    if nspin == 1:
        
        tdos = []; tdos_up = []; tdos_dw = []
        for t in range(nedos):
            l = lines[t+1+nstate].split()
            tdos_up.append(float(l[1])/2)
        tdos_up = np.array(tdos_up, np.float); tdos_dw = tdos_up    
        tdos.append(tdos_up); tdos.append(tdos_up)      
        
        start=nedos
        for s in range(nstate):
            ai = atom_list[s]  # atom index
            st = state_list[s] # state type
            for i in range(nedos):
                l = lines[start+i+1+nstate].split()
                if st == 0: 
                    pdos_up[((ai-1)*nedos)+i][0] = float(l[1]) # s
                elif st == 1:                 
                    pdos_up[((ai-1)*nedos)+i][1] = float(l[2]) # p1
                    pdos_up[((ai-1)*nedos)+i][2] = float(l[3]) # p2
                    pdos_up[((ai-1)*nedos)+i][3] = float(l[4]) # p3
                elif st == 2:
                    pdos_up[((ai-1)*nedos)+i][4] = float(l[2]) # d1
                    pdos_up[((ai-1)*nedos)+i][5] = float(l[3]) # d2
                    pdos_up[((ai-1)*nedos)+i][6] = float(l[4]) # d3
                    pdos_up[((ai-1)*nedos)+i][7] = float(l[5]) # d4
                    pdos_up[((ai-1)*nedos)+i][8] = float(l[6]) # d5
                elif st == 3: 
                    pdos_up[((ai-1)*nedos)+i][9]  = float(l[2]) # f1
                    pdos_up[((ai-1)*nedos)+i][10] = float(l[3]) # f2
                    pdos_up[((ai-1)*nedos)+i][11] = float(l[4]) # f3
                    pdos_up[((ai-1)*nedos)+i][12] = float(l[5]) # f4
                    pdos_up[((ai-1)*nedos)+i][13] = float(l[6]) # f5
                    pdos_up[((ai-1)*nedos)+i][14] = float(l[7]) # f6
                    pdos_up[((ai-1)*nedos)+i][15] = float(l[8]) # f7 
            start = start + nedos
    pdos_up = np.array(pdos_up, np.float)/2; pdos_dw = []
    
    
    if nspin == 2:
        
        tdos = []; tdos_up = []; tdos_dw = []
        for t in range(nedos):
            l = lines[t+1+nstate].split()
            tdos_up.append(float(l[1]))
            tdos_dw.append(float(l[2]))
        tdos_up = np.array(tdos_up, np.float); tdos_dw = np.array(tdos_dw, np.float)    
        tdos.append(tdos_up); tdos.append(tdos_dw)
        
        pdos_dw = pdos_up
        start=nedos
        for s in range(nstate):
            ai = atom_list[s]  # atom index
            st = state_list[s] # state type
            for i in range(nedos):
                l = lines[start+i+1+nstate].split()
                if st == 0: 
                    pdos_up[((ai-1)*nedos)+i][0] = float(l[3]) # s
                    pdos_dw[((ai-1)*nedos)+i][0] = float(l[4]) # s
                elif st == 1:                 
                    pdos_up[((ai-1)*nedos)+i][1] = float(l[3]) # p1
                    pdos_dw[((ai-1)*nedos)+i][1] = float(l[4]) # p1                    
                    pdos_up[((ai-1)*nedos)+i][2] = float(l[5]) # p2
                    pdos_dw[((ai-1)*nedos)+i][2] = float(l[6]) # p2
                    pdos_up[((ai-1)*nedos)+i][3] = float(l[7]) # p3
                    pdos_dw[((ai-1)*nedos)+i][3] = float(l[8]) # p3                    
                elif st == 2:
                    pdos_up[((ai-1)*nedos)+i][4] = float(l[3])  # d1
                    pdos_dw[((ai-1)*nedos)+i][4] = float(l[4])  # d1
                    pdos_up[((ai-1)*nedos)+i][5] = float(l[5])  # d2
                    pdos_dw[((ai-1)*nedos)+i][5] = float(l[6])  # d2
                    pdos_up[((ai-1)*nedos)+i][6] = float(l[7])  # d3
                    pdos_dw[((ai-1)*nedos)+i][6] = float(l[8])  # d3
                    pdos_up[((ai-1)*nedos)+i][7] = float(l[9])  # d4
                    pdos_dw[((ai-1)*nedos)+i][7] = float(l[10]) # d4
                    pdos_up[((ai-1)*nedos)+i][8] = float(l[11]) # d5
                    pdos_dw[((ai-1)*nedos)+i][8] = float(l[12]) # d5                    
                elif st == 3: 
                    pdos_up[((ai-1)*nedos)+i][9]  = float(l[3]) # f1
                    pdos_dw[((ai-1)*nedos)+i][9]  = float(l[4]) # f1
                    pdos_up[((ai-1)*nedos)+i][10] = float(l[5]) # f2
                    pdos_dw[((ai-1)*nedos)+i][10] = float(l[6]) # f2
                    pdos_up[((ai-1)*nedos)+i][11] = float(l[7]) # f3
                    pdos_dw[((ai-1)*nedos)+i][11] = float(l[8]) # f3
                    pdos_up[((ai-1)*nedos)+i][12] = float(l[9]) # f4 
                    pdos_dw[((ai-1)*nedos)+i][12] = float(l[10]) # f4
                    pdos_up[((ai-1)*nedos)+i][13] = float(l[11]) # f5
                    pdos_dw[((ai-1)*nedos)+i][13] = float(l[12]) # f5
                    pdos_up[((ai-1)*nedos)+i][14] = float(l[13]) # f6
                    pdos_dw[((ai-1)*nedos)+i][14] = float(l[14]) # f6
                    pdos_up[((ai-1)*nedos)+i][15] = float(l[15]) # f7
                    pdos_dw[((ai-1)*nedos)+i][15] = float(l[16]) # f7                     
            start = start + nedos
      
    pdos_up = np.array(pdos_up, np.float); pdos_dw = np.array(pdos_dw, np.float)
    
    
    dos_info = []
    dos_info.append(nspin)
    dos_info.append(nedos)
    dos_info.append(Edos[1]-Edos[0]) # dE
    dos_info.append(int(max(state_list)))


    efermi = []
    return dos_info, efermi, Edos, tdos, pdos_up, pdos_dw
 
 

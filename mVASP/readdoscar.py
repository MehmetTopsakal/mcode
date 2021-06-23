#!/usr/bin/env python


import numpy as np





def readdoscar(file=None):
    
    if file is None: file='DOSCAR'
                   
    d = []
    with open(file) as f:
        lines = f.readlines()
        
    natom = int(lines[0].split()[0])
    emax = float(lines[5].split()[0])
    emin = float(lines[5].split()[1])
    nedos = int(lines[5].split()[2])
    efermi = float(lines[5].split()[3])
    line7w = int(len(lines[6].split()))
    
    
    # total-DOS =========================================== 
    Edos = []
    tdos = []
    tdos0 = []
    
    for t in range(nedos):
        l = lines[t+6].split()
        Edos.append(l[0])
        tdos0.append(l[1:])
     
    Edos  = np.array(Edos, np.float) 
    tdos0 = np.array(tdos0, np.float) 
    
    if len(tdos0[0]) == 2:
        nspin = 1
        tdos_up = tdos0[:,0]/2; #tdos0/2  for integrated-dos
        tdos_dw = tdos_up;      #tdos_up
        tdos.append(tdos_up); tdos.append(tdos_dw)
    elif len(tdos0[0]) == 4:
        nspin = 2    
        tdos_up = tdos0[:,[0]]; #tdos_up = tdos0[:,[0,2]]
        tdos_dw = tdos0[:,[1]]; #tdos_dw = tdos0[:,[1,3]]   
        tdos.append(tdos_up); tdos.append(tdos_dw)
    else: ispin = 3
            
    
    # partial-DOS ===========================================
    try:
        len(lines[t+7].split())
    except:
        print('\n LORBIT was NOT set to 11 \n pdos is empty....')
        pdos_up = []; pdos_dw = []; lenpdos = 0
    
    try:
        pdos_up
    except:
        pdos0 = []
        for p in range((nedos+1)*natom):
            l = lines[p+nedos+6].split()
            if l[-1]=='1.00000000': continue
            pdos0.append(l[1:])
        pdos0  = np.array(pdos0, np.float)
        
        if len(tdos0[0]) == 2:
            lenpdos = len(l)
            if lenpdos == 5: print('\nThis DOSCAR is non-magnetic and contains s,p')
            elif lenpdos == 10: print('\nThis DOSCAR is non-magnetic and contains s,p,d')
            elif lenpdos == 17: print('\nThis DOSCAR is non-magnetic and contains s,p,d,f')    
            pdos_up = pdos0/2; pdos_dw = []; 
        else:
            lenpdos = len(l)
            if lenpdos == 9: 
                print('\nThis DOSCAR is magnetic and contains s,p')
                pdos_up = pdos0[:,[0,2,4,6]]; pdos_dw = pdos0[:,[1,3,5,7]];
            elif lenpdos == 19: 
                print('\nThis DOSCAR is magnetic and contains s,p,d')
                pdos_up = pdos0[:,[0,2,4,6,8,10,12,14,16]]; pdos_dw = pdos0[:,[1,3,5,7,9,11,13,15,17]];
            elif lenpdos == 33: 
                print('\nThis DOSCAR is magnetic and contains s,p,d,f')
                pdos_up = pdos0[:,[0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,30]]; pdos_dw = pdos0[:,[1,3,5,7,9,11,13,15,17,19,21,23,25,27,29,31]];



        
    dos_info = []
    dos_info.append(nspin)
    dos_info.append(nedos)
    dos_info.append(Edos[1]-Edos[0]) # dE
    dos_info.append(lenpdos)
  


    return dos_info, efermi, Edos, tdos, pdos_up, pdos_dw







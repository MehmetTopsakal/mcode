#!/usr/bin/python

import mQE
import os
import sys
import numpy as np


#### ========================================================  NOTE:



#!/usr/bin/env python

import numpy as np
import mSMOOTH
import os
import subprocess as sp 
import time
from functools import reduce
import operator


### USAGE:
### 
### 
### 
### 
### 
### 
#### ========================================================


def readscfout(file=None,savekey=None):
    
    if file is None: file='scf.out'
    if savekey is None: savekey=0  
      
    lattice = []; positions = [];  positions_d = []; alabels = []; 
    recipro = []; scfout_info = []; atypes = []; kpoints = []; efermi = [];
    etot = []; ptot = []; tmag = []; bands = []; bands2 = []; bands_up = []; bands_dw = [];  
    
    with open(file, mode='r') as f:
      lines = [line for line in f.readlines()]
      for i, line in enumerate(lines):
        
        if 'lattice parameter (alat)  =' in line:
            alat= lines[i].split()[4]; alat = float(alat) * 0.529177257507 
            volume= lines[i+1].split()[3]; volume = float(volume) * 0.148184711486445 ; scfout_info.append(volume)	
            natom = lines[i+2].split()[4];  natom = int(natom)    ; scfout_info.append(natom)
            ntype = lines[i+3].split()[5];  ntype = int(ntype)    ; scfout_info.append(ntype)
            nelec = lines[i+4].split()[4];  nelec = float(nelec)  ; scfout_info.append(nelec)
            nband = lines[i+5].split()[4];  nband = int(nband)    ; scfout_info.append(nband) ; math1=nband/8 ; math2=nband%8; 
            ecutw = lines[i+6].split()[3];  ecutw = float(ecutw)  ; scfout_info.append(ecutw)
            ecutr = lines[i+7].split()[4];  ecutr = float(ecutr)  ; scfout_info.append(ecutr)
            
        if 'celldm(1)=' in line:
            lattice.append(lines[i+4].split()[3:6])
            lattice.append(lines[i+5].split()[3:6])
            lattice.append(lines[i+6].split()[3:6])	
            lattice = np.array(lattice); lattice = lattice.astype(np.float); lattice = lattice*alat
            recipro.append(lines[i+9].split()[3:6])	
            recipro.append(lines[i+10].split()[3:6])	
            recipro.append(lines[i+11].split()[3:6])		
            recipro = np.array(recipro); recipro = recipro.astype(np.float); recipro = recipro*2*3.141592653589793*(1/alat)
 
        if 'atomic species   valence    mass     pseudopotential' in line:
            for t in range(ntype):	
                t = lines[i+1].split()[0]; atypes.append(t); i += 1 
             
        if 'Starting magnetic structure' in line:
            nspin = 2;
            i += 1 
 
        if 'site n.     atom                  positions (alat units)' in line: 
            for e in range(natom):	
               positions.append(lines[i+1].split()[6:9]); alabels.append(lines[i+1].split()[1])
               i += 1 
            positions = np.array(positions); positions = positions.astype(np.float); positions = positions*alat 

        if '     site n.     atom                  positions (cryst. coord.)' in line: 
            for e in range(natom):	
                positions_d.append(lines[i+1].split()[6:9])
                i += 1 
            positions_d = np.array(positions_d); positions_d = positions_d.astype(np.float);	
 
        if 'cart. coord. in units 2pi/alat' in line: 
            nkpts = lines[i-1].split()[4]; nkpts = int(nkpts)			
            for k in range(nkpts):
                kpoints.append(lines[i+1].strip().split(') = (')[1].strip().split('), wk =')[0].split())
                i += 1 
            kpoints = np.array(kpoints); kpoints = kpoints.astype(np.float);

        if '     the Fermi energy is' in line:
            efermi = lines[i].split()[4]; efermi = float(efermi)
 
        if 'highest occupied level (ev):' in line:
            efermi = lines[i].split()[4]; efermi = float(efermi)	

        if 'highest occupied, lowest unoccupied level (ev):' in line:
            efermi = lines[i].split()[6]; efermi = float(efermi)	

        if 'the spin up/dw Fermi energies are' in line:
            efermi_up = lines[i].split()[6]; efermi_up = float(efermi_up)	
            efermi_dw = lines[i].split()[7]; efermi_dw = float(efermi_dw)	
            efermi.append(efermi_up); efermi.append(efermi_dw); 
            print("Attention: Separate Fermi energies !!!!")
            print(efermi); print("maximum selected");	efermi = max(efermi)

        if '!    total energy              =' in line:
            etot = lines[i].split()[4]; etot = float(etot)	

        if '          total   stress  ' in line:
            ptot = lines[i].split()[5]; ptot = float(ptot)  
 
        if 'total magnetization       = ' in line:
            tmag = lines[i].split()[3]; tmag = float(tmag)	

        if ')   bands (ev):' in line:
            energies = [];
            if math1 == 0:
                math1 = 1
            for bi in range(int(math1)):
                energies.append(lines[i+2+bi].split());
            if math1 != 0:  
                energies.append(lines[i+3+bi].split());
            bands.append(reduce(operator.add, energies))   
      
        if '     band energies (ev):' in line:
            energies = [];
            if math1 == 0:
               math1=1
            for bi in range(int(math1)):
              energies.append(lines[i+2+bi].split());
            if math1 != 0:  
              energies.append(lines[i+3+bi].split());
            bands.append(reduce(operator.add, energies))  
    
    
    bands=np.array(bands); bands=bands.astype(np.float); bands=np.transpose(bands);
    
    
    try:
      nspin
    except:
      nspin = 1 
      
    scfout_info.append(nspin)  

    if len(bands) == 0:
        bands_up = []; bands_dw = []
    else:
        if nspin == 1:
            bands_up = bands; bands_dw = bands;  
        
        if nspin == 2:
            for u in range(nband):
                bands_up.append(bands[u][0:nkpts]); bands_dw.append(bands[u][nkpts:nkpts*2]);
            bands_up = np.array(bands_up); bands_up = bands_up.astype(np.float);
            bands_dw = np.array(bands_dw); bands_dw = bands_dw.astype(np.float);
            kpoints = kpoints[:nkpts];
    
    if savekey == 1: 
        np.save('scfout_info', np.array(scfout_info, np.float))        
        np.save('efermi', efermi)
        np.save('kpoints', kpoints)
        np.save('bands_up', bands_up)        
        np.save('bands_dw', bands_dw)
        np.save('lattice', lattice)
        np.save('recipro', recipro)
        np.save('positions', positions)
        np.save('positions_d', positions_d) 
        np.save('etot', etot)        
        np.save('ptot', ptot) 
        np.save('tmag', tmag) 
        np.save('alabels', alabels)
        np.save('atypes', atypes)  
        
    return







#########################################################################################
#########################################################################################
#########################################################################################
#########################################################################################
#########################################################################################
#########################################################################################
#########################################################################################
#########################################################################################
#########################################################################################
#########################################################################################
#########################################################################################
#########################################################################################
#########################################################################################
#########################################################################################
#########################################################################################
#########################################################################################
#########################################################################################
#########################################################################################
#########################################################################################
#########################################################################################
#########################################################################################
#########################################################################################









def readxml(tmpfolder=None,savekey=None):
    
    if tmpfolder is None: tmpfolder='./qetmp'
    if savekey is None: savekey=0    
    
    if os.path.isdir(tmpfolder) == True:
        if os.path.isfile(tmpfolder+'/pwscf.save/data-file.xml') == True:
            xmlfile = tmpfolder+'/pwscf.save/data-file.xml'
        else:
            if os.path.isfile(tmpfolder+'/wfc/pwscf.save/data-file.xml') == True:
                xmlfile = tmpfolder+'/wfc/pwscf.save/data-file.xml'
    else:
        print('qetmp folder does not exist !!!')
        return
 
    with open(xmlfile) as f:
        lines = f.readlines()
    
    POSITIONS = []
    LATTICE = []
    NSPIN = 1
    CELL_DIMENSIONS = []
    SPECIES = []
    
    for i, line in enumerate(lines):

        if line.startswith('    <LATTICE_PARAMETER type='):
            LATTICE_PARAMETER = float(lines[i+1])

        if line.startswith('    <CELL_DIMENSIONS type='):
            for a in range(6):
                CELL_DIMENSIONS.append(float(lines[i+1+a]))
            CELL_DIMENSIONS = np.array(CELL_DIMENSIONS, np.float)
 
        if line.startswith('    <NUMBER_OF_ATOMS'):
            NATOMS = int(lines[i+1].split()[0])

        if line.startswith('    <NUMBER_OF_SPECIES'):
            NTYPES = int(lines[i+1].split()[0])                          
 
        if line.startswith('    <WFC_CUTOFF'):                   
            ECUTWFC  = float(lines[i+1].split()[0])
            ECUTRHO  = float(lines[i+4].split()[0])

        if line.startswith('    <LSDA'):                   
            if lines[i+1].split()[0] == 'T': NSPIN = 2
            LNONCOL = lines[i+4].split()[0]     
            LSORBIT = lines[i+7].split()[0]
                                 
        if line.startswith('    <UNITS_FOR_ATOMIC_POSITIONS UNITS='):
            for a in range(NATOMS):
                POSITIONS.append(lines[i+1+a].strip().split('"')[5].split()[0:3])
                SPECIES.append(lines[i+1+a].strip().split('"')[1])
            POSITIONS = np.array(POSITIONS, np.float)
            
        if line.startswith('      <UNITS_FOR_DIRECT_LATTICE_VECTORS UNITS='):
            LATTICE.append(lines[i+2].split()[0:3]) 
            LATTICE.append(lines[i+5].split()[0:3]) 
            LATTICE.append(lines[i+8].split()[0:3])
            LATTICE = np.array(LATTICE, np.float)
    
    slist = []
    for e in SPECIES:
        if e not in slist:
            slist.append(e)
    
    alist = []
    for a in range(len(slist)):
        c = SPECIES.count(slist[a])
        alist.append(c)
       
        
    qexml_info = []
    qexml_info.append(NATOMS)
    qexml_info.append(NTYPES)
    qexml_info.append(ECUTWFC)  
    qexml_info.append(ECUTRHO)
    qexml_info.append(NSPIN) 
    qexml_info.append(LNONCOL)  
    qexml_info.append(LSORBIT)
    qexml_info.append(slist)
    qexml_info.append(alist)
    qexml_info.append(SPECIES)
    
        
    qexml_lattice = LATTICE/1.88972612456506
    qexml_positions = POSITIONS/1.88972612456506 
    
    qexml_alat = LATTICE_PARAMETER
    qexml_cell = CELL_DIMENSIONS   
    
    if savekey == 1: 
        #np.save('qexml_info', qexml_info)
        np.save('qexml_lattice', qexml_lattice)
        np.save('qexml_positions', qexml_positions)
        np.save('qexml_alat', qexml_alat)
        np.save('qexml_cell', qexml_cell)
    
    return qexml_info, qexml_lattice, qexml_positions, qexml_alat, qexml_cell




#########################################################################################
#########################################################################################
#########################################################################################
#########################################################################################
#########################################################################################
#########################################################################################
#########################################################################################
#########################################################################################
#########################################################################################
#########################################################################################
#########################################################################################
#########################################################################################
#########################################################################################
#########################################################################################
#########################################################################################
#########################################################################################
#########################################################################################
#########################################################################################
#########################################################################################
#########################################################################################
#########################################################################################
#########################################################################################




def write_scf_in(no,sys):
        
    scfout_info, lattice, positions, qe_alat, qe_cell = mQE.readxml()
    
    a=lattice[0][0]
    c=lattice[2][2]
    
    f = open('scf.in', 'w');
    f.write('&control                                                                    \n')
    f.write('calculation = \'scf\'                                                       \n')
    #f.write('pseudo_dir = \'/home/wentzcov/topsakal/calculations/REN-revisited/_pseudo\' \n')
    f.write('pseudo_dir = \'./qetmp/pwscf.save\'                                           \n')
    f.write('outdir=\'./qetmp\', wfcdir=\'./qetmp/wfc\',                                     \n')
    f.write('disk_io = \'low\'                                                           \n')
    f.write('verbosity = \'high\'                                                        \n')
    f.write('lkpoint_dir = .false.                                                       \n')
    f.write('tprnfor = .true.,  tstress = .true.                                         \n')
    f.write('/                                                                           \n')
    f.write('                                                                            \n')
    f.write('&system                                                                     \n')
    f.write('ibrav=4,                                                                    \n')
    f.write('a='+str(a)+', c='+str(c)+'                                                  \n')
    f.write('nat=5, ntyp=3, nspin=2,                                                     \n')
    f.write('ecutwfc=80, ecutrho=400,                                                    \n')
    f.write('starting_magnetization(1) = +0.5                                            \n')
    f.write('starting_magnetization(2) = -0.5                                            \n')
    f.write('occupations   = \'smearing\'                                                \n')
    f.write('smearing      = \'fd\'                                                      \n')
    f.write('degauss       = 0.002                                                       \n')
    f.write('lda_plus_u = .true.,                                                        \n')
    f.write('lda_plus_u_kind=0                                                           \n')
    f.write('U_projection_type = \'atomic\'                                              \n')
    f.write('Hubbard_U(1) = 3.0                                                          \n')
    f.write('Hubbard_U(2) = 3.0                                                          \n')
    f.write('/                                                                           \n')
    f.write('                                                                            \n')
    f.write('&electrons                                                                  \n')
    f.write('diagonalization=\'david\',                                                  \n')
    f.write('mixing_beta = 0.2,                                                          \n')
    f.write('conv_thr = 1.0d-8,                                                          \n')
    f.write('electron_maxstep=150                                                        \n')
    f.write('startingwfc = \'atomic\'                                                    \n')
    f.write('startingpot = \'file\'                                                      \n')
    f.write('/                                                                           \n')
    f.write('                                                                            \n')
    f.write('&ions                                                                       \n')
    f.write('/                                                                           \n')
    f.write('                                                                            \n')
    f.write('&cell                                                                       \n')
    f.write('/                                                                           \n')
    f.write('                                                                            \n')
    f.write('ATOMIC_SPECIES                                                              \n')
    f.write('Re1 1.0  '+sy+'.pbe-kjpaw_repl.1.0.UPF                                      \n')
    f.write('Re2 1.0  '+sy+'.pbe-kjpaw_repl.1.0.UPF                                      \n')
    f.write('O   1.0  O.pbe-kjpaw.UPF                                                    \n')
    f.write('                                                                            \n')
    f.write('ATOMIC_POSITIONS angstrom                                                   \n')
                                                                                  
    l0 = '   '.join('%12.8f'%F for F in positions[0,:]);           f.write('Re1  '+l0+'  \n')
    l1 = '   '.join('%12.8f'%F for F in positions[1,:]);           f.write('Re2  '+l1+'  \n')
    l2 = '   '.join('%12.8f'%F for F in positions[2,:]);           f.write('O    '+l2+'  \n')
    l3 = '   '.join('%12.8f'%F for F in positions[3,:]);           f.write('O    '+l3+'  \n')
    l4 = '   '.join('%12.8f'%F for F in positions[4,:]);           f.write('O    '+l4+'  \n')
                                                                                  
    f.write('                                                                            \n')
    f.write('K_POINTS {automatic}                                                        \n')
    f.write('6 6 4  0 0 0                                                                \n')
    f.write('                                                                            \n')
    f.write('                                                                            \n')
    f.close()
    
    return








#########################################################################################
#########################################################################################
#########################################################################################
#########################################################################################
#########################################################################################
#########################################################################################
#########################################################################################
#########################################################################################
#########################################################################################
#########################################################################################
#########################################################################################
#########################################################################################
#########################################################################################
#########################################################################################
#########################################################################################
#########################################################################################
#########################################################################################
#########################################################################################
#########################################################################################
#########################################################################################
#########################################################################################
#########################################################################################







def readpdos(file=None,savekey=None):
    
    if file is None: file='pdos.dos'
    if savekey is None: savekey=0
    
    d = []
    with open(file) as f:
        lines = f.readlines()
        
    natom = int(lines[0].split()[0])
    ndos = int(lines[0].split()[1])
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
    

    Epdos = []
    for i in range(ndos):
        l = lines[i+1+len(state_list)].split()
        Epdos.append(l[0])
    Epdos = np.array(Epdos, np.float) 

    if max(state_list) == 1:  pdos_up = np.zeros((natom*ndos, 4))
    if max(state_list) == 2:  pdos_up = np.zeros((natom*ndos, 9))
    if max(state_list) == 3:  pdos_up = np.zeros((natom*ndos, 16))
    
    if nspin == 1:
        
        tpdos = []; tpdos_up = []; tpdos_dw = []
        for t in range(ndos):
            l = lines[t+1+nstate].split()
            tpdos_up.append(float(l[1])/2)
        tpdos_up = np.array(tpdos_up, np.float); tpdos_dw = tpdos_up    
        tpdos.append(tpdos_up); tpdos.append(tpdos_up)      
        
        start=ndos
        for s in range(nstate):
            ai = atom_list[s]  # atom index
            st = state_list[s] # state type
            for i in range(ndos):
                l = lines[start+i+1+nstate].split()
                if st == 0: 
                    pdos_up[((ai-1)*ndos)+i][0] = float(l[1]) # s
                elif st == 1:                 
                    pdos_up[((ai-1)*ndos)+i][1] = float(l[2]) # p1
                    pdos_up[((ai-1)*ndos)+i][2] = float(l[3]) # p2
                    pdos_up[((ai-1)*ndos)+i][3] = float(l[4]) # p3
                elif st == 2:
                    pdos_up[((ai-1)*ndos)+i][4] = float(l[2]) # d1
                    pdos_up[((ai-1)*ndos)+i][5] = float(l[3]) # d2
                    pdos_up[((ai-1)*ndos)+i][6] = float(l[4]) # d3
                    pdos_up[((ai-1)*ndos)+i][7] = float(l[5]) # d4
                    pdos_up[((ai-1)*ndos)+i][8] = float(l[6]) # d5
                elif st == 3: 
                    pdos_up[((ai-1)*ndos)+i][9]  = float(l[2]) # f1
                    pdos_up[((ai-1)*ndos)+i][10] = float(l[3]) # f2
                    pdos_up[((ai-1)*ndos)+i][11] = float(l[4]) # f3
                    pdos_up[((ai-1)*ndos)+i][12] = float(l[5]) # f4
                    pdos_up[((ai-1)*ndos)+i][13] = float(l[6]) # f5
                    pdos_up[((ai-1)*ndos)+i][14] = float(l[7]) # f6
                    pdos_up[((ai-1)*ndos)+i][15] = float(l[8]) # f7 
            start = start + ndos
    pdos_up = np.array(pdos_up, np.float)/2; pdos_dw = []
    
    
    if nspin == 2:
        
        tpdos = []; tpdos_up = []; tpdos_dw = []
        for t in range(ndos):
            l = lines[t+1+nstate].split()
            tpdos_up.append(float(l[1]))
            tpdos_dw.append(float(l[2]))
        tpdos_up = np.array(tpdos_up, np.float); tpdos_dw = np.array(tpdos_dw, np.float)    
        tpdos.append(tpdos_up); tpdos.append(tpdos_dw)
        
        pdos_dw = pdos_up
        start=ndos
        for s in range(nstate):
            ai = atom_list[s]  # atom index
            st = state_list[s] # state type
            for i in range(ndos):
                l = lines[start+i+1+nstate].split()
                if st == 0: 
                    pdos_up[((ai-1)*ndos)+i][0] = float(l[3]) # s
                    pdos_dw[((ai-1)*ndos)+i][0] = float(l[4]) # s
                elif st == 1:                 
                    pdos_up[((ai-1)*ndos)+i][1] = float(l[3]) # p1
                    pdos_dw[((ai-1)*ndos)+i][1] = float(l[4]) # p1                    
                    pdos_up[((ai-1)*ndos)+i][2] = float(l[5]) # p2
                    pdos_dw[((ai-1)*ndos)+i][2] = float(l[6]) # p2
                    pdos_up[((ai-1)*ndos)+i][3] = float(l[7]) # p3
                    pdos_dw[((ai-1)*ndos)+i][3] = float(l[8]) # p3                    
                elif st == 2:
                    pdos_up[((ai-1)*ndos)+i][4] = float(l[3])  # d1
                    pdos_dw[((ai-1)*ndos)+i][4] = float(l[4])  # d1
                    pdos_up[((ai-1)*ndos)+i][5] = float(l[5])  # d2
                    pdos_dw[((ai-1)*ndos)+i][5] = float(l[6])  # d2
                    pdos_up[((ai-1)*ndos)+i][6] = float(l[7])  # d3
                    pdos_dw[((ai-1)*ndos)+i][6] = float(l[8])  # d3
                    pdos_up[((ai-1)*ndos)+i][7] = float(l[9])  # d4
                    pdos_dw[((ai-1)*ndos)+i][7] = float(l[10]) # d4
                    pdos_up[((ai-1)*ndos)+i][8] = float(l[11]) # d5
                    pdos_dw[((ai-1)*ndos)+i][8] = float(l[12]) # d5                    
                elif st == 3: 
                    pdos_up[((ai-1)*ndos)+i][9]  = float(l[3]) # f1
                    pdos_dw[((ai-1)*ndos)+i][9]  = float(l[4]) # f1
                    pdos_up[((ai-1)*ndos)+i][10] = float(l[5]) # f2
                    pdos_dw[((ai-1)*ndos)+i][10] = float(l[6]) # f2
                    pdos_up[((ai-1)*ndos)+i][11] = float(l[7]) # f3
                    pdos_dw[((ai-1)*ndos)+i][11] = float(l[8]) # f3
                    pdos_up[((ai-1)*ndos)+i][12] = float(l[9]) # f4 
                    pdos_dw[((ai-1)*ndos)+i][12] = float(l[10]) # f4
                    pdos_up[((ai-1)*ndos)+i][13] = float(l[11]) # f5
                    pdos_dw[((ai-1)*ndos)+i][13] = float(l[12]) # f5
                    pdos_up[((ai-1)*ndos)+i][14] = float(l[13]) # f6
                    pdos_dw[((ai-1)*ndos)+i][14] = float(l[14]) # f6
                    pdos_up[((ai-1)*ndos)+i][15] = float(l[15]) # f7
                    pdos_dw[((ai-1)*ndos)+i][15] = float(l[16]) # f7                     
            start = start + ndos
      
    pdos_up = np.array(pdos_up, np.float); pdos_dw = np.array(pdos_dw, np.float)
    
    
    pdos_info = []
    pdos_info.append(nspin)
    pdos_info.append(natom)
    pdos_info.append(ndos)
    pdos_info.append(len(pdos_up))
    pdos_info.append(len(pdos_dw))
    pdos_info.append(int(max(state_list)))

    if savekey == 1: 
        np.save('pdos_info', pdos_info)
        np.save('Epdos', Epdos)
        np.save('tpdos', tpdos)
        np.save('pdos_up', pdos_up)
        np.save('pdos_dw', pdos_dw)
        
    return pdos_info, Epdos, tpdos, pdos_up, pdos_dw





#########################################################################################
#########################################################################################
#########################################################################################
#########################################################################################
#########################################################################################
#########################################################################################
#########################################################################################
#########################################################################################
#########################################################################################
#########################################################################################
#########################################################################################
#########################################################################################
#########################################################################################
#########################################################################################
#########################################################################################
#########################################################################################
#########################################################################################
#########################################################################################
#########################################################################################
#########################################################################################
#########################################################################################
#########################################################################################







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







#########################################################################################
#########################################################################################
#########################################################################################
#########################################################################################
#########################################################################################
#########################################################################################
#########################################################################################
#########################################################################################
#########################################################################################
#########################################################################################
#########################################################################################
#########################################################################################
#########################################################################################
#########################################################################################
#########################################################################################
#########################################################################################
#########################################################################################
#########################################################################################
#########################################################################################
#########################################################################################
#########################################################################################
#########################################################################################










def getpdos(pdosin,sel,sigma):
    
    pdos_info, Epdos, tpdos, pdos_up, pdos_dw = pdosin
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
    else: spin=1
    
    ndos = pdos_info[2]
    nspin = pdos_info[0]
    
    if spin == 1: pdos_sel = pdos_up; tsel = tpdos[0]
    elif nspin == 1: pdos_sel= pdos_up; tsel = tpdos[0]
    else: pdos_sel = pdos_dw; tsel = tpdos[1] 
    
    out = Epdos*0
    for a in range(len(atoms)):
        tmp = []
        for i in range(ndos):
            current_line = pdos_sel[(ndos*(atoms[a]-1))+i]
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
    
    Esel, tsel = mSMOOTH.Gaussian(Epdos,tsel,sigma,0)
    Esel, psel = mSMOOTH.Gaussian(Epdos,out,sigma,0)
    
    return Esel, tsel, psel 









#########################################################################################
#########################################################################################
#########################################################################################
#########################################################################################
#########################################################################################
#########################################################################################
#########################################################################################
#########################################################################################
#########################################################################################
#########################################################################################
#########################################################################################
#########################################################################################
#########################################################################################
#########################################################################################
#########################################################################################
#########################################################################################
#########################################################################################
#########################################################################################
#########################################################################################
#########################################################################################
#########################################################################################
#########################################################################################






def readqe(scffile=None,tmpfolder=None,cleankey=None): 
    
    if cleankey == 1:
        if os.path.isfile('qe.npz') == True:
            print('  qe.npz exists !!!. Remove it first.')
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
    
    if os.path.isfile('pdos.out') == True:
        sp.call(' sed -n \'/Charges/,/Spilling/p\' pdos.out  > lowdin.dat ', shell=True)
    else: sp.call('  > lowdin.dat ', shell=True)    
           
    if os.path.isfile('pdos.dos') == True:
        readpdos(savekey=1)
        
    if os.path.isfile('pwscf.dos') == True:
        readtdos(savekey=1)
    else: 
        if os.path.isfile('pwscf.pdos_tot') == True:
            readtdos(savekey=1)
        
    if os.path.isfile(scffile) == True:
        readscfout(file=scffile,savekey=1)

    #if os.path.isdir(tmpfolder) == True:
        #print('reading qetmp folder')
        #readxml(tmpfolder=tmpfolder,savekey=1)

   
    if cleankey == 1:
        if os.path.isfile('qe.npz') == True:
            print('  qe.npz exists !!!. Remove it first.')
        else:    
            sp.call(' rm -f pdos.dos pwscf.dos pwscf.pdos_tot pdos.out pdos.mat', shell=True)
            sp.call(' zip pseudos.zip *.UPF *.upf ', shell=True)
            sp.call(' rm -f *.upf *.UPF pdos.* pwscf.pdos_* dos.*', shell=True) 
            sp.call(' zip qe.npz *.npy pseudos.zip tdos_*.dat lowdin.dat ', shell=True)
            time.sleep(1)
            sp.call('  rm -f *.npy pseudos.zip tdos_*.dat lowdin.dat', shell=True)
    else:
        sp.call(' rm -rf qe.npz ', shell=True)        
        sp.call(' zip qe.npz *.npy  tdos_*.dat lowdin.dat ', shell=True)
        time.sleep(1)
        sp.call(' rm -f *.npy tdos_*.dat lowdin.dat supportInfo.kpath kpts.pwscf', shell=True)
    
    return
























params, lattice, positions, qe_alat, qe_cell = readxml()


#print(params)


f = open('./qetmp/pwscf.vasp', 'w')
f.write('generated by qe2poscar.py  \n')
f.write('1.000  \n')

print('%12.8f' %(lattice[0][0]),  '%12.8f' %(lattice[0][1]),  '%12.8f' %(lattice[0][2]), file=f)
print('%12.8f' %(lattice[1][0]),  '%12.8f' %(lattice[1][1]),  '%12.8f' %(lattice[1][2]), file=f) 
print('%12.8f' %(lattice[2][0]),  '%12.8f' %(lattice[2][1]),  '%12.8f' %(lattice[2][2]), file=f) 

for s in params[7]:
    f.write(s+' ')
f.write('\n')    
for n in params[8]:
    f.write(str(n)+' ')
f.write('\n')
f.write('C \n')

for p in range(len(positions)):
    print('%12.8f' %(positions[p][0]),  '%12.8f' %(positions[p][1]),  '%12.8f' %(positions[p][2]), file=f)
    
    
f.close() 


















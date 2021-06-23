#!/usr/bin/env python

import numpy as np
from functools import reduce
import operator




def readqeout(file=None):
    
    if file is None: file='scf.out'
      
    lattice = []; positions = [];  positions_d = []; alabels = []; 
    recipro = []; qe_params = []; atypes = []; kpoints = []; efermi = [];
    etot = []; ptot = []; tmag = []; bands = []; bands2 = []; bands_up = []; bands_dw = [];  
    
    with open(file, mode='r') as f:
      lines = [line for line in f.readlines()]
      for i, line in enumerate(lines):
        
        if 'lattice parameter (alat)  =' in line:
            alat= lines[i].split()[4]; alat = float(alat) * 0.529177257507 
            volume= lines[i+1].split()[3]; volume = float(volume) * 0.148184711486445 ; qe_params.append(volume)	
            natom = lines[i+2].split()[4];  natom = int(natom)    ; qe_params.append(natom)
            ntype = lines[i+3].split()[5];  ntype = int(ntype)    ; qe_params.append(ntype)
            nelec = lines[i+4].split()[4];  nelec = float(nelec)  ; qe_params.append(nelec)
            nband = lines[i+5].split()[4];  nband = int(nband)    ; qe_params.append(nband) ; math1=nband/8 ; math2=nband%8; 
            ecutw = lines[i+6].split()[3];  ecutw = float(ecutw)  ; qe_params.append(ecutw)
            ecutr = lines[i+7].split()[4];  ecutr = float(ecutr)  ; qe_params.append(ecutr)
            
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

        #print(file)

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
      
    qe_params.append(nspin)  

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
            
            
    ### generate kpts path
    kpoints_path = []
    kpoints_path.append(0) 
    
    for k in range(len(kpoints)-1):
      k0=kpoints[k];
      k1=kpoints[k+1];
      dx=k0[0]-k1[0]; dy=k0[1]-k1[1]; dz=k0[2]-k1[2];
      newk=kpoints_path[k]+np.sqrt(dx*dx+dy*dy+dz*dz);
      kpoints_path.append(newk)
    kpoints_path = np.array(kpoints_path, np.float)  
    kpoints_path = kpoints_path/kpoints_path[-1]  
        
    #if savekey == 1: 
        #np.save('qe_params', np.array(qe_params, np.float))        
        #np.save('efermi', efermi)
        #np.save('kpoints', kpoints)
        #np.save('kpoints_path', kpoints_path)        
        #np.save('bands_up', bands_up)        
        #np.save('bands_dw', bands_dw)
        #np.save('lattice', lattice)
        #np.save('recipro', recipro)
        #np.save('positions', positions)
        #np.save('positions_d', positions_d) 
        #np.save('etot', etot)        
        #np.save('ptot', ptot) 
        #np.save('tmag', tmag) 
        #np.save('alabels', alabels)
        #np.save('atypes', atypes)  
        
    return qe_params, efermi, kpoints, bands_up, bands_dw, lattice, recipro, positions, positions_d, etot, tmag, alabels, atypes    
    
    
 
 

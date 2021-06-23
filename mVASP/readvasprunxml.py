#!/usr/bin/env python


import numpy as np



# DOES NOT read partial stuff !!
def readvasprunxml(file=None):
    
    if file is None: file='vasprun.xml'
    
    with open(file) as f:
        lines = f.readlines()
    
    kpointsDir = []
    vasp_params  = []
    poscar0 = []
    bands0  = []
    occups0 = []
    Edos0   = []
    tdos0   = []
    rec_basis = []
    pdos0 = []
    klines0 = []
    
    for i, line in enumerate(lines):

        if '  <generation param="listgenerated">' in line:
            kl = i
            while True:
                t = lines[kl].split()
                if t[0]=='<v>':
                    klines0.append((lines[kl].split()[1:4]))
                if t[0]=='</generation>':
                    break
                kl += 1
            klines0  = np.array(klines0, np.float)

        if '  <varray name="kpointlist" >' in line:
            k = i
            while True:
                t = lines[k].split()
                if t[0]=='<v>':
                    kpointsDir.append((lines[k].split()[1:4]))
                if t[0]=='</varray>':
                    break
                k += 1
            NKPTS  = int(len(kpointsDir))
            kpointsDir  = np.array(kpointsDir, np.float)
        
        if line.startswith(' <parameters>'):                   
            ENCUT  = float(lines[i+7].split()[2][:-4])                  # ENCUT
            NBANDS = int(lines[i+12].split()[3][:-4])                 # NBANDS
            NELECT = float(lines[i+13].split()[2][:-4])                # NELECT
            
        if line.startswith('   <separator name="electronic spin" >'):
            NSPIN   = int(lines[i+1][-6:-5])         
            LNONCOL = str(lines[i+2][-8:-7])
            LSORBIT = str(lines[i+5][-8:-7])                       

        if line.startswith('  <separator name="ionic" >'):
            NSW  = int(lines[i+1].split()[3][:-4])                  # NSW
            ISIF = int(lines[i+3].split()[3][:-4])                  # ISIF

        if line.startswith('  <separator name="dos" >'):
            NEDOS = int(lines[i+3].split()[3][:-4])                  # NEDOS
            
        if line.startswith(' <atominfo>'):
            NATOMS = int(lines[i+1][-17:-9])                      # NATOMS
            NTYPES = int(lines[i+2][-17:-9])                         # NTYPES

        if line.startswith(' <structure name="initialpos" >'):
            poscar0.append(lines[i+3].split()[1:4])                    # lat1
            poscar0.append(lines[i+4].split()[1:4])                    # lat2
            poscar0.append(lines[i+5].split()[1:4])                    # lat3
            
            rec_basis.append(lines[i+9].split()[1:4])                    # rec1
            rec_basis.append(lines[i+10].split()[1:4])                   # rec2
            rec_basis.append(lines[i+11].split()[1:4])                   # rec3
            rec_basis  = np.array(rec_basis, np.float)
            
            t=4
            for a in range(NATOMS):
                poscar0.append(lines[i+11+t].split()[1:4])
                t += 1
         
        if '    <field>eigene</field>' in line:
            n = i
            while True:
                t = lines[n].split();
                if t[0]=='<r>':
                    bands0.append((t[1]))             
                    occups0.append((t[2]))
                if t[0]=='</eigenvalues>':  
                    break
                n += 1

        if '  <dos>' in line:
            m = i
            efermi = lines[m+1][-20:-5]; efermi=float(efermi);
            while True:
                t = lines[m].split();
                if t[0]=='<r>':
                    tdos0.append((t[1:3]))
                if t[0]=='</dos>':
                    break
                if t[0]=='</total>':
                    break                
                m += 1
            #break
        
        
        if '   <partial>' in line:
            orbitals = []

            p = i+6           
            for o in range(16):
                t = lines[p]
                #print t
                if '<field>' in t:
                    orbitals.append(t[12:15])
                p += 1
                
            p = i+6
            while True:
                t = lines[p].split();
                if t[0]=='<r>':
                    pdos0.append((t[2:len(orbitals)+2]))
                if t[0]=='</partial>':
                    break
                p += 1
            break
                    




    if LNONCOL=='T':
        vasp_params.append(1)
        bdivisor = 1
    else:
        vasp_params.append(0) 
        bdivisor = 2        
    if LSORBIT=='T':
        vasp_params.append(1)
    else:
        vasp_params.append(0)         

    vasp_params.append(NSPIN)
    vasp_params.append(NKPTS)
    vasp_params.append(NBANDS)
    vasp_params.append(NEDOS)    
    vasp_params.append(NATOMS)
    vasp_params.append(NTYPES)
    vasp_params.append(NELECT)
    vasp_params.append(NSW)    
    vasp_params.append(ISIF)     

    bands_up = [] 
    bands_dw = []  

    # re-arrange bands
    if NSPIN==1 and not LNONCOL=='T':
        for b in range(NBANDS):
            n=b; tmp = []
            for k in range(NKPTS):
               tmp.append(bands0[n])
               n += NBANDS
            bands_up.append(tmp)
        bands_dw = bands_up
    elif NSPIN==2 and not LNONCOL=='T':       
        for b in range(NBANDS):
            n=b 
            tmp1 = []; tmp2 = []
            for k in range(NKPTS):
               tmp1.append(bands0[n])
               tmp2.append(bands0[n+(NBANDS*NKPTS)])               
               n += NBANDS
            bands_up.append(tmp1)
            bands_dw.append(tmp2)
    else:
        print('')
        print('Non-collinear case !!')
        print('I am setting spin-orbit bands as bands_up')
        print('')
        for b in range(NBANDS):
            n=b 
            tmp = [];
            for k in range(NKPTS):
               tmp.append(bands0[n])            
               n += NBANDS
            bands_up.append(tmp) 
        bands_dw = bands_up

## re-arrange tdos        
    #Edos    = []
    #tdos_up = []
    #tdos_dw = []

    #if NSPIN==1 and not LNONCOL=='T':
        #for d in range(NEDOS):
            #Edos.append(tdos0[d][0])
            #tdos_up.append(float(tdos0[d][1])/2)
        #tdos_dw = tdos_up
    #elif NSPIN==2 and not LNONCOL=='T ':
        #for d in range(NEDOS):
            
            #try:
                #tdos0[d][0]
            #except:
                #efermi=0
                #break
                
            #Edos.append(tdos0[d][0])
            #tdos_up.append(tdos0[d][1])
        #for d in range(NEDOS,NEDOS*2):
            
            #try:
                #tdos0[d][0]
                #efermi=0
            #except:
                #break                     
            
            #tdos_dw.append(tdos0[d][1])
    #else:
        #print('Non-collinear TDOS is not implemeted yet !!!!' )
        
        
## re-arrange pdos
    #pdos0  = np.array(pdos0, np.float)
    #pdos_up = []; pdos_dw = []
    
    #if len(pdos0) != 0:
        #if NSPIN==1 and not LNONCOL=='T':
            #for a in range(NATOMS):
                #t = a*1*NEDOS
                #for p in range(NEDOS):
                    #pdos_up.append(pdos0[t]/2)
                    #pdos_dw.append(pdos0[t]/2)
                    #t += 1        
        #elif NSPIN==2 and not LNONCOL=='T':
            #for a in range(NATOMS):
                #t = a*2*NEDOS
                #for p in range(NEDOS):
                    #pdos_up.append(pdos0[t])
                    #pdos_dw.append(pdos0[t+NEDOS])
                    #t += 1
        #else:
            #print() 
            #print('Non-collinear PDOS is not implemeted yet !!!!')
    #else:
        #print()
        #print('Projected DOS is empty !!! Set LORBIT = 11 to get it ')
        



    
    #get kpoints_path
    kpoints_new = []; tmp = []
    for k in range(NKPTS):
        tmp.append( kpointsDir[k][0]*rec_basis[0][0] + kpointsDir[k][1]*rec_basis[1][0] + kpointsDir[k][2]*rec_basis[2][0] );
        tmp.append( kpointsDir[k][0]*rec_basis[0][1] + kpointsDir[k][1]*rec_basis[1][1] + kpointsDir[k][2]*rec_basis[2][1] );
        tmp.append( kpointsDir[k][0]*rec_basis[0][2] + kpointsDir[k][1]*rec_basis[1][2] + kpointsDir[k][2]*rec_basis[2][2] );
        kpoints_new.append(tmp); tmp = [] 

    kpoints_new  = np.array(kpoints_new, np.float)    
    kpoints_path = []
    kpoints_path.append(0)
    for k in range(len(kpoints_new)-1):
        k0=kpoints_new[k]
        k1=kpoints_new[k+1]
        dx=k0[0]-k1[0]; dy=k0[1]-k1[1]; dz=k0[2]-k1[2]
        newk=kpoints_path[k]+np.sqrt(dx*dx+dy*dy+dz*dz)
        kpoints_path.append(newk)    
    kpoints_path = np.array(kpoints_path, np.float)
    
    
    #get klines_path
    klines_new = []; tmp = []
    for k in range(len(klines0)):
        tmp.append( klines0[k][0]*rec_basis[0][0] + klines0[k][1]*rec_basis[1][0] + klines0[k][2]*rec_basis[2][0] );
        tmp.append( klines0[k][0]*rec_basis[0][1] + klines0[k][1]*rec_basis[1][1] + klines0[k][2]*rec_basis[2][1] );
        tmp.append( klines0[k][0]*rec_basis[0][2] + klines0[k][1]*rec_basis[1][2] + klines0[k][2]*rec_basis[2][2] );
        klines_new.append(tmp); tmp = [] 
        
    klines_new  = np.array(klines_new, np.float)    
    klines_path = []
    klines_path.append(0)
    for k in range(len(klines_new)-1):
        k0=klines_new[k]
        k1=klines_new[k+1]
        dx=k0[0]-k1[0]; dy=k0[1]-k1[1]; dz=k0[2]-k1[2]
        newk=klines_path[k]+np.sqrt(dx*dx+dy*dy+dz*dz)
        klines_path.append(newk)    
    klines_path = np.array(klines_path, np.float)
    

    kpoints_path = kpoints_path/kpoints_path[-1]    
    klines_path  = klines_path/kpoints_path[-1]
    
    
    bands_up = np.array(bands_up, np.float)
    bands_dw = np.array(bands_dw, np.float)


## bandgap part 
    gap_data = []; 
    
    # alternative method to find band gap
    bminsu = []; bmaxsu = []; 
    
    for ub in range(NBANDS):
        tmp=float(min(bands_up[ub])-efermi);   
        if tmp > 0:
            bminsu.append(tmp)
  
    for ub in range(NBANDS):
        tmp=float(efermi-max(bands_up[ub]));   
        if tmp > -0.001:
            bmaxsu.append(tmp)
            
    gapu1 = min(bminsu)+min(bmaxsu)
    fcoru1 = min(bminsu)-gapu1/2
    
    bminsd = []; bmaxsd = [];
    
    for db in range(NBANDS):
        tmp=float(min(bands_dw[db])-efermi);   
        if tmp > 0:
            bminsd.append(tmp)
  
    for db in range(NBANDS):
        tmp=float(efermi-max(bands_dw[db]));   
        if tmp > -0.001:
            bmaxsd.append(tmp)
            
    gapd1 = min(bminsd)+min(bmaxsd) 
    fcord1 = min(bminsd)-gapd1/2  
    
    gap_data.append(round(gapu1,3))
    gap_data.append(round(gapd1,3))
    
  
  
  
    vmax = int(vasp_params[8]/bdivisor);
    Evmaxpointsu=[]; Ecminpointsu=[]
    Evmaxu=max(bands_up[vmax-1]); Ecminu=min(bands_up[vmax])  
    gapu2=min(bands_up[vmax])-max(bands_up[vmax-1]); gap_data.append(round(gapu2, 3))
    
    Evmaxpointsd=[]; Ecminpointsd=[]
    Evmaxd=max(bands_dw[vmax-1]); Ecmind=min(bands_dw[vmax])  
    gapd2=min(bands_dw[vmax])-max(bands_dw[vmax-1]); gap_data.append(round(gapd2, 3))  
    
    fcoru2=efermi-Evmaxu
    fcord2=efermi-Evmaxd    
    
    for p, vmaxbandu in enumerate(bands_up[vmax-1]):
        if Evmaxu == vmaxbandu:
            Evmaxpointsu.append(p)
    #print Evmaxpointsu           
            
    for p, cminbandu in enumerate(bands_up[vmax]):
        if Ecminu == cminbandu:
            Ecminpointsu.append(p)           
    #print Ecminpointsu          
            
    if Evmaxpointsu == Ecminpointsu:
        gap_data.append(1) # direct
    else:
        gap_data.append(2) # indirect
        #print Ecminpointsu
        #print Evmaxpointsu        
   

    for p, vmaxbandd in enumerate(bands_dw[vmax-1]):
        if Evmaxd == vmaxbandd:
            Evmaxpointsd.append(p)         
            
    for p, cminbandd in enumerate(bands_dw[vmax]):
        if Ecmind == cminbandd:
            Ecminpointsd.append(p)               
            
    if Evmaxpointsd == Ecminpointsd:
        gap_data.append(1) # direct
    else:
        gap_data.append(2) # indirect
        #print Ecminpointsd
        #print Evmaxpointsd

    
    fcor = (min(gapu2,gapd2)/2)-min(fcoru2,fcord2); gap_data.append(fcor)
    
    
    
    #efermi = (efermi+fcor)
    #print()
    #print(('ATTENTION: '+str(round(fcor,3))+' eV fermi-level correction was applied.'))
    #print('           This might give rise to wrong Fermi energy if your system is metallic !!')   
    #print('')


    vasp_params.extend(gap_data)

   
    kpointsDir  = np.array(kpointsDir, np.float)
    vasp_params  = np.array(vasp_params, np.float)

    poscar0 = np.array(poscar0, np.float) 
    
    kpoints=kpointsDir
    

    return vasp_params, kpoints, kpoints_path, klines_path, poscar0, bands_up, bands_dw, efermi
 

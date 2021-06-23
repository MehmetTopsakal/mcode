#!/usr/bin/python2

import numpy as np
from   pylab import *
import scipy.io as sio

import operator

import numpy as np
from functools import reduce
#from ase.atoms import Atoms, Atom
#from ase import units
#from ase.calculators.singlepoint import SinglePointCalculator


inputs = sys.argv
ilen   = len(inputs)

if ilen == 1:
  inputs.append('scf.out'); inputs.append(1); inputs.append(2); 
if ilen == 2:
  inputs.append(1); inputs.append(2);
if ilen == 3:
  inputs.append(1);

file = inputs[1]       # input file
rkey = int(inputs[2])  # read key
wkey = int(inputs[3])  # write key




def reader1(file):
  lattice = []; positions = [];  positions_d = []; alabels = []; 
  recipro = []; params = []; atypes = []; kpoints = []; efermi = [];
  etot = []; ptot = []; tmag = []; bands = []; bands_up = []; bands_dw = [];
  with open(file, mode='r') as f:
    lines = [line for line in f.readlines()]
    for i, line in enumerate(lines):
      
      if 'lattice parameter (alat)  =' in line:
	alat= lines[i].split()[4]; alat = float(alat) * 0.529177257507 
	volume= lines[i+1].split()[3]; volume = float(volume) * 0.148184711486445 ; params.append(volume)	
	natom = lines[i+2].split()[4];  natom = int(natom)    ; params.append(natom)
	ntype = lines[i+3].split()[5];  ntype = int(ntype)    ; params.append(ntype)
	nelec = lines[i+4].split()[4];  nelec = float(nelec)  ; params.append(nelec)
	nband = lines[i+5].split()[4];  nband = int(nband)    ; params.append(nband) ; math1=nband/8 ; math2=nband%8; 
	ecutw = lines[i+6].split()[3];  ecutw = float(ecutw)  ; params.append(ecutw)
	ecutr = lines[i+7].split()[4];  ecutr = float(ecutr)  ; params.append(ecutr)
	#thrsh = lines[i+8].split()[3];  thrsh = float(thrsh)  ; params.append(thrsh)
	
      if 'celldm(1)=' in line:
	lattice.append(lines[i+4].split()[3:6])
	lattice.append(lines[i+5].split()[3:6])
	lattice.append(lines[i+6].split()[3:6])	
	lattice = np.array(lattice); lattice = lattice.astype(np.float); lattice = lattice*alat
	recipro.append(lines[i+9].split()[3:6])	
	recipro.append(lines[i+10].split()[3:6])	
	recipro.append(lines[i+11].split()[3:6])		
	recipro = np.array(recipro); recipro = recipro.astype(np.float); recipro = recipro*2*pi*(1/alat)
	
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
			
      if 'total magnetization       = ' in line:
	tmag = lines[i].split()[3]; tmag = float(tmag)			
      
      if ')   bands (ev):' in line:
	  energies = [];
	  if math1 == 0:
	    math1=1
	  for bi in range(math1):
	    energies.append(lines[i+2+bi].split());
	  if math1 != 0:  
	    energies.append(lines[i+3+bi].split());
	  bands.append(reduce(operator.add, energies))   
      
      if '     band energies (ev):' in line:
	  energies = [];
	  if math1 == 0:
	    math1=1
	  for bi in range(math1):
	    energies.append(lines[i+2+bi].split());
	  if math1 != 0:  
	    energies.append(lines[i+3+bi].split());
	  bands.append(reduce(operator.add, energies))  	  
	  	  
  bands=np.array(bands); 
  bands=bands.astype(np.float); 
  bands=np.transpose(bands);
  

  try:
    nspin
  except:
    nspin = 1
  
  params.append(nspin);
 
 
  if nspin == int(1):
    bands_up = bands; bands_dw = bands; 

  if nspin == int(2):
    for u in range(nband):
      bands_up.append(bands[u][0:nkpts/2]); bands_dw.append(bands[u][nkpts/2:nkpts]);
    bands_up = np.array(bands_up); bands_up = bands_up.astype(np.float);
    bands_dw = np.array(bands_dw); bands_dw = bands_dw.astype(np.float);
    kpoints = kpoints[:nkpts/2];
    nkpts = nkpts/2; 
 
 
## bandgap part  

  bminsu = []; bmaxsu = []; gap_data = []; 
  
  for ub in range(int(params[4])):
      tmp=float(min(bands_up[ub])-efermi);   
      if tmp > 0:
          bminsu.append(tmp)

  for ub in range(int(params[4])):
      tmp=float(efermi-max(bands_up[ub]));   
      if tmp > -0.001:
          bmaxsu.append(tmp)
          
  gapu1 = min(bminsu)+min(bmaxsu)
  fcoru = min(bminsu)-gapu1/2
  
  bminsd = []; bmaxsd = [];
  
  for db in range(int(params[4])):
      tmp=float(min(bands_dw[db])-efermi);   
      if tmp > 0:
          bminsd.append(tmp)

  for db in range(int(params[4])):
      tmp=float(efermi-max(bands_dw[db]));   
      if tmp > -0.001:
          bmaxsd.append(tmp)
          
  gapd1 = min(bminsd)+min(bmaxsd) 
  fcord = min(bminsd)-gapd1/2  
  
  gap_data.append(gapu1)
  gap_data.append(gapd1)




  vmax = params[3]/2;
  Evmaxpointsu=[]; Ecminpointsu=[]
  Evmaxu=max(bands_up[vmax-1]); Ecminu=min(bands_up[vmax])  
  gapu2=min(bands_up[vmax])-max(bands_up[vmax-1]); gap_data.append(gapu2)
  
  

  vmax = params[3]/2;  
  Evmaxpointsd=[]; Ecminpointsd=[]
  Evmaxd=max(bands_dw[vmax-1]); Ecmind=min(bands_dw[vmax])  
  gapd2=min(bands_dw[vmax])-max(bands_dw[vmax-1]); gap_data.append(gapd2)  
  
  
  
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
 
    
  for p, vmaxbandd in enumerate(bands_dw[vmax-1]):
      if Evmaxd == vmaxbandd:
          Evmaxpointsd.append(p)
  #print Evmaxpointsd            
          
  for p, cminbandd in enumerate(bands_dw[vmax]):
      if Ecmind == cminbandd:
          Ecminpointsd.append(p)           
  #print Ecminpointsd          
          
  if Evmaxpointsd == Ecminpointsd:
      gap_data.append(1) # direct
  else:
      gap_data.append(2) # indirect
 

# used for aligning E-fermi line  
  gap_data.append(fcoru)
  gap_data.append(fcord)  
  
  #print gap_data
  #print ptot
  

 
 
  sio.savemat('.readqe.mat', dict(params=params, lattice=lattice, recipro=recipro, positions=positions,  positions_d=positions_d, kpoints=kpoints, efermi=efermi, etot=etot, ptot=ptot, tmag=tmag, atypes=atypes, alabels=alabels, bands_up=bands_up, bands_dw=bands_dw, gap_data=gap_data )) #http://docs.scipy.org/doc/scipy-0.14.0/reference/tutorial/io.html 
  return


reader1(file)










































## "some parts" of this code are stolen from ase (Why ? Because Mehmet is a lazy person....)
#def qe_readscf(fileobj, index):

    #if isinstance(fileobj, str):
        #fileobj = open(fileobj, 'rU')
    #lines = fileobj.readlines()
    #images = []

    ## Get unit cell info.
    #bl_line = [line for line in lines if 'bravais-lattice index' in line]
    #if len(bl_line) != 1:
        #raise NotImplementedError('Unsupported: unit cell changing.')
    #bl_line = bl_line[0].strip()
    #brav_latt_index = bl_line.split('=')[1].strip()    
    #lp_line = [line for line in lines if 'lattice parameter (alat)' in
               #line]
    #if len(lp_line) != 1:
        #raise NotImplementedError('Unsupported: unit cell changing.')    
    #lp_line = lp_line[0].strip().split('=')[1].strip().split()[0]
    #lattice_parameter = float(lp_line) * 0.529177257507
    
    #ca_line_no = [number for (number, line) in enumerate(lines) if
                  #'crystal axes: (cart. coord. in units of alat)' in line]
    #if len(ca_line_no) != 1:
        #raise NotImplementedError('Unsupported: unit cell changing.')
    #ca_line_no = int(ca_line_no[0])
    
    
    #cell = np.zeros((3, 3))
    #for number, line in enumerate(lines[ca_line_no + 1: ca_line_no + 4]):
        #line = line.split('=')[1].strip()[1:-1]
        #values = [eval(value) for value in line.split()]
        #cell[number, 0] = values[0]
        #cell[number, 1] = values[1]
        #cell[number, 2] = values[2]
    #cell *= lattice_parameter # in Angst.

    ### Find atomic positions and add to images.
    ##for number, line in enumerate(lines):
        ##key = 'Begin final coordinates'  # these just reprint last posn.
        ##if key in line:
            ##break
        ##key = 'Cartesian axes'
        ##if key in line:
            ##atoms = make_atoms(number, lines, key, cell)
            ##images.append(atoms)
        ##key = 'ATOMIC_POSITIONS (crystal)'
        ##if key in line:
            ##atoms = make_atoms(number, lines, key, cell)
            ##images.append(atoms)
    ##return images[index]
    #return cell 
 

#cell = qe_readscf('scf1.out', 1)
#print cell

 
 
 
#def make_atoms(index, lines, key, cell):
    #"""Scan through lines to get the atomic positions."""
    #atoms = Atoms()
    #if key == 'Cartesian axes':
        #for line in lines[index + 3:]:
            #entries = line.split()
            #if len(entries) == 0:
                #break
            #symbol = entries[1][:-1]
            #x = float(entries[6])
            #y = float(entries[7])
            #z = float(entries[8])
            #atoms.append(Atom(symbol, (x, y, z)))
        #atoms.set_cell(cell)
    #elif key == 'ATOMIC_POSITIONS (crystal)':
        #for line in lines[index + 1:]:
            #entries = line.split()
            #if len(entries) == 0 or (entries[0] == 'End'):
                #break
            #symbol = entries[0][:-1]
            #x = float(entries[1])
            #y = float(entries[2])
            #z = float(entries[3])
            #atoms.append(Atom(symbol, (x, y, z)))
        #atoms.set_cell(cell, scale_atoms=True)
    ## Energy is located after positions.
    #energylines = [number for number, line in enumerate(lines) if
                   #('!' in line and 'total energy' in line)]
    #energyline = min([n for n in energylines if n > index])
    #energy = float(lines[energyline].split()[-2]) * units.Ry
    ## Forces are located after positions.
    #forces = np.zeros((len(atoms), 3))
    #forcelines = [number for number, line in enumerate(lines) if
                  #'Forces acting on atoms (Ry/au):' in line]
    #forceline = min([n for n in forcelines if n > index])
    #for line in lines[forceline + 4:]:
        #words = line.split()
        #if len(words) == 0:
            #break
        #fx = float(words[-3])
        #fy = float(words[-2])
        #fz = float(words[-1])
        #atom_number = int(words[1]) - 1
        #forces[atom_number] = (fx, fy, fz)
    #forces *= units.Ry / units.Bohr
    #calc = SinglePointCalculator(atoms, energy=energy, forces=forces)
    #atoms.set_calculator(calc)
    #return atoms
 
 
 
 
 
 
 
 
 
 
 



















#print lat
#print pos
##sio.savemat('POSCAR.mat', dict(lat=lat, pos=pos)) #http://docs.scipy.org/doc/scipy-0.14.0/reference/tutorial/io.html









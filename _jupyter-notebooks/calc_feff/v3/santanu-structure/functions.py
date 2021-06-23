
# this gets POSCAR file from MP
def get_poscar(mpid):
    
    data = mpr.get_data(mpid, data_type="vasp")
    
    # if icsd_id is not available, this stucture 
    # might be artifical. So I get relaxed coordinates.
    if data[0]['icsd_ids']:
        structure = mpr.get_structure_by_material_id(mpid,final=False) # get initial coordinates ()
        structure.to(filename = "POSCAR")       
    else:
        structure = mpr.get_structure_by_material_id(mpid,final=True)
        structure.to(filename = "POSCAR")        
    return


# this reads POSCAR
def readposcar(file):
    
    lattice = []; positions_dir = []; labels = []
    
    with open(file, mode='r') as f:
        
        f.readline()
        f.readline()
        
        for i in range(3):
            l =  f.readline()
            l = l.split()
            l = [float(x) for x in l]
            lattice.append(l)
        lattice = np.array(lattice)
        
        f.readline()
        natoms = f.readline().split(); natoms = [int(x) for x in natoms]; natoms = np.array(natoms)
        mode = f.readline().split()
        
        labels = []
        for i in range(sum(natoms)):
            p = f.readline()
            l = p.split()[3]
            p = p.split()[0:3]
            p = [float(x) for x in p]
            positions_dir.append(p)
            labels.append(l)
                              
        positions = []; pnew = [] 
        for p in range(len(positions_dir)):
            pnew.append(positions_dir[p][0]*lattice[0][0]+positions_dir[p][1]*lattice[1][0] + positions_dir[p][2]*lattice[2][0] ); 
            pnew.append(positions_dir[p][0]*lattice[0][1]+positions_dir[p][1]*lattice[1][1] + positions_dir[p][2]*lattice[2][1] );
            pnew.append(positions_dir[p][0]*lattice[0][2]+positions_dir[p][1]*lattice[1][2] + positions_dir[p][2]*lattice[2][2] );
            positions.append(pnew); pnew = []   
        positions = np.array(positions) 
        positions = positions.reshape(len(positions),3,order='F').copy()

    return labels, natoms, lattice, positions, positions_dir


# this creates 3x3x3 supercell
def make_333_supercell(labels, natoms, lattice, positions):
    
    supercell = []; pnew=[]; p=positions; l=lattice; ls = []

    for s in range(len(p)):

        pnew.append(p[s][0]); pnew.append(p[s][1]); pnew.append(p[s][2]); ls.append(labels[s]); supercell.append(pnew); pnew=[]

        pnew.append(p[s][0]+l[0][0]); pnew.append(p[s][1]+l[0][1]); pnew.append(p[s][2]+l[0][2]); ls.append(labels[s]); supercell.append(pnew); pnew=[] # +x
        pnew.append(p[s][0]-l[0][0]); pnew.append(p[s][1]-l[0][1]); pnew.append(p[s][2]-l[0][2]); ls.append(labels[s]); supercell.append(pnew); pnew=[] # -x
        pnew.append(p[s][0]+l[1][0]); pnew.append(p[s][1]+l[1][1]); pnew.append(p[s][2]+l[1][2]); ls.append(labels[s]); supercell.append(pnew); pnew=[] # +y
        pnew.append(p[s][0]-l[1][0]); pnew.append(p[s][1]-l[1][1]); pnew.append(p[s][2]-l[1][2]); ls.append(labels[s]); supercell.append(pnew); pnew=[] # -y
        pnew.append(p[s][0]+l[2][0]); pnew.append(p[s][1]+l[2][1]); pnew.append(p[s][2]+l[2][2]); ls.append(labels[s]); supercell.append(pnew); pnew=[] # +z
        pnew.append(p[s][0]-l[2][0]); pnew.append(p[s][1]-l[2][1]); pnew.append(p[s][2]-l[2][2]); ls.append(labels[s]); supercell.append(pnew); pnew=[] # -z

        pnew.append(p[s][0]+l[0][0]+l[1][0]); pnew.append(p[s][1]+l[0][1]+l[1][1]); pnew.append(p[s][2]+l[0][2]+l[1][2]); ls.append(labels[s]); supercell.append(pnew); pnew=[] # +x+y
        pnew.append(p[s][0]+l[0][0]-l[1][0]); pnew.append(p[s][1]+l[0][1]-l[1][1]); pnew.append(p[s][2]+l[0][2]-l[1][2]); ls.append(labels[s]); supercell.append(pnew); pnew=[] # +x-y
        pnew.append(p[s][0]-l[0][0]+l[1][0]); pnew.append(p[s][1]-l[0][1]+l[1][1]); pnew.append(p[s][2]-l[0][2]+l[1][2]); ls.append(labels[s]); supercell.append(pnew); pnew=[] # -x+y
        pnew.append(p[s][0]-l[0][0]-l[1][0]); pnew.append(p[s][1]-l[0][1]-l[1][1]); pnew.append(p[s][2]-l[0][2]-l[1][2]); ls.append(labels[s]); supercell.append(pnew); pnew=[] # -x-y
        pnew.append(p[s][0]+l[2][0]+l[0][0]); pnew.append(p[s][1]+l[2][1]+l[0][1]); pnew.append(p[s][2]+l[2][2]+l[0][2]); ls.append(labels[s]); supercell.append(pnew); pnew=[] # +z+x
        pnew.append(p[s][0]+l[2][0]-l[0][0]); pnew.append(p[s][1]+l[2][1]-l[0][1]); pnew.append(p[s][2]+l[2][2]-l[0][2]); ls.append(labels[s]); supercell.append(pnew); pnew=[] # +z-x
        pnew.append(p[s][0]-l[2][0]+l[0][0]); pnew.append(p[s][1]-l[2][1]+l[0][1]); pnew.append(p[s][2]-l[2][2]+l[0][2]); ls.append(labels[s]); supercell.append(pnew); pnew=[] # -z+x
        pnew.append(p[s][0]-l[2][0]-l[0][0]); pnew.append(p[s][1]-l[2][1]-l[0][1]); pnew.append(p[s][2]-l[2][2]-l[0][2]); ls.append(labels[s]); supercell.append(pnew); pnew=[] # -z-x
        pnew.append(p[s][0]+l[2][0]+l[1][0]); pnew.append(p[s][1]+l[2][1]+l[1][1]); pnew.append(p[s][2]+l[2][2]+l[1][2]); ls.append(labels[s]); supercell.append(pnew); pnew=[] # +z+y
        pnew.append(p[s][0]+l[2][0]-l[1][0]); pnew.append(p[s][1]+l[2][1]-l[1][1]); pnew.append(p[s][2]+l[2][2]-l[1][2]); ls.append(labels[s]); supercell.append(pnew); pnew=[] # +z-y
        pnew.append(p[s][0]-l[2][0]+l[1][0]); pnew.append(p[s][1]-l[2][1]+l[1][1]); pnew.append(p[s][2]-l[2][2]+l[1][2]); ls.append(labels[s]); supercell.append(pnew); pnew=[] # -z+y
        pnew.append(p[s][0]-l[2][0]-l[1][0]); pnew.append(p[s][1]-l[2][1]-l[1][1]); pnew.append(p[s][2]-l[2][2]-l[1][2]); ls.append(labels[s]); supercell.append(pnew); pnew=[] # -z-y

        pnew.append(p[s][0]+l[2][0]+l[0][0]+l[1][0]); pnew.append(p[s][1]+l[2][1]+l[0][1]+l[1][1]); pnew.append(p[s][2]+l[2][2]+l[0][2]+l[1][2]); ls.append(labels[s]); supercell.append(pnew); pnew=[] # +z+x+y
        pnew.append(p[s][0]+l[2][0]+l[0][0]-l[1][0]); pnew.append(p[s][1]+l[2][1]+l[0][1]-l[1][1]); pnew.append(p[s][2]+l[2][2]+l[0][2]-l[1][2]); ls.append(labels[s]); supercell.append(pnew); pnew=[] # +z+x-y
        pnew.append(p[s][0]+l[2][0]-l[0][0]-l[1][0]); pnew.append(p[s][1]+l[2][1]-l[0][1]-l[1][1]); pnew.append(p[s][2]+l[2][2]-l[0][2]-l[1][2]); ls.append(labels[s]); supercell.append(pnew); pnew=[] # +z-x-y
        pnew.append(p[s][0]+l[2][0]-l[0][0]+l[1][0]); pnew.append(p[s][1]+l[2][1]-l[0][1]+l[1][1]); pnew.append(p[s][2]+l[2][2]-l[0][2]+l[1][2]); ls.append(labels[s]); supercell.append(pnew); pnew=[] # +z-x+y
        pnew.append(p[s][0]-l[2][0]+l[0][0]+l[1][0]); pnew.append(p[s][1]-l[2][1]+l[0][1]+l[1][1]); pnew.append(p[s][2]-l[2][2]+l[0][2]+l[1][2]); ls.append(labels[s]); supercell.append(pnew); pnew=[] # -z+x+y
        pnew.append(p[s][0]-l[2][0]+l[0][0]-l[1][0]); pnew.append(p[s][1]-l[2][1]+l[0][1]-l[1][1]); pnew.append(p[s][2]-l[2][2]+l[0][2]-l[1][2]); ls.append(labels[s]); supercell.append(pnew); pnew=[] # -z+x-y
        pnew.append(p[s][0]-l[2][0]-l[0][0]-l[1][0]); pnew.append(p[s][1]-l[2][1]-l[0][1]-l[1][1]); pnew.append(p[s][2]-l[2][2]-l[0][2]-l[1][2]); ls.append(labels[s]); supercell.append(pnew); pnew=[] # -z-x-y
        pnew.append(p[s][0]-l[2][0]-l[0][0]+l[1][0]); pnew.append(p[s][1]-l[2][1]-l[0][1]+l[1][1]); pnew.append(p[s][2]-l[2][2]-l[0][2]+l[1][2]); ls.append(labels[s]); supercell.append(pnew); pnew=[] # -z-x+y

    positions_supercell = np.array(supercell) ;
    positions_supercell = positions_supercell.reshape(len(p)*27,3,order='F').copy()
    
    lattice_supercell = lattice*3
    natoms_supercell = natoms*3
    labels_supercell = ls
    
    return labels_supercell, natoms_supercell, lattice_supercell, positions_supercell


def getKey0(item):
    return item[0]
def getKey4(item):
    return item[4]


# gr is like radial distrubution function.
# I use this to determine ineqiuivalent ions.
def get_gr(labels_supercell,positions_supercell):

    ds = []
    Zs = []
    dZs = []
    for i in range(len(labels_supercell)):

        # distances
        n = LA.norm(positions_supercell[i])
        ds.append(n)
        n = float('{:.2f}'.format(n))

        # Zs
        el = Element(labels_supercell[i])
        d = el.data
        Z = d['Atomic no']
        Zs.append(Z)

        # distance_round * Z
        dZs.append(n*Z)


    zipped = zip(ds,Zs,dZs)
    zipped = list(zipped)
    
    zipped_sorted = sorted(zipped, key=getKey0)

    gr = []
    for i in range(len(zipped_sorted)):
        if zipped_sorted[i][0] < 15: gr.append([i,zipped_sorted[i][2]])
    gr = np.array(gr)

    return gr


# this returns sum of gr
def get_sumgr(ca,nmax): 
    
    [labels, natoms, lattice, positions, positions_dir] = readposcar('POSCAR')
    
    shifts = positions[ca] 
    
    # move selected to origin
    positions_shifted = []
    for i in range(len(positions)):
        p = [positions[i][0]-shifts[0],positions[i][1]-shifts[1],positions[i][2]-shifts[2]]
        positions_shifted.append(p)
    positions_shifted  

    labels_supercell, natoms_supercell, lattice_supercell, positions_supercell = make_333_supercell(labels, natoms, lattice, positions_shifted)
    ds = []
    for i in positions_supercell:
        n = LA.norm(i)
        ds.append(n)    
    # if supercell radius less than 20 A, we create another 3x3x3 supercell    
    if max(ds) < 20:
        labels_supercell, natoms_supercell, lattice_supercell, positions_supercell = make_333_supercell(labels_supercell, natoms_supercell, lattice_supercell, positions_supercell)

    gr = get_gr(labels_supercell,positions_supercell)    
    sumgr = sum(gr[:,1][0:nmax])
    
    return int(sumgr), gr

# returns list of sum of grs of each ion in the structure
# if two ion has same gr, we can assume that they are equivalent.
def get_sgr_list(es,nmax):
    
    [labels, natoms, lattice, positions, positions_dir] = readposcar('POSCAR')
    
    clist=[]
    for i in range(len(labels)):
        if labels[i] == es:
            clist.append(i) 
    
    sumgrs = []
    for i in clist:
        sumgr, gr = get_sumgr(i,nmax)
        sumgrs.append(sumgr)
        
    z= zip(clist,sumgrs)
    z = list(z)
    
    labels_short = []
    for i in labels:
        if i not in labels_short:
            labels_short.append(i)
            
    # formula_text
    formula = '$'
    for i,s in enumerate(labels_short):
        formula = formula + s + '_{' + str(natoms[i]) + '}'
    formula = formula + '$'
            
    return z, formula      






# this writes feff.inp
def write_feffinp(ca,dmax,rFMS,rSCF,corehole): 
    
    [labels, natoms, lattice, positions, positions_dir] = readposcar('../POSCAR')
    
    labels_short = []
    for i in labels:
        if i not in labels_short:
            labels_short.append(i)
    
    shifts = positions[ca] 
    
    # move selected to origin
    positions_shifted = []
    for i in range(len(positions)):
        p = [positions[i][0]-shifts[0],positions[i][1]-shifts[1],positions[i][2]-shifts[2]]
        positions_shifted.append(p)
    positions_shifted  

    labels_supercell, natoms_supercell, lattice_supercell, positions_supercell = make_333_supercell(labels, natoms, lattice, positions_shifted)
        
    ds = []
    for i in positions_supercell:
        n = LA.norm(i)
        ds.append(n)    
    # if supercell radius less than dmax*3, we create another 3x3x3 supercell    
    if max(ds) < (dmax*3):
        labels_supercell, natoms_supercell, lattice_supercell, positions_supercell = make_333_supercell(labels_supercell, natoms_supercell, lattice_supercell, positions_supercell)
   
    atoms = []
    ds = []
    for i,s in enumerate(positions_supercell):
        n = LA.norm(s)
        if n <= dmax:
            atoms.append([s[0],s[1],s[2],labels_supercell[i],n])
                                 
    atoms = sorted(atoms, key=getKey4)
    
    for i,a in enumerate(atoms):
        s = a[3]
        ind = labels_short.index(s)
        atoms[i][3] = ind
 
    f=open('feff.inp',"w+")    
    f.write("""TITLE xx             

 *  Ni K edge energy = 8333 eV
 EDGE      K
 S02       1.0

 *         pot    xsph  fms   paths genfmt ff2chi
 CONTROL   1      1     1     1     1      1
 PRINT     1      0     0     0     0      3

 *         ixc  [ Vr  Vi ]     *** ixc=0 means to use Hedin-Lundqvist
 EXCHANGE  0
                                           *** Radius for self-consistent pots (2 shells is a good choice)
 *         r_scf  [ l_scf   n_scf   ca ]   *** l_scf = 0 for a solid, 1 for a molecule
 SCF       5.0

 *         kmax   [ delta_k  delta_e ]     *** Upper limit of XANES calculation.
 * XANES     4.0

 *         r_fms     l_fms      *** Radius for Full Mult. Scatt. l_fms = 0 for a solid, 1 for a molecule
 * FMS      28.71636  0

 *         emin  emax   eimag   *** Energy grid over which to calculate DOS functions
 * LDOS      -30   20     0.1

               *** for EXAFS: RPATH 5.0 and uncomment the EXAFS card
 RPATH     5.0
 EXAFS     20
  * POLARIZATION  0   0   0


    
""" % vars())
    
    Sca =  labels[ca]      
    el = Element(Sca); d = el.data; Zca = d['Atomic no']    
    
    f.write("""POTENTIALS
*   ipot   Z      element   l_scmt   l_fms   stoichiometry
    0      %(Zca)i     %(Sca)s        -1       -1      0.001 """ % vars())     
    
    
    for i in range(len(labels_short)):
        n = (i+1)
        s = labels_short[i]
        el = Element(s); 
        d = el.data; 
        z = d['Atomic no'] 
        st = natoms[i]
        f.write("""
    %(n)i      %(z)i     %(s)s        -1       -1      %(st)i """ % vars())         
        
    f.write("\n \n")  
    
    f.write("ATOMS\n")
    f.write("       0.000000     0.000000     0.000000     0    0.0     %s\n"%(Sca))    
    for i in atoms[1:]:  
        f.write('  %13.6f%13.6f%13.6f   %3d   %6.3f   %s\n' % (i[0], i[1], i[2], i[3]+1, i[4], labels_short[i[3]]))
    f.write("END\n")    
    f.close()       
    
    for_dist_plot = []
    for i in atoms:
        for_dist_plot.append([i[4],i[3]])
    
    return for_dist_plot, labels_short






def write_xyz(ca,dmax): 
    
    [labels, natoms, lattice, positions, positions_dir] = readposcar('../POSCAR')
    
    labels_short = []
    for i in labels:
        if i not in labels_short:
            labels_short.append(i)
    
    shifts = positions[ca] 
    
    # move selected to origin
    positions_shifted = []
    for i in range(len(positions)):
        p = [positions[i][0]-shifts[0],positions[i][1]-shifts[1],positions[i][2]-shifts[2]]
        positions_shifted.append(p)
    positions_shifted  

    labels_supercell, natoms_supercell, lattice_supercell, positions_supercell = make_333_supercell(labels, natoms, lattice, positions_shifted)
        
    ds = []
    for i in positions_supercell:
        n = LA.norm(i)
        ds.append(n)    
    # if supercell radius less than dmax * 3, we create another 3x3x3 supercell    
    if max(ds) < (dmax*3):
        labels_supercell, natoms_supercell, lattice_supercell, positions_supercell = make_333_supercell(labels_supercell, natoms_supercell, lattice_supercell, positions_supercell)
   
    atoms = []
    ds = []
    for i,s in enumerate(positions_supercell):
        n = LA.norm(s)
        if n <= dmax:
            atoms.append([s[0],s[1],s[2],labels_supercell[i],n])
                                 
    atoms = sorted(atoms, key=getKey4)
    
    for i,a in enumerate(atoms):
        s = a[3]
        ind = labels_short.index(s)
        atoms[i][3] = ind
 
    f=open('feff.xyz',"w+")  
    
    nat = len(atoms)
    f.write("""%(nat)d
    generated by calc_feff  
""" % vars())
    
    Sca =  labels[ca]      
    

    f.write("%s    0.000000     0.000000     0.000000     0    0.0     \n"%(Sca))    
    for i in atoms[1:]:  
        f.write('%s  %13.6f%13.6f%13.6f   %3d   %6.3f  \n' % (labels_short[i[3]], i[0], i[1], i[2], i[3]+1, i[4]))  
    f.close()       
    
    for_dist_plot = []
    for i in atoms:
        for_dist_plot.append([i[4],i[3]])
    
    return 



import sys
import pickle
import os
import numpy as np


# this was a good idea, thank you
sys.path.append('t4iss')
#sys.path.append(os.path.join(os.environ['HOME'], "gd", "BNL-ml4xas", "1-code"))

import t4iss
from t4iss.core import *
from t4iss.feff_utils import *
from t4iss.mp_utils import *

from pymatgen import MPRester
# HnEctIuK6wbkQGse (Matt)
# JCRhEVIMvKOrQ1ot (Mehmet)
mpr = MPRester('JCRhEVIMvKOrQ1ot')



# extract available.tgz here
t4iss_defaults['t4iss_xanes_data'] = os.getcwd()+'/available'






# this collect available data from MP into t4iss_xanes_data folder
os.makedirs(t4iss_defaults['t4iss_xanes_data'],exist_ok=True)
os.chdir(t4iss_defaults['t4iss_xanes_data'])


# this needs ~15 minutes to complete
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++                             
mpids = search_MP(mpr, search_pattern='Ni-Cl', nmax=200)                      #                             
#mpids += search_MP(mpr, search_pattern='Ti-O-*', nmax=200)                   #                             
#mpids += search_MP(mpr, search_pattern='Ti-O-*-*', nmax=200)                 #                            
print(len(mpids))                                                            #                     
                                                                             #    
counter = 0                                                                  #               
missing = []                                                                 #                
for i in mpids:
    print(i) # 
    try:
        missing += download_xanes_from_MP(mpr, mpid=i, absorption_specie='Ni',   #                             
                                      download_to=None, return_missing=True) #                             
        if (counter%100) == 0:                                                   #                             
            print([counter,len(missing)]);                                       #                             
        counter += 1 
        
    except:
        print('something is wrong for '+i)
        os.chdir(t4iss_defaults['t4iss_xanes_data'])
                                                                              
                                                                             #                             
pickle.dump(missing,open('../missing.pkl','wb'))                             #                             
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


os.chdir('..')
missing = pickle.load(open('missing.pkl', 'rb'))
print(len(missing))









# this writes feff.inp for each missing site
# takes about ~11 minutes to complete

# params for FEFF calculations
rFMS = 7.1
rSCF = 5.1
corehole = 'RPA'


os.chdir(t4iss_defaults['t4iss_xanes_data'])
os.chdir('..')
os.makedirs('missing',exist_ok=True)
os.chdir('missing')


counter = 0
for i in missing:
    
    if (counter%500) == 0:
        print(counter)
    counter += 1
    
    if not os.path.isdir(i[0]):
        os.mkdir(i[0])
    os.chdir(i[0])

    if not os.path.isfile('CONTCAR'):
        structure = mpr.get_structure_by_material_id(i[0],final=True)
        #     structure.to(fmt='poscar',filename='POSCAR') #
        structure = SpacegroupAnalyzer(structure).get_symmetrized_structure()    

        #     structure.to(fmt='poscar',filename='CONTCAR') # this doesn't work
        cf=open('CONTCAR',"w+") 
        cf.write('symmetrized structure\n')
        cf.write('1.0\n')
        cf.write('%11.6f %11.6f %11.6f\n'%(structure.lattice.matrix[0][0],structure.lattice.matrix[0][1],structure.lattice.matrix[0][2]))
        cf.write('%11.6f %11.6f %11.6f\n'%(structure.lattice.matrix[1][0],structure.lattice.matrix[1][1],structure.lattice.matrix[1][2]))
        cf.write('%11.6f %11.6f %11.6f\n'%(structure.lattice.matrix[2][0],structure.lattice.matrix[2][1],structure.lattice.matrix[2][2])) 

        for j in structure.types_of_specie:
            cf.write(j.symbol+' ')
        cf.write('\n')

        for j in structure.types_of_specie:
            cf.write(str(structure.species.count(j))+' ')
        cf.write('\n')  

        cf.write('Direct\n')

        for j in structure.sites:
            cf.write('%8.6f %8.6f %8.6f %s \n'%(j.frac_coords[0],j.frac_coords[1],j.frac_coords[2],j.species_string))

        cf.close()
        
        
    f = 'feff_%03d_%s-K'%(i[1]+1,'Ti')
    os.makedirs(f,exist_ok=True)
    os.chdir(f)
    if not os.path.isfile('feff.inp'):
        feff_write_inp(structure={'poscar':'../CONTCAR','isite':i[1]},dmax=10.1,rFMS=rFMS,rSCF=rSCF,corehole='RPA')
    os.chdir('..')
    
    os.chdir('..')
    
    
os.chdir('..')    










# this creates slurm script for FEFF calculations

n_cpu = 36 # number of physical CPUs on one node
feff_cmd = os.path.join(t4iss_defaults['scripts_path'],'feff_cmd.sh')


os.chdir(t4iss_defaults['t4iss_xanes_data'])
os.chdir('..')
missing = pickle.load(open('missing.pkl', 'rb'))
chunks = [missing [i:i+n_cpu] for i in range(0, len(missing), n_cpu) ]


account = 'cfn35847'
time = '23:30:00'
partition = 'long'



f=open('slurm.sh',"w+")

f.write("""\
#!/bin/bash
#SBATCH --account=%(account)s 
#SBATCH --nodes=1
#SBATCH --time=%(time)s
#SBATCH --partition=%(partition)s
#SBATCH --job-name=Ni


cd missing

""" % vars())


#for c in [chunks[0]]:
for c in chunks:    
    for i in c:
        path = './%s/feff_%03d_%s-K'%(i[0],i[1]+1,'Ti')
        f.write('cd '+path+'; ')
        f.write(feff_cmd+' > /dev/null 2> /dev/null  &\n')
#         f.write('pwd &\n')       
        f.write('cd ../.. \n')
    f.write('wait\n\n\n\n\n')

f.close()  
subprocess.call(' chmod +x slurm.sh ', shell=True)
#subprocess.call(' sbatch slurm.sh ', shell=True)







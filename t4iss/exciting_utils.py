# -*- coding: iso-8859-1 -*-
# coding: utf-8

"""
This provides classes and functions for dealing with FEFF i/o
"""

__author__ = "Mehmet Topsakal"
__email__ = "metokal@gmail.com"
__status__ = "Development"
__date__ = "March 20, 2018"



import numpy as np
from numpy import linalg as LA
import os,sys

from pymatgen.core.periodic_table import Element

import numpy as np
import os,sys,shutil,subprocess,pickle
from os.path import join

from pymatgen.analysis.local_env import VoronoiNN
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer
import pymatgen as mg

from scipy import interpolate

from . import t4iss_defaults
from .core import mXANES







#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
# 
def write_inputxml(absorption_specie,title='by_MehmetTopsakal',speciespath='./',
                   doground='fromscratch',
                   xctype='LDA_PW',ngridk='4 4 2',
                   writexs=True, copyfromscf=True,
                   ngridk_xs='4 4 2',ngridq=None,
                   nempty_xs=1400,nempty_screen=2000,nempty_bse=700,
                   gqmax='1.0',
                   intv=[177.5, 181.5],
                   mpdownload=None):
    
    if mpdownload:
        mprester = mpdownload[0]
        mpid     = mpdownload[1]
        structure = mprester.get_structure_by_material_id(mpid,final=True)
        structure.to(fmt='poscar',filename='CONTCAR')   
    
    struct = mg.Structure.from_file("CONTCAR")
    finder = SpacegroupAnalyzer(struct)
    struct = finder.get_symmetrized_structure()
    [sites, indices]  = struct.equivalent_sites, struct.equivalent_indices

    s = []
    for i in struct:
        s.append(i.species_string)
    if absorption_specie not in s:
        raise ValueError(mpid+' does not have '+absorption_specie+' element in it. Please check...')
    
    
    for_xs_sym = [sites[0][0].species_string]
    for_xs_counter = []
    for_xs_ind_cur = 0
    counter = 0
    for i in sites:
        for j in i:   
            if j.species_string in for_xs_sym:
                for_xs_counter.append(counter)
                counter += 1 
            else:
                counter = 0
                for_xs_ind_cur += 1
                for_xs_sym.append(j.species_string)
                for_xs_counter.append(counter)
                counter += 1 
    
 

    for i,s in enumerate(sites):
        
        
        if s[0].species_string is absorption_specie: 
            
            if writexs:
                f = 'exciting_{:03d}_{}-K'.format(indices[i][0]+1,absorption_specie) 
            else:
                f = 'scf'
            
            
            cur_ind = indices[i][0]
            
            xasspecies = i + 1
            
            
            os.makedirs(f,exist_ok=True)
            os.chdir(f)
            
            ef=open('input.xml',"w+")    
           
            
            ef.write('<input>\n')
            ef.write('<title>'+title+'</title>\n\n')
            ef.write('<structure autormt="true" speciespath="'+speciespath+'">\n')
            ef.write('    <crystal scale=\"1.88972612456\"> \n')
            
            for i in struct.lattice.matrix:
                ef.write('        <basevect> {:10.6f} {:10.6f} {:10.6f} </basevect> \n'.format(i[0],i[1],i[2]))
                
            ef.write('    </crystal>\n')
            
            site0 = sites[0][0].species_string
            site_current = site0
            ef.write('    <species speciesfile="'+site0+'.xml">\n') 
            
            for i in sites:
                for j in i:   
                    if j.species_string is site_current:
                        ef.write('        <atom coord=" {:10.6f} {:10.6f} {:10.6f}  "/> \n'.format(j.frac_coords[0],j.frac_coords[1],j.frac_coords[2]))

                    else:
                        site_current = j.species_string
                        ef.write('    </species>\n')                        
                        ef.write('    <species speciesfile="'+site_current+'.xml">\n')
                        ef.write('        <atom coord=" {:10.6f} {:10.6f} {:10.6f}  "/> \n'.format(j.frac_coords[0],j.frac_coords[1],j.frac_coords[2]))
                        
            ef.write('    </species>\n')                         
            ef.write('</structure>\n')  
            
            ef.write("""
<groundstate do="%(doground)s"              
    xctype="%(xctype)s"
    rgkmax="7.0"
    ngridk="%(ngridk)s"
    epsocc="1.0d-6"
    stype="Gaussian" 
    swidth="0.001"
    gmaxvr="14.0"         
    >
</groundstate>

""" % vars())
            
            if writexs:
                
                if ngridq is None:
                    ngridq = ngridk_xs
                
                intv0 = intv[0]
                intv1 = intv[1]
                npts = int((intv[1]-intv[0])*27.211396132/0.1 +1)
                
                xasspecies = for_xs_sym.index(absorption_specie) + 1
                xasatom = for_xs_counter[cur_ind] + 1
                
                
                
                ef.write("""
<xs
    xstype="BSE" 
    ngridk="%(ngridk_xs)s"
    rgkmax="7.0" 
    lmaxapw="12"
    ngridq="%(ngridq)s"
    vkloff="0.05 0.15 0.25"
    reduceq="false"
    reducek="false"
    nempty="%(nempty_xs)d" 
    gqmax="%(gqmax)s"     
    broad="0.018"
    tevout="true" >

    <energywindow 
       intv="%(intv0).3f %(intv1).3f"
       points="%(npts)d" />

    <screening 
       screentype="full" 
       nempty="%(nempty_screen)d"  />

    <BSE
       xas="true"
       xasspecies="%(xasspecies)d"
       xasatom="%(xasatom)d"
       xasedge="K" 
       bsetype="singlet" 
       nstlxas="1 %(nempty_bse)d" />
    
    <qpointset>
       <qpoint>0.0 0.0 0.0</qpoint>
    </qpointset>  
    
</xs> 

""" % vars()) 
                
                
                

            ef.write('</input>\n')
            ef.close()
            
            
            if copyfromscf:
                if os.path.isfile('../scf/STATE.OUT'):
                    shutil.copy('../scf/STATE.OUT','STATE.OUT')
                    shutil.copy('../scf/EFERMI.OUT','EFERMI.OUT')            

            
            os.chdir('..')
                




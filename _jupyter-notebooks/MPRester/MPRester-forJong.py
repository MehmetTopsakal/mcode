
# coding: utf-8

# In[1]:


from pymatgen import MPRester
mpr = MPRester('AdhiVtzgaqU02rZT')  # here I put my API key to access MP


# In[2]:


# this gets POSCAR file from MP
def get_poscar(mpid,fmt=None,filename=None):
    
    if fmt is None: fmt='poscar'
    if filename is None: filename='POSCAR.vasp' 
        
    data = mpr.get_data(mpid, data_type="vasp")
    
    structure = mpr.get_structure_by_material_id(mpid,final=False)
    structure.to(fmt=fmt,filename=filename)
    return


# this gets CONTCAR file from MP
def get_contcar(mpid,fmt=None,filename=None):
    
    if fmt is None: fmt='poscar'
    if filename is None: filename='CONTCAR.vasp' 
        
    data = mpr.get_data(mpid, data_type="vasp")
    
    structure = mpr.get_structure_by_material_id(mpid,final=True)
    structure.to(fmt=fmt,filename=filename)
    return


# In[3]:


mpid = 'mp-2292'
get_poscar(mpid)
get_contcar(mpid)


# In[4]:


mpid = 'mp-1968'
get_poscar(mpid)
get_contcar(mpid)


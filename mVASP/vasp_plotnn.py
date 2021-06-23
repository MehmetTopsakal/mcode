#!/home/mt/software/anaconda3/bin/python

import matplotlib
matplotlib.use('Agg') # see http://matplotlib.org/faq/usage_faq.html#what-is-a-backend

import numpy as np
import subprocess

from pylab import *
from matplotlib import gridspec

import sys,os
from mVASP import readposcar

import PT

font = {'size':6}
matplotlib.rc('font', **font)



inputs = sys.argv


for a in range(1,len(inputs)):
    s=inputs[a].split('=')
    if s[0] == 'p' or s[0] == 'f': pfile = s[1] 
    elif s[0] == 'a': ainput = s[1]    
    elif s[0] == 'nnmax': nnmax = int(s[1])   
    elif s[0] == 'dmax' or s[0] == 'd': d = float(s[1])       
    elif s[0] == 'savekey' or s[0] == 'sk': savekey = int(s[1]) 
    elif s[0] == 'plotkey' or s[0] == 'pk':plotkey = int(s[1]) 
    
    
try:
    pfile
except:
    pfile='POSCAR'

try:
    nnmax
except:
    nnmax=50

try:
    savekey
except:
    savekey=0

try:
    d
except:
    d=11

try:
    plotkey
except:
    plotkey=1    
    
    
labels, natoms, lattice, positions_cart, positions_dir = readposcar(pfile)
try:
    ainput
except:
    ainput='1:'+str(len(positions_dir))


alist = ainput.split('|')[0]
atoms = []
if len(alist.split(',')) == 1: 
    a = alist.split(',')[0]
    if ':' in a:
        start = int(a.split(':')[0])
        stop  = int(a.split(':')[1])+1
        for j in range(start,stop,1):
            atoms.append(j)
    else:
        atoms.append(int(a))
else:
    for i in range(len(alist.split(','))):
        a = alist.split(',')[i]
        if ':' in a:
            start = int(a.split(':')[0])
            stop  = int(a.split(':')[1])+1
            for j in range(start,stop,1):
                atoms.append(j)
        else:
            atoms.append(int(a))               

symbol_list_all = []
for i in range(len(natoms)):
    for j in range(natoms[i]):
        symbol_list_all.append(labels[i])


set = []; coulombs = []
for i in range(len(atoms)):
    print(d)
    subprocess.call(' mpy feff_poscar2atoms.py t='+str(atoms[i])+' d='+str(d)+' p='+pfile+' ', shell=True)
    read = np.loadtxt('atoms.dat', unpack=True, comments='END', usecols=(3,4), skiprows=1)
    
    z_list = [ PT.get_z( symbol_list_all[i]) ]
    for i in range(1,len(read[0])):
        z_list.append( PT.get_z( labels[ int(read[0][i])-1 ]  ) )
    c_list = [0.5*z_list[0]**(2.4)]
    for i in range(1,len(z_list)):
        c = (z_list[0]*z_list[i])/read[1][i]
        c_list.append(c)
    c_list  = np.array(c_list, np.float)        
    coulombs.append(c_list[0:100])
   
    set.append(read)

#os.remove('atoms.dat')
#os.remove('atoms.xyz')


ineq_set = [set[0]]
ineq_a = []; ineq_a.append(atoms[0])
ineq_csums = []; ineq_csums.append(round(sum(coulombs[0]),2))
ineq_cs = [coulombs[0]]



for i in range(len(atoms)):
    c = round(sum(coulombs[i]),2)
    a = atoms[i]
    for j in range(len(atoms)):
        if (c not in ineq_csums): 
            ineq_csums.append(c); 
            ineq_a.append(a)
            ineq_set.append(set[i])
            ineq_cs.append(coulombs[i])

print(ineq_csums)
#print('inequivalent sites are : ', ineq_a)
#print('# of inequivalent sites is : ', len(ineq_a))






# ========================================================================================= ### 


#print(symbol_list_all)
#print(ineq_a)

#i=1
#print(symbol_list_all[ineq_a[i]-1])
#print(ineq_a[i])


ineq_info = []
for i in range(len(ineq_a)):
    s1, s2 = symbol_list_all[ineq_a[i]-1], ineq_a[i]
    ineq_info.append([s1, s2])

if savekey == 1: np.savez('nn.npz', ineq_info=ineq_info, ineq_a=ineq_a, ineq_cs=ineq_cs, atoms=atoms, symbol_list_all=symbol_list_all)
#readnpz = np.load('ineq.npz')
#ineq_info2 = readnpz['ineq_info']
#print(ineq_info2[0][1])

print(ineq_info)


atoms = ineq_a
set   = ineq_set



# ========================================================================================= ### 
if plotkey == 1:
    
    rcParams['figure.figsize'] =7,2*len(atoms) 
    fig = plt.figure()
    gs = gridspec.GridSpec(len(atoms), 1 )    
    gs.update(top=0.95, bottom=0.15, left=0.1, right=0.8, wspace=0.05, hspace=0.05)
    
    
    
    colors=['','r','g','b','m','c','y','silver']
    
    
    for g in range(len(atoms)):
        ax=fig.add_subplot(gs[g])
        plt.setp(ax.get_xticklabels(), visible=False)
        ax.plot(range(1,nnmax), set[g][1][1:nnmax], 'k-', lw=1, alpha=1)
        for c in range(1,nnmax):
            ax.plot(c, set[g][1][c], 'o', ms=5, markeredgecolor=colors[int(set[g][0][c])], markerfacecolor=colors[int(set[g][0][c])])
        ax.set_yticks(np.arange(-10,10,1)); ax.grid(True)
        ax.set_ylim( min(set[g][1][1:nnmax])-0.2, max(set[g][1][1:nnmax])+0.2)
        ax.set_xlim( 0, nnmax)
        ax.set_ylabel('atom-'+str(atoms[g])+' ('+symbol_list_all[ineq_a[g]-1]+')');
    
        
    plt.setp(ax.get_xticklabels(), visible=True)
    
    
    
    ax.set_xlabel('nn index'); 
    
    
    
    savefig('nn.png', format='png', dpi=300)


































# ATTENTION   as in spinel-NTO   atom-by-atom



##!/home/mt/software/anaconda3/bin/python

#import matplotlib
#matplotlib.use('Agg') # see http://matplotlib.org/faq/usage_faq.html#what-is-a-backend

#import numpy as np
#import subprocess

#from pylab import *
#from matplotlib import gridspec

#import sys

#font = {'size':10}
#matplotlib.rc('font', **font)



#inputs = sys.argv
#print(inputs)

#for a in range(1,len(inputs)):
    #s=inputs[a].split('=')
    #if s[0] == 'p' or s[0] == 'f': pfile = s[1] 
    #elif s[0] == 'a': ainput = s[1]    
    #elif s[0] == 'nnmax': nnmax = int(s[1])   

#print(pfile)
#print(ainput)

#try:
    #pfile
#except:
    #pfile='POSCAR'

#try:
    #nnmax
#except:
    #nnmax=50

#try:
    #ainput
#except:
    #ainput='1:2'




 
    

## ========================================================================================= ### 
#rcParams['figure.figsize'] =10,6
#fig = plt.figure()
#gs = gridspec.GridSpec(1,5)    
#gs.update(top=0.95, bottom=0.15, left=0.05, right=0.9, wspace=0.05, hspace=0.05)
#colors=['','r','g','b','m','c','y','silver']





#atoms=[9,10]

#set = []
#for i in range(len(atoms)):
    #subprocess.call(' feff_poscar2atoms.py t='+str(atoms[i])+' d=10 p='+pfile+' ', shell=True)
    #read = np.loadtxt('atoms.dat', unpack=True, comments='END', usecols=(3,4), skiprows=1)
    #set.append(read)

#for g in range(len(atoms)):
    ##ax=fig.add_subplot(gs[g])
    #ax=fig.add_subplot(gs[0])
    #plt.setp(ax.get_yticklabels(), visible=True); ax.set_ylabel('nn dist. [Angst.]');
    #ax.plot(range(1,nnmax), set[g][1][1:nnmax], lw=2, alpha=1)
    ##for c in range(1,nnmax):
        ##ax.plot(c, set[g][1][c], 'o', ms=5, markeredgecolor=colors[int(set[g][0][c])], markerfacecolor=colors[int(set[g][0][c])])
    #ax.set_yticks(np.arange(-10,10,1)); ax.grid(True)
    #ax.set_ylim( min(set[g][1][1:nnmax])-0.2, max(set[g][1][1:nnmax])+0.2)
    #ax.set_xlim( 0, nnmax)
    #ax.set_title('Ti 1,2'); ax.set_xlabel('nn index');


#atoms=[11,12,13,14]

#set = []
#for i in range(len(atoms)):
    #subprocess.call(' feff_poscar2atoms.py t='+str(atoms[i])+' d=10 p='+pfile+' ', shell=True)
    #read = np.loadtxt('atoms.dat', unpack=True, comments='END', usecols=(3,4), skiprows=1)
    #set.append(read)

#for g in range(len(atoms)):
    ##ax=fig.add_subplot(gs[g])
    #ax=fig.add_subplot(gs[1])
    #plt.setp(ax.get_yticklabels(), visible=False)
    #ax.plot(range(1,nnmax), set[g][1][1:nnmax], lw=2, alpha=1)
    ##for c in range(1,nnmax):
        ##ax.plot(c, set[g][1][c], 'o', ms=5, markeredgecolor=colors[int(set[g][0][c])], markerfacecolor=colors[int(set[g][0][c])])
    #ax.set_yticks(np.arange(-10,10,1)); ax.grid(True)
    #ax.set_ylim( min(set[g][1][1:nnmax])-0.2, max(set[g][1][1:nnmax])+0.2)
    #ax.set_xlim( 0, nnmax)
    #ax.set_title('Ti 3,4,5,6'); ax.set_xlabel('nn index');


#atoms=[15,16]

#set = []
#for i in range(len(atoms)):
    #subprocess.call(' feff_poscar2atoms.py t='+str(atoms[i])+' d=10 p='+pfile+' ', shell=True)
    #read = np.loadtxt('atoms.dat', unpack=True, comments='END', usecols=(3,4), skiprows=1)
    #set.append(read)

#for g in range(len(atoms)):
    ##ax=fig.add_subplot(gs[g])
    #ax=fig.add_subplot(gs[2])
    #plt.setp(ax.get_yticklabels(), visible=False)
    #ax.plot(range(1,nnmax), set[g][1][1:nnmax], lw=2, alpha=1)
    ##for c in range(1,nnmax):
        ##ax.plot(c, set[g][1][c], 'o', ms=5, markeredgecolor=colors[int(set[g][0][c])], markerfacecolor=colors[int(set[g][0][c])])
    #ax.set_yticks(np.arange(-10,10,1)); ax.grid(True)
    #ax.set_ylim( min(set[g][1][1:nnmax])-0.2, max(set[g][1][1:nnmax])+0.2)
    #ax.set_xlim( 0, nnmax)
    #ax.set_title('Ti 7,8'); ax.set_xlabel('nn index');


#atoms=[17,18]

#set = []
#for i in range(len(atoms)):
    #subprocess.call(' feff_poscar2atoms.py t='+str(atoms[i])+' d=10 p='+pfile+' ', shell=True)
    #read = np.loadtxt('atoms.dat', unpack=True, comments='END', usecols=(3,4), skiprows=1)
    #set.append(read)

#for g in range(len(atoms)):
    ##ax=fig.add_subplot(gs[g])
    #ax=fig.add_subplot(gs[3])
    #plt.setp(ax.get_yticklabels(), visible=False)
    #ax.plot(range(1,nnmax), set[g][1][1:nnmax], lw=2, alpha=1)
    ##for c in range(1,nnmax):
        ##ax.plot(c, set[g][1][c], 'o', ms=5, markeredgecolor=colors[int(set[g][0][c])], markerfacecolor=colors[int(set[g][0][c])])
    #ax.set_yticks(np.arange(-10,10,1)); ax.grid(True)
    #ax.set_ylim( min(set[g][1][1:nnmax])-0.2, max(set[g][1][1:nnmax])+0.2)
    #ax.set_xlim( 0, nnmax)
    #ax.set_title('Ti 9,10'); ax.set_xlabel('nn index');




#atoms=[9,10,11,12,13,14,15,16,17,18]

#set = []
#for i in range(len(atoms)):
    #subprocess.call(' feff_poscar2atoms.py t='+str(atoms[i])+' d=10 p='+pfile+' ', shell=True)
    #read = np.loadtxt('atoms.dat', unpack=True, comments='END', usecols=(3,4), skiprows=1)
    #set.append(read)

#for g in range(len(atoms)):
    ##ax=fig.add_subplot(gs[g])
    #ax=fig.add_subplot(gs[4])
    #plt.setp(ax.get_yticklabels(), visible=False)
    #ax.plot(range(1,nnmax), set[g][1][1:nnmax], lw=2, alpha=1)
    ##for c in range(1,nnmax):
        ##ax.plot(c, set[g][1][c], 'o', ms=5, markeredgecolor=colors[int(set[g][0][c])], markerfacecolor=colors[int(set[g][0][c])])
    #ax.set_yticks(np.arange(-10,10,1)); ax.grid(True)
    #ax.set_ylim( min(set[g][1][1:nnmax])-0.2, max(set[g][1][1:nnmax])+0.2)
    #ax.set_xlim( 0, nnmax)
    #ax.set_title('Ti all'); ax.set_xlabel('nn index');


#ax.set_xlabel('nn index'); 


#savefig('nn.png', format='png', dpi=300)




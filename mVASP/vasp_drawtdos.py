#!/home/mt/software/anaconda3/bin/python

import matplotlib
matplotlib.use('Agg') # see http://matplotlib.org/faq/usage_faq.html#what-is-a-backend

from mVASP import readdoscar  
#import mSMOOTH
import os    
import sys
import numpy as np
from   pylab import *
from   matplotlib import gridspec


font = {'size':12}
matplotlib.rc('font', **font)
#savefig('plot.png', format='png', dpi=200) 
#### ========================================================  NOTE: DNR







inputs = sys.argv



for a in range(1,len(inputs)):
    s=inputs[a].split('=')
    if s[0] == 'lr' : lr = s[1] 
    if s[0] == 'minx' or  s[0] == 'xmin' : minx  = float(s[1])
    if s[0] == 'maxx' or  s[0] == 'xmax' : maxx  = float(s[1])
    if s[0] == 'miny' or  s[0] == 'ymin' : miny  = float(s[1])
    if s[0] == 'maxy' or  s[0] == 'ymax' : maxy  = float(s[1])  
    if s[0] == 'sigma' or s[0] == 's'    : sigma = float(s[1])
    if s[0] == 'lr' : lr = s[1]
    if s[0] == 'file' : file = s[1]    
    
try:
    minx
except:
    minx=-6



    
try:
    sigma
except:
    sigma=0.1    

try:
    shift
except:
    shift=0    

try:
    file
except:
    file='DOSCAR'   



# ========================================================================================= ### 
rcParams['figure.figsize'] =12,5 # konqueror window split
fig, ((ax1)) = plt.subplots(1,1,sharex=False)  
 
subplots_adjust(hspace=0.1)
subplots_adjust(wspace=0.1)
subplots_adjust(top=0.98)
subplots_adjust(bottom=0.07)
subplots_adjust(right=0.90)
subplots_adjust(left=0.09)





doscar_info, Edos, tdos, pdos_up, pdos_dw = readdoscar(file)
tdos[0][0] = 0; tdos[0][-1] = 0; tdos[1][0] = 0; tdos[1][-1] = 0


try:
    maxx
except:
    maxx=Edos[-1]

try:
    minx
except:
    minx=Edos[0]
 
 

ax=ax1; #plt.setp( ax.get_yticklabels(), visible=False); 
#ax.tick_params(top="off", left="off", right="off", direction="out")
ax.fill(Edos,tdos[0], 'r-', lw=2, alpha=0.9, label='total DOS')
ax.fill(Edos,-tdos[1], 'r-', lw=2, alpha=0.9)
ax.plot([ -200, 100 ], [ 0, 0 ], 'k-', linewidth=1.2)
ax.plot([ 0, 0 ], [ -800, 800 ], 'k-', linewidth=1.2)
ax.set_xlim( (minx, maxx) ); 
ax.set_ylim( (max(tdos[0]), min(-tdos[1])) )
plt.xlabel('Energy (eV)'); plt.ylabel('States/eV'); ax.grid(True)
ax.legend(loc='upper center', bbox_to_anchor=(0.90, 0.95), ncol=1, fontsize='small', fancybox=True, shadow=True)


#ax=ax2; #plt.setp( ax.get_yticklabels(), visible=False); 
##ax.tick_params(top="off", left="off", right="off", direction="out")
#Esu, dsu = mSMOOTH.Gaussian(Edos,tdos[0],sigma,0); dsu[0] = 0; dsu[-1] = 0;
#Esd, dsd = mSMOOTH.Gaussian(Edos,tdos[1],sigma,0); dsd[0] = 0; dsd[-1] = 0;
#ax.fill(Esu, dsu, 'r-', lw=2, alpha=0.9, label='total DOS')
#ax.fill(Esd,-dsd, 'r-', lw=2, alpha=0.9)
#ax.plot([ -200, 100 ], [ 0, 0 ], 'k-', linewidth=1.2)
#ax.plot([ 0, 0 ], [ -800, 800 ], 'k-', linewidth=1.2)
#ax.set_xlim( (minx, maxx) ); #ax.set_ylim( (max(dsu)*1.1, (min(-dsd)*1.1 )) )
#plt.xlabel('Energy (eV)'); plt.ylabel('States/eV'); ax.grid(True)
#ax.legend(loc='upper center', bbox_to_anchor=(0.90, 0.95), ncol=1, fontsize='small', fancybox=True, shadow=True)


plt.savefig('dos.png', format='png', dpi=200)


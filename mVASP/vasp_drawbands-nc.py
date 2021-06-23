#!/usr/bin/python2

import matplotlib
matplotlib.use('Agg') # see http://matplotlib.org/faq/usage_faq.html#what-is-a-backend

import os
import numpy as np
from   pylab import *
import scipy.io as sio
from   matplotlib import gridspec


font = {'size':8}
matplotlib.rc('font', **font)
#savefig('plot.png', format='png', dpi=200) 
#### ========================================================  NOTE: DNR




#### ========================================================  NOTE: inputs
inputs = sys.argv
ilen   = len(inputs)

if ilen == 1:
    bf = os.getcwd(); df = os.getcwd(); cf = os.getcwd()
    inputs.extend(['l',bf,df,-6,6,0,10,0.05,0,0,cf]); 
if ilen == 2:
    bf = os.getcwd(); df = os.getcwd(); cf = os.getcwd()
    inputs.extend([bf,df,-6,6,0,10,0.05,0,0,cf]);
if ilen == 3:
    df = os.getcwd(); cf = os.getcwd()
    inputs.extend([df,-6,6,0,10,0.05,0,0,cf]);
if ilen == 4:
    cf = os.getcwd()
    inputs.extend([-6,6,0,10,0.05,0,0,cf]);
if ilen == 5:
    cf = os.getcwd()
    inputs.extend([6,0,10,0.05,0,0,cf]);
if ilen == 6:
    cf = os.getcwd()
    inputs.extend([0,10,0.05,0,0,cf]);
if ilen == 7:
    cf = os.getcwd()
    inputs.extend([10,0.05,0,0,cf]);
if ilen == 8:
    cf = os.getcwd()
    inputs.extend([0.05,0,0,cf]);
if ilen == 9:
    cf = os.getcwd()
    inputs.extend([0,0,cf]);
if ilen == 10:
    cf = os.getcwd()
    inputs.extend([0,cf]);    
if ilen == 11:
    cf = os.getcwd()
    inputs.extend([cf]);     
   
    
lr = inputs[1]
bf = inputs[2]
df = inputs[3]
ymin = float(inputs[4])
ymax = float(inputs[5])    
dxmin = float(inputs[6])
dxmax = float(inputs[7]) 
sigma = float(inputs[8])
bshift = float(inputs[9])
dshift = float(inputs[10])    
cf = inputs[11]





#### ========================================================  NOTE: reader
def readvasprunnpz(lr,sigma):
    if lr == 'r':
      if os.path.isfile('vasprun.xml') == False:
        print('vasprun.xml DOES NOT exist !!!', file=sys.stderr)
        print("Exception: %s" % str(1), file=sys.stderr)
        sys.exit(1)
      print()  
      print('reading available vasprun.xml....')  
      os.popen("vasp_readxml.py")
      print()

    if lr == 'l':
        if os.path.isfile('vasprun.npz') == False:
            print('vasprun.npz DOES NOT exist !!!', file=sys.stderr)
            print('reading available vasprun.xml....')
            os.popen("vasp_readxml.py")
        else:
            print('reading available vasprun.xml....')

    readdata = np.load('vasprun.npz')
    
    params = readdata['params']; nspin  = int(params[2]); natom  = int(params[6]); ndos   = int(params[5]); nelect   = int(params[8]);
    efermi = readdata['efermi']
    kpoints_path=readdata['kpoints_path']; klines_path=readdata['klines_path'];
    bands_up=readdata['bands_up']; bands_dw=readdata['bands_dw']
        
    return params, kpoints_path, klines_path, bands_up, bands_dw, efermi   






 

#### ========================================================  NOTE: bands
ax1 = plt.subplot(111)
ax1.tick_params(top="off", right="on", direction="out" )

# read data
os.chdir(bf)  
params, kpoints_path, klines_path, bands_up, bands_dw, efermi = readvasprunnpz(lr,sigma)
os.chdir(cf)

print(efermi)

# draw vertical lines band structure
for kl in range(1,len(klines_path)-1):
    plt.plot([ klines_path[kl],  klines_path[kl]  ], [ ymin, ymax ], 'k-', linewidth=0.1) 

for b in range(len(bands_up)):
  ax1.plot(kpoints_path,bands_up[b]-efermi+bshift, 'k-', lw=2, mfc='k', ms=3)
  if params[2] == 2: 
    ax1.plot(kpoints_path,bands_dw[b]-efermi+bshift, 'b--', lw=1, mfc='k', ms=0)

# shade band gap
vband=params[8]
cband=(params[8])+1
ax1.fill_between(kpoints_path, bands_up[vband-1]-efermi+bshift, 0, lw=0, facecolor='y')
ax1.fill_between(kpoints_path, 0, bands_up[cband-1]-efermi+bshift, lw=0, facecolor='y')



# arrange limits
ax1.plot([ 0, max(kpoints_path) ], [ 0, 0 ], 'k-.',linewidth=0.4)
plt.xticks([]); plt.ylabel('Energy (eV)', fontsize=12) 
xlim( (0, max(kpoints_path)) ); ylim( ymin, ymax ) 
#plt.xlabel('( KPOINTS PATH : $\Gamma$  ->   X  ->   S  ->   $\Gamma$  ->   Y )')

#### ========================================================  NOTE: text
test = '$E_{gap}$=%.3f (%.3f) [%.3f (%.3f)]; dir/indir=%d (%d); fermi-cor=%.2f '%(params[11], params[12], params[13], params[14], params[16], params[2], params[17])
props = dict(boxstyle='round', facecolor='red', alpha=0.5)
ax1.text(-0.02, -0.05, test, transform=ax1.transAxes, fontsize=9,
        verticalalignment='top', bbox=props)


 
 
 
 



#### ========================================================  NOTE: export
plt.savefig('bands.eps', format='eps', dpi=200) 





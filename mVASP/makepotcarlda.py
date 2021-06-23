#!/usr/bin/python

import subprocess
import sys
from sys import argv


potlist = sys.argv


potroot='~/_potentials/vasp/potpaw_LDA.54'

subprocess.call('> POTCAR', shell=True); 



for i in range(len(potlist)-1): 
    subprocess.call('cat '+potroot+'/'+potlist[i+1]+'/POTCAR >> POTCAR', shell=True) 





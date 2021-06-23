#!/usr/bin/python

import subprocess
import sys
from sys import argv


potlist = sys.argv


potroot='/home/mt/gd/work/_potcars/potpaw_PBE.54'

subprocess.call('> POTCAR', shell=True); 



for i in range(len(potlist)-1): 
    subprocess.call('cat '+potroot+'/'+potlist[i+1]+'/POTCAR >> POTCAR', shell=True) 





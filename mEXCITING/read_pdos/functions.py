

import numpy as np
import os 
import subprocess

file='dos.agr'



#if not os.path.exists(file):
    #subprocess.call(' xsltproc $EXCITINGVISUAL/xmldos2grace.xsl dos.xml > dos.agr ', shell=True)
subprocess.call(' xsltproc $EXCITINGVISUAL/xmldos2grace.xsl dos.xml > dos.agr ', shell=True)




with open(file) as f:
    lines = f.readlines()


    
states=[] 
data=[]
for i, line in enumerate(lines):
    
    if line.startswith('@s'):
        t = line.split('"')[1]
        t = t.split('\\')[0]
        states.append(t)
    elif line.startswith('&'):
        1
    elif line.startswith('#'):
        1    
    elif line.startswith('@'):
        1 
    else:
        if len(line) > 1:
            data.append(line.split())
        

data = np.array(data, np.float )





natoms = (len(states)-2) // 25
ndos   = (len(data)) // (25*natoms+2)



E = data[0:ndos, 0]
tdos   = data[0:ndos, 1]
intdos = data[ndos:2*ndos, 1]
p = data[2*ndos:, 1]



tmp = []
s=0
for i in range(natoms):
    tmp.append(p[s:s+ndos*25])
    s = s + ndos*25
                   
              
pdoss = []
for i in range(natoms):
    t = np.reshape(tmp[i], (25,ndos))
    t = t.T
    s = t[:,0]
    p = np.sum(t[:,1:4],  axis=1)
    d = np.sum(t[:,4:9],  axis=1)
    f = np.sum(t[:,9:16], axis=1)
    pdoss.append([s,p,d,f])
    


np.savez('exciting', E=E, tdos=tdos, intdos=intdos, pdoss=pdoss)
subprocess.call('  zip -rq exciting.npz dos.xml input.xml', shell=True)






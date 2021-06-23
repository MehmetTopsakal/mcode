#!/usr/bin/python2

from   sys   import stdin
import os    as os
import pylab as pyl
import numpy as np
import itertools as it 
from   io import StringIO
from   pylab import *
from   string import *

#### ========================================================  NOTE: DNR




f = open('DOSCAR','r')
natom = int(split(f.readline())[0])
line2 = f.readline()
line2 = split(line2)
v1    = float(line2[0]) ; v2 = float(line2[1]) ; v3 = float(line2[2]) ; v4 = float(line2[3]) ;
f.readline()
f.readline()
f.readline()
line6 = f.readline()
line6 = split(line6)
emax  = float(line6[0]) ; emin = float(line6[1]) ; ndos = int(line6[2]) ; fermi = float(line6[3]) ;
line7 = f.readlines()[6]
line7 = np.genfromtxt(StringIO(line7))
f.close()

did =  v1+v2+v3+v4+fermi+emin+emax


## check .DOSCAR.npz ------------------------------------------------------------- |
oldnpz = os.path.exists('.DOSCAR.npz')
if (oldnpz):
  readdata = np.load('.DOSCAR.npz')
  did_old = readdata['did']
  if did_old==did:
    print("...")
    print(".DOSCAR.npz exist !!!")
    sys.exit("\n")



with open('DOSCAR') as dfile:
    for line in it.islice(dfile,ndos+6,ndos+8):
      lenpdos = len(line) 
      
try:
    lenpdos
except:
    lenpdos = 0
  
  

## read pdos ------------------------------------------------------------- | 
print("Reading DOSCAR...")

if len(line7) == 5:
  E =  [] ; tu =  [] ; td =  [] ; su =  [] ; sd =  [] ; pu =  [] ; pd =  [] ;   du =  [] ; dd =  [] ;   fu =  [] ; fd =  [] ; ai = 1
  if lenpdos == 33*12:
    print("This is a magnetic DOSCAR and contains s,p,d,f") 
    with open('DOSCAR') as dfile:
      for line in it.islice(dfile, 6, 6+ndos):     # start=17, stop=None 
        r = np.genfromtxt(StringIO(line),usecols=(0,1,2))
        E.append(r[0]) ; tu.append(r[1]) ; td.append(r[2])
      E = np.array(E) ; tu = np.array(tu) ; td = np.array(td) ;
      for line in it.islice(dfile, 1, None):  # start=17, stop=None
        if len(line) != lenpdos: 
	  print(ai) ; ai += 1
	  continue
        r = np.genfromtxt(StringIO(line))
        su.append(r[1])  ; sd.append(r[2])
        pu.append(r[3]+r[5]+r[7]) ; pd.append(r[4]+r[6]+r[8]) ;  
        du.append(r[9]+r[11]+r[13]+r[15]+r[17]) ; dd.append(r[10]+r[12]+r[14]+r[16]+r[18]) ; 
        fu.append(r[19]+r[21]+r[23]+r[25]+r[27]+r[29]+r[31]) ; fd.append(r[20]+r[22]+r[24]+r[26]+r[28]+r[30]+r[32]) ; 
      su = np.array(su) ; sd = np.array(sd) ; pu = np.array(pu) ; pd = np.array(pd) ; du = np.array(du) ; dd = np.array(dd) ; fu = np.array(fu) ; fd = np.array(fd)  
    su = su.reshape(ndos,natom,order='F').copy()
    sd = sd.reshape(ndos,natom,order='F').copy()
    pu = pu.reshape(ndos,natom,order='F').copy()
    pd = pd.reshape(ndos,natom,order='F').copy()
    du = du.reshape(ndos,natom,order='F').copy()
    dd = dd.reshape(ndos,natom,order='F').copy()
    fu = fu.reshape(ndos,natom,order='F').copy()
    fd = fd.reshape(ndos,natom,order='F').copy()
    np.savez('.DOSCAR.npz', did=did, fermi=fermi, E=E, tu=tu, td=td, su=su, sd=sd, pu=pu, pd=pd, du=du, dd=dd, fu=fu, fd=fd)
  else:
    if lenpdos == 19*12:
      print("This is a magnetic DOSCAR and contains s,p,d") 
      with open('DOSCAR') as dfile:
        for line in it.islice(dfile, 6, 6+ndos):     # start=17, stop=None 
          r = np.genfromtxt(StringIO(line),usecols=(0,1,2))
          E.append(r[0]) ; tu.append(r[1]) ; td.append(r[2])
        E = np.array(E) ; tu = np.array(tu) ; td = np.array(td) ;
        for line in it.islice(dfile, 1, None):  # start=17, stop=None
          if len(line) != lenpdos: 
	    print(ai) ; ai += 1
	    continue
          r = np.genfromtxt(StringIO(line))
          su.append(r[1])  ; sd.append(r[2])
          pu.append(r[3]+r[5]+r[7]) ; pd.append(r[4]+r[6]+r[8]) ;  
          du.append(r[9]+r[11]+r[13]+r[15]+r[17]) ; dd.append(r[10]+r[12]+r[14]+r[16]+r[18]) ; 
      su = np.array(su) ; sd = np.array(sd) ; pu = np.array(pu) ; pd = np.array(pd) ; du = np.array(du) ; dd = np.array(dd) ; 
      su = su.reshape(ndos,natom,order='F').copy()
      sd = sd.reshape(ndos,natom,order='F').copy()
      pu = pu.reshape(ndos,natom,order='F').copy()
      pd = pd.reshape(ndos,natom,order='F').copy()
      du = du.reshape(ndos,natom,order='F').copy()
      dd = dd.reshape(ndos,natom,order='F').copy()
      np.savez('.DOSCAR.npz', did=did, fermi=fermi, E=E, tu=tu, td=td, su=su, sd=sd, pu=pu, pd=pd, du=du, dd=dd)
    else:
      if lenpdos == 0:
	print("This is a magnetic DOSCAR but do not contain partial dos!!")
        with open('DOSCAR') as dfile:
          for line in it.islice(dfile, 6, 6+ndos):     # start=17, stop=None 
            r = np.genfromtxt(StringIO(line),usecols=(0,1,2))
            E.append(r[0]) ; tu.append(r[1]) ; td.append(r[2])
          E = np.array(E) ; tu = np.array(tu) ; td = np.array(td) ;
        np.savez('.DOSCAR.npz', did=did, fermi=fermi, E=E, tu=tu, td=td)  
       
       
if len(line7) == 3:
  E =  [] ; t =  [] ; s =  [] ; p =  [] ; d =  [] ; f = []
  if lenpdos == 17*12:
    print("This is a non-magnetic DOSCAR and contains s,p,d,f")
    with open('DOSCAR') as dfile:
      for line in it.islice(dfile, 6, 6+ndos):     # start=17, stop=None 
        r = np.genfromtxt(StringIO(line),usecols=(0,1,2))
        E.append(r[0]) ; t.append(r[1]) ;
      E = np.array(E) ; t = np.array(t) ;
      for line in it.islice(dfile, 1, None):  # start=17, stop=None
        if len(line) != lenpdos: continue
        r = np.genfromtxt(StringIO(line))
        s.append(r[1]) ; 
        p.append(r[2]+r[3]+r[4]) ; 
        d.append(r[5]+r[6]+r[7]+r[8]+r[9]) ;
        f.append(r[10]+r[11]+r[12]+r[13]+r[14]+r[15]+r[16]) ; 
      s = np.array(s) ; p = np.array(p) ; d = np.array(d) ; f = np.array(f) ;
    s = s.reshape(ndos,natom,order='F').copy()
    p = p.reshape(ndos,natom,order='F').copy()
    d = d.reshape(ndos,natom,order='F').copy()
    f = f.reshape(ndos,natom,order='F').copy()
    np.savez('.DOSCAR.npz', did=did, fermi=fermi, E=E, t=t, s=s, p=p, d=d, f=f, tu=t/2, td=t/2, su=s/2, sd=s/2, pu=p/2, pd=p/2, du=d/2, dd=d/2, fu=d/2, fd=d/2)
  else:
    if lenpdos == 10*12:
      print("This is a non-magnetic DOSCAR and contains s,p,d")
      with open('DOSCAR') as dfile:
        for line in it.islice(dfile, 6, 6+ndos):     # start=17, stop=None 
          r = np.genfromtxt(StringIO(line),usecols=(0,1,2))
          E.append(r[0]) ; t.append(r[1]) ; 
        E = np.array(E) ; t = np.array(t) ; 
        for line in it.islice(dfile, 1, None):  # start=17, stop=None
          if len(line) != lenpdos: continue
          r = np.genfromtxt(StringIO(line))
          s.append(r[1]) ;
          p.append(r[2]+r[3]+r[4]) ; 
          d.append(r[5]+r[6]+r[7]+r[8]+r[9]) ;
        s = np.array(s) ; p = np.array(p) ; d = np.array(d) ; 
      s = s.reshape(ndos,natom,order='F').copy()
      p = p.reshape(ndos,natom,order='F').copy()
      d = d.reshape(ndos,natom,order='F').copy()
      np.savez('.DOSCAR.npz', did=did, fermi=fermi, E=E, t=t, s=s, p=p, d=d, f=f, tu=t/2, td=t/2, su=s/2, sd=s/2, pu=p/2, pd=p/2, du=d/2, dd=d/2 )
    else:
      if lenpdos == 0:
        with open('DOSCAR') as dfile:
	  print("This is a non-magnetic DOSCAR but do not contain partial dos!!")
          for line in it.islice(dfile, 6, 6+ndos):     # start=17, stop=None 
            r = np.genfromtxt(StringIO(line),usecols=(0,1,2))
            E.append(r[0]) ; t.append(r[1]) ;
          E = np.array(E) ; t = np.array(t) ;
        np.savez('.DOSCAR.npz', did=did, fermi=fermi, E=E, t=t, tu=t/2, td=t/2)         
        
        
        
        
        
        
        
        
        
        
        
        
        
  

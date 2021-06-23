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
  E =  [] ; tu =  [] ; td =  [] ; su =  [] ; sd =  [] ; pu =  [] ; pd =  [] ;  pu1 =  [] ; pd1 =  [] ; pu2 =  [] ; pd2 =  [] ;  pu3 =  [] ; pd3 =  [] ;     
  du =  [] ; dd =  [] ; du1 =  [] ; dd1 =  [] ; du2 =  [] ; dd2 =  [] ; du3 =  [] ; dd3 =  [] ; du4 =  [] ; dd4 =  [] ; du5 =  [] ; dd5 =  [] ;   fu =  [] ; fd =  [] ; ai = 1
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
        pu1.append(r[3]) ; pd1.append(r[4]) ;        
        pu2.append(r[5]) ; pd2.append(r[6]) ;
        pu3.append(r[7]) ; pd3.append(r[8]) ;        
        du.append(r[9]+r[11]+r[13]+r[15]+r[17]) ; dd.append(r[10]+r[12]+r[14]+r[16]+r[18]) ;
        du1.append(r[9])  ; dd1.append(r[10]) ;
        du2.append(r[11]) ; dd2.append(r[12]) ;
        du3.append(r[13]) ; dd3.append(r[14]) ;
        du4.append(r[15]) ; dd4.append(r[16]) ;
        du5.append(r[17]) ; dd5.append(r[18]) ;        
        fu.append(r[19]+r[21]+r[23]+r[25]+r[27]+r[29]+r[31]) ; fd.append(r[20]+r[22]+r[24]+r[26]+r[28]+r[30]+r[32]) ; 
      su = np.array(su) ; sd = np.array(sd) ;  
      pu = np.array(pu) ; pd = np.array(pd) ;       
      pu1 = np.array(pu1) ; pd1 = np.array(pd1) ; pu2 = np.array(pu2) ; pd2 = np.array(pd2) ; pu3 = np.array(pu3) ; pd3 = np.array(pd3) ;  
      du = np.array(du) ; dd = np.array(dd) ; 
      du1 = np.array(du1) ; dd1 = np.array(dd1) ;  du2 = np.array(du2) ; dd2 = np.array(dd2) ; du3 = np.array(du3) ; dd3 = np.array(dd3) ; du4 = np.array(du4) ; dd4 = np.array(dd4) ; du5 = np.array(du5) ; dd5 = np.array(dd5) ;      
      fu = np.array(fu) ; fd = np.array(fd)       
    su = su.reshape(ndos,natom,order='F').copy() ; sd = sd.reshape(ndos,natom,order='F').copy()
    pu = pu.reshape(ndos,natom,order='F').copy() ; pd = pd.reshape(ndos,natom,order='F').copy()
    pu1 = pu1.reshape(ndos,natom,order='F').copy() ; pd1 = pd1.reshape(ndos,natom,order='F').copy()
    pu2 = pu2.reshape(ndos,natom,order='F').copy() ; pd2 = pd2.reshape(ndos,natom,order='F').copy()
    pu3 = pu3.reshape(ndos,natom,order='F').copy() ; pd3 = pd3.reshape(ndos,natom,order='F').copy()    
    du = du.reshape(ndos,natom,order='F').copy() ; dd = dd.reshape(ndos,natom,order='F').copy()
    du1 = du1.reshape(ndos,natom,order='F').copy() ; dd1 = dd1.reshape(ndos,natom,order='F').copy()
    du2 = du2.reshape(ndos,natom,order='F').copy() ; dd2 = dd2.reshape(ndos,natom,order='F').copy()
    du3 = du3.reshape(ndos,natom,order='F').copy() ; dd3 = dd3.reshape(ndos,natom,order='F').copy()
    du4 = du4.reshape(ndos,natom,order='F').copy() ; dd4 = dd4.reshape(ndos,natom,order='F').copy()
    du5 = du5.reshape(ndos,natom,order='F').copy() ; dd5 = dd5.reshape(ndos,natom,order='F').copy()    
    fu = fu.reshape(ndos,natom,order='F').copy() ; fd = fd.reshape(ndos,natom,order='F').copy()
    np.savez('.DOSCAR.npz', did=did, fermi=fermi, E=E, tu=tu, td=td, su=su, sd=sd, pu=pu, pd=pd, pu1=pu1, pd1=pd1, pu2=pu2, pd2=pd2, pu3=pu3, pd3=pd3,  du=du, dd=dd, du1=du1, dd1=dd1, du2=du2, dd2=dd2, du3=du3, dd3=dd3, du4=du4, dd4=dd4, du5=du5, dd5=dd5, fu=fu, fd=fd)
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
          pu1.append(r[3]) ; pd1.append(r[4]) ;        
          pu2.append(r[5]) ; pd2.append(r[6]) ;
          pu3.append(r[7]) ; pd3.append(r[8]) ;        
          du.append(r[9]+r[11]+r[13]+r[15]+r[17]) ; dd.append(r[10]+r[12]+r[14]+r[16]+r[18]) ;
          du1.append(r[9])  ; dd1.append(r[10]) ;
          du2.append(r[11]) ; dd2.append(r[12]) ;
          du3.append(r[13]) ; dd3.append(r[14]) ;
          du4.append(r[15]) ; dd4.append(r[16]) ;
          du5.append(r[17]) ; dd5.append(r[18]) ;        
        su = np.array(su) ; sd = np.array(sd) ;  
        pu = np.array(pu) ; pd = np.array(pd) ;       
        pu1 = np.array(pu1) ; pd1 = np.array(pd1) ; pu2 = np.array(pu2) ; pd2 = np.array(pd2) ; pu3 = np.array(pu3) ; pd3 = np.array(pd3) ;  
        du = np.array(du) ; dd = np.array(dd) ; 
        du1 = np.array(du1) ; dd1 = np.array(dd1) ;  du2 = np.array(du2) ; dd2 = np.array(dd2) ; du3 = np.array(du3) ; dd3 = np.array(dd3) ; du4 = np.array(du4) ; dd4 = np.array(dd4) ; du5 = np.array(du5) ; dd5 = np.array(dd5) ;      
      su = su.reshape(ndos,natom,order='F').copy() ; sd = sd.reshape(ndos,natom,order='F').copy()
      pu = pu.reshape(ndos,natom,order='F').copy() ; pd = pd.reshape(ndos,natom,order='F').copy()
      pu1 = pu1.reshape(ndos,natom,order='F').copy() ; pd1 = pd1.reshape(ndos,natom,order='F').copy()
      pu2 = pu2.reshape(ndos,natom,order='F').copy() ; pd2 = pd2.reshape(ndos,natom,order='F').copy()
      pu3 = pu3.reshape(ndos,natom,order='F').copy() ; pd3 = pd3.reshape(ndos,natom,order='F').copy()    
      du = du.reshape(ndos,natom,order='F').copy() ; dd = dd.reshape(ndos,natom,order='F').copy()
      du1 = du1.reshape(ndos,natom,order='F').copy() ; dd1 = dd1.reshape(ndos,natom,order='F').copy()
      du2 = du2.reshape(ndos,natom,order='F').copy() ; dd2 = dd2.reshape(ndos,natom,order='F').copy()
      du3 = du3.reshape(ndos,natom,order='F').copy() ; dd3 = dd3.reshape(ndos,natom,order='F').copy()
      du4 = du4.reshape(ndos,natom,order='F').copy() ; dd4 = dd4.reshape(ndos,natom,order='F').copy()
      du5 = du5.reshape(ndos,natom,order='F').copy() ; dd5 = dd5.reshape(ndos,natom,order='F').copy()    
      np.savez('.DOSCAR.npz', did=did, fermi=fermi, E=E, tu=tu, td=td, su=su, sd=sd, pu=pu, pd=pd, pu1=pu1, pd1=pd1, pu2=pu2, pd2=pd2, pu3=pu3, pd3=pd3,  du=du, dd=dd, du1=du1, dd1=dd1, du2=du2, dd2=dd2, du3=du3, dd3=dd3, du4=du4, dd4=dd4, du5=du5, dd5=dd5)
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
  E =  [] ; t =  [] ; s =  [] ; p =  [] ; d =  [] ; p1 =  [] ; p2 =  [] ; p3 =  [] ; d1 =  [] ; d2 =  [] ; d3 =  [] ; d4 =  [] ; d5 =  [] ; f = []
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
        p1.append(r[2]) ; 
        p2.append(r[3]) ; 
        p3.append(r[4]) ; 
        d.append(r[5]+r[6]+r[7]+r[8]+r[9]) ;
        d1.append(r[5]);
        d2.append(r[6]);
        d3.append(r[7]);
        d4.append(r[8]);
        d5.append(r[9]);
        f.append(r[10]+r[11]+r[12]+r[13]+r[14]+r[15]+r[16]) ; 
      s = np.array(s) ; p = np.array(p) ; d = np.array(d) ; f = np.array(f) ;  p1 = np.array(p1) ; p2 = np.array(p2) ; p3 = np.array(p3) ; d1 = np.array(d1) ; d2 = np.array(d2) ; d3 = np.array(d3) ; d4 = np.array(d4) ; d5 = np.array(d5) ;
    s = s.reshape(ndos,natom,order='F').copy();
    p = p.reshape(ndos,natom,order='F').copy();
    d = d.reshape(ndos,natom,order='F').copy();
    p1 = p1.reshape(ndos,natom,order='F').copy();
    p2 = p2.reshape(ndos,natom,order='F').copy();
    p3 = p3.reshape(ndos,natom,order='F').copy();    
    d1 = d1.reshape(ndos,natom,order='F').copy();
    d2 = d2.reshape(ndos,natom,order='F').copy();
    d3 = d3.reshape(ndos,natom,order='F').copy();
    d4 = d4.reshape(ndos,natom,order='F').copy();
    d5 = d5.reshape(ndos,natom,order='F').copy();
    f = f.reshape(ndos,natom,order='F').copy()
    np.savez('.DOSCAR.npz', did=did, fermi=fermi, E=E, t=t, s=s, p=p, d=d, f=f, tu=t/2, td=t/2, su=s/2, sd=s/2, pu=p/2, pd=p/2, du=d/2, dd=d/2, fu=f/2, fd=f/2, p1=p1, p2=p2, p3=p3, d1=d1, d2=d2, d3=d3, d4=d4, d5=d5,  pu1=p1/2, pu2=p2/2, pu3=p3/2, pd1=p1/2, pd2=p2/2, pd3=p3/2, du1=d1/2, du2=d2/2, du3=d3/2, du4=d4/2, du5=d5/2, dd1=d1/2, dd2=d2/2, dd3=d3/2, dd4=d4/2, dd5=d5/2)
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
        
        
        
        
        
        
        
        
        
        
        
        
        
  

#!/usr/bin/env python

import numpy as np 
import mSMOOTH
import subprocess 
import itertools



def readoctahedra(p=None,ca=None,ci=None):
    
    if p is None: p='POSCAR'
    if ca is None: ca=1    
    if ci is None: ci=2 
    nn=6
    supercell=2
    

    subprocess.call(' feff_poscar2atoms.py t='+str(ca)+' d=5 p='+p+'; grep "     '+str(ci)+'    " atoms.dat | head -n '+str(nn)+'  > dis.dat', shell=True)
    distances = np.loadtxt('dis.dat', unpack=True, comments='#', usecols=(0,1,2,3,4), skiprows=0)
    
    d_ave=sum(distances[4])/int(nn)
    v_ave = (4/3)*d_ave*d_ave*d_ave
    
    
    
    #  some parts from http://stackoverflow.com/questions/9866452/calculate-volume-of-any-tetrahedron-given-4-points
    def determinant_3x3(m):
        return (m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1]) -
                m[1][0] * (m[0][1] * m[2][2] - m[0][2] * m[2][1]) +
                m[2][0] * (m[0][1] * m[1][2] - m[0][2] * m[1][1]))
    
    
    def subtract(a, b):
        return (a[0] - b[0],
                a[1] - b[1],
                a[2] - b[2])
    
    def tetrahedron_calc_volume(a, b, c, d):
        return (abs(determinant_3x3((subtract(a, b),
                                     subtract(b, c),
                                     subtract(c, d),
                                     ))) / 6.0)
    
    
    ## calc v1
    distancesT =  np.transpose(distances)
    a = [0,0,0]
    b = distancesT[0][:3].tolist()
    c = distancesT[1][:3].tolist()
    d = distancesT[2][:3].tolist()
    

    clist = list(itertools.combinations('012345',3))

    b = distancesT[int(clist[0][0])][:3].tolist()
    
    
    v_oct = 0
    for i in range(len(clist)):
        
        a = [0,0,0]
        b = distancesT[int(clist[i][0])][:3].tolist()
        c = distancesT[int(clist[i][1])][:3].tolist()
        d = distancesT[int(clist[i][2])][:3].tolist()
        
        v = tetrahedron_calc_volume(a, b, c, d)
        if v > v_ave/100: v_oct = v_oct+v
    
    d_ideal = (v_oct*(3/4))**(1/3)
    

# ===========================     
    # calculate quadratic elongation, lambda
    qe = []
    for i in range(len(distances[4])):
        qe.append((distances[4][i]/d_ideal)**2)
    
    qe = sum(qe)/6   
  

# ===========================     
    # calculate bond length distortion index, delta
    D = []
    for i in range(len(distances[4])):
        D.append( abs(distances[4][i]-d_ave)/d_ave )    
    D = sum(D)/6   


# ===========================  
    # calculate center of mass displacement
    sumx = sumy = sumz = 0
    for i in range(len(distancesT)):
        sumx = sumx + distancesT[i][0]
        sumy = sumy + distancesT[i][1]    
        sumz = sumz + distancesT[i][2]
    ocd = np.sqrt((sumx/6)*(sumx/6)+(sumy/6)*(sumy/6)+(sumz/6)*(sumz/6))


# =========================== 
    # calculate s2 >> \sigma2=\sum_i (R_i- R_avg)2
    s2 = []
    for i in range(len(distancesT)):
        s2.append( (distancesT[i][4]-d_ave)*(distancesT[i][4]-d_ave) )    
    s2  = np.array(s2, np.float)    
    s2 = sum(s2/6)

    
    #clist2 = list(itertools.combinations('012345',4)) 
    #print(distancesT)
    #print(clist2)
    
    #print(distancesT[int(clist2[i][0])])

    #for i in range(len(clist2)):
        #p1 = distancesT[int(clist2[i][0])][0:3]
        #p2 = distancesT[int(clist2[i][1])][0:3]
        #p3 = distancesT[int(clist2[i][2])][0:3]                       
        #p4 = distancesT[int(clist2[i][3])][0:3] 
        #tx = (p1[0]+p2[0]+p3[0]+p4[0])/4
        #ty = (p1[1]+p2[1]+p3[1]+p4[1])/4
        #tz = (p1[2]+p2[2]+p3[2]+p4[2])/4
        
    #for i in range(len(clist2)):
        #print(distancesT[int(clist2[i][0])])
        
    
    
    subprocess.call(' rm -f atoms.dat atoms.xyz dis.dat', shell=True)
    
    
    #out=[d_ideal, d_ave, v_oct, qe, D]
    #print(out)




    return d_ideal, d_ave, v_oct, qe, D, ocd, s2








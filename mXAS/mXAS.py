#!/usr/bin/env python

import numpy as np
import mSMOOTH
from scipy.interpolate import InterpolatedUnivariateSpline

### 
### 
### 
### 
### 
### 
### 
#### ========================================================




def darrange_old(datax,datay,wbin=None,peakrange=None,xshift=None,yscale=None):
        
    if wbin is None: wbin=0
    if peakrange is None: peakrange=[datax[0],datax[-1]]


    if wbin != 0: 
        Sbroad=float(wbin[0]);Cbroad=float(wbin[1]);Vswitch=int(wbin[2]);edgeoffset=float(wbin[3])
        dbx, dby = mSMOOTH.wien(datax,datay,Sbroad,Cbroad,Vswitch,edgeoffset)
    else:   dbx, dby = datax, datay  

    sel = (dbx > peakrange[0]) & (dbx < peakrange[1]); dsx, dsy = dbx[sel], dby[sel];

    peaky = dsy[0]
    for p in range(len(dsy)):
        if dsy[p] > peaky: peaky = dsy[p]; peakx = dsx[p]

    print([peakx,1/peaky])

    if xshift is None: 
        xshift=peakx  
    
    if yscale is None: 
        yscale=1/peaky
        
 
    newx = dbx-xshift
    newy = dby*yscale

    return newx, newy
    



def findpeaks(dx,dy):
    peaks = []
    peaksx = []
    peaksy = []
    peaky = dy[0]
    for p in range(1,len(dx)-1):
        if dy[p] > peaky: 
            peaky = dy[p]; peakx = dx[p]; 
            if (dy[p-1] < peaky) and (dy[p+1] < peaky) : peaks.append([peakx,peaky,0])
    #peaks.append([dx[-1],dy[-1]])        
    peaks = np.array(peaks)  
    
    return peaks
    



def peak2gauss(dx,dy):
    
    peaks = findpeaks(dx,dy)    
    mu = peaks[0][0]
    height = peaks[0][1]
    range_sigma=np.arange(1,5, 0.1)
    diffs = []
    for i in range(len(range_sigma)):
        
        sigma=range_sigma[i]
        h=height*np.sqrt(2 * np.pi)*sigma
        g = h/(sigma * np.sqrt(2 * np.pi)) * np.exp( - (dx - mu)**2 / (2 * sigma**2) )

        diff = dy-g
        tmpy = diff
        
        absdiff = []
        for j in range(len(tmpy)):
            absdiff.append(abs(tmpy[j]))
        diffs.append([range_sigma[i],sum(absdiff)])    
    
    diffs = np.array(diffs) 
    diffs = diffs[diffs[:,1].argsort()]
    
    sigma = diffs[0][0]     
    
    h = height*np.sqrt(2 * np.pi)*sigma
    g = h/(sigma * np.sqrt(2 * np.pi)) * np.exp( - (dx - mu)**2 / (2 * sigma**2) )
    
    xg = dx; yg = g 
        
    return mu, height, sigma, xg, yg     






















    

#################################################################################################
#################################################################################################
#################################################################################################
#################################################################################################
#################################################################################################

def GaussDecompose(x0,y0,NNLS=None,padd=None,sigma=None,xayar1=None,xayar2=None,yayar1=None,yayar2=None,sayar1=None,sayar2=None):
    
    if NNLS is None: NNLS=0
    if padd is None: padd=2     
    if sigma is None: sigma=0.2   
    if xayar1 is None: xayar1=[0,1] 
    if xayar2 is None: xayar2=[0,1]
    if yayar1 is None: yayar1=[0,1] 
    if yayar2 is None: yayar2=[0,1]
    if sayar1 is None: sayar1=[0,1] 
    if sayar2 is None: sayar2=[0,1]
    
    omode=1


    def gauss(xin,sigma,peakheight,mu): 
        
        h=peakheight*np.sqrt(2 * np.pi)*sigma
        gout = h/(sigma * np.sqrt(2 * np.pi)) * np.exp( - (xin - mu)**2 / (2 * sigma**2) )
        return gout 
    
    
    def optimize_sigma(xin,yin,peakheight,mu,omode):
        
        sigma_range1 = np.linspace(0.1,25,50)
        diffs = []
        sel = (xin >= 0) & (xin <= mu)    
        for i in range(len(sigma_range1)):
            g = gauss(xin[sel],sigma_range1[i],peakheight,mu)
            diff = yin[sel]-g
            absdiff = []
            for j in range(len(diff)):
                absdiff.append(abs(diff[j]))
            diffs.append([sigma_range1[i],sum(absdiff)])        
        diffs = np.array(diffs) 
        diffs = diffs[diffs[:,1].argsort()]       
        sigma_best = diffs[0][0]
        
        
        sigma_range2 = np.linspace(sigma_best*0.5,sigma_best*1.5,50)
        #sigma_range2 = np.linspace(0.1,25,50)
        diffs = []
        if omode == 0: sel = (xin >= 0) & (xin <= mu)
        if omode == 1: sel = (xin >= (mu-sigma_best)) & (xin <= (mu+sigma_best)) 
        if omode == 2: sel = (xin >= (mu-sigma_best/2)) & (xin <= (mu+sigma_best/2))
        if omode == 3: sel = (xin >= (mu)) & (xin <= (mu+sigma_best))
        if omode == 4: sel = (xin >= (mu)) & (xin <= (mu+sigma_best/2))  
        
        #sel = (xin >= (mu-2*sigma_best)) & (xin <= (mu))    
        for i in range(len(sigma_range2)):
            g = gauss(xin[sel],sigma_range2[i],peakheight,mu)
            diff = yin[sel]-g
            absdiff = []
            for j in range(len(diff)):
                absdiff.append(abs(diff[j]))
            diffs.append([sigma_range2[i],sum(absdiff)])        
        diffs = np.array(diffs) 
        diffs = diffs[diffs[:,1].argsort()] 
        sigma_best = diffs[0][0] 

        return sigma_best

    

    def search_gaussians(xin,yin,peaks,omode):
        
        #peaks = peaks[peaks[:,0].argsort()]
        residue = yin
        gaussians = []
        sigmas = []
        for i in range(len(peaks)):
            sigma = optimize_sigma(xin,residue,peakheight=peaks[i][1],mu=peaks[i][0],omode=omode)
            peaks[i][2] = sigma
            g = gauss(xin,sigma,peakheight=peaks[i][1],mu=peaks[i][0])
            gaussians.append(g)
            residue = residue - g
        return peaks, gaussians, residue 
    

    def NNLS_peaks(xin,yin,peaks):       
            
        sel = (xin >= 0) & (xin <= peaks[-1][0]) 
         
        #A=gaussians[0][sel] 
        A = gauss(xin[sel],peaks[0][2],peaks[0][1],peaks[0][0])
        
        for i in range(1,len(peaks)):
            g = gauss(xin[sel],peaks[i][2],peaks[i][1],peaks[i][0])
            #A = np.append(A,gaussians[i][sel])
            A = np.append(A,g)        
        A = A.reshape(len(xin[sel]),len(peaks),order='F').copy()
        b = yin[sel]    
        import scipy
        from scipy.optimize import nnls
        out = nnls(A,b); #print(out)    
        #update peak heights
        for i in range(len(peaks)):
            if out[0][i] < 1: peaks[i][1] = peaks[i][1]*out[0][i]
            
        return peaks


    # find xpsearch, ypsearch 
    #------------------------
    x = x0 
    y = y0
    peaks = findpeaks(x,y)
    peaks, gaussians, residue = search_gaussians(x,y,peaks,omode=1)
    sel  = (x >= 0) & (x <= (peaks[-1][0]+peaks[-1][2]))     
    xpsearch = x[sel]
    ypsearch = y[sel]

    npeaks = len(peaks)+padd

    peaks_final = []
    
    for i in range(npeaks):
        
        # find peaks  
        #-----------
        peaks = findpeaks(xpsearch,ypsearch)
        peaks, gaussians, residue = search_gaussians(xpsearch,ypsearch,peaks,omode=2)    
    
        # remove highest peak from ypsearch
        #---------------------------
        ps = peaks[peaks[:,1].argsort()]; peaks_final.append(ps[-1])
        g = gauss(xpsearch,ps[-1][2],ps[-1][1],ps[-1][0])
        ypsearch = ypsearch - g
    
        # trim ypsearch
        #---------------------------
        yps = []
        for i in range(len(ypsearch)):
            if ypsearch[i] >= 0.0 : yps.append(ypsearch[i])
            else: yps.append(0.0)
        ypsearch = np.array(yps, np.float)

        # smooth ypsearch 
        #---------------------------
        xpsearch, ypsearch = mSMOOTH.Gaussian(xpsearch, ypsearch, sigma)


    peaks_final = np.array(peaks_final, np.float)
    peaks_final = peaks_final[peaks_final[:,0].argsort()]
    #print(peaks_final)
  
    
    for i in range(NNLS):
        peaks_final = NNLS_peaks(x0,y0,peaks_final)      
     

    # ayar1
    peaks_final[xayar1[0]][0]=peaks_final[xayar1[0]][0]*xayar1[1]
    peaks_final[xayar2[0]][0]=peaks_final[xayar2[0]][0]*xayar2[1]
    peaks_final[yayar1[0]][1]=peaks_final[yayar1[0]][1]*yayar1[1]
    peaks_final[yayar2[0]][1]=peaks_final[yayar2[0]][1]*yayar2[1]
    peaks_final[sayar1[0]][2]=peaks_final[sayar1[0]][2]*sayar1[1] 
    peaks_final[sayar2[0]][2]=peaks_final[sayar2[0]][2]*sayar2[1] 
    
    gaussians = []
    for g in range(len(peaks_final)):
        g = gauss(x0,peaks_final[g][2],peaks_final[g][1],peaks_final[g][0])
        gaussians.append(g)

     
    gaussians_sum = x0*0
    for i in range(len(peaks_final)):
        gaussians_sum = gaussians_sum+gaussians[i]    

    residue = y0 - gaussians_sum
    
    #sel = ( >= 0) & (xin <= peaks[-1][0])
    

    return peaks_final, gaussians, gaussians_sum, residue


























#     
#     
#     
#     def findpeaks(dx,dy):    
#         f = InterpolatedUnivariateSpline(dx,dy)
#         dxi = np.arange(dx[0], dx[-1]+0.1, 0.05) 
#         dyi = f(dxi)
#         
#         peaks = []
#         peaksx = []
#         peaksy = []
#         peaky = dyi[0]
#         for p in range(1,len(dxi)-1):
#             if dxi[p] > peaky: 
#                 peaky = dyi[p]; peakx = dxi[p]; 
#                 if (dyi[p-1] < peaky) and (dyi[p+1] < peaky) : peaks.append([peakx,peaky,0.5])
#         
#     #     if max(np.array(peaks)[:,1]) < dyi[-1]: peaks.append([dx[-1],dy[-1],0])
#         return peaks
#     
#     def gauss(xin,mu,peakheight,sigma): 
#         h=peakheight*np.sqrt(2 * np.pi)*sigma
#         gout = h/(sigma * np.sqrt(2 * np.pi)) * np.exp( - (xin - mu)**2 / (2 * sigma**2) )
#         return gout 
#     
#     # ====================================================== 
#     def peaks2gaus(xin,peaks):
#         gaussians = []
#         for g in range(len(peaks)):
#             g = gauss(ei,peaks[g][0],peaks[g][1],peaks[g][2])
#             gaussians.append(g)        
#     
#         gaussians_sum = ei*0
#         for i in range(len(peaks)):
#             gaussians_sum = gaussians_sum+gaussians[i] 
#             
#         return gaussians, gaussians_sum
#     
#     # ====================================================== 
#     def SortPeaks(peaksin):
#     
#         peaksout = peaksin.copy()
#         
#         # sort peaks    
#         peaksout = np.array(peaksout,np.float); 
#         peaksout = peaksout[peaksout[:,0].argsort()]
#         peaksout = list(peaksout)
#         #round peaks ( a better way of doing this should exist )
#         if peaksout[0][1]   > 0.01 : yround = 4
#         elif peaksout[0][1] > 0.001 : yround = 5 
#         elif peaksout[0][1] > 0.0001 : yround = 6     
#         elif peaksout[0][1] > 0.00001 : yround = 7
#         elif peaksout[0][1] > 0.000001 : yround = 8    
#         elif peaksout[0][1] > 0.0000001 : yround = 9 
#         elif peaksout[0][1] > 0.00000001 : yround = 10
#         elif peaksout[0][1] > 0.000000001 : yround = 11   
#         else : yround = 11
#             
#         peaksoutr = []
#         for i in peaksout:
#             peaksoutr.append([ round(float(i[0]),3), round(float(i[1]),yround), round(float(i[2]),2) ])
#         peaksout = peaksoutr  
#         
#         return peaksout
#     
#     # ======================================================
#     def optimize_sigmas(xin,yin,peaksin,omode):
#     
#         peaksout = peaksin.copy()    
#         
#         def optimize_sigma(xin,yin,peakin,omode):
#             sigma_range1 = np.linspace(0.1,10,10)
#             diffs = []
#             sel = (xin <= peakin[0])    
#             for i in sigma_range1:
#                 g = gauss(xin[sel],peakin[0],peakin[1],i)
#                 diff = yin[sel]-g
#                 absdiff = []
#                 for j in range(len(diff)):
#                     absdiff.append(abs(diff[j]))
#                 diffs.append([i,sum(absdiff)])        
#             diffs = np.array(diffs) 
#             diffs = diffs[diffs[:,1].argsort()]       
#             sigma_best = diffs[0][0]
#     
#             sigma_range2 = np.linspace(sigma_best*0.5,sigma_best*1.5,50)
#             diffs = []
#             mu = peakin[0]
#             if omode == 0: sel = (xin <= mu)
#             if omode == 1: sel = (xin >= (mu-sigma_best)) & (xin <= (mu+sigma_best)) 
#             if omode == 2: sel = (xin >= (mu-sigma_best/2)) & (xin <= (mu+sigma_best/2))
#             if omode == 3: sel = (xin >= (mu)) & (xin <= (mu+sigma_best))
#             if omode == 4: sel = (xin >= (mu)) & (xin <= (mu+sigma_best/2))
#             if omode == 5: sel = (xin >= (mu-2*sigma_best)) & (xin <= (mu+sigma_best/2))            
#             for i in sigma_range2:
#                 g = gauss(xin[sel],peakin[0],peakin[1],i)
#                 diff = yin[sel]-g
#                 absdiff = []
#                 for j in range(len(diff)):
#                     absdiff.append(abs(diff[j]))
#                 diffs.append([i,sum(absdiff)])        
#             diffs = np.array(diffs) 
#             diffs = diffs[diffs[:,1].argsort()] 
#             sigma_best = diffs[0][0] 
#     
#             return sigma_best    
#         
#         residue = yin
#         for i in range(len(peaksin)):
#             peaksout[i][2] = optimize_sigma(xin,residue,peaksout[i],omode=omode)
#             g = gauss(xin,peaksout[i][0],peaksout[i][1],peaksout[i][2])
#             residue = residue - g
#     
#         peaksout = SortPeaks(peaksout)          
#         return peaksout
#     
#     # ======================================================
#     def optimize_heights(xin,yin,peaksin,nnnls):
#         
#         peaksout = peaksin.copy()      
#      
#         def do_nnls(xin,yin,peaks):
#             sel = (xin <= peaks[-1][0]) 
#             A = gauss(xin[sel],peaks[0][0],peaks[0][1],peaks[0][2])
#             for i in range(1,len(peaks)):
#                 g = gauss(xin[sel],peaks[i][0],peaks[i][1],peaks[i][2])
#                 A = np.append(A,g)        
#             A = A.reshape(len(xin[sel]),len(peaks),order='F').copy()
#             b = yin[sel]    
#             out = nnls(A,b) 
#             for i in range(len(peaks)):
#                 if out[0][i] > 0.2: peaks[i][1] = peaks[i][1]*out[0][i]
#             return(peaks)
#         
#         for i in range(nnnls):
#             peaksout = do_nnls(xin,yin,peaksout)
#     
#         peaksout = SortPeaks(peaksout)          
#         return peaksout     
#     
#     
#     # ======================================================
#     def optimize_mus(xin,yin,peaksin,dx):
#         
#         peaksout = peaksin.copy()     
#         
#         def optimize_mu(xin,yin,peakin,dx):
#             mu_range1 = np.linspace(peakin[0]-dx,peakin[0]+dx,50)
#             diffs = []
#             sel = (xin <= peakin[0])    
#             for i in mu_range1:
#                 g = gauss(xin[sel],i,peakin[1],peakin[2])
#                 diff = yin[sel]-g
#                 absdiff = []
#                 for j in range(len(diff)):
#                     absdiff.append(abs(diff[j]))
#                 diffs.append([i,sum(absdiff)])        
#             diffs = np.array(diffs) 
#             diffs = diffs[diffs[:,1].argsort()]       
#             mu_best = diffs[0][0]
#             return mu_best
#     
#         residue = yin
#         for i in range(len(peaksout)):
#             peaksout[i][0] = optimize_mu(xin,residue,peaksout[i],dx)
#             g = gauss(xin,peaksout[i][0],peaksout[i][1],peaksout[i][2])
#             residue = residue - g
#              
#         peaksout = SortPeaks(peaksout)          
#         return peaksout   
#     
#     # ======================================================
#     def find_shoulders(xin,yin,peaksin,sigma,toadd=None): 
#         
#         peaksout = peaksin.copy()
#         
#         def GaussianSmooth(xin,yin,sigma):  
#             delta = xin[1]-xin[0]
#     
#             if sigma == 0: sigma = delta
#     
#             f  = InterpolatedUnivariateSpline(xin,yin)
#             xin = np.arange(min(xin), max(xin), sigma/2)
#             yin = f(xin)
#     
#             xs = xin; ys = xin*0
#             carpan1 = ( delta/( np.sqrt(2*3.14159265359) * sigma) )
#             carpan2 = (-2*sigma**2)   
#     
#             for i in range(len(xin)):
#                 for j in range(len(xin)):
#                     ys[i]=ys[i]+yin[j]*carpan1*np.exp ( ((xin[i]-xin[j])**2)/carpan2 )
#             return xs, ys    
#     
#         gaussians = []
#         for g in range(len(peaks)):
#             g = gauss(ei,peaks[g][0],peaks[g][1],peaks[g][2])
#             gaussians.append(g)        
#         gaussians_sum = ei*0
#         for i in range(len(peaks)):
#             gaussians_sum = gaussians_sum+gaussians[i]     
#         
#         xsearch = xin; ysearch = yin - gaussians_sum    
#         xsearch, ysearch = GaussianSmooth(xsearch, ysearch, sigma)        
#         shoulders = findpeaks(xsearch, ysearch)
#           
#         for i in shoulders:
#             if i[1] <= 0: shoulders.remove(i)
#         
#         shoulders = np.array(shoulders,np.float);
#         shoulders = shoulders[shoulders[:,1].argsort()]
#         
#         if toadd is None : toadd = [-1,-2]
#         
#         for i in toadd:
#             peaksout.append(list(shoulders[i]))   
#         
#         peaksout = SortPeaks(peaksout)          
#         return peaksout            
#                 
#     
#     def plot_peaks(xin,peaksin,peaksABCin):
#     
#         plt.style.use('seaborn-white')
#         fig = plt.figure(figsize=(6,5))
#         
#         gaussians, gaussians_sum = peaks2gaus(xin,peaksin)    
#     
#         ax = fig.add_subplot(1,1,1)
#         ax.plot(e,c, 'ko', ms=2, lw=0.5, alpha=1)
#         ax.plot(ei,ci, 'r-', ms=2, lw=0.5, alpha=1, label='exp. data')
#         for p in peaks:
#             ax.plot(p[0],p[1], 'bo', ms=5, lw=1.5, alpha=0.7)
#         for g in gaussians:    
#             ax.plot(ei,g,alpha=0.7)
#         ax.plot(ei,gaussians_sum, 'k:', alpha=0.7, label='sum of Gaussians')        
#         ax.set_xlim(e[0]-2,e[-1]+2)
#     
#         peaksABCin = np.array(peaksABCin,np.float)
#         gaussians, gaussians_sum = peaks2gaus(xin,peaksABCin)    
#         for g in gaussians:    
#             ax.fill(ei,g,alpha=0.7)
#             
#         ax.set_xlim(xin[0],xin[-1])    
#         ax.set_ylim(0,0.5)      
#         ax.legend(loc='best')
#         
#         return
#     
#     
#     
#     
# peaks = findpeaks(ei,ci) 
# peaks = optimize_sigmas(ei,ci,peaks,omode=5)
# peaks = optimize_heights(ei,ci,peaks,nnnls=3)
# peaks = optimize_mus(ei,ci,peaks,dx=0.2)
# peaks = find_shoulders(ei,ci,peaks,sigma=0.2,toadd=[-2]) 
# peaks = optimize_sigmas(ei,ci,peaks,omode=5)
# peaks = optimize_heights(ei,ci,peaks,nnnls=3)
# peaks = optimize_mus(ei,ci,peaks,dx=0.2)













#################################################################################################
#################################################################################################
#################################################################################################
#################################################################################################
#################################################################################################

def darrange(dx, dy, E0=None, Emax=None, gamma=None, sigma=None, bonset=None, bmethod=None):
    
    if E0 is None: E0=dx[0]
    if Emax is None: Emax=51    
    if sigma is None: sigma=0.25
    if bonset is None: bonset=0 
    if bmethod is None: bmethod=1  

    if E0+Emax > max(dx):
       Emax = max(dx)-E0 

    if E0 <= min(dx):
       E0 = min(dx) 
    
    #interpolate to 0.05
    f  = InterpolatedUnivariateSpline(dx,dy)
    xi = np.arange(E0, E0+Emax+0.1, 0.05)
    yi = f(xi)    
    
    #shift E0 to zero
    xi = xi - E0
    
    #shift y[0] to zero    
    yi = yi - yi[0]
    
    if sigma == -1: 
        xG, yG = xi, yi
    else: xG, yG = mSMOOTH.Gaussian(xi, yi, sigma)
    
    if gamma == -1: 
        xL, yL = xG, yG
    else: xL, yL = mSMOOTH.Lorentzian(xG, yG, gamma, bonset, bmethod) 
    
    xL = xL - xL[0]; yL = yL - yL[0]

    return xL, yL








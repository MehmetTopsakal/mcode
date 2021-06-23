#-*- coding: utf-8 -*-



import numpy as np 
import shutil,subprocess,os,time,pickle

from pylab import *
from matplotlib import gridspec
from matplotlib import pyplot as plt

import scipy.io as sio

from . import t4iss_defaults


import numpy as np
from scipy import interpolate
from scipy import signal
from scipy.signal import argrelextrema

from pymatgen.analysis.local_env import VoronoiNN
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer



from scipy.stats import pearsonr,spearmanr,kendalltau 
from sklearn.metrics import mean_absolute_error as mae
from sklearn.metrics import mean_squared_error as mse
from fastdtw import fastdtw
from scipy.spatial.distance import euclidean 




class mXANES:
    
    def __init__(self, evsmu=None, srange=None, sstruct=None, ca=None, E0=None, 
                 xanesid=None, source=None, vcn=None, edge=None): 

        if evsmu is None:
            self.X0 = np.array([])
            self.Y0 = np.array([])
        else:
            self.X0 = np.array(evsmu[0])
            self.Y0 = np.array(evsmu[1])

        if srange:
            sel = (self.X0 >= srange[0]) & (self.X0 <= srange[1])
            self.X0 = self.X0[sel]
            self.Y0 = self.Y0[sel]            

        # Energy offset
        if E0 is None:
            self.E0 = self.X0[0]
        else:
            self.E0 = E0
            
        # XANES id
        if xanesid is None:
            self.xanesid = 'not_set'
        else:
            self.xanesid = xanesid 
            
        # XANES edge
        if edge is None:
            self.edge = 'not_set'
        else:
            self.edge = edge 
            
        # central atom
        if ca is None:
            self.ca = 'not_set'
        else:
            self.ca = ca             
            
        # source
        if source is None:
            self.source = 'not_set'
        else:
            self.source = source            
            
        # symmetrized structure
        if sstruct is None:
            self.sstruct = [[],[]]
        else:
            self.sstruct = sstruct   
            
        # vcn holder
        if vcn is None:
            self.vcn = [[],[]]
        else:
            self.vcn = vcn  
                        
        self.peaks = []
        
            
                                
    def Interpolate(self,iterprange,stepsize=0.1):
        
        
        if self.X[0] > iterprange[0]:
            # left padding
            npts = int((self.X[0]-iterprange[0])/stepsize)+1
            x_patch = np.linspace(iterprange[0],self.X[0]-stepsize,npts)
            y_patch=np.empty(len(x_patch)); y_patch.fill(self.Y[0])
            self.X = np.concatenate((x_patch,self.X.T), axis=0)
            self.Y = np.concatenate((y_patch,self.Y.T), axis=0)
            
            
        if self.X[-1] < iterprange[1]:
            # right padding            
            npts = int((iterprange[1]-self.X[-1])/stepsize)+2
            x_patch = np.linspace(self.X[-1],iterprange[1],npts)
            y_patch=np.empty(len(x_patch)); y_patch.fill(self.Y[-1])
            self.X = np.concatenate((self.X.T,x_patch), axis=0)
            self.Y = np.concatenate((self.Y.T,y_patch), axis=0)   

          
        f = interpolate.interp1d(self.X,self.Y,kind='linear')
        self.X = np.linspace(iterprange[0],iterprange[1], int((iterprange[1]-iterprange[0])/stepsize)+1  )
        self.Y = f(self.X) 
        
        
        

    def FindPeaks(self,xin=None,yin=None,srangep=None):
        
        if (xin is None) or (yin is None):
            xsearch = self.X0
            ysearch = self.Y0
        else:
            xsearch = xin
            ysearch = yin
                        
        if srangep:
            sel = (xsearch >= srangep[0]) & (xsearch <= srangep[1])
            xsearch = xsearch[sel]; ysearch = ysearch[sel]
        
        ipeaks = argrelextrema(ysearch, np.greater)[0] 
        
        peaks = []
        for i in ipeaks:
            peaks.append([xsearch[i],ysearch[i]])
        self.peaks = peaks 
        
        return peaks
 
 
    def yscale_by(self,yscale):
        self.Y = self.Y*yscale
        
    def normalize_to(self,nstr):
        if nstr == 'max':            
            self.Y = self.Y/max(self.Y)
        elif nstr == 'tail':
            self.Y = self.Y/self.Y[-1]      
        else:
            self.Y = self.Y 
 
 
    def transform(self,srange=None,irange=None,e0shift=False,
                  y0shift=True,normalize='max',xshift=None):
        
        self.X = self.X0.copy()
        self.Y = self.Y0.copy()
        
        if e0shift:
            self.X = self.X -self.E0         
               
        if xshift:
            self.X = self.X + xshift            

        if irange:
            self.Interpolate(irange)
                  
        if y0shift:
            self.Y = self.Y -self.Y[0]  

        if normalize == 'max':            
            self.Y = self.Y/max(self.Y)
        elif normalize == 'tail':
            self.Y = self.Y/self.Y[-1]
        elif normalize == 'none':
            self.Y = self.Y         
        else:
            self.Y = self.Y/max(self.Y)
            
            
        #self.FindPeaks()        
#         self.e0 = self.X0[np.argmax(np.gradient(self.Y) / np.gradient(self.X))]






    def get_vcn(self,vcncutoff=3):
        
        if self.sstruct and self.ca:
            try:
                nnfinder = VoronoiNN(cutoff=vcncutoff,allow_pathological=True)
                vcn = nnfinder.get_cn(self.sstruct, indices[i], use_weights=True)
                self.vcn = vcn
            except:
                nnfinder = VoronoiNN(cutoff=vcncutoff*2,allow_pathological=True)                
                vcn = nnfinder.get_cn(self.sstruct[0], self.sstruct[1], use_weights=True) 
                self.vcn = vcn
        
        return self.vcn



  
  
def get_average_vcn(structure,ca,vcncutoff=3,symmetrized=False,verbose=False):
    
    if not symmetrized:
        analyzer = SpacegroupAnalyzer(structure)
        structure_sym = analyzer.get_symmetrized_structure() 
    else:
        structure_sym = structure

    species = [i[0].species_string   for i in structure_sym.equivalent_sites ]
    indices = [i[0]   for i in structure_sym.equivalent_indices ]
    weights = [len(i) for i in structure_sym.equivalent_indices]
    
    if ca not in species:
        raise ValueError("central atom is not in species list !!!")
    
    # site-specific coordination numbers by Voronoi method 
    cns = []
    for i,s in enumerate(species):
        try:
            nnfinder = VoronoiNN(cutoff=vcncutoff,allow_pathological=True)
            cn = nnfinder.get_cn(structure_sym, indices[i], use_weights=True)
            cns.append(cn)
        except:
            nnfinder = VoronoiNN(cutoff=vcncutoff*2,allow_pathological=True)
            cn = nnfinder.get_cn(structure_sym, indices[i], use_weights=True)
            cns.append(cn)        
            
    struct_info = list( zip(species,indices,weights,cns) )

    # average coordination number
    acn = []
    for i in struct_info:
        if verbose:
            print(i)
        if i[0] == ca:
            for a in range(i[2]):
                acn.append(i[3])
    avcn = sum(acn)/len(acn)
    if verbose:
        print('average '+ca+' Voronoi CN is: '+str(avcn))
        
    return avcn
    
    




















class find_candidates:
    
    def __init__(self, target_sp, search_sps, loadfrom=None, Erange=[0,50], normalize_to='tail',
                 xshifts_coarse=np.linspace(-5,5,11), xshifts_fine=np.linspace(-0.9,0.9,10)): 
        #
        if loadfrom:
            if not os.path.isfile(loadfrom):
                [optSPs_pcc,optSPs_spm,optSPs_tau,optSPs_dtw] = [[],[],[],[]]
            else:
                try:
                    [optSPs_pcc,optSPs_spm,optSPs_tau,optSPs_dtw] = pickle.load(open(loadfrom, "rb"))
                except:
                    [optSPs_pcc,optSPs_spm,optSPs_tau,optSPs_dtw] = [[],[],[],[]]
        else:
            [optSPs_pcc,optSPs_spm,optSPs_tau,optSPs_dtw] = [[],[],[],[]]
                
        self.target_sp      = target_sp
        self.search_sps     = search_sps
        self.xshifts_coarse = xshifts_coarse
        self.xshifts_fine   = xshifts_fine
        self.normalize_to   = normalize_to
        self.Erange         = Erange    
        self.optSPs_pcc     = optSPs_pcc
        self.optSPs_spm     = optSPs_spm
        self.optSPs_tau     = optSPs_tau       
        self.optSPs_dtw     = optSPs_dtw
        
    def pearson_score(self,Xin,Yin):
        return pearsonr(Xin,Yin)[0]
    def spearman_score(self,Xin,Yin):
        return spearmanr(Xin,Yin)[0]
    def kendalltau_score(self,Xin,Yin):
        return kendalltau(Xin,Yin)[0]    
    def dtw_score(self,Xin,Yin):
        return -fastdtw(Xin,Yin, dist=euclidean)[0]         
    
    def optimize(self,Erange_opt=[0,25],optDTW=False,saveto=None):         
        self.target_sp.transform(irange=Erange_opt,e0shift=True,normalize=self.normalize_to)  
        
        def getKey(item): return item[1]
        
        # PCC
        sps_opt = []
        opts = []        
        for i in self.search_sps:            
            scores = np.zeros([len(self.xshifts_coarse)])
            for x,xs in enumerate(self.xshifts_coarse):
                #transform 
                i.transform(irange=Erange_opt,e0shift=True,xshift=xs,normalize=self.normalize_to)
                # calc. score
                scores[x] = self.pearson_score(i.Y,self.target_sp.Y)
            coarse_xshift = self.xshifts_coarse[np.unravel_index(scores.argmax(), scores.shape)]            
            scores = np.zeros([len(self.xshifts_fine)])
            for x,xs in enumerate(self.xshifts_fine):
                #transform 
                i.transform(irange=Erange_opt,e0shift=True,xshift=xs+coarse_xshift,normalize=self.normalize_to)
                # calc. score
                scores[x] = self.pearson_score(i.Y,self.target_sp.Y)
            fine_xshift = coarse_xshift + self.xshifts_fine[np.unravel_index(scores.argmax(), scores.shape)]
            i.transform(irange=self.Erange,e0shift=True,xshift=fine_xshift,normalize=self.normalize_to)
            sps_opt.append([i.xanesid,max(scores),i])
            opts.append([fine_xshift,1.0])
        opts_pcc=opts
        self.optSPs_pcc = sorted(sps_opt, key=getKey, reverse=True)
        # SPM
        sps_opt = []
        opts = []        
        for i in self.search_sps:            
            scores = np.zeros([len(self.xshifts_coarse)])
            for x,xs in enumerate(self.xshifts_coarse):
                #transform 
                i.transform(irange=Erange_opt,e0shift=True,xshift=xs,normalize=self.normalize_to)
                # calc. score
                scores[x] = self.spearman_score(i.Y,self.target_sp.Y)
            coarse_xshift = self.xshifts_coarse[np.unravel_index(scores.argmax(), scores.shape)]            
            scores = np.zeros([len(self.xshifts_fine)])
            for x,xs in enumerate(self.xshifts_fine):
                #transform 
                i.transform(irange=Erange_opt,e0shift=True,xshift=xs+coarse_xshift,normalize=self.normalize_to)
                # calc. score
                scores[x] = self.spearman_score(i.Y,self.target_sp.Y)
            fine_xshift = coarse_xshift + self.xshifts_fine[np.unravel_index(scores.argmax(), scores.shape)] 
            i.transform(irange=self.Erange,e0shift=True,xshift=fine_xshift,normalize=self.normalize_to)
            sps_opt.append([i.xanesid,max(scores),i])
            opts.append([fine_xshift,1.0])
        opts_spm=opts
        self.optSPs_spm = sorted(sps_opt, key=getKey, reverse=True)    
        # TAU
        sps_opt = []
        opts = []        
        for i in self.search_sps:            
            scores = np.zeros([len(self.xshifts_coarse)])
            for x,xs in enumerate(self.xshifts_coarse):
                #transform 
                i.transform(irange=Erange_opt,e0shift=True,xshift=xs,normalize=self.normalize_to)
                # calc. score
                scores[x] = self.kendalltau_score(i.Y,self.target_sp.Y)
            coarse_xshift = self.xshifts_coarse[np.unravel_index(scores.argmax(), scores.shape)]            
            scores = np.zeros([len(self.xshifts_fine)])
            for x,xs in enumerate(self.xshifts_fine):
                #transform 
                i.transform(irange=Erange_opt,e0shift=True,xshift=xs+coarse_xshift,normalize=self.normalize_to)
                # calc. score
                scores[x] = self.kendalltau_score(i.Y,self.target_sp.Y)
            fine_xshift = coarse_xshift + self.xshifts_fine[np.unravel_index(scores.argmax(), scores.shape)] 
            i.transform(irange=self.Erange,e0shift=True,xshift=fine_xshift,normalize=self.normalize_to)
            sps_opt.append([i.xanesid,max(scores),i])
            opts.append([fine_xshift,1.0])
        opts_tau=opts
        self.optSPs_tau = sorted(sps_opt, key=getKey, reverse=True)
        
        ## DTW (initials from PCC)
        #if optDTW:
            #sps_opt = []
            #opts = [] 
            #dtw_xshifts = np.linspace(-1,1,9)
            #dtw_yscales = np.linspace(0.9,1.1,9)
            #for i,sp in enumerate(self.search_sps): 
                #scores = np.zeros([len(dtw_xshifts),len(dtw_yscales)])
                #for x,xs in enumerate(dtw_xshifts):
                    #for y,ys in enumerate(dtw_yscales):
                        #sp.transform(irange=Erange_opt,e0shift=True,xshift=xs+opts_pcc[i][0],normalize=self.normalize_to)
                        #sp.yscale_by(ys)
                        #scores[x,y] = self.dtw_score(sp.Y,self.target_sp.Y)   
                #dtw_xy = np.unravel_index(scores.argmax(), scores.shape)
                #sp.transform(irange=self.Erange,e0shift=True,xshift=dtw_xshifts[dtw_xy[0]]+opts_pcc[i][0],normalize=self.normalize_to)
##                 sp.yscale_by(dtw_yscales[dtw_xy[1]])
                #sps_opt.append([sp.xanesid,scores[dtw_xy[0],dtw_xy[1]],sp])
                #opts.append([dtw_xshifts[dtw_xy[0]]+opts_pcc[i][0],dtw_yscales[dtw_xy[1]]])
            #opts_dtw=opts
            #self.optSPs_dtw = sorted(sps_opt, key=getKey, reverse=True)
        #else:
            #opts_dtw=[]
            #self.optSPs_dtw = []
            
        #if saveto:
            #pickle.dump([self.optSPs_pcc,self.optSPs_spm,self.optSPs_tau,self.optSPs_dtw], open(saveto,'wb'))
            
            
            
        # DTW (initials from PCC)
        if optDTW:
            sps_opt = []
            opts = [] 
            dtw_xshifts = np.linspace(-1,1,9)
            dtw_yscales = np.linspace(1,1,1)
            for i,sp in enumerate(self.search_sps): 
                scores = np.zeros([len(dtw_xshifts),len(dtw_yscales)])
                for x,xs in enumerate(dtw_xshifts):
                    for y,ys in enumerate(dtw_yscales):
                        
                        
                        sp.transform(irange=Erange_opt,e0shift=True,xshift=xs+opts_pcc[i][0],normalize=self.normalize_to)
                        sp.yscale_by(ys)
                        
                        sp_scaled = (sp.Y - np.mean(sp.Y))/np.std(sp.Y)
                        target_scaled = (self.target_sp.Y - np.mean(self.target_sp.Y))/np.std(self.target_sp.Y)
                        
                        #scores[x,y] = self.dtw_score(sp.Y,self.target_sp.Y)  
                        scores[x,y] = self.dtw_score(sp_scaled,target_scaled)
                        
                        
                dtw_xy = np.unravel_index(scores.argmax(), scores.shape)
                sp.transform(irange=self.Erange,e0shift=True,xshift=dtw_xshifts[dtw_xy[0]]+opts_pcc[i][0],normalize=self.normalize_to)
#                 sp.yscale_by(dtw_yscales[dtw_xy[1]])
                sps_opt.append([sp.xanesid,scores[dtw_xy[0],dtw_xy[1]],sp])
                opts.append([dtw_xshifts[dtw_xy[0]]+opts_pcc[i][0],dtw_yscales[dtw_xy[1]]])
            opts_dtw=opts
            self.optSPs_dtw = sorted(sps_opt, key=getKey, reverse=True)
        else:
            opts_dtw=[]
            self.optSPs_dtw = []
            
        if saveto:
            pickle.dump([self.optSPs_pcc,self.optSPs_spm,self.optSPs_tau,self.optSPs_dtw], open(saveto,'wb'))            
            
            
            
            
            
            
            
            
            
            
            
            


    def plot(self,nout=10,normalize='max'):
        
        self.target_sp.transform(irange=self.Erange,e0shift=True,normalize=normalize)
        
        if self.optSPs_dtw:
            fig = plt.figure(figsize=(12,8))
            sbplt = '14'
        else:
            fig = plt.figure(figsize=(9,8))
            sbplt = '13'
            
        
        ax = fig.add_subplot(sbplt+'1')
        s = 0
        for i in self.optSPs_pcc[0:nout]:
            ax.plot(self.target_sp.X,s+self.target_sp.Y,'k:',label='unknown') 
            i[2].normalize_to(normalize)
            ax.plot(i[2].X,s+i[2].Y,lw=2)
            ax.text(i[2].X[-1]-6.5,s+i[2].Y[-1]+0.1, i[0]+'\n ('+str(round(i[1],3))+')',weight='bold', size=5, va="center", ha="left", rotation=0)  
            s -= 0.5
        ax.set_xlim([-2,self.target_sp.X[-1]+3])
        ax.set_yticks([])
        ax.set_title('metric=Pearson')  
        
        ax = fig.add_subplot(sbplt+'2')
        s = 0
        for i in self.optSPs_spm[0:nout]:
            ax.plot(self.target_sp.X,s+self.target_sp.Y,'k:',label='unknown') 
            i[2].normalize_to(normalize)
            ax.plot(i[2].X,s+i[2].Y,lw=2)
            ax.text(i[2].X[-1]-6.5,s+i[2].Y[-1]+0.1, i[0]+'\n ('+str(round(i[1],3))+')',weight='bold', size=5, va="center", ha="left", rotation=0)  
            s -= 0.5
        ax.set_xlim([-2,self.target_sp.X[-1]+3])
        ax.set_yticks([])
        ax.set_title('metric=Spearman')    
        
        ax = fig.add_subplot(sbplt+'3')
        s = 0
        for i in self.optSPs_tau[0:nout]:
            ax.plot(self.target_sp.X,s+self.target_sp.Y,'k:',label='unknown') 
            i[2].normalize_to(normalize)
            ax.plot(i[2].X,s+i[2].Y,lw=2)
            ax.text(i[2].X[-1]-6.5,s+i[2].Y[-1]+0.1, i[0]+'\n ('+str(round(i[1],3))+')',weight='bold', size=5, va="center", ha="left", rotation=0)  
            s -= 0.5
        ax.set_xlim([-2,self.target_sp.X[-1]+3])
        ax.set_yticks([])
        ax.set_title('metric=Kendall')   
        
        if self.optSPs_dtw:
            ax = fig.add_subplot(sbplt+'4')
            s = 0
            for i in self.optSPs_dtw[0:nout]:
                ax.plot(self.target_sp.X,s+self.target_sp.Y,'k:',label='unknown') 
                i[2].normalize_to(normalize)
                ax.plot(i[2].X,s+i[2].Y,lw=2)
                ax.text(i[2].X[-1]-6.5,s+i[2].Y[-1]+0.1, i[0]+'\n ('+str(round(i[1],3))+')',weight='bold', size=5, va="center", ha="left", rotation=0)  
                s -= 0.5
            ax.set_xlim([-2,self.target_sp.X[-1]+3])
            ax.set_yticks([])
            ax.set_title('metric=DTW')         
        

    

# -*- coding: iso-8859-1 -*-
# coding: utf-8

"""
This provides functions for dealing with Materials Project data
"""

__author__ = "Mehmet Topsakal"
__email__ = "metokal@gmail.com"
__status__ = "Development"
__date__ = "March 20, 2018"


import pickle,os
import numpy as np
from pylab import *
from matplotlib import gridspec
from matplotlib import pyplot as plt
from scipy.stats import pearsonr,spearmanr,kendalltau 
from fastdtw import fastdtw
from scipy.spatial.distance import euclidean 
import scipy.io as sio
from copy import deepcopy

from scipy.stats import rankdata



#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class find_candidates:
    
    def __init__(self, target_sp, search_sps, loadfrom=None, Erange=[0,50], normalize_to='tail',
                 xshifts_coarse=np.linspace(-5,5,11), xshifts_fine=np.linspace(-0.9,0.9,21)): 
        #
        if loadfrom:
            if not os.path.isfile(loadfrom):
                [optSPs_pcc,optSPs_spm,optSPs_tau,optSPs_dtw,optSPs_dtw_rank] = [[],[],[],[],[]]
            else:
                try:
                    [optSPs_pcc,optSPs_spm,optSPs_tau,optSPs_dtw,optSPs_dtw_rank] = pickle.load(open(loadfrom, "rb"))
                except:
                    [optSPs_pcc,optSPs_spm,optSPs_tau,optSPs_dtw,optSPs_dtw_rank] = [[],[],[],[],[]]
        else:
            [optSPs_pcc,optSPs_spm,optSPs_tau,optSPs_dtw,optSPs_dtw_rank] = [[],[],[],[],[]]
                
        self.target_sp       = target_sp
        self.search_sps      = search_sps
        self.xshifts_coarse  = xshifts_coarse
        self.xshifts_fine    = xshifts_fine
        self.normalize_to    = normalize_to
        self.Erange          = Erange    
        self.optSPs_pcc      = optSPs_pcc
        self.optSPs_spm      = optSPs_spm
        self.optSPs_tau      = optSPs_tau       
        self.optSPs_dtw      = optSPs_dtw
        self.optSPs_dtw_rank = optSPs_dtw_rank

        
    def pearson_score(self,Xin,Yin):
        return pearsonr(Xin,Yin)[0]
    def spearman_score(self,Xin,Yin):
        return spearmanr(Xin,Yin)[0]
    def kendalltau_score(self,Xin,Yin):
        return kendalltau(Xin,Yin)[0]    
    def dtw_score(self,Xin,Yin):
        return -fastdtw(Xin,Yin, dist=euclidean)[0]         
    
    def optimize(self,Erange_opt=[0,25],optDTW=False,saveto=None):         
        self.target_sp.transform(irange=Erange_opt,y0shift=True,x0shift=True,normalize=self.normalize_to)  
        
        def getKey(item): return item[1]
        
        # PCC
        sps_opt = []
        opts = []        
        for i in self.search_sps:            
            scores = np.zeros([len(self.xshifts_coarse)])
            for x,xs in enumerate(self.xshifts_coarse):
                #transform 
                i.transform(irange=Erange_opt,y0shift=True,x0shift=True,xshift=xs,normalize=self.normalize_to)
                # calc. score
                scores[x] = self.pearson_score(i.I,self.target_sp.I)
            coarse_xshift = self.xshifts_coarse[np.unravel_index(scores.argmax(), scores.shape)]            
            scores = np.zeros([len(self.xshifts_fine)])
            for x,xs in enumerate(self.xshifts_fine):
                #transform 
                i.transform(irange=Erange_opt,y0shift=True,x0shift=True,xshift=xs+coarse_xshift,normalize=self.normalize_to)
                # calc. score
                scores[x] = self.pearson_score(i.I,self.target_sp.I)
            fine_xshift = coarse_xshift + self.xshifts_fine[np.unravel_index(scores.argmax(), scores.shape)]
            i.transform(irange=self.Erange,y0shift=True,x0shift=True,xshift=fine_xshift,normalize=self.normalize_to)
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
                i.transform(irange=Erange_opt,y0shift=True,x0shift=True,xshift=xs,normalize=self.normalize_to)
                # calc. score
                scores[x] = self.spearman_score(i.I,self.target_sp.I)
            coarse_xshift = self.xshifts_coarse[np.unravel_index(scores.argmax(), scores.shape)]            
            scores = np.zeros([len(self.xshifts_fine)])
            for x,xs in enumerate(self.xshifts_fine):
                #transform 
                i.transform(irange=Erange_opt,y0shift=True,x0shift=True,xshift=xs+coarse_xshift,normalize=self.normalize_to)
                # calc. score
                scores[x] = self.spearman_score(i.I,self.target_sp.I)
            fine_xshift = coarse_xshift + self.xshifts_fine[np.unravel_index(scores.argmax(), scores.shape)] 
            i.transform(irange=self.Erange,y0shift=True,x0shift=True,xshift=fine_xshift,normalize=self.normalize_to)
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
                i.transform(irange=Erange_opt,y0shift=True,x0shift=True,xshift=xs,normalize=self.normalize_to)
                # calc. score
                scores[x] = self.kendalltau_score(i.I,self.target_sp.I)
            coarse_xshift = self.xshifts_coarse[np.unravel_index(scores.argmax(), scores.shape)]            
            scores = np.zeros([len(self.xshifts_fine)])
            for x,xs in enumerate(self.xshifts_fine):
                #transform 
                i.transform(irange=Erange_opt,y0shift=True,x0shift=True,xshift=xs+coarse_xshift,normalize=self.normalize_to)
                # calc. score
                scores[x] = self.kendalltau_score(i.I,self.target_sp.I)
            fine_xshift = coarse_xshift + self.xshifts_fine[np.unravel_index(scores.argmax(), scores.shape)] 
            i.transform(irange=self.Erange,y0shift=True,x0shift=True,xshift=fine_xshift,normalize=self.normalize_to)
            sps_opt.append([i.xanesid,max(scores),i])
            opts.append([fine_xshift,1.0])
        opts_tau=opts
        self.optSPs_tau = sorted(sps_opt, key=getKey, reverse=True)         


         
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
                        
                        
                        sp.transform(irange=Erange_opt,y0shift=True,x0shift=True,xshift=xs+opts_pcc[i][0],normalize=self.normalize_to)
                        sp.yscale_by(ys)
                        
                        sp_scaled = (sp.I - np.mean(sp.I))/np.std(sp.I)
                        target_scaled = (self.target_sp.I - np.mean(self.target_sp.I))/np.std(self.target_sp.I)
                        
                        #scores[x,y] = self.dtw_score(sp.I,self.target_sp.I)  
                        scores[x,y] = self.dtw_score(sp_scaled,target_scaled)
                        
                        
                dtw_xy = np.unravel_index(scores.argmax(), scores.shape)
                sp.transform(irange=self.Erange,y0shift=True,x0shift=True,xshift=dtw_xshifts[dtw_xy[0]]+opts_pcc[i][0],normalize=self.normalize_to)
#                 sp.yscale_by(dtw_yscales[dtw_xy[1]])
                sps_opt.append([sp.xanesid,scores[dtw_xy[0],dtw_xy[1]],sp])
                opts.append([dtw_xshifts[dtw_xy[0]]+opts_pcc[i][0],dtw_yscales[dtw_xy[1]]])
            opts_dtw=opts
            self.optSPs_dtw = sorted(sps_opt, key=getKey, reverse=True)
            
            
            sps_opt = []
            opts = [] 
            dtw_xshifts = np.linspace(-1,1,9)
            dtw_yscales = np.linspace(1,1,1)
            for i,sp in enumerate(self.search_sps): 
                scores = np.zeros([len(dtw_xshifts),len(dtw_yscales)])
                for x,xs in enumerate(dtw_xshifts):
                    for y,ys in enumerate(dtw_yscales):
                        
                        sp.transform(irange=Erange_opt,y0shift=True,x0shift=True,xshift=xs+opts_pcc[i][0],normalize=self.normalize_to)
                        sp.yscale_by(ys)
                        
                        sp_scaled = (sp.I - np.mean(sp.I))/np.std(sp.I)
                        target_scaled = (self.target_sp.I - np.mean(self.target_sp.I))/np.std(self.target_sp.I)
                        
                        sp_scaled = rankdata(sp_scaled); sp_scaled = sp_scaled / len(sp_scaled)                        
                        target_scaled = rankdata(target_scaled); target_scaled = target_scaled / len(target_scaled)
                        
                        #scores[x,y] = self.dtw_score(sp.I,self.target_sp.I)  
                        scores[x,y] = self.dtw_score(sp_scaled,target_scaled)
                                                
                dtw_xy = np.unravel_index(scores.argmax(), scores.shape)
                sp.transform(irange=self.Erange,y0shift=True,x0shift=True,xshift=dtw_xshifts[dtw_xy[0]]+opts_pcc[i][0],normalize=self.normalize_to)
#                 sp.yscale_by(dtw_yscales[dtw_xy[1]])
                sps_opt.append([sp.xanesid,scores[dtw_xy[0],dtw_xy[1]],sp])
                opts.append([dtw_xshifts[dtw_xy[0]]+opts_pcc[i][0],dtw_yscales[dtw_xy[1]]])
            opts_dtw=opts
            self.optSPs_dtw_rank = sorted(sps_opt, key=getKey, reverse=True)            
            
            
            
        else:
            opts_dtw=[]
            self.optSPs_dtw = []
            
        if saveto:
            pickle.dump([self.optSPs_pcc,self.optSPs_spm,self.optSPs_tau,self.optSPs_dtw], open(saveto,'wb')) 
            
            
            
    def plot(self,nout=10,normalize='max'):
        
        self.target_sp.transform(irange=self.Erange,y0shift=True,x0shift=True,normalize=normalize)
        
        if self.optSPs_dtw:
            fig = plt.figure(figsize=(15,8))
            sbplt = '15'
        else:
            fig = plt.figure(figsize=(9,8))
            sbplt = '13'
            
        
        ax = fig.add_subplot(sbplt+'1')
        s = 0
        for i in self.optSPs_pcc[0:nout]:
            ax.plot(self.target_sp.E,s+self.target_sp.I,'k-',lw=1,label='unknown') 
            i[2].normalize_to(normalize)
            ax.plot(i[2].E,s+i[2].I,lw=2,alpha=0.7)
            ax.text(i[2].E[-1]-12,s+i[2].I[-1]+0.1, i[0]+'\n ('+str(round(i[1],3))+')',weight='bold', size=7, va="center", ha="left", rotation=0)  
            s -= 0.5
        ax.set_xlim([-2,self.target_sp.E[-1]+3])
        ax.set_yticks([])
        ax.set_title('metric=Pearson')
        ax.set_ylabel('Normalized to '+normalize)
        
        ax = fig.add_subplot(sbplt+'2')
        s = 0
        for i in self.optSPs_spm[0:nout]:
            ax.plot(self.target_sp.E,s+self.target_sp.I,'k-',lw=1,label='unknown') 
            i[2].normalize_to(normalize)
            ax.plot(i[2].E,s+i[2].I,lw=2,alpha=0.7)
            ax.text(i[2].E[-1]-12,s+i[2].I[-1]+0.1, i[0]+'\n ('+str(round(i[1],3))+')',weight='bold', size=7, va="center", ha="left", rotation=0)  
            s -= 0.5
        ax.set_xlim([-2,self.target_sp.E[-1]+3])
        ax.set_yticks([])
        ax.set_title('metric=Spearman')    
        
        ax = fig.add_subplot(sbplt+'3')
        s = 0
        for i in self.optSPs_tau[0:nout]:
            ax.plot(self.target_sp.E,s+self.target_sp.I,'k-',lw=1,label='unknown') 
            i[2].normalize_to(normalize)
            ax.plot(i[2].E,s+i[2].I,lw=2,alpha=0.7)
            ax.text(i[2].E[-1]-12,s+i[2].I[-1]+0.1, i[0]+'\n ('+str(round(i[1],3))+')',weight='bold', size=7, va="center", ha="left", rotation=0)  
            s -= 0.5
        ax.set_xlim([-2,self.target_sp.E[-1]+3])
        ax.set_yticks([])
        ax.set_title('metric=Kendall')   


        
        if self.optSPs_dtw:
            ax = fig.add_subplot(sbplt+'4')
            s = 0
            for i in self.optSPs_dtw[0:nout]:
                ax.plot(self.target_sp.E,s+self.target_sp.I,'k-',lw=1,label='unknown') 
                i[2].normalize_to(normalize)
                ax.plot(i[2].E,s+i[2].I,lw=2,alpha=0.7)
                ax.text(i[2].E[-1]-12,s+i[2].I[-1]+0.1, i[0]+'\n ('+str(round(i[1],3))+')',weight='bold', size=7, va="center", ha="left", rotation=0)  
                s -= 0.5
            ax.set_xlim([-2,self.target_sp.E[-1]+3])
            ax.set_yticks([])
            ax.set_title('metric=DTW')
            

            ax = fig.add_subplot(sbplt+'5')
            s = 0
            for i in self.optSPs_dtw_rank[0:nout]:
                ax.plot(self.target_sp.E,s+self.target_sp.I,'k-',lw=1,label='unknown') 
                i[2].normalize_to(normalize)
                ax.plot(i[2].E,s+i[2].I,lw=2,alpha=0.7)
                ax.text(i[2].E[-1]-12,s+i[2].I[-1]+0.1, i[0]+'\n ('+str(round(i[1],3))+')',weight='bold', size=7, va="center", ha="left", rotation=0)  
                s -= 0.5
            ax.set_xlim([-2,self.target_sp.E[-1]+3])
            ax.set_yticks([])
            ax.set_title('metric=DTWrank')            
               
            

# imports here
import os,pickle,sys,fnmatch,shutil
import yaml

#import tifffile
#import skbeam
import numpy as np

import warnings
warnings.filterwarnings('ignore')

#from pyFAI.azimuthalIntegrator import AzimuthalIntegrator
#import skbeam

#from xpdtools.tools import overlay_mask

import time


#import matplotlib
#matplotlib.use('Agg') # 

import matplotlib.pyplot as plt
from matplotlib import gridspec


#from sklearn.preprocessing import StandardScaler 
#from sklearn.decomposition import PCA, IncrementalPCA
from numpy import linalg as LA
from scipy.stats import rankdata
from scipy import interpolate
#from sklearn.cluster import DBSCAN
from scipy.stats import pearsonr, spearmanr, kendalltau
from scipy.stats import rankdata
import glob

from pathlib import Path

from copy import deepcopy


import gzip
import os



class TIFF:
    def __init__(self,filename=None,
                 root_folder=None,
                 sample_name=None,
                 date_time='na',
                 dx=None,
                 dy=None,    
                 meta_id='na',
                 ind=None,
                 tiff_ext='.tiff',
                 
                 load_now=True,
                 read_1d=True,read_2d=True,
                 load_1d=True,load_2d=True,  
                 
                 save_npz = False
                 ):
                 
        if root_folder is None:
            self.root_folder = os.getcwd()
        else:
            self.root_folder = root_folder
            
        self.sample_name = sample_name    
        self.date_time = date_time
        self.dx = dx
        self.dy = dy
        self.meta_id = meta_id
        self.ind = ind
        self.tiff_ext = tiff_ext
        self.save_npz = save_npz
 
        if not filename:
            if dx and dy:
                self.filename = '{:s}_{:s}_dx_{:.3f}mm_dy_{:.3f}mm_{:s}_{:04d}'.\
                    format(sample_name,date_time,dx,dy,meta_id,ind)
            elif dx and not dy:
                self.filename = '{:s}_{:s}_dx_{:.3f}mm_{:s}_{:04d}'.\
                    format(sample_name,date_time,dx,meta_id,ind)
            elif not dx and dy:
                self.filename = '{:s}_{:s}_dy_{:.3f}mm_{:s}_{:04d}'.\
                    format(sample_name,date_time,dy,meta_id,ind)
            else:
                self.filename = '{:s}_{:s}_{:s}_{:04d}'.\
                    format(sample_name,date_time,meta_id,ind) 
        else:
            if filename.endswith('_dark_corrected_img'+self.tiff_ext):
                self.filename = filename[:-len(self.tiff_ext)-19]
                self.abs_path = os.path.join(self.root_folder,self.sample_name,'dark_sub',self.filename+'_dark_corrected_img'+self.tiff_ext)
            elif filename.endswith(self.tiff_ext):
                self.filename = filename[:-len(self.tiff_ext)]
                self.abs_path = os.path.join(self.root_folder,self.sample_name,'dark_sub',self.filename+self.tiff_ext)
            else:
                self.filename = filename
                self.abs_path = filename
        
        
        self.Q = []
        self.I = []
        self.F = []
        self.S = []
        self.R = []
        self.G = []
        self.meta_yaml = []
        self.mask = []
        self.raw  = []
        
        self.read_1d  = read_1d
        self.read_2d  = read_2d       
        
        if load_now:
            self.load()

    def read(self,read_1d=True,read_2d=True):
        
            meta_yaml = os.path.join(self.root_folder,self.sample_name,'meta',self.sample_name+'_'+self.date_time+'_'+self.meta_id+'.yaml')
            if os.path.isfile(meta_yaml):
                self.meta_yaml = yaml.load(open(meta_yaml)) 
                if self.meta_yaml['bt_wavelength']:
                    self.wl = self.meta_yaml['bt_wavelength']
            
            if self.read_1d:
                               
                fq_file = os.path.join(self.root_folder,self.sample_name,'fq',self.filename+'.fq')
                if os.path.isfile(fq_file):
                    fq = np.loadtxt(fq_file,unpack=True,comments=['#','\''], usecols=(0,1))
                    self.Q_fq = fq[0]; self.F = fq[1]                
                sq_file = os.path.join(self.root_folder,self.sample_name,'sq',self.filename+'.sq')
                if os.path.isfile(sq_file):
                    sq = np.loadtxt(sq_file,unpack=True,comments=['#','\''], usecols=(0,1))
                    self.Q_sq = sq[0]; self.S = sq[1]   
                gr_file = os.path.join(self.root_folder,self.sample_name,'pdf',self.filename+'.gr')
                if os.path.isfile(gr_file):
                    gr = np.loadtxt(gr_file,unpack=True,comments=['#','\''], usecols=(0,1))
                    self.R = gr[0]; self.G = gr[1]    
                    
                chi_file = os.path.join(self.root_folder,self.sample_name,'iq',self.filename+'.chi')
                if os.path.isfile(chi_file):
                    chi = np.loadtxt(chi_file,unpack=True,comments=['#','\''], usecols=(0,1), skiprows=8)
                    self.Q = chi[0]; self.I = chi[1] 
                    if self.wl:
                        pre_factor = self.wl / (4 * np.pi)
                        self.TTH = np.rad2deg( 2 * np.arcsin( self.Q * pre_factor) ) 
                        
                chi_file = os.path.join(self.root_folder,self.sample_name,'integration',self.filename+'_mean_q.chi')
                if os.path.isfile(chi_file):
                    chi = np.loadtxt(chi_file,unpack=True,comments=['#','\''], usecols=(0,1), skiprows=8)
                    self.Q = chi[0]; self.I = chi[1] 
                tth_file = os.path.join(self.root_folder,self.sample_name,'integration',self.filename+'_mean_tth.chi')
                if os.path.isfile(tth_file):
                    tth = np.loadtxt(tth_file,unpack=True,comments=['#','\''], usecols=(0,1), skiprows=8)
                    self.Q = tth[0]; self.I = tth[1] 
                    
                print(self.Q)
                        
                        
                        
            if self.read_2d:
                import imageio # no need to install imageio if we won't deal with tiff files
                tiff_file = os.path.join(self.root_folder,self.sample_name,'dark_sub',self.filename+self.tiff_ext)
                mask_file = os.path.join(self.root_folder,self.sample_name,'mask',self.filename+'.npy')
                if os.path.isfile(tiff_file):
                    self.raw = imageio.imread(tiff_file)
                if os.path.isfile(mask_file):
                    self.mask = np.load(mask_file)
                    
    def save(self,save_to=None,save_2d=True):
        
        if not save_2d:
            self.raw  = []            
            self.mask = []

        if save_to is None:
            f = os.path.join(self.root_folder,self.sample_name,'dark_sub',self.filename+'.pklz')
        else:
            f = save_to
        p = gzip.open(f,'wb')   
        pickle.dump(self.__dict__, p , 2)
        p.close()
                
    def load(self,load_from=None,load_2d=True):
        
        if load_from is None:
            f = os.path.join(self.root_folder,self.sample_name,'dark_sub',self.filename+'.pklz')
        else:
            f = load_from
            
        if os.path.isfile(f):    
            p = gzip.open(f,'rb')
            tmp_dict = pickle.load(p)
            p.close()
            self.__dict__.update(tmp_dict)
        else:
            self.read()
            if self.save_npz:
                self.save()
            
        if not load_2d:
            self.raw  = []            
            self.mask = []  


    def q_interp(self, qin=None, qrange=None, dq=0.001):

        if isinstance(qin,np.ndarray): 

            self.Qi, self.Ii = self.Q, self.I   

            # left padding
            if min(self.Q) > min(qin):

                self.Qi = [min(qin)]
                for i in self.Q:
                    self.Qi.append(i)
                self.Qi = np.array(self.Qi)  
                  
                self.Ii = [self.I[np.argmin(self.Q)]]
                for i in self.I:
                    self.Ii.append(i)
                self.Ii = np.array(self.Ii)

            # right padding
            if max(self.Q) < max(qin):

                self.Qi = []
                for i in self.Q:
                    self.Qi.append(i)
                self.Qi.append(max(qin))
                self.Qi = np.array(self.Qi)  
                  
                self.Ii = []
                for i in self.I:
                    self.Ii.append(i)
                self.Ii.append(self.I[np.argmax(self.Q)])
                self.Ii = np.array(self.Ii)

            f = interpolate.interp1d(self.Qi, self.Ii, kind='linear')
            self.Qi = qin
            self.Ii = f(qin)


        elif qrange:

            self.Qi, self.Ii = self.Q, self.I   

            # left padding
            if min(self.Q) > qrange[0]:

                self.Qi = [qrange[0]]
                for i in self.Q:
                    self.Qi.append(i)
                self.Qi = np.array(self.Qi)  
                  
                self.Ii = [self.I[np.argmin(self.Q)]]
                for i in self.I:
                    self.Ii.append(i)
                self.Ii = np.array(self.Ii)

            # right padding
            if max(self.Q) < qrange[1]:

                self.Qi = []
                for i in self.Q:
                    self.Qi.append(i)
                self.Qi.append(qrange[1])
                self.Qi = np.array(self.Qi)  
                  
                self.Ii = []
                for i in self.I:
                    self.Ii.append(i)
                self.Ii.append(self.I[np.argmax(self.Q)])
                self.Ii = np.array(self.Ii)

            f = interpolate.interp1d(self.Qi, self.Ii, kind='linear')
            self.Qi = np.linspace(qrange[0], qrange[1],int((qrange[1]-qrange[0])/dq)+1)
            self.Ii = f(self.Qi)







#
class SAMPLE:
    
    def __init__(self,sample_name=None,root_folder=None,read_2d=True,
                 load_now=False,load_from=None,meta_id=None,save_npz=False):
        
        self.sample_name = sample_name
            
        if root_folder is None:
            self.root_folder = os.getcwd()
        else:
            self.root_folder = root_folder
            
        if load_now:
            self.load(load_from=None,meta_id=None)
            
        self.save_npz=save_npz

    def read(self,meta_id=None,tiff_ext='.tiff',read_2d=False,load_2d=False):         
        
        self.meta_ids = []
        for file in os.listdir(os.path.join(self.root_folder, self.sample_name, 'meta')):
            if fnmatch.fnmatch(file, '*.yaml'):
                meta_yaml = yaml.load(open(os.path.join(self.root_folder, self.sample_name, 'meta',file)))
                timestamp_in_yaml = meta_yaml['time']
                self.meta_ids.append([file.split('_')[-1][-11:-5],timestamp_in_yaml])
        self.meta_ids.sort(key=lambda x: x[1])
        self.meta_ids = [i[0] for i in self.meta_ids]
                  
        tiffs = []
        for file in os.listdir(os.path.join(self.root_folder, self.sample_name, 'dark_sub')):
            if fnmatch.fnmatch(file, '*'+tiff_ext):
                tiffs.append(file)                

        if isinstance(meta_id, int):
            meta_id = self.meta_ids[meta_id]
              
        tiffs_cls = []
        for i in tiffs:

            filename = i
            date_time   = i.split(self.sample_name)[1].split('_')[1]
            timestamp   = int(time.mktime(time.strptime(date_time, '%Y%m%d-%H%M%S')))

            if i.split('_')[-2] == 'corrected':
                dx_dy_positions = i[0:-24].split(date_time)[1].split('_')[1:-2]
                meta_id = i.split('_')[-5]
                ind = int(i.split('_')[-4])
            else:
                dx_dy_positions = i[0:-5].split(date_time)[1].split('_')[1:-2]   
                meta_id = i.split('_')[-2]
                ind = int(i.split('_')[-1])

            if dx_dy_positions:
                if len(dx_dy_positions) == 4:
                    dx = float(dx_dy_positions[1].split('mm')[0]) 
                    dy = float(dx_dy_positions[3].split('mm')[0])
                elif dx_dy_positions[0] == 'dx':
                    dx = float(dx_dy_positions[1].split('mm')[0])
                    dy = None
                elif dx_dy_positions[0] == 'dy':
                    dy = float(dx_dy_positions[1].split('mm')[0])
                    dx = None 
            else:
                dx = None
                dy = None


            t = TIFF(filename=filename,
                     root_folder=self.root_folder,
                     sample_name=self.sample_name,
                     date_time=date_time,
                     dx=dx,
                     dy=dy,    
                     meta_id=meta_id,
                     ind=ind,
                     tiff_ext=tiff_ext,
                     load_now = True,
                     read_2d=read_2d,
                     load_2d=load_2d,                 
                     )

            tiffs_cls.append([t,timestamp])      
        tiffs_cls.sort(key=lambda x: x[1])
        self.tiffs = [i[0] for i in tiffs_cls]


    def load(self,load_from=None,meta_id=None):
        if load_from is None:
            if self.sample_name:
                f = os.path.join(self.root_folder,self.sample_name,'saved.pklz')
            else:
                f = 'saved.pklz'
        else:
            f = load_from
        if os.path.isfile(f):    
            p = gzip.open(f,'rb')
            tmp_dict = pickle.load(p)
            p.close()
            self.__dict__.update(tmp_dict)
            
            if isinstance(meta_id, int):
                meta_id = self.meta_ids[meta_id] 
                
            if meta_id:
                if meta_id in self.meta_ids:
                    new_tiffs = []
                    for i in self.tiffs:
                        if i.meta_id == meta_id:
                            new_tiffs.append(i)
                    self.tiffs = new_tiffs
                else:
                    print(meta_id+' is not available\Returning all tiffs.')
        else:
            try:
                self.read()
                if self.save_npz:
                    self.save()
            except Exception as exc:
                print('Error: \n Unable to read. Something is wrong...')
                print(exc)
                

    def save(self,save_to=None):
        if save_to is None:
            f = os.path.join(self.root_folder,self.sample_name,'saved.pklz')
        else:
            f = save_to
            print('saving to '+save_to)
        p = gzip.open(f,'wb')    
        pickle.dump(self.__dict__, p , 2)
        p.close()
        
        
    def cleanup(self,to_clean_arr,overwrite=False):
        self.tiffs_clean = []
        for i in range(len(self.tiffs)):
            if i not in to_clean_arr:
                self.tiffs_clean.append(self.tiffs[i])
        if overwrite:
            self.tiffs = self.tiffs_clean
        

        
    def plot(self,plot_type=None,q_range=(0.5,7.5),q_range_metric=(1,6),
             y_bottom=0.1,y_logscale=True,export_fig=False,
             figsize=(12,6),numbers_on=False,text_xyshift=0.1,axin=None):
            
        if plot_type=='2d-scan': 
                        
            fig, axes = plt.subplots(1,2,figsize=figsize)
            
            ax = axes[0]
            min_intensities = []
            for i in self.tiffs:
                sel = (i.Q > q_range[0]) & (i.Q < q_range[1])
                ax.plot(i.Q,i.I)
                min_intensities.append(min(i.I[sel]))
            ax.set_xlim(q_range[0],q_range[1])    
            ax.set_ylim(bottom=max(y_bottom,min(min_intensities)))
            
            if y_logscale:
                ax.set_yscale('log')
            ax.set_xlabel(u'Q ($\AA^{-1}$)', fontsize=14, weight='bold')
            ax.set_ylabel(u'Intensity', fontsize=14, weight='bold')
            ax.set_title('{:s}'.format(self.sample_name), fontsize=15) 
            
            ax = axes[1]
            metrics = []
            dxdys = []
            for c,i in enumerate(self.tiffs):
                sel = (i.Q > q_range_metric[0]) & (i.Q < q_range_metric[1])
                metrics.append(pearsonr( i.I[sel], self.tiffs[0].I[sel] )[0])
                dxdys.append([i.dx,i.dy])
                if numbers_on:
                    ax.text(text_xyshift+i.dx,text_xyshift+i.dy,str(c),fontsize=10,alpha=0.7)
                
            dxdys = np.array(dxdys)
            metrics = np.array(metrics)
            metrics = metrics-np.mean(metrics)
            ax.scatter(dxdys[:,0],dxdys[:,1],c=metrics,cmap='jet',s=200)  
            ax.set_xlabel('dx (mm)', fontsize=14, weight='bold')
            ax.set_ylabel('dy (mm)', fontsize=14, weight='bold')             

            plt.tight_layout()
            return [fig,axes]
            
        elif plot_type=='1d-scan' or plot_type=='rotation': 
            
            from matplotlib import gridspec
            
            fig = plt.figure(figsize=figsize)
            gs = gridspec.GridSpec(1, 2, width_ratios=[2,1] )    

            ax = fig.add_subplot(gs[0])
            dxs = []
            dys = []
            metrics = []
            max_intensities = []
            min_intensities = []
            indexes = []
            
            for c,i in enumerate(self.tiffs):
                if i.dx:
                    dxs.append(i.dx)
                    sel = (i.Q > q_range_metric[0]) & (i.Q < q_range_metric[1])
                    #metrics.append(pearsonr( i.I[sel], self.tiffs[-1].I[sel] )[0])
                    metrics.append(spearmanr( i.I[sel], self.tiffs[-1].I[sel] )[0])                    
                    max_intensities.append(max(i.I[sel]))
                    min_intensities.append(min(i.I[sel]))
                    indexes.append(c)
                elif i.dy:
                    dys.append(i.dy)
                    sel = (i.Q > q_range_metric[0]) & (i.Q < q_range_metric[1])
                    #metrics.append(pearsonr( i.I[sel], self.tiffs[-1].I[sel] )[0])
                    metrics.append(spearmanr( i.I[sel], self.tiffs[-1].I[sel] )[0])                    
                    max_intensities.append(max(i.I[sel]))
                    min_intensities.append(min(i.I[sel]))
                    indexes.append(c)                    
            metrics = np.array(metrics)
            import matplotlib.cm as cm
            mcolors = cm.rainbow(metrics)
            
            
            for c,i in enumerate(self.tiffs):
                ax.plot(i.Q,i.I)          
            ax.set_ylim(bottom=max(y_bottom,0.9*min(min_intensities)))
            if q_range:
                ax.set_xlim([q_range[0],q_range[1]])         
            if y_logscale:
                ax.set_yscale('log')
            ax.set_xlabel(u'Q ($\AA^{-1}$)', fontsize=14, weight='bold')
            ax.set_ylabel(u'Intensity', fontsize=14, weight='bold') 
            dxs = np.array(dxs); dys = np.array(dys) 
            max_intensities = np.array(max_intensities)
            
            ax1 = ax
            ax = fig.add_subplot(gs[1])
            if dxs.any():
                ax.bar(dxs,height=max_intensities,width=0.2,color=mcolors)  
                ax.set_xlabel('dx (mm)', fontsize=14, weight='bold')
                if numbers_on:
                    for i in indexes:
                        ax.text(self.tiffs[i].dx,max_intensities[i]*1.02,str(i),fontsize=10,weight='bold')          
            elif dys.any():
                ax.bar(dys,height=max_intensities,width=0.2,color=mcolors)  
                ax.set_xlabel('dy (mm)', fontsize=14, weight='bold') 
                if numbers_on:
                    for i in indexes:
                        ax.text(self.tiffs[i].dy,max_intensities[i]*1.02,str(i),fontsize=10,weight='bold')                  
            ax.set_yscale('log')
            ax.set_ylabel(u'Max intensity', fontsize=14, weight='bold')
            ax.set_title('{:s}'.format(self.sample_name), fontsize=12)     
            ax2 = ax 
            
            axes = [ax1,ax2]  
            plt.tight_layout()  
            return [fig,axes]
            
        elif plot_type=='XRD&PDF': 
            
            fig, axes = plt.subplots(1,3,figsize=figsize)
            
            sel = (self.tiffs[0].Q > q_range[0]) & (self.tiffs[0].Q < q_range[1])
            for i in self.tiffs:
                axes[0].plot(i.Q,i.I)
            axes[0].set_xlabel(u'Q ($\AA^{-1}$)', fontsize=14, weight='bold')
            axes[0].set_ylabel(u'Intensity', fontsize=14, weight='bold')
            
            sel = (self.tiffs[0].Q_sq > q_range[0]) & (self.tiffs[0].Q_sq < q_range[1])
            for i in self.tiffs:
                axes[1].plot(i.Q_sq,i.S)
            axes[1].set_ylabel(u'S (Q)', fontsize=14, weight='bold')
            axes[1].set_xlabel(u'Q ($\AA^{-1}$)', fontsize=14, weight='bold')                               

            for i in self.tiffs:
                axes[2].plot(i.R,i.G)  
            axes[2].set_xlabel(u'r ($\AA$)', fontsize=14, weight='bold')
            axes[2].set_ylabel(u'G(r)', fontsize=14, weight='bold')
            
            if y_logscale:
                axes[0].set_yscale('log')
                
            plt.tight_layout()          

            return [fig,axes]

        else: 
            if axin:
                axes = axin
                fig = None
            else:
                fig, axes = plt.subplots(1,1,figsize=figsize)
            if len(self.tiffs) == 1:
                sel = (self.tiffs[0].Q > q_range[0]) & (self.tiffs[0].Q < q_range[1])
                axes.plot(self.tiffs[0].Q,self.tiffs[0].I)
                axes.set_xlim(q_range[0],q_range[1])                    
                axes.set_ylim(bottom=max(y_bottom,min(self.tiffs[0].I)))                
            else:
                min_intensities = []
                for i in self.tiffs:
                    sel = (i.Q > q_range[0]) & (i.Q < q_range[1])
                    axes.plot(i.Q,i.I)
                    min_intensities.append(min(i.I[sel]))
                axes.set_xlim(q_range[0],q_range[1])    
                axes.set_ylim(bottom=max(y_bottom,min(min_intensities)))  
            if y_logscale:
                axes.set_yscale('log')
            axes.set_xlabel(u'Q ($\AA^{-1}$)', fontsize=14, weight='bold')
            axes.set_ylabel(u'Intensity', fontsize=14, weight='bold')
            axes.set_title('{:s}'.format(self.sample_name), fontsize=12)       
            plt.tight_layout()  
            return [fig,axes]





    def average(self,indexes,q_range=(0.5,7.5),y_bottom=0.1,
                y_logscale=True,figsize=(12,6),yshift=50,y_max=None,
                export_csv=False,export_chi=False,wl=None):

        fig, axes = plt.subplots(1,2,figsize=figsize)
        
        ax = axes[0]        
        I_ave = 0*self.tiffs[indexes[0]].I
        Q_ave = self.tiffs[indexes[0]].Q        
        for i in indexes:
            ax.plot(self.tiffs[i].Q,self.tiffs[i].I,alpha=0.8,label=str(i))
            I_ave += self.tiffs[i].I
        I_ave = I_ave/len(indexes)
        if len(indexes) > 1:
            ax.plot(Q_ave,I_ave,'k:',alpha=0.7,label='average')
        ax.legend(fontsize=10,ncol=max(1,int(len(indexes)/2)))
        ax.set_xlim(q_range[0],q_range[1])                    
        ax.set_ylim(bottom=max(y_bottom,min(self.tiffs[0].I)))   
        ax.set_xlabel(u'Q ($\AA^{-1}$)', fontsize=14, weight='bold')
        ax.set_ylabel(u'Intensity', fontsize=14, weight='bold')        

        if y_logscale:
            ax.set_yscale('log')
            
        ax = axes[1]
        shift = 0
        for i in indexes:
            ax.plot(self.tiffs[i].Q,shift+self.tiffs[i].I,alpha=0.8)
            shift += yshift
        if len(indexes) > 1:
            ax.plot(Q_ave,-yshift+I_ave,'k:',alpha=0.8,label='average') 
        ax.set_xlim(q_range[0],q_range[1])  
        
        if y_max:
            ax.set_ylim(bottom=max(y_bottom,min(self.tiffs[indexes[0]].I))-yshift,top=y_max) 
        ax.set_xlabel(u'Q ($\AA^{-1}$)', fontsize=14, weight='bold')         
            
        plt.tight_layout() 
        ave = np.column_stack( (Q_ave, I_ave) )
        if export_csv:
            np.savetxt('average.csv', ave, delimiter=',')

            
        if export_chi:
            out = np.column_stack( (Q_ave, I_ave) )
            np.savetxt('average.chi', out, delimiter=' ')            
        if wl:
            # tth = np.rad2deg(skbeam.core.utils.q_to_twotheta(Q_ave, wl))
            pre_factor = wl / (4 * np.pi)
            tth = np.rad2deg( 2 * np.arcsin(Q_ave * pre_factor) )  
            
            out = np.column_stack( (tth, I_ave) )
            np.savetxt('average.xy', out, delimiter=' ')            
            
            
            
            
            
        return [fig,axes,ave]
    
    
    
    
    
    
    
    
    
# topas automation stuff here    
def write_xy(smpl,ind,wl,tiff_bg,bgscale,save_to=os.getcwd()):
    
    from skbeam.core.utils import q_to_twotheta
    tiff_bg.q_interp(qin=smpl.tiffs[ind].Q)
    
    Q, I = smpl.tiffs[ind].Q, smpl.tiffs[ind].I-bgscale*tiff_bg.Ii
    TTH = np.rad2deg(q_to_twotheta(Q,wl))
    
    out = np.column_stack( (TTH,I ) )
    np.savetxt(os.path.join(save_to,smpl.tiffs[ind].filename.split('/')[-1]+'.xy'), out, delimiter=' ')
    
    return [TTH,I]

def write_inp(smpl,ind,wl,save_to=os.getcwd()):
    
    xyfile = smpl.tiffs[ind].filename.split('/')[-1]+'.xy'

    f=open(os.path.join(save_to,smpl.tiffs[ind].filename.split('/')[-1]+'.inp'),"w+")  
    f.write("""
r_exp  23.169676 r_exp_dash  45.8793749 r_wp  11.301856 r_wp_dash  22.3793414 r_p  8.52307273 r_p_dash  23.4616632 weighted_Durbin_Watson  0.360683884 gof  0.487786537
iters 100000
do_errors
xdd "%(xyfile)s"
    r_exp  23.169676 r_exp_dash  45.8793749 r_wp  11.301856 r_wp_dash  22.3793414 r_p  8.52307273 r_p_dash  23.4616632 weighted_Durbin_Watson  0.360683884 gof  0.487786537
    x_calculation_step 0.002
    range 1
    bkg @  11.7056269`_0.0495132686  2.99137558`_0.0798722926 -1.75073253`_0.07532075  0.740034659`_0.0732614746  0.27492922`_0.0700315145 -0.378864895`_0.0679030194  0.113033711`_0.0660782348  0.0815393622`_0.0667017504  0.505631902`_0.062303958  1.122974`_0.0634920618
    start_X  2.5
    finish_X  15
    LP_Factor( 90)
    Rp 217.5
    Rs 217.5
    lam
        ymin_on_ymax  0.001
        la  1 lo  %(wl).5f lh  0.1
    hkl_Is 
        lebail  1
        hkl_m_d_th2 1 1 1 8  2.054194     5.11767      I  4.42477
        hkl_m_d_th2 2 0 0 6  1.778984     5.91003      I  2.31580
        hkl_m_d_th2 2 2 0 12  1.257932     8.36176      I  5.61486
        hkl_m_d_th2 3 1 1 24  1.072768     9.80831      I  12.62934
        hkl_m_d_th2 2 2 2 8  1.027097     10.24558     I  6.82321
        hkl_m_d_th2 4 0 0 6  0.889492     11.83586     I  1.23060
        hkl_m_d_th2 3 3 1 24  0.816254     12.90215     I  19.03299
        hkl_m_d_th2 4 2 0 24  0.795586     13.23881     I  7.34270
        hkl_m_d_th2 4 2 2 24  0.726267     14.50888     I  9.05854
        LVol_FWHM_CS_G_L( 1, 24.32394`_0.33591, 0.89, 34.00508`_0.46960,,,@, 38.20796`_0.52764)
        TCHZ_Peak_Type(, 0.043745,, 0.002665796,, 0.0004827216,, 0,, 0.01274415,, 0.002455547)
        r_bragg  1.05293318
        phase_MAC  0
        phase_name "Fm3m"
        space_group "Fm-3m"
        scale @  0.0080581142`_4.611e-005
        MVW( 0.000, 45.041`_0.002, 0.000`_0.000)
        Cubic(@  3.557968`_0.000058)
  
""" % vars())
    f.close()    

    
from subprocess import call
def run_topas(start_dir,filename,topas_dir='C:\\TOPAS6\\'):
    os.chdir(topas_dir)
    call('./TC' + ' ' + '"'+ start_dir + '\\' + filename + '"') 
    os.chdir(start_dir)
    
    
def plot_outs(outs):    
    fig = plt.figure(figsize=(8,4))
    ax = fig.add_subplot('111')
    for i in outs:
        ax.plot(i[0],i[1])
    ax.set_yscale('log')
    ax.set_ylim(bottom=1)
    ax.set_xlim([0,15])    
    plt.tight_layout()
    ax.set_xlabel(u'Two theta ($^{o}$)', fontsize=14, weight='bold')
    ax.set_ylabel(u'Intensity', fontsize=14, weight='bold')
    
    
def get_xy_and_lattice(filename):
    xy = np.loadtxt(filename+'.xy',unpack=True)
    f = open(filename+'.out','r')
    for line in f:
        if line.startswith('        Cubic'):
            return [xy,float(line.split()[1][0:6])]
        

def plot_xy_and_lattice(xys,cs,startfrom=0,stopfrom=None,title=None):
    fig = plt.figure(figsize=(8,4))
    ax = fig.add_subplot('121')

    for i in xys[startfrom:stopfrom]:
        ax.plot(i[0],i[1])
    ax.set_yscale('log')
    ax.set_ylim(bottom=1)
    ax.set_xlim([2.5,15])    
    ax.set_xlabel(u'Two theta ($^{o}$)', fontsize=14, weight='bold')
    ax.set_ylabel(u'Intensity', fontsize=14, weight='bold') 
    if title:
        ax.set_title(title,fontsize=15, weight='bold') 

    ax = fig.add_subplot('122')

    ax.plot(cs[startfrom:stopfrom],'-o',ms=2)
    ax.set_xlabel(u'Scan index', fontsize=14, weight='bold')
    ax.set_ylabel(u'Fm3m lattice constant', fontsize=14, weight='bold') 

    plt.tight_layout()
        
    
    
    
    
    
    
    
    


######################################################################################################################
######################################################################################################################
######################################################################################################################
######################################################################################################################
######################################################################################################################
######################################################################################################################
######################################################################################################################
######################################################################################################################
######################################################################################################################
######################################################################################################################
######################################################################################################################
######################################################################################################################
######################################################################################################################
######################################################################################################################
######################################################################################################################
######################################################################################################################
######################################################################################################################
######################################################################################################################
######################################################################################################################
######################################################################################################################
######################################################################################################################
######################################################################################################################
######################################################################################################################
######################################################################################################################
######################################################################################################################
######################################################################################################################
######################################################################################################################
######################################################################################################################
######################################################################################################################
######################################################################################################################
######################################################################################################################
######################################################################################################################
######################################################################################################################
######################################################################################################################
######################################################################################################################
######################################################################################################################








#
class TIFF_old:
    
    def __init__(self,tiff_path,sample_name=None,exp_path=None,meta_id=None,filename=None,
                 ext=None,ind=None,date=None,other_info=None, load_raw=True,
                 mask_dir='mask',load_mask=True,
                 chi_dir='iq',load_chi=True,
                 wl=None,bg_tiff=None,meta_dir='meta',poni=None):
        
        if wl is None:
            self.wl = wl
        else:
            self.wl = []
            
        if bg_tiff is None:
            self.bg_tiff = bg_tiff
        else:
            self.bg_tiff = []            
            
        self.tiff_path = tiff_path
        self.sample_name = sample_name
        

        if filename is None:
            self.filename = Path(tiff_path).name
        if exp_path is None:
            self.exp_path = tiff_path.split(self.filename)[0]
        if ext is None:
            self.ext = Path(tiff_path).suffix
        if ind is None:
            self.ind = tiff_path.split('_')[-1][0:-5]
        if meta_id is None:
            self.meta_id = tiff_path.split('_')[-2]
            
        if date is None:
            if sample_name:
                self.date   = self.filename.split(sample_name)[1].split('_')[1]
                self.timestamp = int(time.mktime(time.strptime(self.date, '%Y%m%d-%H%M%S')))
                self.other_info = tiff_path.split(self.date)[1].split('_')[1:-2]
            else:
                self.date = 'na'
                self.timestamp = 'na'
                self.other_info = 'na'   
        else:
            self.date = date
            self.timestamp = int(time.mktime(time.strptime(self.date, '%Y%m%d-%H%M%S')))
            self.other_info = other_info              
                
        if load_raw:
            self.raw = tifffile.imread(tiff_path)
        else:
            self.raw = []
            
        if load_mask:
            if os.path.isfile(os.path.join(self.exp_path,'..',mask_dir,self.filename.split(self.ext)[0]+'_mask.npy')):
                self.mask = np.load(os.path.join(self.exp_path,'..',mask_dir,self.filename.split(self.ext)[0]+'_mask.npy'))
            else:
                self.mask = []
        else:
            self.mask = []            
            
        if poni is None:
            if os.path.isfile(os.path.join(self.exp_path,'..',meta_dir,self.sample_name+'_'+self.meta_id+'.poni')):
                self.poni = os.path.join(self.exp_path,'..',meta_dir,self.sample_name+'_'+self.meta_id+'.poni')
                f = open(self.poni,'r')
                for line in f:
                    if line.startswith('Wavelength:'):
                        self.wl = float(line.split()[1])*10000000000                
            elif os.path.isfile(os.path.join(self.exp_path,'..',meta_dir,self.sample_name+'_'+self.meta_id+'.yaml')):
                try:
                    ai = AzimuthalIntegrator()
                    meta = yaml.load(open(os.path.join(self.exp_path,'..',meta_dir,self.sample_name+'_'+self.meta_id+'.yaml')))
                    ai.setPyFAI(**meta['calibration_md'])
                    ai.save(os.path.join(self.exp_path,'..',meta_dir,self.sample_name+'_'+self.meta_id+'.poni')) ## NOTE: doesn't overwrite
                    self.poni = os.path.join(self.exp_path,'..',meta_dir,self.sample_name+'_'+self.meta_id+'.poni')
                    self.wl = meta['calibration_md']['wavelength']*10000000000
                except:
                    self.poni = 'na'
                    self.wl = None
                    
            else:
                self.poni = 'na'
        else:
            self.poni = poni
            f = open(self.poni,'r')
            for line in f:
                if line.startswith('Wavelength:'):
                    self.wl = float(line.split()[1])*10000000000  
                    
                    
        if load_chi:
            if os.path.isfile(os.path.join(self.exp_path,'..',chi_dir,self.filename.split(self.ext)[0]+'.chi')):
                chi = np.loadtxt(os.path.join(self.exp_path,'..',chi_dir,self.filename.split(self.ext)[0]+'.chi'),
                                       unpack=True,comments=['#','\''], usecols=(0,1), skiprows=8)
                self.Q = chi[0]
                self.I = chi[1]
                if self.wl:
                    self.tth = np.rad2deg(skbeam.core.utils.q_to_twotheta(self.Q,self.wl))
            else:
                self.Q = []
                self.I = []
                self.tth = []
        else:
            self.Q = []
            self.I = []
            self.tth = [] 
            
            
            
        
            
            
            
    def integrate(self,edge=20,pol=0.99,alpha=2.5,auto_type='median',
                  mask_settings='auto',mask_file=None,
                  bg_tiff=None,lower_thresh=None,
                  clean_up=True,overwrite=True,
                  load_raw=True,load_chi=True,load_mask=True):
        
        try:
            del xpdtools_processtiff
        except:
            pass
        
        from xpdtools.cli.process_tiff import main as xpdtools_processtiff
        
        
        omain = xpdtools_processtiff(image_files=self.tiff_path, poni_file=self.poni, bg_file=bg_tiff,
             mask_file=mask_file, polarization=pol, edge=edge, lower_thresh=lower_thresh,
             alpha=alpha, auto_type=auto_type, mask_settings=mask_settings) 
        
        if load_raw:
            self.raw = tifffile.imread(self.tiff_path)            
            
        if load_chi:
            self.Q = omain[0][0]
            self.I = omain[1][0]       
            self.tth = np.rad2deg(skbeam.core.utils.q_to_twotheta(self.Q, self.wl))
            
        if load_mask:
            self.mask = np.load(os.path.join(self.exp_path,self.filename.split(self.ext)[0]+'_mask.npy'))    

        if overwrite:
            shutil.copyfile(os.path.join(self.exp_path,self.filename.split(self.ext)[0]+'.chi'), 
                            os.path.join(self.exp_path,'..','iq',self.filename.split(self.ext)[0]+'.chi'))
            shutil.copyfile(os.path.join(self.exp_path,self.filename.split(self.ext)[0]+'.msk'), 
                            os.path.join(self.exp_path,'..','mask',self.filename.split(self.ext)[0]+'.msk')) 
            shutil.copyfile(os.path.join(self.exp_path,self.filename.split(self.ext)[0]+'_mask.npy'), 
                            os.path.join(self.exp_path,'..','mask',self.filename.split(self.ext)[0]+'_mask.npy'))            
            
        if clean_up:
            for c in ['_mask.npy','.msk','.chi','_median.chi','_std.chi','_zscore.tif']:
                os.remove(os.path.join(self.exp_path,self.filename.split(self.ext)[0]+c)) \
                if os.path.exists(os.path.join(self.exp_path,self.filename.split(self.ext)[0]+c)) else None 
                
        self.integration_params = {
            'image_files':self.tiff_path,
            'poni_file':self.poni,
            'bg_file':bg_tiff,
            'mask_file':mask_file, 
            'polarization':pol,
            'edge':edge,
            'lower_thresh':lower_thresh,
            'alpha':alpha,
            'auto_type':auto_type,
            'mask_settings':mask_settings,
            'clean_up':clean_up,
            'overwrite':overwrite}
        
        
    def q_interp(self, qrange=None, dq=0.001):
        from scipy import interpolate
        # left padding
        if self.Q[0] > qrange[0]:
            npts = int((self.Q[0]-qrange[0])/dq)+1
            x_patch = np.linspace(qrange[0], self.I[0]-dq, npts)
            y_patch = np.empty(len(x_patch))
            y_patch.fill(self.I[0])
            self.Qi = np.concatenate((x_patch, self.Q.T), axis=0)
            self.Ii = np.concatenate((y_patch, self.I.T), axis=0)
        else:
            self.Qi, self.Ii = self.Q, self.I

        # right padding
        if self.Q[-1] < qrange[1]:
            npts = int((qrange[1]-self.Q[-1])/dq)+2
            x_patch = np.linspace(self.Q[-1], qrange[1], npts)
            y_patch = np.empty(len(x_patch))
            y_patch.fill(self.I[-1])
            self.Qi = np.concatenate((self.Q.T, x_patch), axis=0)
            self.Ii = np.concatenate((self.I.T, y_patch), axis=0)
        else:
            self.Qi, self.Ii = self.Q, self.I            

        f = interpolate.interp1d(self.Q, self.I, kind='linear')
        self.Qi = np.linspace(qrange[0], qrange[1],
                             int((qrange[1]-qrange[0])/dq)+1)
        self.Ii = f(self.Qi)  
        self.tthi = np.rad2deg(skbeam.core.utils.q_to_twotheta(self.Qi, self.wl))        
        
   
        
    def plot(self,vmax=100,mode=0,limits=[[],[]],logscale=[False,True],other_info_as_label=False):
        if isinstance(self.Q,np.ndarray):
            fig = plt.figure(figsize=(8,6))
            gs1 = gridspec.GridSpec(2, 3, width_ratios=[1,1,1], height_ratios=[1,1] )
            gs1.update(top=0.95, bottom=0.07, left=0.05, right=0.95, wspace=0.05, hspace=0.05)
            gs2 = gridspec.GridSpec(2, 1, width_ratios=[1], height_ratios=[1,1] )
            gs2.update(top=0.95, bottom=0.09, left=0.05, right=0.95, wspace=0.05, hspace=0.05)             
        else:
            fig = plt.figure(figsize=(8,3))
            gs1 = gridspec.GridSpec(1, 3, width_ratios=[1,1,1], height_ratios=[1] )
            gs1.update(top=0.92, bottom=0.07, left=0.05, right=0.95, wspace=0.05, hspace=0.05)        
        
        if isinstance(self.raw,np.ndarray):
            ax = fig.add_subplot(gs1[0])
        
        
        if isinstance(self.mask,np.ndarray): 
            if self.bg_tiff:
                bg_npy  = tifffile.imread(self.bg_tiff)
                ax.imshow(self.raw-bg_npy, vmin=0,vmax=vmax,cmap='viridis')
                ax.set_xticklabels([]); ax.set_yticklabels([])
                ax.set_title('data (background subs.)')
                ax = fig.add_subplot(gs1[1])
                ax.imshow(self.mask,cmap='gray')
                ax.set_xticklabels([]); ax.set_yticklabels([])
                ax.set_title('mask')                
                ax = fig.add_subplot(gs1[2])
                overlay = overlay_mask(self.raw-bg_npy, self.mask)
                ax.imshow(overlay, vmin=0,vmax=vmax,cmap='viridis')
                ax.set_xticklabels([]); ax.set_yticklabels([])
                ax.set_title('masked data')  
            else:
                ax.imshow(self.raw, vmin=0,vmax=vmax,cmap='viridis')
                ax.set_xticklabels([]); ax.set_yticklabels([])
                ax.set_title('data')
                ax = fig.add_subplot(gs1[1])
                ax.imshow(self.mask,cmap='gray',vmax=1)
                ax.set_xticklabels([]); ax.set_yticklabels([])
                ax.set_title('mask')                 
                ax = fig.add_subplot(gs1[2])
                overlay = overlay_mask(self.raw, self.mask)
                ax.imshow(overlay, vmin=0,vmax=vmax,cmap='viridis')
                ax.set_xticklabels([]); ax.set_yticklabels([])
                ax.set_title('masked data') 
        else:
            if isinstance(self.raw,np.ndarray):
                ax.imshow(self.raw, vmin=0,vmax=vmax,cmap='viridis')
                ax.set_xticklabels([]); ax.set_yticklabels([])
                ax.set_title('data')                
        
        if isinstance(self.Q,np.ndarray):  
            ax = fig.add_subplot(gs2[1])
            
            if mode == 0:
                if isinstance(self.tth,np.ndarray):
                    ax.plot(self.tth,self.I,'-k',lw=2)
                    ax.set_xlabel(u'2$\Theta$ ($^o$)', fontsize=10, weight='bold')
                else:
                    ax.plot(self.Q,self.I,'-k',lw=2)
                    ax.set_xlabel(u'Q ($\AA^{-1}$)', fontsize=10, weight='bold')
                    
            if mode == 1: 
                ax.plot(self.Q,self.I,'-k',lw=2)                
                ax.set_xlabel(u'Q ($\AA^{-1}$)', fontsize=10, weight='bold')                    
                
            if other_info_as_label:
                plt.figtext(0.50, 0.45, self.other_info,fontsize=15, bbox=None)
                
            if logscale[0]:
                ax.set_xscale('log')
            if logscale[1]:
                ax.set_yscale('log')  
            if limits[0]:
                ax.set_xlim(limits[0])
            if limits[1]:
                ax.set_ylim(limits[1])   
            
            ax.set_yticklabels([])        
        

        
#
class SAMPLE_old:
    
    def __init__(self,sample_name, root_folder=None, load_now=True):
        
        self.sample_name = sample_name
        
        if root_folder is None:
            self.root_folder = os.getcwd()
        else:
            self.root_folder = root_folder
            
        if load_now:
            self.load()

    def read(self,meta_id=None,tiff_ext='.tiff',load_raw=False,load_chi=True,load_mask=False):
        
        self.meta_ids = []
        for file in os.listdir(os.path.join(self.root_folder, self.sample_name, 'meta')):
            if fnmatch.fnmatch(file, '*.yaml'):
                self.meta_ids.append(file.split('_')[-1][-11:-5]) 
        
        if meta_id:
            tiffs = []
            for file in os.listdir(os.path.join(self.root_folder, self.sample_name, 'dark_sub')):
                if fnmatch.fnmatch(file, '*'+tiff_ext):
                    tiffs.append(file)
            tiffs_cls = []
            for i in tiffs:
                t = TIFF_old(os.path.join(self.root_folder,self.sample_name,'dark_sub',i),self.sample_name,
                        load_raw=load_raw,load_chi=load_chi,load_mask=load_mask,poni=None)
                if t.meta_id == meta_id:
                    tiffs_cls.append([t,t.timestamp])  
            tiffs_cls.sort(key=lambda x: x[1])
            self.tiffs = [i[0] for i in tiffs_cls]
        else:
            tiffs = []
            for file in os.listdir(os.path.join(self.root_folder, self.sample_name, 'dark_sub')):
                if fnmatch.fnmatch(file, '*'+tiff_ext):
                    tiffs.append(file)
            tiffs_cls = []
            for i in tiffs:
                t = TIFF_old(os.path.join(self.root_folder,self.sample_name,'dark_sub',i),self.sample_name,
                        load_raw=load_raw,load_chi=load_chi,load_mask=load_mask,poni=None)
                tiffs_cls.append([t,t.timestamp])  
            tiffs_cls.sort(key=lambda x: x[1])
            self.tiffs = [i[0] for i in tiffs_cls]            
            
    
    def load(self,load_from=None):
        if load_from is None:
            f = os.path.join(self.root_folder,self.sample_name,'saved.pkl')
        else:
            f = load_from
        if os.path.isfile(f):    
            p = open(f, 'rb')
            tmp_dict = pickle.load(p)
            p.close()
            self.__dict__.update(tmp_dict)
        else:
            self.read()
            self.save()

    def save(self,save_to=None):
        if save_to is None:
            f = os.path.join(self.root_folder,self.sample_name,'saved.pkl')
        else:
            f = save_to
        p = open(f, 'wb')    
        pickle.dump(self.__dict__, p , 2)
        p.close()
        
    def integrate(self,edge=20,pol=0.99,alpha=2.5,auto_type='median',
              mask_settings='auto',mask_file=None,
              bg_tiff=None,lower_thresh=None,
              clean_up=True,overwrite=True,
              load_raw=False,load_chi=True,load_mask=False):
        for i in self.tiffs:
            print('integrating '+i.filename)
            i.integrate(edge=edge,pol=pol,alpha=alpha,auto_type=auto_type,
                        mask_settings=mask_settings,mask_file=mask_file,
                        bg_tiff=bg_tiff,lower_thresh=lower_thresh,
                        clean_up=clean_up,overwrite=overwrite,
                        load_raw=load_raw,load_chi=load_chi,load_mask=load_mask)
        
    def plot(self,meta_id=None,limits=[None,None],logscale=[False,True],export_fig=True,
             do_pca=True, pca_qrange=[1,6],
             do_dbscan=True,dbscan_params={'eps':0.05,'min_samples':20,'n_jobs':1}):

        if meta_id is None:
            meta_id = self.meta_ids[0]
            
        if isinstance(meta_id, int):
            meta_id = self.meta_ids[meta_id]
            
        if do_pca:
            fig = plt.figure(figsize=(8,8))
            ax1 = fig.add_subplot('221')
            ax2 = fig.add_subplot('222')
            ax3 = fig.add_subplot('223') 
            ax4 = fig.add_subplot('224')             
        else:
            fig = plt.figure(figsize=(8,4))
            ax1 = fig.add_subplot('121')
            ax2 = fig.add_subplot('122')            

        
        ax = ax1
        for i in self.tiffs:
            if i.meta_id == meta_id:
                ax.plot(i.Q,i.I)
                
        if do_pca:
            if limits[1]:
                ax.plot([pca_qrange[0],pca_qrange[0]],[limits[1][0],limits[1][1]], ':k', lw=0.5, alpha=0.5)
                ax.plot([pca_qrange[1],pca_qrange[1]],[limits[1][0],limits[1][1]], ':k', lw=0.5, alpha=0.5)
            else:
                ax.plot([pca_qrange[0],pca_qrange[0]],[min(i.I),max(i.I)], ':k', lw=0.5, alpha=0.5)
                ax.plot([pca_qrange[1],pca_qrange[1]],[min(i.I),max(i.I)], ':k', lw=0.5, alpha=0.5)                
        
        ax.set_ylim(bottom=1)
        if limits[0]:
            ax.set_xlim(limits[0])
        if limits[1]:
            ax.set_ylim(limits[1])           
        if logscale[0]:        
            ax.set_xscale('log')        
        if logscale[1]:        
            ax.set_yscale('log')         
        ax.set_xlabel(u'Q ($\AA^{-1}$)', fontsize=10, weight='bold')
        ax.set_ylabel(u'Intensity', fontsize=10, weight='bold') 
        
        ax = ax2
        for i in self.tiffs:
            if i.meta_id == meta_id:
                r = rankdata(i.I, method='average')
                ax.plot(i.Q,r/len(r))
        if limits[0]:
            ax.set_xlim(limits[0])
        if logscale[0]:        
            ax.set_xscale('log')        
        
        ax.set_xlabel(u'Q ($\AA^{-1}$)', fontsize=10, weight='bold')
        ax.set_yticks([])
        ax.set_ylabel(u'Rank', fontsize=10, weight='bold')
        
        
        if do_pca:
            
            for_PCA_i = []
            for_PCA_r = []
            for i in self.tiffs:
                if i.meta_id == meta_id:
                    sel = (i.Q > pca_qrange[0]) & (i.Q < pca_qrange[1])
                    for_PCA_i.append(i.I[sel])
                    for_PCA_r.append(rankdata(i.I[sel], method='average'))
                    
            pca = PCA(n_components=2)  
            Xi = pca.fit_transform(np.array(for_PCA_i))
            Xr = pca.fit_transform(np.array(for_PCA_r))
            
            if do_dbscan:
                dbs = DBSCAN(dbscan_params['eps'], min_samples=dbscan_params['min_samples'], 
                             metric=lambda i, j: 1 - spearmanr(i, j)[0], n_jobs=dbscan_params['n_jobs'])
                labels_i = dbs.fit_predict(np.array(for_PCA_i))
                labels_r = dbs.fit_predict(np.array(for_PCA_r))
            else:
                labels_i = np.zeros(len(for_PCA_i))
                labels_r = np.zeros(len(for_PCA_r))
            
            ax = ax3
            im = ax.scatter(Xi[:,0],Xi[:,1], alpha=0.7, c=labels_i, marker='o', s=30, edgecolor='k', cmap='jet')
            ax.set_xticks([]); ax.set_yticks([])
            ax.set_xlabel('Principal Component 1', fontsize=10, weight='bold')
            ax.set_ylabel('Principal Component 2', fontsize=10, weight='bold')
            ax = ax4
            im = ax.scatter(Xr[:,0],Xr[:,1], alpha=0.7, c=labels_r, marker='s', s=30, edgecolor='k', cmap='jet')
            ax.set_xticks([]); ax.set_yticks([])
            ax.set_xlabel('Principal Component 1', fontsize=10, weight='bold')
            ax.set_ylabel('Principal Component 2', fontsize=10, weight='bold')           
        
        plt.tight_layout()
        
        if export_fig:
            plt.savefig(os.path.join(self.root_folder,self.sample_name,meta_id+'.pdf'))

        


#
def find_sample_from_2dscan(I_arr, xy_arr, Q_arr=None, 
        eps=0.05, min_samples=None, n_jobs=1,
        b_ratio_thres=0.4, qrange=(1,5), use_unclustered=True):
    """Find sample positions from xy-scan 
    
    Parameters
    ----------
    xy_arr : x,y of scan points
    I_arr : Intensities for each scan point
    Q_arr : Q-points (optional)
    
    See DBSCAN documentation:
    http://scikit-learn.org/stable/modules/generated/sklearn.cluster.DBSCAN.html
    
    eps: The maximum distance between two samples for them to 
      be considered as in the same neighborhood.
      
    min_samples: The number of samples (or total weight) 
      in a neighborhood for a point to be considered as a core point. 
      This includes the point itself.
      
    n_jobs: The number of parallel jobs to run. None means 1 
      unless in a joblib.parallel_backend context. 
      -1 means using all processors.  
    
    b_ratio_thres: Clusters more than this threshold will be 
    condidered as background (not belonging to sample).

    use_unclustered: Sometimes DBSCAN is unable to classify 
    points around sample boundary. It that case, it gives -1.
    If this keyword is True, that point is considered in the 
    sample positions (pts).

    
    Returns
    -------
    center : ndarray
        xy coordinates of the center of the sample
    pts : ndarray
        xy coordinates of points considered within the sample
    
    """
    
    if isinstance(Q_arr,np.ndarray):
        # Trim to selected Q range. Because we do not want mess around 
        # beam stopper and high q. This also speedups DBSCAN calculation
        sel = (Q_arr > qrange[0]) & (Q_arr < qrange[1])            
        I_arr = np.array([i[sel] for i in I_arr])
    else:
        print('Q array is not provided. Using all points')
        
         
    # Use DBSCAN package to cluster I_arr
    if min_samples is None:
        min_samples = int(0.5*b_ratio_thres*len(I_arr))
        
    dbs   = DBSCAN(eps, min_samples=min_samples,
                metric=lambda i, j: 1 - spearmanr(i, j)[0], n_jobs=n_jobs)
    preds = dbs.fit_predict(np.array(I_arr))
    uniques, counts = np.unique(preds, return_counts=True)
    ratios = counts / sum(counts)

    # Collect x,y data for determining points which should correspond to the sample.
    clustered_pts   = []
    unclustered_pts = []
    bkg_pts         = []
    sample_pts      = []

    for j,u in enumerate(uniques):
        
        mask = (preds == u)        
        masked = []
        for i,tf in enumerate(mask):
            if tf:
                masked.append([xy_arr[i],i])
        if u == -1:
            unclustered_pts.extend(masked)
            if use_unclustered:
                sample_pts.extend(masked)
        else:
            if (ratios[j] <= b_ratio_thres):
                sample_pts.extend(masked)
                clustered_pts.append(masked)
            else:
                bkg_pts.extend(masked)
    
    if sample_pts:
        center = np.mean(np.array(sample_pts)[:,0], axis=0) 
    else:
        print('Unable to find center of sample!')
        center = None

    pts = [clustered_pts,unclustered_pts,bkg_pts]
    return center, pts





# new modules
from sklearn.cluster import DBSCAN
from scipy.stats import spearmanr

def center_finder(smpl,meta_id=None,eps=0.05, min_samples=None, n_jobs=1,
        b_ratio_thres=0.4, qrange=(1,5), use_unclustered=True, plot=True,
        good_bkg_TIFF_old=None,last_cut=20,
        exportfig=True):  
    
    if meta_id is None:    
        meta_id = smpl.meta_ids[0]  
        
    if isinstance(meta_id, int):
        meta_id = smpl.meta_ids[meta_id]        
        
        
    # collect data
    xy_arr = []
    I_arr  = []
    Q_arr  = []
     
    tiffs = []
    for i in smpl.tiffs:
        if i.meta_id == meta_id:
            tiffs.append(i)
            sel = (i.Q > qrange[0]) & (i.Q < qrange[1])
            Q_arr = i.Q[sel] # assuming Q_arr is same for all spectra
            I_arr.append(i.I[sel])
            xy_arr.append([float(i.other_info[1][0:-2]),float(i.other_info[3][0:-2])])         
    I_arr = np.array(I_arr)        
    xy_arr= np.array(xy_arr)             
                 
    center, pts = find_sample_from_2dscan(I_arr, xy_arr,
        Q_arr=Q_arr, eps=eps, min_samples=min_samples, n_jobs=n_jobs, 
        b_ratio_thres=b_ratio_thres, qrange=qrange, use_unclustered=use_unclustered)
    
    # sort pts by their distance to the center
    [clustered_pts,unclustered_pts,bkg_pts] = pts
    if isinstance(center,np.ndarray):
        # sort unclustered_pts and bkg_pts by their distance to center
        unclustered_pts = [[i[0],i[1],np.linalg.norm(i[0]-center)] for j,i in enumerate(unclustered_pts)]
        unclustered_pts = sorted(unclustered_pts, key=lambda i: i[2])
        bkg_pts = [[i[0],i[1],np.linalg.norm(i[0]-center)] for j,i in enumerate(bkg_pts)]
        bkg_pts = sorted(bkg_pts, key=lambda i: i[2])
        
        # combine and sort clustered_pts
        clustered_pts_combined = []
        for c in clustered_pts:
            clustered_pts_combined.extend([[i[0],i[1],np.linalg.norm(i[0]-center)] for j,i in enumerate(c)])
        if use_unclustered:
            clustered_pts_combined.extend([[i[0],i[1],np.linalg.norm(i[0]-center)] for j,i in enumerate(unclustered_pts)])
        clustered_pts_combined = sorted(clustered_pts_combined, key=lambda i: i[2])
            
        pts = [clustered_pts,clustered_pts_combined,unclustered_pts,bkg_pts] 
        
        
        if  good_bkg_TIFF_old and bkg_pts:
            ref = deepcopy(good_bkg_TIFF_old)
            ref.q_interp(qrange=(1,8))
            
            bkgs_far = []
            for i in bkg_pts[-4:]:
                tmp = tiffs[i[1]]
                tmp.q_interp(qrange=(1,8))
                bkgs_far.append(tmp.Ii)
            bkgs_far = np.mean(np.array(bkgs_far),axis=0)
            
            comp_sp = spearmanr(ref.Ii,bkgs_far)[0]
            comp_pe = pearsonr(ref.Ii,bkgs_far)[0]
            
            correlations = [comp_sp,comp_pe]
            
        else:
            correlations = []
            

    if plot:
        
        colors = ['k','r','g','b','m','c','y']
        
        if isinstance(center,np.ndarray):
            fig = plt.figure(figsize=(8,4))
            ax1 = fig.add_subplot('121')
            ax2 = fig.add_subplot('222')
            ax3 = fig.add_subplot('224')
        else:
            fig = plt.figure(figsize=(4,4))
            ax1 = fig.add_subplot('111')            
        # grid points
        for i in xy_arr:
            ax1.plot(i[0],i[1],'k+', alpha=0.5, ms=5)      
        # unclustered
        for i in pts[2]:
            ax1.plot(i[0][0],i[0][1],'kd', alpha=0.7, ms=8) 
        # clustered
        for c,i in enumerate(pts[0]):
            for j in i:
                ax1.plot(j[0][0],j[0][1],'C'+str(c+5)+'d', alpha=0.9, ms=15) 
                
        if isinstance(center,np.ndarray):
            ax1.plot(center[0],center[1],'y*', alpha=1, ms=11)
            # 
            for e,p in enumerate(clustered_pts_combined):
                if p[2] < 0.6:
                    ax1.plot(p[0][0],p[0][1],colors[e]+'s', alpha=1, ms=5)
                    ax2.plot(tiffs[p[1]].Q,tiffs[p[1]].I,colors[e]+'-')
                    
            for e,b in enumerate(bkg_pts[-4-last_cut:-last_cut]):    
                ax1.plot(b[0][0],b[0][1],colors[e]+'o', alpha=1, ms=5)
                ax3.plot(tiffs[b[1]].Q,tiffs[b[1]].I,colors[e]+'-')
            
            #ax2.set_ylim(bottom=1)
            
            #ax2.set_yscale('log')
            ax2.set_xticklabels([])

            #ax3.set_ylim(bottom=1)
            #ax3.set_yscale('log')            
            
                
            ax1.set_xlabel('dx (mm)', fontsize=10, weight='bold')
            ax1.set_ylabel('dy (mm)', fontsize=10, weight='bold')  
        
            ax1.set_title('{:s} ({:s}) center @ \'dx={:5.2f}mm,dy={:5.2f}mm\''
                         .format(smpl.sample_name,meta_id,center[0],center[1]), fontsize=7)
            
            ax3.set_xlabel(u'Q ($\AA^{-1}$)', fontsize=8, weight='bold')
            
            if correlations:
                if correlations[0] < 0.95:
                    ax3.set_title('Spearman\'s r corr.={:.3f}; Pearson\'s corr.={:.3f}'.
                                  format(correlations[0],correlations[1]),
                                  color='r', weight='bold',fontsize=8)
                else:
                    ax3.set_title('Spearman\'s r corr.={:.3f}; Pearson\'s corr.={:.3f}'.
                                  format(correlations[0],correlations[1]),
                                  color='k',fontsize=8)                    
                    
            
            

        else:
                
            ax1.set_xlabel('dx (mm)', fontsize=10, weight='bold')
            ax1.set_ylabel('dy (mm)', fontsize=10, weight='bold')  
            ax1.set_title('{:s}             Unable to find center!'
                         .format(smpl.sample_name), fontsize=8)


        if exportfig:
            plt.savefig(os.path.join(smpl.root_folder,smpl.sample_name,smpl.sample_name+'.'+meta_id+'.pdf'))         

        plt.tight_layout() 

    return center, pts, tiffs, correlations




    
    
    
    

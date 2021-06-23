import numpy as np
import os,pickle,sys,fnmatch,shutil,yaml
from os.path import join
from pathlib import Path
from copy import deepcopy
import time,json
import imageio 
import traceback
from scipy.stats import rankdata
from scipy import interpolate
from scipy.stats import pearsonr, spearmanr, kendalltau
from scipy.stats import rankdata


import matplotlib.pyplot as plt

import matplotlib.pyplot as plt
from matplotlib import gridspec
plt.rcParams.update({'figure.max_open_warning': 0})
plt.rc('text', usetex=False) 







        

def plot_smpl(smpl,meta_id=None,q_range=(0.5,7.5),q_range_metric=(1,6),
         y_bottom=0.1,y_logscale=True,export_fig=False,markersize=150,
         figsize=(12,6),numbers_on=False,text_xyshift=-0.1,axin=None,
         legend=False,legend_fontsize=5,
         log_y=False,log_x=False,y_shift=0,
         motor1=None,motor2=None):
    


    meta_ids = [[i.info['meta_id'],i.info['timestamp']] for i in smpl.tiffs]
    meta_ids.sort(key=lambda x: x[1])
    meta_ids = [i[0] for i in meta_ids]
    meta_ids = list(set(meta_ids))
    
    if meta_id is None:
        meta_id = meta_ids[-1]
    elif isinstance(meta_id, int):
        meta_id = meta_ids[meta_id]
        
    temp_tiffs = []
    for i in smpl.tiffs:
        if isinstance(i.info['temp'], float):
            if i.info['meta_id'] == meta_id:
                temp_tiffs.append([i,i.info['ind']])
    temp_tiffs.sort(key=lambda x: x[1], reverse=True)
    temp_tiffs = [i[0] for i in temp_tiffs]  

    
    gridscan_tiffs = []
    for i in smpl.tiffs:
        if i.info['pos1'] and i.info['pos2']:
            if i.info['meta_id'] == meta_id:
                gridscan_tiffs.append([i,i.info['ind']])
    gridscan_tiffs.sort(key=lambda x: x[1])
    gridscan_tiffs = [i[0] for i in gridscan_tiffs]
            

    linescan_tiffs = []
    for i in smpl.tiffs:
        if i.info['pos1'] and not i.info['pos2']:
            if i.info['meta_id'] == meta_id:
                linescan_tiffs.append([i,i.info['ind']])            
        elif i.info['pos2'] and not i.info['pos1']:
            if i.info['meta_id'] == meta_id:
                linescan_tiffs.append([i,i.info['ind']])             
    linescan_tiffs.sort(key=lambda x: x[1])        
    linescan_tiffs = [i[0] for i in linescan_tiffs]            




    if gridscan_tiffs:
        
        fig = plt.figure(figsize=figsize)

        ax = fig.add_subplot('143')
        
        min_intensities = []
        for i in gridscan_tiffs:
            sel = (i.iq[0] > q_range[0]) & (i.iq[0] < q_range[1])
            ax.plot(i.iq[0],i.iq[1])
            min_intensities.append(min(i.iq[1][sel]))
        ax.set_xlim(q_range[0],q_range[1])    
        ax.set_ylim(bottom=max(y_bottom,min(min_intensities)))

        if y_logscale:
            ax.set_yscale('log')
        ax.set_xlabel(u'Q ($\AA^{-1}$)', fontsize=14, weight='bold')
        ax.set_ylabel(u'Intensity', fontsize=14, weight='bold')

        ax = fig.add_subplot('121')
        
        metrics = []
        pos1dys = []
        for c,i in enumerate(gridscan_tiffs):
            sel = (i.iq[0] > q_range_metric[0]) & (i.iq[0] < q_range_metric[1])
            metrics.append(pearsonr( i.iq[1][sel], gridscan_tiffs[0].iq[1][sel] )[0])
            pos1dys.append([i.info['pos1'],i.info['pos2']])
            if numbers_on:
                ax.text(text_xyshift+i.info['pos1'],text_xyshift+i.info['pos2'],str(c),color='y',fontsize=5,alpha=0.9)

        pos1dys = np.array(pos1dys)
        metrics = np.array(metrics)
        metrics = metrics-np.mean(metrics)
        ax.scatter(pos1dys[:,0],pos1dys[:,1],marker='+',s=20)  
        ax.scatter(pos1dys[:,0],pos1dys[:,1],c=metrics,marker='s',cmap='jet',s=markersize,alpha=0.7)          
        ax.set_xlabel('%s (mm)'%(motor1), fontsize=14, weight='bold')
        ax.set_ylabel('%s (mm)'%(motor2), fontsize=14, weight='bold') 
        ax.set_title('{:s} (meta_id={:s})'.format(smpl.samplename,i.info['meta_id']), fontsize=13) 
        
        ax.set_aspect('equal', 'box')

        plt.tight_layout()
        
        if export_fig:
            plt.savefig( join(smpl.samplepath,'grid_scan.pdf') )
            
        return gridscan_tiffs







    elif temp_tiffs:
        
        fig = plt.figure(figsize=figsize)

        ax = fig.add_subplot('121')
        
        indexes = []
        metrics = []
        temps = []
        for e,i in enumerate(temp_tiffs):
            sel = (i.iq[0] > q_range[0]) & (i.iq[0] < q_range[1])
            ax.plot(i.iq[0],i.iq[1])
            metrics.append(spearmanr( i.iq[1][sel], temp_tiffs[0].iq[1][sel] )[0])
            indexes.append(e)
            temps.append(i.info['temp'])
        print(indexes)
        print(temps)    
        
        ax.set_xlim(q_range[0],q_range[1])    
        ax.set_ylim(bottom=y_bottom)

        if y_logscale:
            ax.set_yscale('log')
        ax.set_xlabel(u'Q ($\AA^{-1}$)', fontsize=14, weight='bold')
        ax.set_ylabel(u'Intensity', fontsize=14, weight='bold')

        ax_l = fig.add_subplot('122')
        ax_l.plot(indexes,temps,'-ro')
        ax_r = ax_l.twinx()
        ax_r.plot(indexes,metrics,'-bs')
        
        ax_l.set_ylabel(u'Temperature (C)', fontsize=14, weight='bold',color='r')
        ax_r.set_ylabel(u'Correlation Metric', fontsize=14, weight='bold',color='b')
        ax_l.set_xlabel(u'Scan #', fontsize=14, weight='bold',color='k')
        
        
        plt.tight_layout()
        
        if export_fig:
            plt.savefig( join(smpl.samplepath,'temp_scan.pdf') )
            
        return temp_tiffs











    elif linescan_tiffs:
        
        fig = plt.figure(figsize=figsize)

        ax = fig.add_subplot('143')
        
        indexes = []
        metrics = []
        pos1s = []
        dys = []
        min_intensities = []
        max_intensities = []
        for e,i in enumerate(linescan_tiffs):
            sel = (i.iq[0] > q_range[0]) & (i.iq[0] < q_range[1])
            ax.plot(i.iq[0],i.iq[1])
            min_intensities.append(min(i.iq[1]))
            max_intensities.append(max(i.iq[1]))
            metrics.append(spearmanr( i.iq[1][sel], linescan_tiffs[0].iq[1][sel] )[0])
            indexes.append(e)
            if i.info['pos1']:
                pos1s.append(i.info['pos1'])
            else:
                dys.append(i.info['pos1'])
        ax.set_xlim(q_range[0],q_range[1])    
        ax.set_ylim(bottom=max(y_bottom,min(min_intensities)))

        if y_logscale:
            ax.set_yscale('log')
        ax.set_xlabel(u'Q ($\AA^{-1}$)', fontsize=14, weight='bold')
        ax.set_ylabel(u'Intensity', fontsize=14, weight='bold')

        ax = fig.add_subplot('121')
        
        ax.set_ylabel(u'Max intensity', fontsize=14, weight='bold')
        metrics = np.array(metrics)
        import matplotlib.cm as cm
        mcolors = cm.rainbow(metrics)
            
        ax.bar(pos1s,height=max_intensities,width=0.2,color=mcolors)          
        ax.set_xlabel('pos1 (mm)', fontsize=14, weight='bold') 
        ax.set_title('{:s} (meta_id={:s})'.format(smpl.samplename,i.info['meta_id']), fontsize=13) 
        
        if numbers_on:
            for i in indexes:
                ax.text(linescan_tiffs[i].info['pos1']+text_xyshift,max_intensities[i]*1.02,str(i),fontsize=10,weight='bold')         
        
        plt.tight_layout()
        
        if export_fig:
            plt.savefig( join(smpl.samplepath,'line_scan.pdf') )
            
        return linescan_tiffs



        
        
    else:
        
        if log_y:
            
            fig = plt.figure(figsize=figsize)
            
            ax = fig.add_subplot('111')
            
            ys = 0
            for e,i in enumerate(smpl.tiffs):
                sel = (i.iq[0] > q_range[0]) & (i.iq[0] < q_range[1])
                ax.plot(i.iq[0],ys+np.log(i.iq[1]),label='(%d,%d) %s'%(e,max(i.iq[1]),i.info['filename']))
                ys = ys + y_shift
            ax.set_xlim(q_range[0],q_range[1])    
            ax.set_ylim(bottom=y_bottom)

            if log_x:
                ax.set_xscale('log')
            
            ax.set_xlabel(u'Q ($\AA^{-1}$)', fontsize=14, weight='bold')
            ax.set_ylabel(u'Intensity', fontsize=14, weight='bold')
            ax.set_title('{:s}'.format(smpl.samplename), fontsize=15)         
            
            if legend:
                ax.legend(fontsize=legend_fontsize)
            plt.tight_layout()

        if export_fig:
            plt.savefig( join(smpl.samplepath,'img.pdf') )
            
            
            return smpl.tiffs

            
            
            
            
            
        else:
        
        
            fig = plt.figure(figsize=figsize)
            
            ax = fig.add_subplot('111')
            
            for e,i in enumerate(smpl.tiffs):
                try:
                    sel = (i.iq[0] > q_range[0]) & (i.iq[0] < q_range[1])
                    ax.plot(i.iq[0],i.iq[1],label='(%d,%d) %s'%(e,max(i.iq[1]),i.info['filename']))
                except:
                    pass
            ax.set_xlim(q_range[0],q_range[1])    
            ax.set_ylim(bottom=y_bottom)
            
            if y_logscale:
                ax.set_yscale('log')
            ax.set_xlabel(u'Q ($\AA^{-1}$)', fontsize=14, weight='bold')
            ax.set_ylabel(u'Intensity', fontsize=14, weight='bold')
            ax.set_title('{:s}'.format(smpl.samplename), fontsize=15)         
            
            if legend:
                ax.legend(fontsize=legend_fontsize)
            plt.tight_layout()
            

        if export_fig:
            plt.savefig( join(smpl.samplepath,'img.pdf') )            
            
            return smpl.tiffs
























#def plotter_xrd(smpl,ind,y_bottom=None,vmin=1,vmax=100,y_logscale=False,
                #bg=None,bg2=None,save_to=None):
    
    #fig = plt.figure(figsize=(8,8))

    #if isinstance(smpl.tiffs[ind].mask,np.ndarray):
        #ax = fig.add_subplot('221')
        #ax.imshow(smpl.tiffs[ind].img,vmin=1,vmax=vmax)
        #ax.set_xticks([]); ax.set_yticks([])
        #ax.set_title('{:s}'.format(smpl.samplename), fontsize=15) 

    #if isinstance(smpl.tiffs[ind].mask,np.ndarray):
        #ax = fig.add_subplot('222')
        #ax.imshow(smpl.tiffs[ind].mask)
        #ax.axis('off')
        #ax.set_title('mask')
    
    #ax = fig.add_subplot('212')
    #ax.plot(smpl.tiffs[ind].iq[0],smpl.tiffs[ind].iq[1])
    #if bg:
        #if bg2:
            #ax.plot(smpl.tiffs[ind].iq[0],smpl.tiffs[ind].iq[1]-bg.iq[1]-bg2.iq[1],'-k',label='Kapton subtracted')
        #else:
            #ax.plot(smpl.tiffs[ind].iq[0],smpl.tiffs[ind].iq[1]-bg.iq[1],'-k',label='Kapton subtracted')
        
        #ax.legend()    
    #ax.set_ylim(bottom=y_bottom)
    
    #ax.set_xlabel(u'Q ($\AA^{-1}$)', fontsize=10, weight='normal')
    #ax.set_ylabel(u'Intensity', fontsize=10, weight='normal')  
    #if y_logscale:
        #ax.set_yscale('log')
    
    #if smpl.tiffs[ind].meta:
        #fltr = smpl.tiffs[ind].meta['filter_positions']
        #filterstr='%s-%s-%s-%s' %(fltr['flt1'],fltr['flt2'],fltr['flt3'],fltr['flt4'])
        
        #try:
            #textstr = '%s\n (exposure=%.1fsec.   tpf=%.1fsec.   filters: %s)'%(
                    #smpl.tiffs[ind].info['filename'],
                    #smpl.tiffs[ind].meta['sp_computed_exposure'],
                    #smpl.tiffs[ind].meta['sp_time_per_frame'],
                    #filterstr)
        #except:
            #textstr = '%s\n (filters: %s)'%(
                #smpl.tiffs[ind].info['filename'],
                #filterstr)
            
        #props = dict(boxstyle='none', facecolor='wheat', alpha=0.5)    
        #ax.text(0.0, 1.2, textstr, transform=ax.transAxes, 
                #fontsize=12,verticalalignment='top')

    #plt.tight_layout()   
    
    #if save_to:
        #plt.savefig(join(save_to,smpl.samplename,'plot.pdf'))

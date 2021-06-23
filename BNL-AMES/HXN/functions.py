import numpy as np
import os, sys, pickle
import subprocess as sbp


from os.path import join
import h5py
import matplotlib.pyplot as plt
from PIL import Image
import imageio

import random

from scipy import ndimage


from scipy.stats import pearsonr, spearmanr, kendalltau
from scipy.stats import rankdata




from os.path import join
from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
from matplotlib import cm

from ipywidgets import interact, interactive
import ipywidgets as widgets
from IPython.display import display

import matplotlib.gridspec as gridspec



# a patch for imageio ---------------------------------------- +
import imageio.core.util
def silence_imageio_warning(*args, **kwargs):
    pass
imageio.core.util._precision_warn = silence_imageio_warning
# ------------------------------------------------------------ +











# masking function
def calc_mask(data,alpha=10,nthr=20,rsize=10,remove_single_spots=True):

    # mask data
    mask  = np.zeros(data.shape)+1

    # mask along cols
    for i in range(data.shape[1]):
        mean = np.mean(data[:,i])
        median = np.median(data[:,i])
        std = np.std(data[:,i])
        for n,m in enumerate(data[:,i]):
            if abs(m-median) > alpha*std:
                mask[n][i] = 0                         
    # mask along rows
    for i in range(data.shape[0]):
        mean = np.mean(data[i,:])
        median = np.median(data[i,:])    
        std = np.std(data[i,:])
        for n,m in enumerate(data[i,:]):
            if abs(m-median) > alpha*std:
                mask[i][n] = 0     

    if remove_single_spots:
        nonzero_pts  = [ [indexes, i]  for indexes, i in np.ndenumerate(data) if i > 0 ]
        isolated_pts = []
        for i in nonzero_pts:
            x_range = np.arange(max(0,i[0][0]-rsize),min(i[0][0]+rsize,data.shape[0]))
            y_range = np.arange(max(0,i[0][1]-rsize),min(i[0][1]+rsize,data.shape[1]))
            nonzeros = []
            for n in x_range:
                for m in y_range:
                    if data[n][m] > 0:
                        nonzeros.append([n,m])
            if len(nonzeros) < nthr:
                isolated_pts.append(i)
        for i in isolated_pts:
            mask[i[0][0]][i[0][1]] = 0
    return mask


def plot_layer(data,ind=-1,input_mask=None,find_cm=True,
              cmap='viridis',vmax=5):
    
    cm = [[],[]]
    if isinstance(input_mask,np.ndarray):
        fig, ax = plt.subplots(2,1,figsize=(8,8))
        ax[0].imshow(data.astype(np.float32),vmax=vmax,cmap=cmap)   
        data_masked = data * input_mask
        ax[1].imshow(data_masked.astype(np.float32),vmax=vmax,cmap=cmap)
        if find_cm:
            cm = ndimage.measurements.center_of_mass(data_masked)
            ax[1].arrow(0, 0, cm[1],cm[0], head_width=0, head_length=0, fc='y', ec='y')
            ax[1].plot(cm[1],cm[0],'yo',ms=5)
            ax[1].text(5,-5,'CM @ [{:3.2f},{:3.2f}]'.format(cm[1],cm[0]),fontsize=10,alpha=0.6,color='r')                
        ax[1].set_title('Masked data')  
        

        if ind == 0:
            ax[0].text(410,-5,'layer # 00000',fontsize=12,alpha=1,color='g') 
        elif ind > 0:
            ax[0].text(410,-5,'layer # %5.5d'%ind,fontsize=12,alpha=1,color='g')       
        
        plt.tight_layout()
        
 
    else:
        fig, ax = plt.subplots(1,1,figsize=(8,4))
        ax.imshow(data.astype(np.float32),vmax=vmax,cmap=cmap)
        
        if find_cm:
            cm = ndimage.measurements.center_of_mass(data)
            ax.arrow(0, 0, cm[1],cm[0], head_width=0, head_length=0, fc='y', ec='y')
            ax.plot(cm[1],cm[0],'yo',ms=5)
            ax.text(5,-5,'CM @ [{:3.2f},{:3.2f}]'.format(cm[1],cm[0]),fontsize=10,alpha=0.6,color='r')
            
        if ind == 0:
            ax.text(410,-5,'layer # 00000',fontsize=12,alpha=1,color='g') 
        elif ind > 0:
            ax.text(410,-5,'layer # %5.5d'%ind,fontsize=12,alpha=1,color='g') 
            
        plt.tight_layout()  
        
    return [fig,ax], cm




def find_opt_mask(nx,ny,nz,diffdata,export_dir,nempty=20,ytrim=None,pmax=100):

    mask  = np.zeros((nx,ny))+1
    c = 0
    for i in range(nz):
        if c > nempty:
            break
        s = random.choice(range(nz))
        l = np.squeeze(diffdata[:,:,s])
        npts  = len([ [indexes, i]  for indexes, i in np.ndenumerate(l) if i > 0 ])
        if npts < pmax:
            print([i,s,npts])
            m = calc_mask(l)
            if isinstance(mask,np.ndarray):
                mask = mask * m
            else:
                mask = m
            c += 1

    [fig,ax] = plot_layer(mask,cmap='jet',find_cm=False)
    plt.savefig(export_dir+'mask.pdf')

    # refine mask
    rsize=5
    nthr =10
    pts  = [ [indexes, i]  for indexes, i in np.ndenumerate(mask) if i == 0 ]

    if ytrim:
        for i in pts:
            if i[0][1] < ytrim:
                mask[i[0][0]][i[0][1]] = 1

    isolated_pts = []
    for i in pts:
        x_range = np.arange(max(0,i[0][0]-rsize),min(i[0][0]+rsize,mask.shape[0]))
        y_range = np.arange(max(0,i[0][1]-rsize),min(i[0][1]+rsize,mask.shape[1]))
        zeros = []
        for n in x_range:
            for m in y_range:
                if mask[n][m] == 0:
                    zeros.append([n,m])
        if len(zeros) < nthr:
            isolated_pts.append(i)
    for i in isolated_pts:
        mask[i[0][0]][i[0][1]] = 1


    [fig,ax] = plot_layer(mask,cmap='jet',find_cm=False)
    plt.savefig(export_dir+'mask_refined.pdf')
    pickle.dump(mask,open(export_dir+'mask.pkl','wb'))
    
    return mask




def save_pngs(diffdata,mask,nz,export_dir,minpts=500):
    
    outputs = []
    
    for i in range(nz):
        ind = i
        if np.mod(i,1000) == 0:
            print('doing '+str(ind))

        layer = np.squeeze(diffdata[:,:,ind])
        npts  = len([ [indexes, j]  for indexes, j in np.ndenumerate(layer) if j > 0 ])

        if npts < minpts:
            layer = layer * mask
            [fig,ax], cm = plot_layer(layer,ind=ind,find_cm=False)
            ax.text(5,-5,'CM is not calculated',fontsize=10,alpha=0.6,color='r')
        else:
            layer = layer * mask
            [fig,ax], cm = plot_layer(layer,ind=ind,find_cm=True)
            
        plt.savefig(export_dir+'%5.5d.png'%ind,dpi=100)
        
        outputs.append((i,npts,cm))
    
    pickle.dump(outputs,open(export_dir+'CMs.pkl','wb'))    
    #plt.close('all')
        
    return outputs
        

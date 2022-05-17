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




def ave_tiffs(smpl,inds,save_to,copy_yaml=True):
    import imageio 

    ave = 0*imageio.imread(smpl.tiffs[0].info['abspath'])

    for i in inds:
        ave += imageio.imread(smpl.tiffs[i].info['abspath'])
    ave = ave/len(inds)

    imageio.imsave(join(save_to,'img_ave.tiff'), ave)
    
    if copy_yaml:
        shutil.copy2(smpl.tiffs[0].info['meta_abspath'],join(save_to,'img_ave.yaml'))



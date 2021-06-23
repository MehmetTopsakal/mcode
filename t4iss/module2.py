#-*- coding: utf-8 -*-



import numpy as np 
import shutil,subprocess,os,time

from pylab import *
from matplotlib import gridspec
from matplotlib import pyplot as plt

import scipy.io as sio

from . import t4iss_defaults

import pickle



mcr_path = t4iss_defaults['mcr_path']



    
try:
    if t4iss_defaults['matlab_path']:
        pass
    elif t4iss_defaults['octave_path']:
        pass
    else:
        print('\n\nError: \n Either MATLAB or OCTAVE is needed to run module-2. But not found...\n')
        print('You can set MATLAB by: t4iss.set_defaults(\'matlab_path\',\'/path/to/matlab/executable\') ')
        print('or')
        print('You can set OCTAVE by: t4iss.set_defaults(\'octave_path\',\'/path/to/octave/executable\') ')        
except Exception as exc:
    print('\n\nError: \n Either MATLAB or OCTAVE is needed to run module-2. But not found...\n')    
    print('You can set MATLAB by: t4iss.set_defaults(\'matlab_path\',\'/path/to/matlab/executable\') ')    
    print('or')    
    print('You can set OCTAVE by: t4iss.set_defaults(\'octave_path\',\'/path/to/octave/executable\') ') 
    print(exc)   
    
    
    


def plot_spectra(datafile,ds=None,export_fig_as=None):

    # cleanup
    if os.path.isfile('efa.mat'): os.remove('efa.mat')    
    if os.path.isfile('efa.out'): os.remove('efa.out')
    if os.path.isfile('als.mat'): os.remove('als.mat')
    if os.path.isfile('als.out'): os.remove('als.out')        
       

    spectra = np.loadtxt(datafile, unpack=True, comments='#', skiprows=0)
    E = spectra[0,:]; Is = spectra[1:,:]
    
    # ds is for shifting in y-direction for first subplot
    if ds is None:
        ds = 1/len(Is)
    
    fig, axes = plt.subplots(1,2,figsize=(10,5))
    s = 0
    for i in range(len(Is)):
        axes[0].plot(E,s+Is[i], '-', lw=1)
        axes[1].plot(E,Is[i], '-', lw=1 )
        s -= ds
    axes[0].set_xlabel('Energy [eV]') 
    axes[1].set_xlabel('Energy [eV]')  
    axes[0].set_yticks([])
    axes[1].set_yticks([])
    axes[0].set_ylabel(r'$\leftarrow$ Reaction coordinate ')

    axes[0].grid(True)
    axes[1].grid(True)

    
    if export_fig_as:
        plt.savefig(export_fig_as, transparent=True, dpi=300)  
        
    
    plt.tight_layout()
    
    return




def do_EFA(datafile,ncomp,plot=True,cleanup=True,export_fig_as=None):
    
    if t4iss_defaults['octave_path']:
        sp_call_str = ' export OCTAVE_PATH='+mcr_path+'/octave_version/:$OCTAVE_PATH; '+t4iss_defaults['octave_path']+' -qW --eval '+' "efa_t4iss(\''+datafile+'\', '+str(ncomp)+')" > efa.out  '
    elif t4iss_defaults['matlab_path']:
        sp_call_str = 'export MATLABPATH='+mcr_path+'/matlab_version/:$MATLABPATH; '+t4iss_defaults['matlab_path']+' -nodesktop  -nosplash -r '+' "efa_t4iss(\''+datafile+'\', '+str(ncomp)+')" > efa.out  '
    else:
        print('MATLAB or OCTAVE path is not defined. Exitting....')
        return
    
    # check datafile
    msg = 'Error: \n datafile does not exist. Please check it !! '
    try:
        if not os.path.isfile(datafile):
            print(msg)
            return
    except Exception as exc:
        print(msg)
        print(exc)
        return 


    if os.path.isfile('efa.mat'): os.remove('efa.mat')
    subprocess.call(sp_call_str, shell=True)
    time.sleep(3)

    
    if plot:
        # EFA plots
        mat_contents = sio.loadmat('efa.mat')
        xbackward  = mat_contents['xbackward']
        ebl        = mat_contents['ebl']
        xforward   = mat_contents['xforward']  
        efl        = mat_contents['efl']  
        e  = mat_contents['e']
        
        
        fig = plt.figure(figsize=(10,5))
        gs = gridspec.GridSpec(1, 3, width_ratios=[1,1,2], height_ratios=[1] )
           
        ax=fig.add_subplot(gs[0]) 
        for i in range(ebl.shape[1]):
            ax.plot(xbackward[0],ebl[:,i],'-r')    
        for i in range(efl.shape[1]):
            ax.plot(xforward[0],efl[:,i],'-k')     
        ax.set_title('EFA'); 
        ax.set_ylabel('log(eigenvalues)')
        
        
        import warnings; warnings.simplefilter('ignore')
        ax=fig.add_subplot(gs[1]) 
        for i in range(ebl.shape[1]):
            ax.plot(xbackward[0],np.sqrt(ebl[:,i]),'-r')    
        for i in range(efl.shape[1]):
            ax.plot(xforward[0],np.sqrt(efl[:,i]),'-k') 
        ax.set_ylabel('Singular values');
        
        
        ax=fig.add_subplot(gs[2]) 
        for i in range(e.shape[1]):
            ax.plot(e[:,i],'-o',label='comp-'+str(i+1)) 
        ax.set_title('Initial concentrations');
        ax.legend(loc='best', fontsize=7);    
        
        plt.tight_layout()
        
        if export_fig_as:
            plt.savefig(export_fig_as, transparent=True, dpi=300)
        
    if cleanup:
        os.remove('efa.out')
        os.remove('efa.mat')

    return
    






def do_ALS(datafile,ncomp,norm_to=None,nit=300,thr=0.1,
          save_label=None, print_log=False, plot_log=True, export_log=None,
          save_to='als.pkl',plot=True,export_fig_as=None):
    
    if norm_to is None:
        normalization=0
    elif norm_to.lower()[0] == 'm':
        normalization=1
        print('Normalizing each spectrum to its maximum')
    elif norm_to.lower()[0] == 't':
        normalization=2
        print('Normalizing each spectrum to its tail')
        
    if os.path.exists('als.mat'): 
        os.remove('als.mat')
    
    do_EFA(datafile,ncomp,plot=False,cleanup=False)
    

    if t4iss_defaults['octave_path']:
        sp_call_str = ' export OCTAVE_PATH='+mcr_path+'/octave_version/:$OCTAVE_PATH; '+t4iss_defaults['octave_path']+' -qW --eval '+' "als_t4iss('+str(nit)+','+str(thr)+','+str(normalization)+')" > als.out  '
    elif t4iss_defaults['matlab_path']:
        sp_call_str = ' export MATLABPATH='+mcr_path+'/matlab_version/:$MATLABPATH; '+t4iss_defaults['matlab_path']+' -nodesktop  -nosplash -r '+' "als_t4iss('+str(nit)+','+str(thr)+','+str(normalization)+')" > als.out  '
    else:
        print('MATLAB or OCTAVE path is not defined. Exitting....')
        return

    
    # check datafile
    msg = 'Error: \n efa.mat does not exist. Did you run EFA ? '
    try:
        if not os.path.isfile('efa.mat'):
            print(msg)
            return
    except Exception as exc:
        print(msg)
        print(exc)
        return     
      
   
    print('ALS run started.... \n') 
    time_start = time.time()
    subprocess.call(sp_call_str, shell=True)
    time.sleep(5)
    als_time = time.time() - time_start
    print('ALS run completed in {:.3f} seconds \n'.format(als_time))
    
    if print_log: 
        print(open('als.out').read())
    
    
    if save_label is None:
        print('ALS optimization log can be found in als.out\n') 
    else:
        shutil.move('als.mat',save_label+'.mat')
        shutil.move('als.out',save_label+'.out')
        print('ALS optimization log can be found in '+save_label+'.out')    

    with open('als.out') as f:
        lines = f.readlines()
    als_log = lines
        
    # learn normalization method    
    for l in lines:
        if l.startswith('inorm'):
            inorm = l.split()[2]
            break
    
    # read iterations
    ITs = []
    for e,l in enumerate(lines):
        if l.startswith('ITERATION'):
            it = lines[e].split()[1]
            pca_rep = lines[e+1].split('=')[1].split()[0]
            sigma = lines[e+3].split('=')[1].split()[0]
            lof_pca = lines[e+7].split('=')[1].split()[0]
            lof_exp = lines[e+8].split('=')[1].split()[0]
            r2 = lines[e+9].split()[-1]
            ITs.append([int(it),float(pca_rep),float(sigma),
                        float(lof_pca),float(lof_exp),
                        float(r2)])
    ITs = np.array(ITs)
    
    # read "Fitting error (lack of fit, lof)" 
    for e,l in enumerate(lines):
        if l.startswith('Fitting error (lack of fit, lof) in % at the optimum'):
            lof_pca_final = float(lines[e].split('=')[1].split()[0][0:-5])
            lof_exp_final = float(lines[e].split('=')[1].split()[1][0:-5])
            
    # read "Percent of variance explained (r2)at the optimum"
    for e,l in enumerate(lines):
        if l.startswith('Percent of variance explained (r2)at the optimum'):
            r2_final = float(lines[e].split()[8])



    if plot_log:        
        
        fig, ax = plt.subplots(1,1,figsize=(8,6))
        
        ax.plot(ITs[1:,0],ITs[1:,1]/ITs[1,1],'-ys',label='Sum of squares respect PCA reprod. \n initial:%3.2e   final:%3.2e'%(ITs[1,1],ITs[-1,1]))
        #ax.plot(ITs[1:,0],ITs[1:,2]/ITs[1,2],'-r*',label='Sigma respect experimental data \n initial:%3.2e   final:%3.2e'%(ITs[1,2],ITs[-1,2]))
        ax.plot(ITs[1:,0],ITs[1:,3]/ITs[1,3],'-go',label='Fitting error (lack of fit, lof) in percentage (PCA) \n initial:%3.2e   final:%3.2e'%(ITs[1,3],ITs[-1,3]))
        ax.plot(ITs[1:,0],ITs[1:,4]/ITs[1,4],'-b+',label='Fitting error (lack of fit, lof) in percentage (exp) \n initial:%3.2e   final:%3.2e'%(ITs[1,4],ITs[-1,4]))
        ax.set_xlabel('Iteration #')
        ax.set_ylabel('Normalized')
        ax.legend(loc='center right',fontsize=10)
        
        if norm_to:
            ax.set_title('ncomp=%d  normalization=%s'%(ncomp,norm_to),color='r')
        else:
            ax.set_title('ncomp=%d  normalization=None'%(ncomp),color='r')
        
        ax2 = ax.twinx()
        ax2.plot(ITs[1:,0],ITs[1:,5],'-ks')
        ax2.set_ylabel('Percent of variance explained   (initial:%6.4e   final:%6.4e)'%(ITs[1,5],ITs[-1,5]))
        ax2.set_xlim([1,ITs[1:,0][-1]+1])

        plt.tight_layout()
        
     
    if export_log:
        plt.savefig(export_log, transparent=True, dpi=300)    

        
        
    als_data = sio.loadmat('als.mat')    
    copt  = als_data['copt']
    sopt  = als_data['sopt']
    E  = als_data['Energy'] 
    data = np.loadtxt(datafile, unpack=True, comments='#', skiprows=0)
    pickle.dump([data,ncomp,norm_to,als_log,ITs,copt,sopt,E],open(save_to,'wb')) 
    
    
    
    
    if plot:

        fig = plt.figure(figsize=(10,5))
        gs = gridspec.GridSpec(1, 2, width_ratios=[1.5,1], height_ratios=[1] )
        gs.update(top=0.95, bottom=0.1, left=0.08, right=0.95, wspace=0.1, hspace=0.05)

        ax = fig.add_subplot('121'); ax.grid(True)
        markers = ['-ro','--gs','-.bd','-m^','-c<','--yv','-k*']*2
        for i in range(len(copt[0])):
            ax.plot(copt[:,i],markers[i], ms=5, alpha=0.8, label='component-'+str(i+1))

        ax.set_xlabel('Spectra #')
        ax.set_ylabel('Concentration')
        ax.legend(loc='best',fontsize=10,ncol=1)


        ax = fig.add_subplot('122'); ax.grid(False)
        markers = ['-r','-g','-b','-m','-c','-y','-k']*2
        for i in range(len(sopt)):
            ax.plot(E,sopt[i,:], markers[i], lw=3, alpha=0.6, label='component-'+str(i+1))
        ax.set_xlabel('Energy [eV]')
        ax.legend(loc='best',fontsize=10,ncol=1)    
        plt.tight_layout()  
        
        plt.savefig('als.pdf')
        
    
    
    
    os.remove('efa.out')
    os.remove('efa.mat')    
    os.remove('als.out')     
    os.remove('als.mat')
    
    
    return



def load_opt(load_from,norm_to=None,scales=None,plot=False,uscale=1.0):
    
    [data,ncomp,normed_to,als_log,ITs,copt,sopt,E] = pickle.load(open(load_from,'rb'))
    
    if not scales:
        if norm_to == 'tail':
            tails    = [ i[-1] for i in sopt ]
            scales_t = [ i/tails[0] for i in tails ]  
            scales = scales_t
        elif norm_to == 'max':
            maxs     = [ max(i) for i in sopt ] 
            scales_m = [ i/maxs[0] for i in maxs ]
            scales = scales_m
        else:
            scales = [ 1.0 for i in sopt ]
    
    scales = scales*uscale
    copt = copt[:,:]*scales; copt = np.array(copt)
    sopt = [i/scales[e] for e,i in enumerate(sopt)]; sopt = np.array(sopt)
    
    print(scales)
    
    if plot:    
        fig = plt.figure(figsize=(10,5))
        gs = gridspec.GridSpec(1, 2, width_ratios=[1.5,1], height_ratios=[1] )
        gs.update(top=0.95, bottom=0.1, left=0.08, right=0.95, wspace=0.1, hspace=0.05)

        ax = fig.add_subplot('121'); ax.grid(True)
        markers = ['-ro','--gs','-.bd','-m^','-c<','--yv','-k*']*2
        for i in range(len(copt[0])):
            ax.plot(copt[:,i],markers[i], ms=5, alpha=0.8, label='component-'+str(i+1))

        ax.set_xlabel('Spectra #')
        ax.set_ylabel('Concentration')
        ax.legend(loc='best',fontsize=10,ncol=1)

        ax = fig.add_subplot('122'); ax.grid(False)
        markers = ['-r','-g','-b','-m','-c','-y','-k']*2
        for i in range(len(sopt)):
            ax.plot(E,sopt[i,:], markers[i], lw=3, alpha=0.6, label='component-'+str(i+1))
        ax.set_xlabel('Energy [eV]')
        ax.legend(loc='best',fontsize=10,ncol=1)    
        plt.tight_layout()  

    return copt,E,sopt

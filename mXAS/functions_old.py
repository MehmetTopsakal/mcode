from larch.io import read_ascii,read_athena
from larch.xafs import pre_edge,autobk,xftf
from larch import Group
import larch





def get_fl_ISS(pattern,time_line_num=15,time_str="%d %H:%M:%S %Y  \n"):
    fl_in = []
    fl = sorted(glob.glob(pattern))
    for e,f in enumerate(fl):
        l = linecache.getline(f, time_line_num)
        dt = datetime.datetime.strptime('%s_%s'%(l.split()[3],l.split()[4]), "%m/%d/%Y_%H:%M:%S")
        fl_in.append([dt.timestamp(),f]) 
    fl_in.sort(key=lambda x: x[0])
    fl_out = [[e,i[1]] for e,i in enumerate(fl_in)]
    return fl_out


def get_fl_12BM(pattern,time_line_num=1,time_str="%d %H:%M:%S %Y  \n"):
    fl_in = []
    fl = sorted(glob.glob(pattern))
    for e,f in enumerate(fl):
        l = linecache.getline(f, time_line_num)
        dt = datetime.datetime.strptime(l[11:],time_str)
        fl_in.append([dt.timestamp(),f]) 
    fl_in.sort(key=lambda x: x[0])
    fl_out = [[e,i[1]] for e,i in enumerate(fl_in)]
    return fl_out


def get_fl_BMM(pattern,time_line_num=33,time_str="# Scan.start_time: %Y-%m-%dT%H:%M:%S\n"):
    fl_in = []
    fl = sorted(glob.glob(pattern))
    for e,f in enumerate(fl):
        l = linecache.getline(f, time_line_num)
        dt = datetime.datetime.strptime(l,time_str)
        fl_in.append([dt.timestamp(),f]) 
    fl_in.sort(key=lambda x: x[0])
    fl_out = [[e,i[1]] for e,i in enumerate(fl_in)]
    return fl_out

def get_fl_20ID(pattern,time_line_num=1,time_str="%d %H:%M:%S %Y  \n"):
    fl_in = []
    fl = sorted(glob.glob(pattern))
    for e,f in enumerate(fl):
        l = linecache.getline(f, time_line_num)
        dt = datetime.datetime.strptime('%s_%s_%s'%(l.split()[9],l.split()[10],l.split()[11][0:2]),
                                        "%m/%d/%Y_%I:%M:%S_%p")
        fl_in.append([dt.timestamp(),f]) 
    fl_in.sort(key=lambda x: x[0])
    fl_out = [[e,i[1]] for e,i in enumerate(fl_in)]
    return fl_out






def read_as_ds_ISS(fl_in,imin=0,imax=-1,plot=True,legend=False,cut=1):

    Es = []
    MUs_f = []
    MUs_r = []
    
    d0 = np.loadtxt(fl_in[0][1],unpack=True)
    
    read_data = []
    for i in fl_in:
        d = np.loadtxt(i[1],unpack=True)
        MUs_f.append(d[4]/d[1])
        MUs_r.append(-np.log(d[3]/d[2]))    
        Es.append(d[0])
        
        
    if plot:
        fig = plt.figure(figsize=(12,7))
        
        ax = fig.add_subplot('121')
        for e,i in enumerate(MUs_f):
            ax.plot(Es[e],i)
        ax.set_xlabel('E (eV)')
        ax.set_ylabel('$\mu(E)$')
        ax.set_title('Fluoresence')
        
        ax = fig.add_subplot('122')
        for e,i in enumerate(MUs_r):
            ax.plot(Es[e],i,label=fl_in[e][1]+' (%d %d)'%(e,len(Es[e])))
        ax.set_xlabel('E (eV)')
        ax.set_title('Reference')   
        
        if legend:
            ax.legend(fontsize=8,loc='best',frameon=False)
        
        
    arr_f = np.array([i[:len(d0[0])-cut] for i in MUs_f])
    arr_r = np.array([i[:len(d0[0])-cut] for i in MUs_r])
    E = Es[0][:len(d0[0])-cut]

    ds = xr.Dataset()
    try: 
        da_r = xr.DataArray(data=arr_r[:,imin:imax],
                          coords=[np.arange(len(fl_in)), E[imin:imax]],
                          dims=['scan_num', 'energy']) 
        da_r.scan_num.attrs["files"] = fl    
        ds['mu_ref']   = deepcopy(da_r)
        da_f = xr.DataArray(data=arr_f[:,imin:imax],
                          coords=[np.arange(len(fl_in)), E[imin:imax]],
                          dims=['scan_num', 'energy']) 
        da_f.scan_num.attrs["files"] = fl
        ds['mu_fluo']  = deepcopy(da_f)
    except:
        print('Unable to create dataset. Something is wrong')
        if plot:
            ax.legend(fontsize=8,loc='best',frameon=False)
            

    return ds







def read_as_ds_12BM(fl_in,imin=0,imax=-1,plot=True):
    
    read_data = []
    for i in fl_in:
        d = np.loadtxt(i[1],unpack=True)
        read_data.append([i,d])  
    E    = d[0]

    MUs_f = np.array([i[1][9]/i[1][2] for i in read_data])
    MUs_r = np.array([i[1][7]/i[1][2] for i in read_data])

    ds = xr.Dataset()    
    da_r = xr.DataArray(data=MUs_r[:,imin:imax],
                      coords=[np.arange(len(read_data)), E[imin:imax]],
                      dims=['scan_num', 'energy']) 
    da_r.scan_num.attrs["files"] = fl    
    ds['mu_ref']   = deepcopy(da_r)
    da_f = xr.DataArray(data=MUs_f[:,imin:imax],
                      coords=[np.arange(len(read_data)), E[imin:imax]],
                      dims=['scan_num', 'energy']) 
    da_f.scan_num.attrs["files"] = fl
    ds['mu_fluo']  = deepcopy(da_f)
    

    if plot:
        fig = plt.figure(figsize=(10,5))
        ax = fig.add_subplot('121')
        for e,i in enumerate(ds['mu_fluo']):
            i.plot.line('-o',ms=1,ax=ax,label=fl_in[e][1])
        ax.set_title(None)
        ax.set_xlabel('E (eV)')
        ax.set_ylabel('$\mu(E)$')
        ax.legend(fontsize=8,ncol=1)
        ax.set_title('Fluoresence')
        ax = fig.add_subplot('122')
        for e,i in enumerate(ds['mu_ref']):
            i.plot.line('-o',ms=1,ax=ax,label=fl_in[e][1])
        ax.set_title(None)
        ax.set_xlabel('E (eV)')
        ax.set_ylabel('$\mu(E)$')
        ax.legend(fontsize=8,ncol=1)     
        ax.set_title('Reference')
        plt.tight_layout()
    
    return ds











def read_as_ds_BMM(fl_in,imin=0,imax=-1,plot=True):
    
    read_data = []
    for i in fl_in:
        d = np.loadtxt(i[1],unpack=True)
        read_data.append([i,d])  
    E    = d[0]

    MUs_f = np.array([i[1][3] for i in read_data])
    MUs_r = np.array([-np.log(i[1][6]/i[1][4]) for i in read_data])

    ds = xr.Dataset()    
    da_r = xr.DataArray(data=MUs_r[:,imin:imax],
                      coords=[np.arange(len(read_data)), E[imin:imax]],
                      dims=['scan_num', 'energy']) 
    da_r.scan_num.attrs["files"] = fl    
    ds['mu_ref']   = deepcopy(da_r)
    da_f = xr.DataArray(data=MUs_f[:,imin:imax],
                      coords=[np.arange(len(read_data)), E[imin:imax]],
                      dims=['scan_num', 'energy']) 
    da_f.scan_num.attrs["files"] = fl
    ds['mu_fluo']  = deepcopy(da_f)
    

    if plot:
        fig = plt.figure(figsize=(10,5))
        ax = fig.add_subplot('121')
        for e,i in enumerate(ds['mu_fluo']):
            i.plot.line('-o',ms=1,ax=ax,label=fl_in[e][1])
        ax.set_title(None)
        ax.set_xlabel('E (eV)')
        ax.set_ylabel('$\mu(E)$')
        ax.legend(fontsize=8,ncol=1)
        ax.set_title('Fluoresence')
        ax = fig.add_subplot('122')
        for e,i in enumerate(ds['mu_ref']):
            i.plot.line('-o',ms=1,ax=ax,label=fl_in[e][1])
        ax.set_title(None)
        ax.set_xlabel('E (eV)')
        ax.set_ylabel('$\mu(E)$')
        ax.legend(fontsize=8,ncol=1)     
        ax.set_title('Reference')
        plt.tight_layout()
    
    return ds








def read_as_ds_20ID(fl_in,imin=0,imax=-1,plot=True,col=9):
    
    read_data = []
    for i in fl_in:
        d = np.loadtxt(i[1],unpack=True)
        read_data.append([i,d])  
    E    = d[0]

    MUs_f = np.array([i[1][col]/i[1][8] for i in read_data])

    if plot:
        fig = plt.figure(figsize=(10,5))
        try:
            ax = fig.add_subplot('121')
            for e,i in enumerate(MUs_f):
                ax.plot(E,i,'-o',ms=1,label=fl_in[e][1])
            ax.set_title(None)
            ax.set_xlabel('E (eV)')
            ax.set_ylabel('$\mu(E)$')
            ax.legend(fontsize=8,ncol=1)
            ax.set_title('Fluoresence') 
            plt.tight_layout()
        except:
            ax = fig.add_subplot('121')
            for e,i in enumerate(MUs_f):
                ax.plot(i,'-o',ms=1,label=fl_in[e][1])
            ax.set_title(None)
            ax.set_xlabel('E (eV)')
            ax.set_ylabel('$\mu(E)$')
            ax.legend(fontsize=8,ncol=1)
            ax.set_title('Fluoresence') 
            plt.tight_layout()            
    
    ds = xr.Dataset()
    try:
        da_f = xr.DataArray(data=MUs_f[:,imin:imax],
                          coords=[np.arange(len(read_data)), E[imin:imax]],
                          dims=['scan_num', 'energy']) 
        da_f.scan_num.attrs["files"] = fl
        ds['mu_fluo']  = deepcopy(da_f) 
    except:
        print('unable to create data array')
        return
         
    
    return ds






def deglitch(da_in,fl_in,glitches,plot=True):

    Is_new = []
    for i in da_in:
        Enew,Inew = i.energy.values.copy(), i.values.copy()
        for g in glitches:
            Etmp = [Enew[e] for e,s in enumerate(Enew) if (s < float(g.split(':')[0]) or s > float(g.split(':')[1])) ]
            Itmp = [Inew[e] for e,s in enumerate(Enew) if (s < float(g.split(':')[0]) or s > float(g.split(':')[1])) ]
            Enew,Inew = np.array(Etmp), np.array(Itmp)
        Is_new.append(Inew)
    Is_new = np.array(Is_new)      
    da_dg = xr.DataArray(data=Is_new,
                  coords=[np.arange(Is_new.shape[0]), Enew],
                  dims=['scan_num', 'energy']) 
    da_dg.scan_num.attrs["files"] = da_in.scan_num.attrs["files"]
    
    if plot:
        fig = plt.figure(figsize=(10,4))
        ax = fig.add_subplot('121')
        for e,i in enumerate(da_dg):
            i.plot.line('-',ms=1,ax=ax,label=fl_in[e][1])
        for e,i in enumerate(da_in):
            i.plot.line('--o',ms=1,ax=ax)
        ax.set_title(None)
        ax.set_xlabel('E (eV)')
        ax.set_ylabel('$\mu(E)$')
        ax.legend(fontsize=5,ncol=1,bbox_to_anchor=(1.1, 0.99))
        for g in glitches:
            ax.axvline(x=float(g.split(':')[0]),lw=0.2)
            ax.axvline(x=float(g.split(':')[1]),lw=0.2)
        plt.tight_layout()

    return da_dg




def normalize_and_flatten(da_in,e0=8333,pre1=-158,pre2=-20,
                          nvict=2,norm1=250,norm2=936,
                          rbkg=1.0,kweight=2,kmin=2,kmax=10,dk=1,kwindow='hanning',
                          ave_method='mean',plot=True,legend=False): 

    mus = np.zeros((da_in.shape[0],da_in.shape[1]))
    norms = np.zeros((da_in.shape[0],da_in.shape[1]))
    flats = np.zeros((da_in.shape[0],da_in.shape[1]))
    
    for e,i in enumerate(da_in):
        group = Group(energy=da_in.energy.values, mu=da_in.isel(scan_num=e).values, filename=None)
        pre_edge(group, e0=e0, pre1=pre1, pre2=pre2, nvict=nvict, norm1=norm1, norm2=norm2, group=group)
        mus[e,:] = group.mu
        norms[e,:] = group.norm
        flats[e,:] = group.flat   
    
    ds = xr.Dataset()
    da_mu = xr.DataArray(data=mus,
                      coords=[np.arange(norms.shape[0]), da_in.energy.values],
                      dims=['scan_num', 'energy'])
    ds['mu']  = deepcopy(da_mu)
    da_norm = xr.DataArray(data=norms,
                      coords=[np.arange(norms.shape[0]), da_in.energy.values],
                      dims=['scan_num', 'energy'])   
    ds['norm']  = deepcopy(da_norm)
    da_flat = xr.DataArray(data=flats,
                      coords=[np.arange(norms.shape[0]), da_in.energy.values],
                      dims=['scan_num', 'energy'])
    ds['flat']  = deepcopy(da_flat)
    
    ds.attrs['e0'] = e0
    ds.attrs['pre1'] = pre1
    ds.attrs['pre2'] = pre2
    ds.attrs['nvict']= nvict
    ds.attrs['norm1']= norm1
    ds.attrs['norm2']= norm2
    ds.attrs['rbkg']= rbkg     
    ds.attrs['kweight']= kweight
    ds.attrs['kmin']= kmin
    ds.attrs['kmax']= kmax
    ds.attrs['dk']= dk
    ds.attrs['kwindow']= kwindow
    
    
    
    if plot:
        fig = plt.figure(figsize=(10,8))
        
        ax = fig.add_subplot(2,2,1)
        for e,i in enumerate(da_norm):
            i.plot.line('-',ms=1,ax=ax,label=da_in.scan_num.attrs['files'][e][1])
        ax.set_title(None)
        ax.set_xlabel('E (eV)')
        ax.set_ylabel('$\mu(E)$')
        ax.axvline(x=pre1+e0,lw=0.2)
        ax.axvline(x=pre2+e0,lw=0.2)
        ax.axvline(x=norm1+e0,lw=0.2)
        ax.axvline(x=norm2+e0,lw=0.2)
        ax.axvline(x=e0,lw=0.2)
        if legend:
            ax.legend(fontsize=7)
        ax.set_title('Normalized')
        
        ax = fig.add_subplot(2,2,2)
        for e,i in enumerate(da_flat):
            i.plot.line('-',ms=1,ax=ax)
        ax.set_title(None)
        ax.set_xlabel('E (eV)')
        ax.set_ylabel('$\mu(E)$')
        ax.axvline(x=pre1+e0,lw=0.2)
        ax.axvline(x=pre2+e0,lw=0.2)
        ax.axvline(x=norm1+e0,lw=0.2)
        ax.axvline(x=norm2+e0,lw=0.2)
        ax.axvline(x=e0,lw=0.2) 
        ax.set_title('Flattened')   
        
        plt.tight_layout()
    
    
    
    
    try:    
        if ave_method=='median':
            dat_ave = Group(energy=da_mu.energy.values, mu=da_mu.median(axis=0).values, filename=None)
            pre_edge(dat_ave, e0=e0, pre1=pre1, pre2=pre2, nvict=nvict, norm1=norm1, norm2=norm2, group=dat_ave)
            autobk(dat_ave, rbkg=rbkg, kweight=kweight)
            xftf(dat_ave, kmin=kmin, kmax=kmax, dk=dk, kwindow=kwindow)
        else:
            dat_ave = Group(energy=da_mu.energy.values, mu=da_mu.mean(axis=0).values, filename=None)
            pre_edge(dat_ave, e0=e0, pre1=pre1, pre2=pre2, nvict=nvict, norm1=norm1, norm2=norm2, group=dat_ave)
            autobk(dat_ave, rbkg=rbkg, kweight=kweight)
            xftf(dat_ave, kmin=kmin, kmax=kmax, dk=dk, kwindow=kwindow)


        da = xr.DataArray(data=dat_ave.chi,coords=[dat_ave.k],dims=['ave_k'])   
        ds['ave_chi']      = deepcopy(da)
        da = xr.DataArray(data=dat_ave.k*dat_ave.k*dat_ave.chi,coords=[dat_ave.k],dims=['ave_k'])   
        ds['ave_k2chi']    = deepcopy(da)
        da = xr.DataArray(data=dat_ave.chir_mag,coords=[dat_ave.r],dims=['ave_R'])   
        ds['ave_chir_mag'] = deepcopy(da)


        CHIRs = []
        CHIs = []
        k2CHIs = []
        for i in da_mu:
            dat = Group(energy=i.energy.values, mu=i.values, filename=None)
            pre_edge(dat, e0=e0, pre1=pre1, pre2=pre2, nvict=nvict, norm1=norm1, norm2=norm2, group=dat)
            autobk(dat, rbkg=rbkg, kweight=kweight)
            xftf(dat, kmin=kmin, kmax=kmax, dk=dk, kwindow=kwindow)
            CHIRs.append(dat.chir_mag)
            CHIs.append(dat.chi)
            k2CHIs.append(dat.k*dat.k*dat.chi)
            R = dat.r        
            k = dat.k           

        CHIRs = np.array(CHIRs)
        CHIs = np.array(CHIs)
        k2CHIs = np.array(k2CHIs)

        CHIRs_ave = np.mean(CHIRs,axis=0) 
        CHIs_ave = np.mean(CHIs,axis=0)


        da = xr.DataArray(data=CHIRs,
                          coords=[np.arange(CHIRs.shape[0]), R],
                          dims=['scan_num', 'R'])
        ds['chir_mag']  = deepcopy(da)
        da = xr.DataArray(data=CHIs,
                          coords=[np.arange(CHIs.shape[0]), k],
                          dims=['scan_num', 'k'])
        ds['chi']  = deepcopy(da)
        da = xr.DataArray(data=k2CHIs,
                          coords=[np.arange(k2CHIs.shape[0]), k],
                          dims=['scan_num', 'k'])
        ds['k2chi']  = deepcopy(da)
        
    except:
        return ds
    
        
    if plot:
    
        try:
            ax=fig.add_subplot(2,2,3)
            ax.plot(dat_ave.k, dat_ave.k*dat_ave.k*dat_ave.chi, label='average -> FT')
            ax.plot(k, k*k*CHIs_ave, label='FT -> average')
            ax.set_xlabel('$\it{k}$ ($\AA^{-1}$)')
            ax.set_ylabel('$\it{k^{2}}$ $\chi$ ($\it{k}$) ($\AA^{-2}$)')     
            ax.axvline(x=kmin,lw=0.2)   
            ax.axvline(x=kmax,lw=0.2) 
            ax.set_title('rbkg=%.2f, kweight=%.2f, dk=%.2f, kwindow=%s'%(rbkg,kweight,dk,kwindow),fontsize=10)


            ax=fig.add_subplot(2,2,4)
            ax.plot(dat_ave.r, dat_ave.chir_mag, label='average -> FT')
            ax.plot(R, CHIRs_ave, label='FT -> average')
            ax.set_xlabel('$\it{R}$ ($\AA$)')
            ax.set_ylabel('|$\chi$ ($\it{R}$)| ($\AA^{-3}$)')    
            ax.legend() 
            
            plt.tight_layout()
            
        except:
            pass



    return ds


import numpy as np
import xarray as xr
import matplotlib.pyplot as plt





def read_epsilon(folder='.',
                   fstr = "singlet-TDA-BAR_SCR-full",
                   plot=True,
                   save_fig=True):

    Is = []
    for oc in [11,22,33]:
        file = "%s/EPSILON_BSE-%s_OC%d.OUT"%(folder,fstr,oc)
        data = np.loadtxt(file)
        E = data[:,0]
        I = data[:,2]
        Is.append(I)

    broadening = 'nan'
    with open(file) as f:
        lines = f.readlines()
    for i, line in enumerate(lines):
        if line.startswith('# Used broadening in scaled energy units:'):
            broadening = float(line.split()[7])

    da = xr.DataArray(data=np.array(Is),
                      coords=[11+11*np.arange(3),E],
                      dims=['OC', 'energy'],
                      attrs={'fstr':fstr,'broadening':broadening})

    if plot:
        plt.figure()
        da.isel(OC=0).plot(color='r',label='OC11')
        da.isel(OC=1).plot(color='g',label='OC22')
        da.isel(OC=2).plot(color='b',label='OC33')
        da.mean(dim=['OC']).plot(color='k',label='mean')
        plt.legend()
        plt.tight_layout()

    if save_fig:
        plt.savefig("%s/EPSILON_BSE-%s.pdf"%(folder,fstr))

    return da






def read_pdos(xml_path,plot=False):
    """
    Reads dos.xml file from EXCITING calculation as an xarray dataset.

    USAGE:
    ds = read_pdos('dos.xml')
    plt.figure()
    ds.tdos.sum(dim=('spin')).plot(label='tdos')
    ds.interstitialdos.sum(dim=('spin')).plot(label='interstitial dos')
    ds.pdos.sum(dim=('atoms','spin','l')).plot(label='sum pdos')
    (ds.pdos.sum(dim=('atoms','spin','l'))+ds.interstitialdos.sum(dim=('spin'))).plot(label='sum interstital and pdos')
    plt.legend()

    """

    import xarray as xr
    import xml.etree.ElementTree as ET

    tree = ET.parse(xml_path)
    root = tree.getroot()

    E = 27.211386245*np.array([float(child.attrib['e']) for child in root[3][0]])


    ### get number of atoms
    natoms = 0
    for child in root:
        if child.tag == 'partialdos':
            natoms += 1

    ###check spin polarization
    for child in root[4]:
        if child.attrib['nspin'] == '2':
            spin_polarized = True
        else:
            spin_polarized = False

    coor_atoms = range(natoms)
    if spin_polarized:
        coor_spin  = range(2) # up,down
        tdos = np.zeros(( len(coor_spin),len(E) ))
        tdos[0,:] = np.array([float(child.attrib['dos']) for child in root[3][0]])
        tdos[1,:] = np.array([float(child.attrib['dos']) for child in root[3][1]])
        intdos = np.zeros(( len(coor_spin),len(E) ))
        intdos[0,:] = np.array([float(child.attrib['dos']) for child in root[-1][0]])
        intdos[1,:] = np.array([float(child.attrib['dos']) for child in root[-1][1]])
    else:
        coor_spin  = range(1) # up only
        tdos = np.zeros(( len(coor_spin),len(E) ))
        tdos[0,:] = np.array([float(child.attrib['dos']) for child in root[3][0]])
        intdos = np.zeros(( len(coor_spin),len(E) ))
        intdos[0,:] = np.array([float(child.attrib['dos']) for child in root[-1][0]])

    coor_l     = [0,1,2,3,4] # s,p.d,f,g
    coor_m     = [-4,-3,-2,-1,0,1,2,3,4] #
    pdos_all = np.zeros(( len(coor_atoms),len(coor_spin),len(coor_l),len(coor_m), len(E) ))
    for a in coor_atoms:
        for child in root[a+4]:
            dos = np.array([float(dd.attrib['dos']) for dd in child])
            pdos_all[a,int(child.attrib['nspin'])-1,int(child.attrib['l']),int(child.attrib['m'])+4,:] = dos

    pdos = np.zeros(( len(coor_atoms),len(coor_spin),len(coor_l),len(E) ))
    for a in coor_atoms:
        for s in coor_spin:
            for l in coor_l:
                if l == 0:
                    pdos[a,s,l] = pdos_all[a,s,l,4,:]
                elif l == 1:
                    pdos[a,s,l] = np.sum(pdos_all[a,s,l,3:5,:],axis=0)
                elif l == 2:
                    pdos[a,s,l] = np.sum(pdos_all[a,s,l,2:6,:],axis=0)
                elif l == 3:
                    pdos[a,s,l] = np.sum(pdos_all[a,s,l,1:7,:],axis=0)
                elif l == 4:
                    pdos[a,s,l] = np.sum(pdos_all[a,s,l,0:8,:],axis=0)


    ds = xr.Dataset()
    ds['tdos'] = xr.DataArray(data=tdos,
                        coords=[coor_spin,E],
                        dims=['spin', 'energy']
                        )

    ds['interstitialdos']  = xr.DataArray(data=intdos,
                        coords=[coor_spin,E],
                        dims=['spin', 'energy']
                        )

    ds['pdos']  = xr.DataArray(data=pdos,
                        coords=[coor_atoms,coor_spin,coor_l,E],
                        dims=['atoms', 'spin', 'l', 'energy']
                        )

    if plot:
        import matplotlib.pyplot as plt
        plt.figure()
        ds.tdos.sum(dim=('spin')).plot(label='tdos')
        ds.interstitialdos.sum(dim=('spin')).plot(label='interstitial dos')
        ds.pdos.sum(dim=('atoms','spin','l')).plot(label='sum of pdos')
        (ds.pdos.sum(dim=('atoms','spin','l'))+ds.interstitialdos.sum(dim=('spin'))).plot(label='sum of interstital and pdos')
        plt.title(xml_path)
        plt.legend()

    return ds

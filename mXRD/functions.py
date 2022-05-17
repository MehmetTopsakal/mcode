import pyFAI
import fabio
import numpy as np
import os

from pyFAI.gui import jupyter
import tifffile

import glob

from scipy.ndimage import median_filter
import xarray as xr

from mpl_toolkits.axes_grid1.inset_locator import inset_axes

import pymatgen as mg
from pymatgen.analysis.diffraction.xrd import XRDCalculator
from copy import deepcopy
from pymatgen.core.lattice import Lattice
from pymatgen.core.structure import Structure



#from https://github.com/scikit-beam/scikit-beam/blob/master/skbeam/core/utils.py
def twotheta_to_q(twotheta, wavelength):
    twotheta = np.asarray(twotheta)
    wavelength = float(wavelength)
    pre_factor = ((4 * np.pi) / wavelength)
    return pre_factor * np.sin(twotheta / 2)
def q_to_twotheta(q, wavelength):
    q = np.asarray(q)
    wavelength = float(wavelength)
    pre_factor = wavelength / (4 * np.pi)
    return 2 * np.arcsin(q * pre_factor)
def q_to_d(q):
    return (2 * np.pi) / np.asarray(q)
def d_to_q(d):
    return (2 * np.pi) / np.asarray(d)
def twotheta_to_d(twotheta,wavelength):
    th = np.asarray(twotheta)/2
    rad = np.radians(th)
    t = 2*np.sin(rad)
    d = (wavelength)/t
    return d



def xrd_plotter(ax=None,
                ax2=None,
                mp_id=None,
                final=False,
                structure=None,
                str_file=None,
                label=None,
                marker='o',
                color='C0',
                label_x=1.02,
                label_y=0,
                unit='q_A^-1',
                radial_range=(1,10),
                bottom=-0.2,
                wl=0.77,
                scale=1,
                scale_a=1,
                scale_b=1,
                scale_c=1
                ):

    if mp_id is not None:
        from pymatgen.ext.matproj import MPRester
        mpr = MPRester('gI8Qmxe9AnkbTvNd')  ###
        structure = mpr.get_structure_by_material_id(mp_id,final=final)
    elif structure is None:
        structure = Structure.from_file(str_file)

    structure.lattice = Lattice.from_parameters(a=structure.lattice.abc[0]*scale*scale_a,
                                                b=structure.lattice.abc[1]*scale*scale_b,
                                                c=structure.lattice.abc[2]*scale*scale_c,
                                                alpha=structure.lattice.angles[0],
                                                beta =structure.lattice.angles[1],
                                                gamma=structure.lattice.angles[2]
                                                )

    xrdc = XRDCalculator(wavelength=wl) ###computes xrd pattern given wavelength , debye scherrer rings, and symmetry precision

    if unit == 'q_A^-1':
        ps = xrdc.get_pattern(structure, scaled=True, two_theta_range=np.rad2deg(q_to_twotheta(radial_range,wl)))
        X,Y = twotheta_to_q(np.deg2rad(ps.x),wl), ps.y
    elif unit == '2th_deg':
        ps = xrdc.get_pattern(structure, scaled=True, two_theta_range=radial_range)
        X,Y = ps.x, ps.y
    else:
        ps = xrdc.get_pattern(structure, scaled=True, two_theta_range=radial_range)
        X,Y = ps.x, ps.y

    for i in X:
        ax.axvline(x=i,lw=0.6,color=color)
        try:
            ax2.axvline(x=i,lw=0.2,color=color)
        except:
            pass

    #if normalize:
        #Y = Y/max(Y)
    #if stem_scale == 'sqrt':
        #Y = np.sqrt(Y)
    #if stem_scale == 'log':
        #Y = np.log(Y)
    #if stem:
        #ax.stem(X,Y+bottom,bottom=bottom,
                #markerfmt=color+marker,basefmt=color,linefmt=color)

    #ax.axhline(y=bottom,xmin=radial_range[0]+0.1,color=color)

    ax.text(label_x,label_y,label,color=color,transform=ax.transAxes)



def integrator(img,
               ai, #pyFAI azimuthal inegrator object
               mask, #mask
               flip_mask=False, #sometimes we may need to flip mask
               median_filter_size=-1, #if >1, we apply median filter on raw 2D image to get rid of bad pixels
               npt=4000, # number of radial points
               npt_azim=360, # number of azimuthal points
               method='cython', # integration method. see ai.integrate1d?
               radial_range=(1,10), # integration range
               unit="q_A^-1",  # integration unit. For two-theta-vs-intensity plot, change to 2th_deg
               figsize=None, # user provided figure size
               dpi=96, # dpi for exporting figures
               jupyter_style_i2dplot=False, # change to true for using pyFAI.gui
               robust=True, # xarray robust feature
               cmap="inferno", # color map
               vmin=None, # min value of img and cake plots
               vmax=None, # max value of img and cake plots
               plot_img=True,
               plot_i1d=True,
               plot_i2d=True,
               ylogscale=True,
               xlogscale=True,
               bottom=None, # bottom value of 1d plot
               top=None, # top value of 1d plot
               title=None, # user provided title for the figure
               final=False, #if True, structures pulled from Materials Project will be calculated values (CONTCAR). Otherwise, initial POSCAR .
               include_mask=False, # if maskis to be included in xr dataset
               ROIs = None, # region of interest for azimuthal integration
               phases = None, # phases for peak indexing.
               export_i1d_as=None, # filename for exporting 1d plot
               export_i1d_mode='xy', # for two-theta-vs-intensity use xy, for dspacing-vs-intensity use d here.
               ):


    if flip_mask:
        mask = np.flipud(mask)

    if median_filter_size > 1:
        img = median_filter(img, size=median_filter_size)

    i1d_m = ai.integrate1d(img,npt=npt, mask=mask, method=method,
                            unit=unit, radial_range=radial_range)
    ds = xr.Dataset()
    da_1d = xr.DataArray(data=i1d_m.intensity,
                         coords=[i1d_m.radial],
                         dims=['radial'],
                         attrs={'unit':i1d_m.unit,
                                'xlabel':i1d_m.unit.label,
                                'ylabel':r"Intensity",
                                'method':method,
                                'radial_range':radial_range,
                                'azimuth_range':None}
                     )
    ds['i1d'] = da_1d


    i1d_m_rois = []
    if ROIs is not None:
        i1d_m_rois = []
        for e,roi in enumerate(ROIs):
            i1d_m_roi = ai.integrate1d(img,npt=npt, mask=mask, method=method,
                                       unit=unit, radial_range=radial_range, azimuth_range=roi)
            i1d_m_rois.append(i1d_m_roi)

            da_roi = xr.DataArray(data=i1d_m_roi.intensity,
                                  coords=[i1d_m.radial],
                                  dims=['radial'],
                                  attrs={'unit':i1d_m_roi.unit,
                                         'xlabel':i1d_m_roi.unit.label,
                                         'ylabel':r"Intensity",
                                         'method':method,
                                         'radial_range':radial_range,
                                         'azimuth_range':roi
                                         }
                                  )
            ds['i1d_roi%d'%e] = da_roi
    else:
        i1d_m_rois = []





    if mask is None:
        ds['mask'] = None
    else:
        da_mask = xr.DataArray(data=mask,dims=['pixel_y','pixel_x'])
        if include_mask:
            ds['mask'] = da_mask


    if (plot_img and plot_i1d and plot_i2d):
        if figsize is None:
            fig = plt.figure(figsize=(10,5),dpi=dpi)
        ax_img = fig.add_subplot(1,2,1)
        ax_i2d = fig.add_subplot(2,2,2)
        ax_i1d = fig.add_subplot(2,2,4,sharex=ax_i2d)
    elif (plot_img and plot_i1d and not plot_i2d):
        if figsize is None:
            fig = plt.figure(figsize=(10,5),dpi=dpi)
        ax_img = fig.add_subplot(1,2,1)
        ax_i1d = fig.add_subplot(1,2,2)
        ax_i2d = None
    elif plot_i1d and plot_i2d and not plot_img:
        if figsize is None:
            fig = plt.figure(figsize=(8,6),dpi=dpi)
        ax_i2d = fig.add_subplot(2,1,1)
        ax_i1d = fig.add_subplot(2,1,2,sharex=ax_i2d)
        ax_img = None
        ax_i2d.set_title(title)
    elif plot_i1d and not plot_i2d and not plot_img:
        if figsize is None:
            fig = plt.figure(figsize=(8,6),dpi=dpi)
        ax_i1d = fig.add_subplot(1,1,1)
        ax_i2d = None
        ax_img = None
        ax_i1d.set_title(title)
    elif plot_i2d and not plot_i1d and not plot_img:
        if figsize is None:
            fig = plt.figure(figsize=(8,6),dpi=dpi)
        ax_i2d = fig.add_subplot(1,1,1)
        ax_i1d = None
        ax_img = None
        ax_i2d.set_title(title)
    elif plot_img and not plot_i1d and not plot_i2d:
        if figsize is None:
            fig = plt.figure(figsize=(6,8),dpi=dpi)
        ax_img = fig.add_subplot(1,1,1)
        ax_i1d = None
        ax_i2d = None
        ax_img.set_title(title)


    if plot_img:
        da_img = xr.DataArray(data=img,dims=['pixel_y','pixel_x'])
        ds['img'] = da_img

        if jupyter_style_i2dplot:
            jupyter.display(img,ax=ax_img)
            if mask is not None:
                ax_img.imshow(mask,alpha=0.1,cmap='Greys')
            ax_img.set_xlabel('pixel_x')
            ax_img.set_ylabel('pixel_y')
        else:

            ds['img'].plot.imshow(ax=ax_img,robust=robust,cmap=cmap,vmin=vmin,vmax=vmax,
                        yincrease=False,
                        add_colorbar=True,
                        cbar_kwargs=dict(orientation='vertical',
                        pad=0.02, shrink=0.6, label=None))
            ax_img.set_aspect('equal')
            if mask is not None:
                ax_img.imshow(mask,alpha=0.1,cmap='Greys')
            ax_img.set_title(title)



    if plot_i2d:
        i2d_m = ai.integrate2d(img, npt_rad=npt, npt_azim=npt_azim, mask=mask, method=method,
                                   unit=unit, radial_range=radial_range)
        if title is None:
            if median_filter_size > 1:
                ax_i2d.set_title('(Median_filtered 2D image)')
            else:
                ax_i2d.set_title('(2D image)')
        else:
            pass

        if jupyter_style_i2dplot:
            jupyter.plot2d(i2d_m,ax=ax_i2d)
        else:
            da_2d = xr.DataArray(data=i2d_m.intensity,
                                 coords=[i2d_m.azimuthal,i2d_m.radial],
                                 dims=['azimuthal','radial'],
                                 attrs={'unit':i2d_m.unit,
                                        'xlabel':i2d_m.unit.label,
                                        'ylabel':r"Azimuthal angle $\chi$ ($^{o}$)"})
            ds['i2d'] = da_2d
            ds['i2d'].plot.imshow(ax=ax_i2d,robust=robust,cmap=cmap,vmin=vmin,vmax=vmax,
                        yincrease=False,
                        add_colorbar=False)
            ax_i2d.set_ylabel(da_2d.attrs['ylabel'])

        ax_i2d.set_xlim(radial_range)
        ax_i2d.set_xlabel(None)

        if median_filter_size > 1:
            ax_i2d.set_title('(Median_filtered, masked and regrouped)')
        else:
            ax_i2d.set_title('(Masked and regrouped)')

        if ROIs is not None:
            for e,r in enumerate(ROIs):
                rect = matplotlib.patches.Rectangle((radial_range[0],r[0]),
                                                  radial_range[1], r[1]-r[0],
                                                  color ='C%d'%e,alpha=0.1)
                ax_i2d.add_patch(rect)
                ax_i2d.text(radial_range[1],r[0],' ROI-%d'%e,color='C%d'%e)

        ax_i2d.set_xscale('log')



    if plot_i1d:

        if phases is not None:
            for e,p in enumerate(phases):
                xrd_plotter(ax=ax_i1d,ax2=ax_i2d,
                            mp_id=p['mpid'],final=final,
                            str_file=p['cif'],label=p['label'],
                            scale=p['scale'],
                            marker='.',color='C%d'%(e+2),label_x=1.02,label_y=e*0.1,
                            unit=unit, radial_range=radial_range,wl=ai.wavelength*10e9,bottom=bottom)


        jupyter.plot1d(i1d_m,ax=ax_i1d)

        for e,rr in enumerate(i1d_m_rois):
            jupyter.plot1d(rr,ax=ax_i1d,label='ROI-%d'%e)

        if ylogscale:
            ax_i1d.set_yscale('log')

        if bottom is not None:
            ax_i1d.set_ylim(bottom=bottom)
        if top is not None:
            ax_i1d.set_ylim(top=top)

        if xlogscale:
            ax_i1d.set_xscale('log')


        if ROIs is not None:
            ax_i1d.legend(fontsize=8,loc=1)
        else:
            try:
                ax_i1d.get_legend().remove()
            except:
                pass


        ax_i1d.set_xlabel(i1d_m.unit.label,loc='center')
        ax_i1d.set_xlim(radial_range)
        ax_i1d.set_title(None)


    if (plot_img and plot_i1d and plot_i2d):
        ax_img.set_title(title)
    elif (plot_img and plot_i1d and not plot_i2d):
        ax_img.set_title(title)
    elif plot_i1d and plot_i2d and not plot_img:
        ax_i2d.set_title(title)
    elif plot_i1d and not plot_i2d and not plot_img:
        ax_i1d.set_title(title)
    elif plot_i2d and not plot_i1d and not plot_img:
        ax_i2d.set_title(title)
    elif plot_img and not plot_i1d and not plot_i2d:
        ax_img.set_title(title)

    plt.tight_layout()


    if export_fig_as is not None:
        plt.savefig(export_fig_as,dpi=196)

    if export_i1d_as is not None:

        if export_i1d_mode == 'xy' and unit == 'q_A^-1':
            out = np.column_stack((np.rad2deg(q_to_twotheta(ds['i1d'].radial.values,ai.wavelength*10e9)),ds['i1d'].values))
        elif export_i1d_mode == 'xy' and unit == '2th_deg':
            out = np.column_stack((ds['i1d'].radial.values,ds['i1d'].values))
        elif export_i1d_mode == 'd' and unit == 'q_A^-1':
            out = np.column_stack((q_to_d(ds['i1d'].radial.values),ds['i1d'].values))
        elif export_i1d_mode == 'd' and unit == '2th_deg':
            out = np.column_stack((twotheta_to_d(ds['i1d'].radial.values,ai.wavelength*10e9),ds['i1d'].values))
        np.savetxt(export_i1d_as,out)


        if ROIs is not None:
            for e,_ in enumerate(ROIs):
                if export_i1d_mode == 'xy' and unit == 'q_A^-1':
                    out = np.column_stack((np.rad2deg(q_to_twotheta(ds['i1d'].radial.values,ai.wavelength*10e9)),ds['i1d_roi%d'%e].values))
                    np.savetxt(export_i1d_as.split('.xy')[0]+'_roi%d'%e+'.xy',out)
                elif export_i1d_mode == 'xy' and unit == '2th_deg':
                    out = np.column_stack((ds['i1d'].radial.values,ds['i1d_roi%d'%e].values))
                    np.savetxt(export_i1d_as.split('.xy')[0]+'_roi%d'%e+'.xy',out)
                elif export_i1d_mode == 'd' and unit == 'q_A^-1':
                    out = np.column_stack((q_to_d(ds['i1d'].radial.values),ds['i1d_roi%d'%e].values))
                    np.savetxt(export_i1d_as.split('.d')[0]+'_roi%d'%e+'.d',out)
                elif export_i1d_mode == 'd' and unit == '2th_deg':
                    out = np.column_stack((twotheta_to_d(ds['i1d'].radial.values,ai.wavelength*10e9),ds['i1d_roi%d'%e].values))
                    np.savetxt(export_i1d_as.split('.d')[0]+'_roi%d'%e+'.d',out)

    ds.attrs ={'ai':ai,
               'flip_mask':flip_mask,
               'median_filter_size':median_filter_size,
               'npt':npt,
               'npt_azim':npt_azim,
               'method':method,
               'radial_range':radial_range,
               'unit':unit,
               'figsize':figsize,
               'dpi':dpi,
               'export_fig_as':export_fig_as,
               'jupyter_style_i2dplot':jupyter_style_i2dplot,
               'robust':robust,
               'cmap':cmap,
               'vmin':vmin,
               'vmax':vmax,
               'plot_img':plot_img,
               'plot_i1d':plot_i1d,
               'plot_i2d':plot_i2d,
               'ylogscale':ylogscale,
               'xlogscale':xlogscale,
               'bottom':bottom,
               'top':top,
               'title':title,
               'final':final,
               'include_mask':include_mask,
               'ROIs':ROIs,
               'phases':phases,
               'export_i1d_as':export_i1d_as,
               'export_i1d_mode':export_i1d_mode,
               }

    return ds

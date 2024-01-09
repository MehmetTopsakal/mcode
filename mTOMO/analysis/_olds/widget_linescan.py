from ipywidgets import HBox, VBox
import ipywidgets as widgets
from ipywidgets import HBox, VBox, Label
from IPython.display import display,clear_output

style = {'description_width': 'initial'}

space_10_10 = widgets.HTML(layout = widgets.Layout(width='10px', height='10px'),value=" ")
space_50_10 = widgets.HTML(layout = widgets.Layout(width='50px', height='10px'),value=" ")
space_10_50 = widgets.HTML(layout = widgets.Layout(width='10px', height='50px'),value=" ")


#------------------------------------------------------------------------------------------|
#----------------------------- Integrator -------------------------------------------------|

#Fields
w_path = widgets.Text(layout = widgets.Layout(width='470px', height='30px'), style = style,
    value=os.getcwd(),
    placeholder='Type someting')
w_h5file = widgets.Dropdown(layout = widgets.Layout(width='225px', height='30px'),
    options=[])
w_yamlfile = widgets.Dropdown(layout = widgets.Layout(width='225px', height='30px'),
    options=[])
w_ponifile = widgets.Dropdown(layout = widgets.Layout(width='100px', height='30px'),
    options=[])
w_maskfile = widgets.Dropdown(layout = widgets.Layout(width='100px', height='30px'),
    options=[])
w_npt  = widgets.IntText(layout = widgets.Layout(width='60px', height='30px'),
                        value=8000)
w_unit = widgets.Dropdown(layout = widgets.Layout(width='80px', height='30px'),
    options=["q_nm^-1","q_A^-1","2th_deg","2th_rad","r_mm"],
    value="2th_deg",disabled=False)
w_method = widgets.Dropdown(layout = widgets.Layout(width='80px', height='30px'),
    options=["numpy","cython","BBox","splitpixel","lut","csr","nosplit_csr","full_csr","lut_ocl","csr_ocl"],
    value="csr_ocl",disabled=False)

#Buttons
button_listdir = widgets.Button(layout = widgets.Layout(width='120px', height='30px'),
    description='Read file list',
    style=widgets.ButtonStyle(button_color='green'))
button_loadfiles = widgets.Button(layout = widgets.Layout(width='120px', height='30px'),
    description='Load',
    style=widgets.ButtonStyle(button_color='blue'))
button_integrate = widgets.Button(layout = widgets.Layout(width='180px', height='30px'),
    description='Integrate',
    style=widgets.ButtonStyle(button_color='red'))


output_load = widgets.Output();
output_integrate = widgets.Output();


def on_button_listdir_clicked(b):
    button_listdir.description='click to reload' 
    gh = glob.glob('%s/*.h5'%(w_path.value))
    gh.sort()
    w_h5file.options = [i.split('/')[-1] for i in gh]
    gy = glob.glob('%s/*.y*ml'%(w_path.value))
    gy.sort()
    w_yamlfile.options = [i.split('/')[-1] for i in gy]
    gp = glob.glob('%s/*.poni'%(w_path.value))
    gp.sort()
    w_ponifile.options = [i.split('/')[-1] for i in gp]
    gm = glob.glob('%s/*.m*sk'%(w_path.value))
    gm.sort()
    w_maskfile.options = [i.split('/')[-1] for i in gm]
button_listdir.on_click(on_button_listdir_clicked) 


def on_button_loadfiles_clicked(b): 
    with output_load:
        clear_output()       
        ts = time.time()
        button_loadfiles.description='loading'
        global dark_data,bright_data,meta
        hf = h5py.File('%s/%s'%(w_path.value,w_h5file.value),'r')
        meta = yaml.load(open('%s/%s'%(w_path.value,w_yamlfile.value)), Loader=yaml.Loader)
        dark_data = hf.get('dark_data')
        dark_data = np.array(dark_data).astype('float32')
        bright_data = hf.get('bright_data')
        bright_data = np.array(bright_data).astype('float32')
        button_loadfiles.description='Loaded (%.1fs)'%(time.time()-ts)
        del hf
button_loadfiles.on_click(on_button_loadfiles_clicked) 


def on_button_integrate_clicked(b):
    with output_integrate:
        clear_output()    
        os.chdir(w_path.value)
        ai  = pyFAI.load(w_ponifile.value)
        try:
            msk = fabio.open(w_maskfile.value).data
        except:
            msk = None
        button_integrate.description='Integrating'
        global i1ds, intensities, radial
        i1ds = []
        for e,i in enumerate(bright_data):
            if e == 1:
                ts = time.time() 
            i1d = ai.integrate1d((i-dark_data).astype('float32'),w_npt.value,unit=w_unit.value,
                                 method=w_method.value,mask=msk)
            i1ds.append(i1d)  
        intensities = np.zeros((len(i1ds),w_npt.value))
        for e,i in enumerate(i1ds):
            intensities[e,:] = i[1]
        radial = i[0]
        button_integrate.description='Finished in %.3f sec.'%(time.time()-ts)
        display(ui_linescan_analyzer_plotter)
        
button_integrate.on_click(on_button_integrate_clicked) 


f1 = HBox([Label('Project path:'),w_path],background_color="Khaki", width="100%")
f2 = HBox([Label('h5 & yaml files:'),w_h5file,w_yamlfile])
buttons = VBox([button_listdir,button_loadfiles])
b1 = HBox([VBox([f1,f2]),buttons])
b2 = HBox([w_ponifile,w_maskfile,Label('npt:'),w_npt,
           Label('unit:'),w_unit,w_method,button_integrate])

ui_linescan_analyzer = VBox([space_10_10,b1,b2,space_10_10,
                                        output_load,output_integrate])






#------------------------------------------------------------------------------------------|
#-------------------------------- img plotter ---------------------------------------------|

w_scannum_img1 = widgets.IntText(layout = widgets.Layout(width='50px', height='30px'),
    value=1,min=1)
w_scannum_img1_it = widgets.IntSlider(layout = widgets.Layout(width='200px', height='30px'), 
    value=1,min=1,step=1, description='',disabled=False,
    continuous_update=False,orientation='horizontal',readout=False,
    style = style) 
widgets.link((w_scannum_img1, 'value'), (w_scannum_img1_it, 'value'))
w_scannum_img2 = widgets.IntText(layout = widgets.Layout(width='50px', height='30px'),
    value=1,min=1)
w_scannum_img2_it = widgets.IntSlider(layout = widgets.Layout(width='200px', height='30px'), 
    value=1,min=1,step=1, description='',disabled=False,
    continuous_update=False,orientation='horizontal',readout=False,
    style = style) 
widgets.link((w_scannum_img2, 'value'), (w_scannum_img2_it, 'value'))


w_cmap = widgets.Dropdown(
    layout = widgets.Layout(width='80px', height='30px'),
    options=['jet', 'viridis', 'Greys_r', 'binary', 'inferno', 'terrain'],
    value='binary',disabled=False)
w_vmin = widgets.IntText(layout = widgets.Layout(width='50px', height='30px'),
    value=1,min=0)
w_vmax = widgets.IntText(layout = widgets.Layout(width='50px', height='30px'),
    value=100,min=1)

def img_plotter(ind1=1,ind2=1,cmap='jet',vmin=None,vmax=None):  
    try:
        w_scannum_img1_it.max = len(bright_data)
        w_scannum_img2_it.max = len(bright_data)  
        
        fig = plt.figure(figsize=(6,10.5))
        ax = fig.add_subplot('211')
        dat = bright_data[ind1-1,:,:]-dark_data
        ims = ax.imshow(dat.astype('float32'),vmin=vmin,vmax=vmax,cmap=cmap)
        cb = plt.colorbar(ims, orientation='horizontal', shrink=0.5, pad=0.075)
        ax.set_title('Diffraction image %d/%d from %s'%(ind1,len(i1ds),meta['detector']))
        
        ax = fig.add_subplot('212')
        dat = bright_data[ind2-1,:,:]-dark_data
        ims = ax.imshow(dat.astype('float32'),vmin=vmin,vmax=vmax,cmap=cmap)
        cb = plt.colorbar(ims, orientation='horizontal', shrink=0.5, pad=0.075)
        ax.set_title('Diffraction image %d/%d from %s'%(ind2,len(i1ds),meta['detector']))  
        
        plt.tight_layout()

    except Exception as exc:
#         print(exc)
        plt.close()
        pass
    
img_output = widgets.interactive_output(img_plotter, 
                                {"ind1":w_scannum_img1,"ind2":w_scannum_img2,
                                 "cmap":w_cmap,"vmin":w_vmin,"vmax":w_vmax})


lb1 = HBox([Label('Img-1 #:'), w_scannum_img1, w_scannum_img1_it])
lb2 = HBox([Label('Img-2 #:'), w_scannum_img2, w_scannum_img2_it])
lb3 = HBox([Label('cmap:'),w_cmap, 
            Label('vmin'), w_vmin, Label('vmax'), w_vmax])

lui = VBox([lb1,lb2,lb3,img_output])





#------------------------------------------------------------------------------------------|
#-------------------------------- spectrum plotter ----------------------------------------|

from matplotlib.ticker import FormatStrFormatter
from scipy import stats

w_scannum = widgets.IntText(layout = widgets.Layout(width='50px', height='30px'),
    value=1,min=1)
w_scannum_it = widgets.IntSlider(layout = widgets.Layout(width='250px', height='30px'), 
    value=1,min=1, max=100, step=1, description='',disabled=False,
    continuous_update=False,orientation='horizontal',readout=False,
    style = style) 
widgets.link((w_scannum, 'value'), (w_scannum_it, 'value'))

w_roi_slider = widgets.FloatRangeSlider(layout = widgets.Layout(width='320px', height='30px'), 
    value=[1,10],min=0,max=13,step=0.02,disabled=False,
    continuous_update=False,orientation='horizontal',readout=True,
    style = style) 

w_logplot = widgets.Checkbox(layout = widgets.Layout(width='15px', height='30px'),
    value=False,disabled=False,indent=False)
w_ybottom = widgets.FloatLogSlider(layout = widgets.Layout(width='150px', height='30px'),
    value=0.1,base=10,min=-1,max=3,step=0.2,readout=False)

w_scanref1 = widgets.IntText(layout = widgets.Layout(width='45px', height='30px'),
    value=0)
w_scanref2 = widgets.IntText(layout = widgets.Layout(width='45px', height='30px'),
    value=0)
w_scanrefm = widgets.IntText(layout = widgets.Layout(width='45px', height='30px'),
    value=1)

w_marker_on = widgets.Checkbox(layout = widgets.Layout(width='15px', height='30px'),
    value=False,disabled=False,indent=False)

def i1d_plotter(ind=1,ind_ref1=0,ind_ref2=0,ind_refm=0,logplot=False,roi=[0,13],ybottom=0.1,
               marker_on=False):  
    try:
        w_scannum_it.max = len(bright_data)

        fig = plt.figure(figsize=(6,12))
        
        ax = fig.add_subplot('211')
        roi_start = np.argmin(np.abs(radial-w_roi_slider.value[0]))
        roi_stop  = np.argmin(np.abs(radial-w_roi_slider.value[1]))
        to_plot = [radial[roi_start:roi_stop],i1ds[ind-1][1][roi_start:roi_stop]]
        
        if marker_on:
            marker = 'o'
        else:
            marker = None
        ax.plot(to_plot[0],to_plot[1],'-k',lw=2,marker=marker,label='#%d'%(ind))
        
        if ind_ref1 > 0:
            to_plot_ref1 = [radial[roi_start:roi_stop],i1ds[ind_ref1-1][1][roi_start:roi_stop]]
            ax.plot(to_plot_ref1[0],to_plot_ref1[1],'--r',lw=1,label='#%d'%(ind_ref1))
        if ind_ref2 > 0:
            to_plot_ref2 = [radial[roi_start:roi_stop],i1ds[ind_ref2-1][1][roi_start:roi_stop]]
            ax.plot(to_plot_ref2[0],to_plot_ref2[1],'-.g',lw=1,label='#%d'%(ind_ref2))
        if ind_refm > 0:
            to_plot_ref3 = [radial[roi_start:roi_stop],i1ds[ind_refm-1][1][roi_start:roi_stop]]
            ax.plot(to_plot_ref3[0],to_plot_ref3[1],':b',lw=1,label='#%d'%(ind_refm))        
        
        ax.set_xlim(roi)
        ax.set_ylim(bottom=ybottom)
        
        if i1ds[0].unit.name == '2th_deg':
            ax.set_xlabel('Scattering Angle 2$\Theta$ ($^o$)')
        elif i1ds[0].unit.name == 'q_A^-1':
            ax.set_xlabel('Q ($A^{-1}$)')
        else:
            ax.set_xlabel(i1ds[0].unit.name)
        ax.yaxis.set_major_formatter(FormatStrFormatter('%.e'))
        if logplot:
            ax.set_yscale('log')
        ax.legend()
        
        ax = fig.add_subplot('413')
        if ind_refm > 0:
            pearsons  = []
            spearmans = []
            for i in intensities:
                pearsons.append(stats.pearsonr(i[roi_start:roi_stop],intensities[ind_refm-1][roi_start:roi_stop])[0])
                spearmans.append(stats.spearmanr(i[roi_start:roi_stop],intensities[ind_refm-1][roi_start:roi_stop])[0])
            ax.plot(np.arange(1,len(pearsons)+1),1-np.array(pearsons),label='Pearson')
            ax.plot(np.arange(1,len(spearmans)+1),1-np.array(spearmans),label='Spearman')
            ax.legend()
            ax.axvline(x=(ind),color='k',linestyle='--')
            ax.set_xticks([])
            
        ax = fig.add_subplot('817')
        
        if ind_refm > 0:
            maes  = []
            for i in intensities:
                maes.append(sum(i[roi_start:roi_stop]-intensities[ind_refm-1][roi_start:roi_stop])/len(i))
            ax.plot(np.arange(1,len(maes)+1),np.array(maes),'-m',label='MAE')
            ax.legend()
            ax.axvline(x=(ind),color='k',linestyle='--')
            ax.set_xticks([])
            
        ax = fig.add_subplot('818')
        if ind_refm > 0:
            mses = []
            for i in intensities:
                mses.append(np.square(i[roi_start:roi_stop]-intensities[ind_refm-1][roi_start:roi_stop]).mean())
            ax.plot(np.arange(1,len(mses)+1),np.array(mses),'-c',label='MSE')
            ax.legend()
            ax.axvline(x=(ind),color='k',linestyle='--')  
            
    except Exception as exc:
#         print(exc)
        plt.close()
        pass
i1d_output = widgets.interactive_output(i1d_plotter, 
                                {"ind":w_scannum,"roi":w_roi_slider,
                                 "ind_ref1":w_scanref1,"ind_ref2":w_scanref2,"ind_refm":w_scanrefm,
                                 "logplot":w_logplot,"marker_on":w_marker_on,"ybottom":w_ybottom,
                                })


rb1 = HBox([Label('Sp-1 #:'), w_scannum, w_scannum_it])
rb3 = HBox([Label('ROI:'),w_roi_slider])
rb4 = HBox([Label('Log plot:'),w_logplot,Label('Marker:'),w_marker_on,Label('y_bottom:'),w_ybottom])
rb2 = HBox([Label('Sp-2 #:'),w_scanref1,Label('Sp-3 #:'),w_scanref2,Label('Metric-ref #:'),w_scanrefm])

rui = VBox([rb1,rb2,rb3,rb4,i1d_output])


ui_linescan_analyzer_plotter = HBox([lui,space_10_10,rui])



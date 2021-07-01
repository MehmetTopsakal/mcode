from ipywidgets import HBox, VBox
import ipywidgets as widgets
from ipywidgets import HBox, VBox, Label
from IPython.display import display,clear_output

style = {'description_width': 'initial'}


w_dir = widgets.Text(layout = widgets.Layout(width='600px', height='30px'), style = style,
    value=os.getcwd(),
    placeholder='Type someting',               
    description='Data path:')
button_listdir = widgets.Button(layout = widgets.Layout(width='120px', height='30px'),
    description='Read file list',
    style=widgets.ButtonStyle(button_color='green'))
def on_button_listdir_clicked(b):
    button_listdir.description='click to reload' 
    gh = glob.glob('%s/*.h5'%(w_dir.value))
    w_h5file.options = [i.split('/')[-1] for i in gh]
    gy = glob.glob('%s/*.yaml'%(w_dir.value))
    w_yamlfile.options = [i.split('/')[-1] for i in gy]
button_listdir.on_click(on_button_listdir_clicked) 
box_data_path = HBox([w_dir,button_listdir])


w_h5file = widgets.Dropdown(layout = widgets.Layout(width='220px', height='30px'),
    options=[])
w_yamlfile = widgets.Dropdown(layout = widgets.Layout(width='200px', height='30px'),
    options=[])
button_loadfiles = widgets.Button(layout = widgets.Layout(width='132px', height='30px'),
    description='Load',
    style=widgets.ButtonStyle(button_color='blue'))
def on_button_loadfiles_clicked(b):
    button_loadfiles.description='loading'
    global dark_data,bright_data,meta
    hf = h5py.File('%s/%s'%(w_dir.value,w_h5file.value),'r')
    meta = yaml.load(open('%s/%s'%(w_dir.value,w_yamlfile.value)), Loader=yaml.Loader)
    dark_data = hf.get('dark_data')
    dark_data = np.array(dark_data).astype('float32')
    bright_data = hf.get('bright_data')
    bright_data = np.array(bright_data).astype('float32')
    button_loadfiles.description='click to reload' 
    del hf
button_loadfiles.on_click(on_button_loadfiles_clicked) 
box_load = HBox([Label('Select h5 file:'), w_h5file,Label('and yaml file:'), w_yamlfile, button_loadfiles])


w_poni = widgets.Text(layout = widgets.Layout(width='120px', height='30px'),
                     value='LaB6.poni')
w_mask = widgets.Text(layout = widgets.Layout(width='120px', height='30px'),
                     value='mask.edf')
w_npt  = widgets.IntText(layout = widgets.Layout(width='60px', height='30px'),
                        value=4000)
w_unit = widgets.Dropdown(layout = widgets.Layout(width='80px', height='30px'),
    options=["q_nm^-1","q_A^-1","2th_deg","2th_rad","r_mm"],
    value="2th_deg",disabled=False)
w_gpu = widgets.Checkbox(layout = widgets.Layout(width='30px', height='30px'),
    value=True,disabled=False,indent=False)
button_integrate = widgets.Button(layout = widgets.Layout(width='180px', height='30px'),
    description='Integrate',
    style=widgets.ButtonStyle(button_color='red'))
def on_button_integrate_clicked(b):
    
    os.chdir(w_dir.value)
    
    ai  = pyFAI.load(w_poni.value)
    try:
        msk = fabio.open(w_mask.value).data
    except:
        msk = None
    
    button_integrate.description='Integrating'
    
    global i1ds
    i1ds = []
    for e,i in enumerate(bright_data):
        if e == 1:
            ts = time.time() 
        if w_gpu.value:
            method='csr_ocl'
        else:
            method = 'csr'
        i1d = ai.integrate1d(i-dark_data,w_npt.value,unit=w_unit.value,method=method,mask=msk)
        i1ds.append(i1d)  
        
#     i1ds = np.array(i1ds)
    button_integrate.description='Finished in %.3f sec.'%(time.time()-ts) 
button_integrate.on_click(on_button_integrate_clicked) 

box_integrate = HBox([w_poni, w_mask, Label(' npt:'), w_npt, Label('unit:'), w_unit, Label('use GPU:'), w_gpu, button_integrate])










w_scannum = widgets.IntText(layout = widgets.Layout(width='50px', height='30px'),
    value=1,min=1)
w_scannum_it = widgets.IntSlider(layout = widgets.Layout(width='400px', height='30px'), 
    value=1,min=1,step=1, description='',disabled=False,
    continuous_update=False,orientation='horizontal',readout=False,
    style = style) 
widgets.link((w_scannum, 'value'), (w_scannum_it, 'value'))
w_cmap = widgets.Dropdown(
    layout = widgets.Layout(width='80px', height='30px'),
    options=['jet', 'viridis', 'Greys_r', 'binary', 'inferno', 'terrain'],
    value='jet',disabled=False)
w_logplot = widgets.Checkbox(layout = widgets.Layout(width='30px', height='30px'),
    value=False,disabled=False,indent=False)
w_xmin = widgets.FloatText(layout = widgets.Layout(width='50px', height='30px'),
    value=0.1,min=0.1)
w_xmax = widgets.FloatText(layout = widgets.Layout(width='50px', height='30px'),
    value=10,min=20)
w_ymin = widgets.FloatSlider(layout = widgets.Layout(width='190px', height='30px'),
    value=0.1,min=0,max=10,step=0.1)

w_vmin = widgets.IntText(layout = widgets.Layout(width='50px', height='30px'),
    value=None,min=0)
w_vmax = widgets.IntText(layout = widgets.Layout(width='50px', height='30px'),
    value=None,min=1)

try:
    w_scannum_it.max = len(bright_data)
except:
    pass


def plotter(ind=1,logscale=False,cmap='jet',y_bottom=0.1,roi_min=0.1,roi_max=10,vmin=None,vmax=None):
    
    try:
        w_scannum_it.max = len(bright_data)
        fig = plt.figure(figsize=(11,6))
        ax = fig.add_subplot('121')
        ax.imshow(bright_data[ind-1,:,:]-dark_data,vmin=vmin,vmax=vmax,cmap=cmap)
#         ax.imshow(np.arcsinh(bright_data[ind-1,:,:]-dark_data).astype(np.float32),cmap=cmap)
#         ax.imshow(bright_data[ind-1,:,:]-dark_data,cmap=cmap,vmin=1,vmax=10)
        ax.set_title('Diffraction image %d/%d from %s'%(ind,len(i1ds),meta['detector']))
        ax = fig.add_subplot('122')
        jupyter.plot1d(i1ds[ind-1],ax=ax)
        ax.set_title('Motor name=%s   position=%.2fmm'%
                    (meta['motor'],np.linspace(meta['motor_start'],meta['motor_stop'],meta['motor_step'])[ind-1]))
        if logscale:
            ax.set_yscale('log')
            
        ax.set_ylim(bottom=y_bottom)
        ax.set_xlim([roi_min,roi_max])
        
    except Exception as exc:
        print(exc)
        plt.close()
        pass

plot_output = widgets.interactive_output(plotter, 
                                {"ind":w_scannum,"logscale":w_logplot,"cmap":w_cmap,"vmin":w_vmin,"vmax":w_vmax,
                                 "y_bottom":w_ymin,"roi_min":w_xmin,"roi_max":w_xmax})


box1 = HBox([Label('Scan #:'), w_scannum, w_scannum_it, Label('ROI:'), w_xmin, Label('to'), w_xmax])
box2 = HBox([Label('Color map:'),w_cmap,Label('Log plot:'), w_logplot, Label('y-min:'), w_ymin, Label('vmin'), w_vmin, Label('vmax'), w_vmax,])





ui_linescan_analyzer_integrator = VBox([box_data_path,box_load,box_integrate]);
ui_linescan_analyzer_plotter = VBox([box1,box2,plot_output]);
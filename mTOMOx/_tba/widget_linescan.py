
import ipywidgets as widgets
from IPython.display import display,clear_output
import time
import deepdish


style = {'description_width': 'initial'}




w_html1 = widgets.HTML(layout = widgets.Layout(width='93px', height='30px'),
    value="Detector:",
)

w_dd1 = widgets.Dropdown(layout = widgets.Layout(width='100px', height='30px'),
    options=['Blackfly', 'Dexela', 'Prosilica'],
    value='Blackfly',
    disabled=False
)

w_fs1 = widgets.FloatSlider(layout = widgets.Layout(width='460px', height='30px'), style = style,
    value=1.0,
    min=0.1,
    max=10.0,
    step=0.1,
    description='Exposure time (sec.):',
    disabled=False,
    continuous_update=False,
    orientation='horizontal',
    readout=True,
    readout_format='.1f',    
                           
)

w_it1 = widgets.IntText(layout = widgets.Layout(width='90px', height='30px'), style = style,
    value=1,
    min=1,
    max=100,
    step=1,
    description='num',
    disabled=False,
    continuous_update=False,
    orientation='horizontal',
    readout=True,
    readout_format='d'
)





w_html2 = widgets.HTML(layout = widgets.Layout(width='93px', height='30px'),
    value="Motor:",
)

w_dd2 = widgets.Dropdown(layout = widgets.Layout(width='100px', height='30px'),
    options=[('mStackX', mStackX), 
             ('mStackY', mStackY), 
             ('mXBase', mXBase), 
             ('mYBase', mYBase),
             ('mPhi', mPhi),
             ('mQuestarX', mQuestarX),
             ('mSigrayZ', mSigrayZ)
            ],             
    value=mStackY,
    disabled=False
)


w_frs = widgets.FloatRangeSlider(layout = widgets.Layout(width='436px', height='30px'), style = style,
    value=[4.9, 5.1],
    min=4.5,
    max=5.5,
    step=0.1,
    description='Range:',
    disabled=False,
    continuous_update=False,
    orientation='horizontal',
    readout=True,
    readout_format='.3f',
)


w_it2 = widgets.IntText(layout = widgets.Layout(width='100px', height='30px'), style = style,
    value=11,
    min=1,
    max=1000,
    step=1,
    description='nstep',
    disabled=False,
    continuous_update=False,
    orientation='horizontal',
    readout=True,
    readout_format='d'
)

w_t1 = widgets.Text(layout = widgets.Layout(width='483px', height='30px'), style = style,
    value='/data/bf_data/temp',
    description='Save directory:',
    disabled=False)


w_t2 = widgets.Text(layout = widgets.Layout(width='150px', height='30px'), style = style,
    value='linescan.h5',
    description='filename:',
    disabled=False)


space = widgets.HTML(layout = widgets.Layout(width='10px', height='30px'),
    value=" ",
)

button = widgets.Button(layout = widgets.Layout(width='100px', height='30px'),
    description='Start!',
    style=widgets.ButtonStyle(button_color='red')
)



box1 = HBox([w_html1,w_dd1,w_fs1,w_it1])
box2 = HBox([w_html2,w_dd2,w_frs,space,w_it2])
box3 = HBox([w_t1,w_t2,space,button])

ui = VBox([box1,box2,box3])




def on_button_clicked(b):
    print('test1')
    with output:
        clear_output()
        print('\n\nProcess started with %s'%(w_dd1.value))   
        if w_dd1.value == 'Blackfly':
            
            if w_it1.value == 1:
                det = blackfly_single
                det.cam.num_images.put(1)
            else:
                det = blackfly_multiple
                det.cam.num_images.put(w_it1.value)
                
            det.cam.acquire_time.put(w_fs1.value)
            det.cam.acquire_period.put(0.05)
            
            time.sleep(1)
            
            ts = time.time()
            
            
            plan = bp.scan([det], w_dd2.value , w_frs.min , w_frs.max, w_it2.value)
            scan_id = RE(plan)            
            
            
            if os.path.isdir(w_t1.value):
                
                data = np.array(list(db[-1].data('blackfly_det_image')))
                print(data.shape)
                
                if data.ndim == 4:
                    data = data[0,:,:,:] 
                
                print('Saving data to: %s'%(w_t1.value))
                
                info = {
                    'scan_id':scan_id[0],      
                    'detector':w_dd1.value,  
                    'time':time.time(),    
                    'exposure':w_fs1.value, 
                    'num':w_it1.value,                        
                }                

                if os.path.isfile('%s/%s'%(w_t1.value,w_t2.value)):
                    deepdish.io.save('%s/%d_%s'%(w_t1.value,int(time.time()),w_t2.value), 
                               {'data': data.astype('uint16'), 'info': info}, 
                               compression='zlib')  
                else:
                    deepdish.io.save('%s/%s'%(w_t1.value,w_t2.value), 
                               {'data': data.astype('uint16'), 'info': info}, 
                               compression='zlib')  
#                 dd_read = deepdish.io.load('/data/bf_data/temp/count.h5')
                
            
        print('Finished in %.2f seconds'%(time.time() - ts))
button.on_click(on_button_clicked)

output = widgets.Output();

# display(ui,output)

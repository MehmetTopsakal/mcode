
import ipywidgets as widgets
from IPython.display import display,clear_output
import time
import yaml


style = {'description_width': 'initial'}



w_det = widgets.SelectMultiple(layout = widgets.Layout(width='80px', height='80px'),
    options=['Dexela', 'Blackfly', 'Prosilica','test'],
    value=['Blackfly'],
    rows=4,
    disabled=False)
det_box = widgets.HBox([widgets.Label('Detector:'), w_det])

w_exp = widgets.FloatSlider(layout = widgets.Layout(width='300px', height='30px'), style = style,
    value=0.2,
    min=0.1,
    max=10.0,
    step=0.1,
    disabled=False,
    continuous_update=False,
    orientation='horizontal',
    readout=True,
    readout_format='.1f')
exp_box = widgets.HBox([widgets.Label('Exposure (sec):'), w_exp])

w_num_dark = widgets.IntText(layout = widgets.Layout(width='50px', height='30px'), style = style,
    value=5,
    min=2,
    max=100,
    step=1,
    disabled=False,
    continuous_update=False,
    orientation='horizontal',
    readout=True,
    readout_format='d')
num_box_dark = widgets.HBox([widgets.Label('Collect dark:'), w_num_dark])


w_darkuid = widgets.Text(layout = widgets.Layout(width='380px', height='30px'), style = style,
    value=None,
    placeholder='Enter dark uid',               
    description='or re-use:',
    disabled=False)

w_num_bright = widgets.IntText(layout = widgets.Layout(width='52px', height='30px'), style = style,
    value=1,
    min=1,
    max=9999,
    step=1,
    disabled=False,
    continuous_update=False,
    orientation='horizontal',
    readout=True,
    readout_format='d')
num_box_bright = widgets.HBox([widgets.Label('Num bright:'), w_num_bright])



w_motor1 = widgets.Dropdown(layout = widgets.Layout(width='85px', height='30px'),
    options=[('mStackX', mStackX), 
             ('mStackY', mStackY), 
             ('mXBase', mXBase), 
             ('mYBase', mYBase),
             ('mPhi', mPhi),
             ('mQuestarX', mQuestarX),
             ('mSigrayZ', mSigrayZ)
            ],             
    value=mStackY,
    disabled=False)

motor1_box = widgets.HBox([widgets.Label('Motor:'), w_motor1])

motor1_button = widgets.Button(layout = widgets.Layout(width='90px', height='30px'),
    description='Read',
    style=widgets.ButtonStyle(button_color='blue'))

w_motor1_start = widgets.FloatText(layout = widgets.Layout(width='55px', height='30px'), style = style,
    value=0,min=-1,max=1)
motor1_start_box = widgets.HBox([widgets.Label('Range:'),w_motor1_start])

w_motor1_stop = widgets.FloatText(layout = widgets.Layout(width='55px', height='30px'), style = style,
    value=1,min=-1,max=1)
motor1_stop_box = widgets.HBox([widgets.Label('to'),w_motor1_stop])

w_motor1_step = widgets.IntText(layout = widgets.Layout(width='55px', height='30px'), style = style,
    value=10)
motor1_step_box = widgets.HBox([widgets.Label('in '),w_motor1_step,widgets.Label(' steps')])

def on_motor1_button_clicked(b):
    motor1_button.description='@%.3f'%(w_motor1.value.position)   
motor1_button.on_click(on_motor1_button_clicked) 



# w_f1 = widgets.Checkbox(layout = widgets.Layout(width='30px', height='30px'),
#     description='1',value=False,disabled=False,indent=False)
# w_f2 = widgets.Checkbox(layout = widgets.Layout(width='30px', height='30px'),
#     description='2',value=False,disabled=False,indent=False)
# w_f3 = widgets.Checkbox(layout = widgets.Layout(width='30px', height='30px'),
#     description='3',value=False,disabled=False,indent=False)
# w_f4 = widgets.Checkbox(layout = widgets.Layout(width='30px', height='30px'),
#     description='4',value=False,disabled=False,indent=False)
# fltr_box = widgets.HBox([widgets.Label('Filters:'), w_f1,w_f2,w_f3,w_f4])



w_saveto = widgets.Text(layout = widgets.Layout(width='280px', height='30px'), style = style,
    value='/data/ssd2tb/test/bf_processed',
    placeholder='Type someting',               
    description='Save to:',
    disabled=False)

w_fname = widgets.Text(layout = widgets.Layout(width='140px', height='30px'), style = style,
    value='linescan_test',
    placeholder='Type someting',  
    description='as:',
    disabled=False)

space = widgets.HTML(layout = widgets.Layout(width='10px', height='30px'),
    value=" ")

start_button = widgets.Button(layout = widgets.Layout(width='82px', height='30px'),
    description='Start!',
    style=widgets.ButtonStyle(button_color='green'))


hspace10 = widgets.HTML(layout = widgets.Layout(width='100px', height='10px'),
    value=" ")


box1 = det_box
box2 = widgets.HBox([exp_box,num_box_bright])
box3 = widgets.HBox([num_box_dark,space,w_darkuid])
boxm1= widgets.HBox([motor1_box,motor1_button,space,motor1_start_box,motor1_stop_box,motor1_step_box])
box4 = widgets.HBox([w_saveto,w_fname,space,start_button])









output_counter = widgets.Output();
def on_button_clicked(b):

    with output_counter:
        
        clear_output()

        if w_det.value[0] == 'Blackfly':
            
            print('\n\nProcess started with %s\n'%(w_det.value))  
            start_button.description='running..'
            start_button.style=widgets.ButtonStyle(button_color='red')

            # dark---------------------------------------------------------------|
            if w_darkuid.value is '':
                print('taking dark (closing shutter)\n')
                tsd = time.time()
                if w_num_dark.value == 1:
                    det = blackfly_single
                    det.cam.num_images.put(1)
                else:
                    det = blackfly_multiple
                    det.cam.num_images.put(w_num_dark.value)   
                det.cam.acquire_time.put(w_exp.value)
                det.cam.acquire_period.put(0.05)
                time.sleep(1)
                dark_uid = RE(count([det],num=1))
                print('Dark collection finished in %.2f seconds\n'%(time.time() - tsd))
            else:
                print('Using previous dark\n')
                dark_uid = (w_darkuid.value,)
                
            # bright---------------------------------------------------------------|
            print('Taking bright (opening shutter)')
            if w_num_bright.value == 1:
                det = blackfly_single
                det.cam.num_images.put(1)
            else:
                det = blackfly_multiple
                det.cam.num_images.put(w_num_bright.value)   
            det.cam.acquire_time.put(w_exp.value)
            det.cam.acquire_period.put(0.05)
            time.sleep(1)
            
            tsb = time.time()
            plan = bp.scan([det], w_motor1.value , w_motor1_start.value , w_motor1_stop.value, w_motor1_step.value)
            bright_uid = RE(plan)
            print('Linescan finished in %.2f seconds\n'%(time.time() - tsb))
            print('closing shutter\n')                  
            
            det.unstage()
            
            if w_saveto.value and w_fname.value:

                info = {
                    'time':time.time(), 
                    'detector':w_det.value[0],  
                    'dark_uid':dark_uid[0], 
                    'num_dark':w_num_dark.value, 
                    'bright_uid':bright_uid[0],    
                    'num_bright':w_num_bright.value,    
                    'exposure':w_exp.value,  
                    'plan_type':'scan',                     
                    'motor':w_motor1.value.name, 
                    'motor_start':w_motor1_start.value, 
                    'motor_stop':w_motor1_stop.value, 
                    'motor_step':w_motor1_step.value, 
                }                 
                
                ts = time.time()
                print('Reading dark and bright data')                
                dark_data = np.array(list(db[dark_uid[0]].data('blackfly_det_image')))
                if dark_data.ndim == 4:
                    dark_data = np.median(dark_data,axis=1)    
                dark_data = np.median(dark_data,axis=0)                    
                bright_data = np.array(list(db[bright_uid[0]].data('blackfly_det_image')))
                if bright_data.ndim == 4:
                    bright_data = np.mean(bright_data,axis=1)               
                print('\nReading finished in %.2f seconds'%(time.time() - ts)) 
                
                if os.path.isfile('%s/%s.h5'%(w_saveto.value,w_fname.value)):
                    print('Saving data to: %s'%(w_saveto.value))
                    f = open('%s/%d_%s.yaml'%(w_saveto.value,int(time.time()),w_fname.value), 'w+')
                    yaml.dump(info, f, allow_unicode=True)
                    f.close()    
                    with h5py.File('%s/%d_%s.h5'%(w_saveto.value,int(time.time()),w_fname.value), 'w') as hf:
                        hf.create_dataset("dark_data", data=dark_data.astype('uint16'), compression=None)
                        hf.create_dataset("bright_data", data=bright_data.astype('uint16'), compression=None)
                else:       
                    f = open('%s/%s.yaml'%(w_saveto.value,w_fname.value), 'w+')
                    yaml.dump(info, f, allow_unicode=True)
                    f.close()        
                    with h5py.File('%s/%s.h5'%(w_saveto.value,w_fname.value), 'w') as hf:
                        hf.create_dataset("dark_data", data=dark_data.astype('uint16'), compression=None)
                        hf.create_dataset("bright_data", data=bright_data.astype('uint16'), compression=None)

            start_button.description='Start!'
            start_button.style=widgets.ButtonStyle(button_color='green')   
            
            print('\nFinished!')
                    
start_button.on_click(on_button_clicked);



ui_counter = widgets.HBox([box1,space,widgets.VBox([box2,box3,hspace10,boxm1,hspace10,box4])])
ui_linescan_acquire = widgets.VBox([hspace10,ui_counter,output_counter,hspace10]);

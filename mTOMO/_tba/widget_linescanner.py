
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

w_exp = widgets.FloatSlider(layout = widgets.Layout(width='263px', height='30px'), style = style,
    value=1.0,
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
    value=2,
    min=2,
    max=100,
    step=1,
    disabled=False,
    continuous_update=False,
    orientation='horizontal',
    readout=True,
    readout_format='d')
num_box_dark = widgets.HBox([widgets.Label('Collect dark:'), w_num_dark])


w_darkuid = widgets.Text(layout = widgets.Layout(width='340px', height='30px'), style = style,
    value=None,
    placeholder='Enter dark uid',               
    description='or re-use:',
    disabled=False)

w_num_bright = widgets.IntText(layout = widgets.Layout(width='52px', height='30px'), style = style,
    value=2,
    min=2,
    max=9999,
    step=1,
    disabled=False,
    continuous_update=False,
    orientation='horizontal',
    readout=True,
    readout_format='d')
num_box_bright = widgets.HBox([widgets.Label('Num bright:'), w_num_bright])


w_f1 = widgets.Checkbox(layout = widgets.Layout(width='30px', height='30px'),
    description='1',value=False,disabled=False,indent=False)
w_f2 = widgets.Checkbox(layout = widgets.Layout(width='30px', height='30px'),
    description='2',value=False,disabled=False,indent=False)
w_f3 = widgets.Checkbox(layout = widgets.Layout(width='30px', height='30px'),
    description='3',value=False,disabled=False,indent=False)
w_f4 = widgets.Checkbox(layout = widgets.Layout(width='30px', height='30px'),
    description='4',value=False,disabled=False,indent=False)
fltr_box = widgets.HBox([widgets.Label('Filters:'), w_f1,w_f2,w_f3,w_f4])

w_saveto = widgets.Text(layout = widgets.Layout(width='260px', height='30px'), style = style,
    value='/data/current_beamtime/test',
    placeholder='Type someting',               
    description='Save to:',
    disabled=False)

w_fname = widgets.Text(layout = widgets.Layout(width='120px', height='30px'), style = style,
    value='count_test',
    placeholder='Type someting',  
    description='as:',
    disabled=False)

space = widgets.HTML(layout = widgets.Layout(width='10px', height='30px'),
    value=" ")

button = widgets.Button(layout = widgets.Layout(width='82px', height='30px'),
    description='Start!',
    style=widgets.ButtonStyle(button_color='green'))


hspace10 = widgets.HTML(layout = widgets.Layout(width='100px', height='10px'),
    value=" ")


box1 = det_box
box2 = widgets.HBox([exp_box,num_box_bright])
box3 = widgets.HBox([num_box_dark,space,w_darkuid])
box4 = widgets.HBox([w_saveto,w_fname,space,button])



ui_counter = widgets.HBox([box1,space,widgets.VBox([box2,box3,box4])])
# display(ui_counter)

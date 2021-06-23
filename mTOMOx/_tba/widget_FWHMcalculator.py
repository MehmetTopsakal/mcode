
import matplotlib.pyplot as plt
import matplotlib

def plotter(tiff_path=None,x=1000,x_range=100,y=1000,y_range=100,
            vmin=10,vmax=20000,cmap='jet',print_code=False,ave_window=2,
            multiplier=1, calc_fwhm=False,window_size=100,export_fig_to=None):
    
    if not os.path.isfile(tiff_path):
        return
    else:
        img = multiplier*fabio.open(tiff_path).data.astype('int16')
    

    
    fig = plt.figure(figsize=(14,12))
    
    ax = fig.add_subplot('221')
#     ax.imshow(np.arcsinh(img).astype(np.float32), origin="upper", cmap="Greys_r",vmin=100,vmax=2000)
    i = ax.imshow(img, origin="upper", cmap=cmap,vmin=vmin,vmax=vmax)
    cb = fig.colorbar(i, orientation='vertical', shrink=0.5,anchor=(0.0,0.0))
    
    
    rect = matplotlib.patches.Rectangle((x-x_range/2, y-ave_window), x_range, ave_window*2,color='red',alpha=0.2) 
    ax.add_patch(rect)
    ax.arrow(x-x_range/2, y, x_range-ave_window, 0, head_width=ave_window/2, head_length=ave_window/2, fc='r', ec='r', alpha=0.5)
    
    rect = matplotlib.patches.Rectangle((x-ave_window, y-y_range/2), ave_window*2, y_range,color='green',alpha=0.2) 
    ax.add_patch(rect)
    ax.arrow(x, y-y_range/2, 0, y_range-ave_window, head_width=ave_window/2, head_length=ave_window/2, fc='g', ec='g', alpha=0.5)     
    
    
    rect = matplotlib.patches.Rectangle((x-window_size/2, y-window_size/2), window_size, window_size,color='yellow',alpha=0.2)                  
    ax.add_patch(rect)
    
    ax.set_title('...%s'%(tiff_path[-50:]))
    
    
    
    ax = fig.add_subplot('223')
    
    ax.plot(x,y,'+')
#     ax.imshow(np.arcsinh(img).astype(np.float32), origin="upper", cmap="Greys_r",vmin=vmin,vmax=vmax)
    ax.imshow(img, origin="upper", cmap=cmap,vmin=vmin,vmax=vmax)
    
    rect = matplotlib.patches.Rectangle((x-x_range/2, y-ave_window), x_range, ave_window*2,color='red',alpha=0.2) 
    ax.add_patch(rect)
    ax.arrow(x-x_range/2, y, x_range-ave_window, 0, head_width=ave_window/2, head_length=ave_window/2, fc='r', ec='r', alpha=0.5)
    
    rect = matplotlib.patches.Rectangle((x-ave_window, y-y_range/2), ave_window*2, y_range,color='green',alpha=0.2) 
    ax.add_patch(rect)
    ax.arrow(x, y-y_range/2, 0, y_range-ave_window, head_width=ave_window/2, head_length=ave_window/2, fc='g', ec='g', alpha=0.5) 
    
    ax.set_xlim([x-window_size/2,x+window_size/2])
    ax.set_ylim([y+window_size/2,y-window_size/2])
    
#     ax.set_xticks([])
#     ax.set_yticks([])  
    ax.set_title('Zoomed region',fontsize=10)

              
    ax = fig.add_subplot('222') 
    ROI = img[y-ave_window:y+ave_window,x-int(x_range/2):x+int(x_range/2)]
    ROI_ave_x = np.mean(ROI,axis=0)  
    
    

    
    ax.plot(ROI_ave_x-min(ROI_ave_x),'-r',lw=3) 
#     ax.plot(ROI_ave_x,'-r') 
        
    if calc_fwhm:
        fit_x = np.linspace(0,x_range,x_range)
        fit_y = ROI_ave_x-min(ROI_ave_x)
        
        mod = GaussianModel()    
        pars = mod.guess(fit_y, x=fit_x)
        out_g = mod.fit(fit_y, pars, x=fit_x)
        st = out_g.fit_report(min_correl=0.5)
        fwhm_g = st.split('fwhm:')[1].split()          
        
        mod = LorentzianModel()    
        pars = mod.guess(fit_y, x=fit_x)
        out_l = mod.fit(fit_y, pars, x=fit_x)
        st = out_l.fit_report(min_correl=0.5)
        fwhm_l = st.split('fwhm:')[1].split()
      
        mod = VoigtModel()    
        pars = mod.guess(fit_y, x=fit_x)
        out_v = mod.fit(fit_y, pars, x=fit_x)
        st = out_v.fit_report(min_correl=0.5)
        fwhm_v = st.split('fwhm:')[1].split()        
        
        fwhm_text_g = 'Gaussian=%.2f +/- %.2f'%(
                    float(fwhm_g[0])*(100/75),float(fwhm_g[2])*(100/75))
        fwhm_text_l = 'Lorentzian=%.2f +/- %.2f'%(
                    float(fwhm_l[0])*(100/75),float(fwhm_l[2])*(100/75))
        fwhm_text_v = 'Voigt=%.2f +/- %.2f'%(
                    float(fwhm_v[0])*(100/75),float(fwhm_v[2])*(100/75))
        
        ax.plot(out_g.best_fit,'--m', label=fwhm_text_g)  
        ax.plot(out_l.best_fit,'-.c', label=fwhm_text_l)  
        ax.plot(out_v.best_fit,':y',  label=fwhm_text_v)  
        ax.legend() 
    
    ax.set_xlabel('Pixel')
    ax.set_ylabel('Intensity')    
    ax.set_ylim([-20,vmax*1.15])
    ax.set_title('Horizontal profile')     
              
        
        
        
    ax = fig.add_subplot('224') 
    ROI = img[y-int(y_range/2):y+int(y_range/2),x-ave_window:x+ave_window]
    ROI_ave_y = np.mean(ROI,axis=1)   
    
    ax.plot(ROI_ave_y-min(ROI_ave_y),'-g',lw=3)
#     ax.plot(ROI_ave_y,'-g')
    
    if calc_fwhm:
        fit_x = np.linspace(0,y_range,y_range)
        fit_y = ROI_ave_y-min(ROI_ave_y) 
        
        mod = GaussianModel()    
        pars = mod.guess(fit_y, x=fit_x)
        out_g = mod.fit(fit_y, pars, x=fit_x)
        st = out_g.fit_report(min_correl=0.5)
        fwhm_l = st.split('fwhm:')[1].split()          
        
        mod = LorentzianModel()    
        pars = mod.guess(fit_y, x=fit_x)
        out_l = mod.fit(fit_y, pars, x=fit_x)
        st = out_l.fit_report(min_correl=0.5)
        fwhm_v = st.split('fwhm:')[1].split()
      
        mod = VoigtModel()    
        pars = mod.guess(fit_y, x=fit_x)
        out_v = mod.fit(fit_y, pars, x=fit_x)
        st = out_v.fit_report(min_correl=0.5)
        fwhm_g = st.split('fwhm:')[1].split()        
        
        fwhm_text_g = 'Gaussian=%.2f +/- %.2f'%(
                    float(fwhm_g[0])*(100/75),float(fwhm_g[2])*(100/75))
        fwhm_text_l = 'Lorentzian=%.2f +/- %.2f'%(
                    float(fwhm_l[0])*(100/75),float(fwhm_l[2])*(100/75))
        fwhm_text_v = 'Voigt=%.2f +/- %.2f'%(
                    float(fwhm_v[0])*(100/75),float(fwhm_v[2])*(100/75))
        
        ax.plot(out_g.best_fit,'--m', label=fwhm_text_g)  
        ax.plot(out_l.best_fit,'-.c', label=fwhm_text_l)  
        ax.plot(out_v.best_fit,':y',  label=fwhm_text_v)  
        ax.legend() 
    
    ax.set_xlabel('Pixel')
    ax.set_ylabel('Intensity')    
    ax.set_ylim([-20,vmax*1.15])
    ax.set_title('Vertical profile') 
    
    
    
    plt.tight_layout()
    

    
    
    if export_fig_to is not None:  
        plt.savefig(export_fig_to)    

    if print_code:
        print('\nplotter(tiff_path=\'%s\',\nx=%d,y=%d,x_range=%d,y_range=%d,vmin=%d,vmax=%d,ave_window=%d,window_size=%d,multiplier=%.2f,cmap=\'%s\',calc_fwhm=True)\n'%(tiff_path,x,y,x_range,y_range,vmin,vmax,ave_window,window_size,multiplier,cmap))

        
style = {'description_width': 'initial'}

wt = widgets.Text(layout = widgets.Layout(width='820px', height='30px'),
    value=None,
    placeholder='Type something',
    description='Tiff path:',
    disabled=False)


x_init = widgets.IntText(layout = widgets.Layout(width='140px', height='30px'),
    value=1130, description='Horizontal', disabled=False)
xs = widgets.IntSlider(
    value=x_init.value,min=0,max=2448,step=1, layout = widgets.Layout(width='500px', height='30px'), 
    description='',disabled=False,
    continuous_update=False,orientation='horizontal',readout=False,
    style = style)  
widgets.jslink((x_init, 'value'), (xs, 'value'))
x_range = widgets.IntSlider(
    value=100,min=10,max=2000,step=10, layout = widgets.Layout(width='200px', height='30px'), 
    description='',disabled=False,
    continuous_update=False,orientation='horizontal',readout=True,
    style = style)  


y_init = widgets.IntText(layout = widgets.Layout(width='140px', height='30px'),
    value=827, description='Vertical', disabled=False)
ys = widgets.IntSlider(
    value=y_init.value,min=0,max=2048,step=1, layout = widgets.Layout(width='500px', height='30px'), 
    description='',disabled=False,
    continuous_update=False,orientation='horizontal',readout=False,
    style = style)  
widgets.jslink((y_init, 'value'), (ys, 'value'))
y_range = widgets.IntSlider(
    value=100,min=10,max=2000,step=10, layout = widgets.Layout(width='200px', height='30px'), 
    description='',disabled=False,
    continuous_update=False,orientation='horizontal',readout=True,
    style = style)  


cmap_sel = widgets.Dropdown(
    layout = widgets.Layout(width='200px', height='30px'),
    options=['jet', 'viridis', 'Greys_r', 'binary', 'inferno', 'terrain'],
    value='jet',
    description='Color map:',
    disabled=False,
)


svmin= widgets.IntSlider(
    value=1000,min=0,max=2000,step=10, layout = widgets.Layout(width='250px', height='30px'), 
    description='vmin',disabled=False,
    continuous_update=False,orientation='horizontal',readout=True,
    style = style)  
svmax= widgets.IntSlider(
    value=10000,min=0,max=20000,step=10, layout = widgets.Layout(width='300px', height='30px'), 
    description='vmax',disabled=False,
    continuous_update=False,orientation='horizontal',readout=True,
    style = style)  


wft = widgets.FloatText(
    layout = widgets.Layout(width='130px', height='30px'),
    value=1.0,
    description='Multiplier:',
    disabled=False
)

wcb = widgets.Checkbox(
    layout = widgets.Layout(width='180px', height='30px'),
    value=False,
    description='Calc. FWHM',
    disabled=False,
    indent=False
)


wcb_code = widgets.Checkbox(
    layout = widgets.Layout(width='180px', height='30px'),
    value=False,
    description='Show code',
    disabled=False,
    indent=False
)

wis_aws= widgets.IntSlider(
    value=2,min=2,max=50,step=1, layout = widgets.Layout(width='300px', height='30px'), 
    description='Averaging window size',disabled=False,
    continuous_update=False,orientation='horizontal',readout=True,
    style = style)  



wis_ws= widgets.IntSlider(
    value=200,min=20,max=2000,step=10, layout = widgets.Layout(width='280px', height='30px'), 
    description='Fig. window size:',disabled=False,
    continuous_update=False,orientation='horizontal',readout=True, 
    style = style)  

wt_exportto = widgets.Text(layout = widgets.Layout(width='600px', height='30px'),
    value=None,style=style,
    placeholder='Type something',
    description='Export fig as:',
    disabled=False)


space10 = widgets.HTML(layout = widgets.Layout(width='10px', height='30px'),
    value=" ",
)


# this is quick
out = interactive_output(plotter, {"tiff_path":wt, "x":xs, "x_range":x_range, 
                                   "y":ys, "y_range":y_range, "ave_window":wis_aws,
                                   "cmap":cmap_sel, "vmin":svmin, "vmax":svmax,
                                   "multiplier":wft, "calc_fwhm":wcb, "window_size":wis_ws,
                                   "export_fig_to":wt_exportto,"print_code":wcb_code,
                                      })

hbox1 = HBox([x_init,xs,x_range])
hbox2 = HBox([y_init,ys,y_range])
hbox3 = HBox([cmap_sel,space10,svmin,svmax])
hbox4 = HBox([wft,wis_aws,wis_ws,wcb])
hbox5 = HBox([wt_exportto,space10,wcb_code])
ui = VBox([wt, hbox1, hbox2, hbox3, hbox4, hbox5]);

# display(ui, out);

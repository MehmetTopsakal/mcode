
def configure_area_det(det,acq_time,exposure,num_exposure=1):
    
    if det.cam.acquire.get() == 0:
        yield from bps.abs_set(det.cam.acquire, 1, wait=True)

    yield from bps.abs_set(det.cam.acquire_time, acq_time, wait=True)
    acq_time = det.cam.acquire_time.get()

    num_frame = np.ceil(exposure / acq_time)
    
    yield from bps.abs_set(det.images_per_set, num_frame, wait=True)
    
    yield from bps.abs_set(det.number_of_sets, num_exposure, wait=True)    

    print("{} is configured as: acq_time = {}; exposure = {} (num frames = {}); num_exposure = {}".format(det.name,det.cam.acquire_time.get(),exposure,num_frame,num_exposure))  
    
    
    return 



        
def beam_on(shutter_motor=None,sleep=0.1):
    if shutter_motor is None:
       shutter_motor = FastShutter
    shutter_motor.move(-7,wait=True)
    time.sleep(sleep)

def beam_off(shutter_motor=None,sleep=0.1):
    if shutter_motor is None:
       shutter_motor = FastShutter  
    shutter_motor.move(-47,wait=True)
    time.sleep(sleep)
    
    
        
        
def pud_switcher(ipdu, state='off', sleep=1.0, verbose=False):
    
    pdus = (pdu1,pdu2,pdu3,pdu4)
    
    if state.lower() == 'on' or state == 1:
        current_state = pdus[ipdu].get()
        if current_state == 1:
            if verbose:
                print('it is already on!')
        else:
            pdus[ipdu].put(1)
            time.sleep(sleep)
    if state.lower() == 'off' or state == 0:
        current_state = pdus[ipdu].get()
        if current_state == 0:
            if verbose:
                print('it is already off!')
        else:
            pdus[ipdu].put(0)
            time.sleep(sleep)
            
            


        
        
def read_tiff_as_xarray(tiffpath,
                       figsize=(6,6),
                       robust=True,
                       plot=False,
                       cbar=False,
                       mode=None):
    
    """
    Reads a tiff file as xarray
    """

    if mode == 'prosilica':
        img = fabio.open(tiffpath).data
    else:
        img = tifffile.imread(tiffpath).astype('float32')

    da = xr.DataArray(data=img,
                      coords=[np.arange(img.shape[0]),np.arange(img.shape[1])],
                      dims=['pixel_y', 'pixel_x'])

    if plot:

        fig = plt.figure(figsize=figsize)
        
        ax = fig.add_subplot(1,1,1)

        if not cbar:
            xp = da.plot.imshow(ax=ax,robust=robust,
                                yincrease=False,
                                cmap='Greys_r',
                                add_colorbar=cbar)
        else:
            xp = da.plot.imshow(ax=ax,robust=robust,
                                yincrease=False,
                                cmap='Greys_r',
                                cbar_kwargs=dict(orientation='vertical',
                                            pad=0.07, 
                                            shrink=0.4, 
                                            label='Intensity'))            
        
        xp.axes.set_aspect('equal', 'box')
     
        plt.tight_layout()

    
    return da
            

    
def print_det_keys(det_class):
    import pprint
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(det_class.tiff.__dict__)
    
    


    
    
    
    
    
# def sample_picture_taker(
    
#     ds_in = None,
    
#     cam1=prosilica_c,
#     cam1_acq_time=1,
#     cam1_exposure=1,

#     cam2=emergent_c,
#     cam2_acq_time=32,
#     cam2_exposure=32,
    
#     plot=True,
#     figsize=(8,4),
#     vmin1=None,
#     vmax1=None,
#     vmin2=None,
#     vmax2=None,
#     title1_motor1=mPhi,
#     title1_motor2=mTopY,
#     title2_motor1=mBaseX,
#     title2_motor2=mBaseY,
#     ROI1=None,
#     axv1=0,
#     axh1=0,
#     ROI2=None,
#     axv2=0,
#     axh2=0,


#     save_to=None,
#     save_name=None    
    
#     ):

    
#     if ds_in is None:
#         RE(configure_area_det(cam1,acq_time=cam1_acq_time,exposure=cam1_exposure))
#         RE(configure_area_det(cam2,acq_time=cam2_acq_time,exposure=cam2_exposure))


#         uid = RE(count([cam1,cam2],num=1))[0]

#         run = raw[-1]
#         ds  = run.primary.read()
        
#     else:
#         ds = ds_in
#         save_to=None
#         uid = ds.attrs['uid']
        
    
    

#     if plot:

#         fig = plt.figure(figsize=figsize,dpi=96)

#         ax = fig.add_subplot(1,2,1)

#         img_1 = ds['%s_image'%cam1.name]

#         if len(img_1.shape) == 5:
#                img_1 = img_1.mean(axis=-1)
#         img_1 = img_1.mean(axis=1)

#         img_1.isel(time=0).plot.imshow(robust=True,
#                                        yincrease=False,
#                                        ax=ax,
#                                        add_colorbar=True,
#                                        cmap='Greys_r',
#                                        vmin=vmin1, vmax=vmax1,
#                                        cbar_kwargs=dict(orientation='vertical',
#                                        pad=0.01, shrink=0.5))
#         ax.set_aspect('equal') 
#         ax.set_title('%s @ %.3f | %s @ %.3f'\
#                      %(title1_motor1.name,title1_motor1.position,title1_motor2.name,title1_motor2.position),
#                     fontsize=8)

#         ax.axvline(x=axv1,linestyle='--',color='r',alpha=0.5)
#         ax.axhline(y=axh1,linestyle=':',color='g',alpha=0.5)

#         if ROI1 is None:
#             pass
#         else:
#             ax.set_xlim(left=ROI1[0][0],right=ROI1[0][1])
#             ax.set_ylim(bottom=ROI1[1][1],top=ROI1[1][0])




#         ax = fig.add_subplot(1,2,2)

#         img_2 = ds['%s_image'%cam2.name]

#         if len(img_2.shape) == 5:
#                img_2 = img_2.mean(axis=-1)
#         img_2 = img_2.mean(axis=1)

#         img_2.isel(time=0).plot.imshow(robust=True,
#                                        yincrease=False,
#                                        ax=ax,
#                                        add_colorbar=True,
#                                        cmap='Greys_r',
#                                        vmin=vmin2, vmax=vmax2,
#                                        cbar_kwargs=dict(orientation='vertical',
#                                        pad=0.01, shrink=0.5))
#         ax.set_aspect('equal') 
#         ax.set_title('%s @ %.3f | %s @ %.3f'\
#                      %(title2_motor1.name,title2_motor1.position,title2_motor2.name,title2_motor2.position),
#                     fontsize=8)

#         ax.axvline(x=axv2,linestyle='--',color='b',alpha=0.5)
#         ax.axhline(y=axh2,linestyle=':',color='m',alpha=0.5)

#         if ROI1 is None:
#             pass
#         else:
#             ax.set_xlim(left=ROI2[0][0],right=ROI2[0][1])
#             ax.set_ylim(bottom=ROI2[1][1],top=ROI2[1][0])


#         plt.tight_layout()        
        
        
    


#     md={'type':'sample_picture',
#         'uid':uid,
#         'time': time.time(),   
#         'filter1':Filters.flt1.get(),
#         'filter2':Filters.flt2.get(),
#         'filter3':Filters.flt3.get(),
#         'filter4':Filters.flt4.get(), 
#         'mBaseX':mBaseX.position,
#         'mBaseY':mBaseY.position,
#         'mTopX':mTopX.position,
#         'mTopY':mTopY.position, 
#         'mTopZ':mTopZ.position,
#         'mPhi':mPhi.position,  
#         'mSlitsTop':mSlitsTop.position,     
#         'mSlitsBottom':mSlitsBottom.position,    
#         'mSlitsOutboard':mSlitsOutboard.position,   
#         'mSlitsInboard':mSlitsInboard.position,     
#         'mPitch':mPitch.position,       
#         'mRoll':mRoll.position,      
#         'mDexelaPhi':mDexelaPhi.position,       
#         'mQuestarX':mQuestarX.position,      
#         'mSigrayX':mSigrayX.position,    
#         'mSigrayY':mSigrayY.position,    
#         'mSigrayZ':mSigrayZ.position,    
#         'mSigrayPitch':mSigrayPitch.position,   
#         'mSigrayYaw':mSigrayYaw.position,     
#         'FastShutter':FastShutter.position, 
#         'RingCurrent':ring_current.get(),
#         'mHexapodsZ':mHexapodsZ.position,
#         'ePhi':ePhi.position,


#         'cam1':cam1.name,
#         'cam1_acq_time':cam1_acq_time,
#         'cam1_exposure':cam1_exposure,

#         'cam2':cam2.name,
#         'cam2_acq_time':cam2_acq_time,
#         'cam2_exposure':cam2_exposure,        
        
#         'axv1':axv1,
#         'axh1':axh1,
#         'axv2':axv2,
#         'axh2':axh2,
#        }

#     ds.attrs = md
    
    
    
#     if save_to:
#         comp = dict(zlib=True, dtype='float32')
#         encoding = {var: comp for var in ds.data_vars}
#         if save_name is None:
#             save_name = 'sample_picture'
#         ds.to_netcdf('%s/%d_%s.nc'%(save_to,ds.attrs['time'],save_name), encoding=encoding) 
#         print('%s/%d_%s.nc'%(save_to,ds.attrs['time'],save_name))    
    
    
#     return ds





    
    
    
def counter(det, 
            acq_time,
            num_exposure=1,
            expo_dark=0, 
            expo_bright=0, 
            auto_off=True
            ):

    
    ds = xr.Dataset()

    
    if expo_dark>0:

        beam_off()
        RE(configure_area_det(det,acq_time,exposure=expo_dark,num_exposure=num_exposure))
        uid = RE(count([det],num=1))[0]
        
        img = np.array(list(db[-1].data('%s_image'%(det.name))))

        img = img.mean(axis=(0,1))
        if det.name == 'prosilica':
            img = np.mean(img,-1)
        
        da = xr.DataArray(data=img.astype('float32'),
                  coords=[np.arange(img.shape[0]), np.arange(img.shape[1])],
                  dims=['pixel_y', 'pixel_x'],attrs=dict(uid=uid,
                                                         det=det.name,
                                                         acq_time=acq_time,
                                                         exposure=expo_dark)
                              )
        ds['dark'] = da
        


    if expo_bright>0:

        beam_on()
        RE(configure_area_det(det,acq_time,exposure=expo_bright,num_exposure=num_exposure))
        uid = RE(count([det],num=1))[0]
        
        if auto_off:
            beam_off()
        
        img = np.array(list(db[-1].data('%s_image'%(det.name))))

        img = img.mean(axis=(0,1))
        if det.name == 'prosilica':
            img = np.mean(img,-1)

        da = xr.DataArray(data=img.astype('float32'),
                  coords=[np.arange(img.shape[0]), np.arange(img.shape[1])],
                  dims=['pixel_y', 'pixel_x'],attrs=dict(uid=uid,
                                                         det=det.name,
                                                         acq_time=acq_time,
                                                         exposure=expo_bright)
                              )
        ds['bright'] = da



    md={'type': 'count',
        'time': time.time(),   
        'filter1':Filters.flt1.get(),
        'filter2':Filters.flt2.get(),
        'filter3':Filters.flt3.get(),
        'filter4':Filters.flt4.get(), 
        'mBaseX':mBaseX.position,
        'mBaseY':mBaseY.position,
        'mTopX':mTopX.position,
        'mTopY':mTopY.position, 
        'mTopZ':mTopZ.position,
        'mPhi':mPhi.position,  
        'mSlitsTop':mSlitsTop.position,     
        'mSlitsBottom':mSlitsBottom.position,    
        'mSlitsOutboard':mSlitsOutboard.position,   
        'mSlitsInboard':mSlitsInboard.position,     
        'mPitch':mPitch.position,       
        'mRoll':mRoll.position,      
        'mDexelaPhi':mDexelaPhi.position,       
        'mQuestarX':mQuestarX.position,      
        'mSigrayX':mSigrayX.position,    
        'mSigrayY':mSigrayY.position,    
        'mSigrayZ':mSigrayZ.position,    
        'mSigrayPitch':mSigrayPitch.position,   
        'mSigrayYaw':mSigrayYaw.position,     
        'FastShutter':FastShutter.position, 
        'RingCurrent':ring_current.get(),
        'mHexapodsZ':mHexapodsZ.position,
        'ePhi':ePhi.position,
       }

    ds.attrs = md
    
    
    return ds



def scanner(det, 
            motor,
            acq_time,
            num_exposure=1,
            expo_dark=0, 
            expo_bright=0, 
            
            motor_start = -0.1,
            motor_stop =  0.1,
            motor_nstep = 11, 
            
            come_back = False

            ):

    
    ds = xr.Dataset()
    
    motor_initial_pos = motor.position

    
    if expo_dark>0:

        beam_off()
        RE(configure_area_det(det,acq_time,exposure=expo_dark,num_exposure=1))
        uid = RE(count([det],num=1))[0]
        
        img = np.array(list(db[-1].data('%s_image'%(det.name))))
        if det.name == 'prosilica':
            img = np.mean(img,-1)
        img = img.mean(axis=(0,1))

        da = xr.DataArray(data=img.astype('float32'),
                  coords=[np.arange(img.shape[0]), np.arange(img.shape[1])],
                  dims=['pixel_y', 'pixel_x'],attrs=dict(uid=uid,
                                                         det=det.name,
                                                         acq_time=acq_time,
                                                         exposure=expo_dark)
                              )
        ds['dark'] = da
        


    if expo_bright>0:

        beam_on()
        RE(configure_area_det(det,acq_time,exposure=expo_bright,num_exposure=1))
        uid = RE(scan([det],motor,motor_start,motor_stop,motor_nstep))[0]
        beam_off()
        
        imgs = np.array(list(db[-1].data('%s_image'%(det.name))))
        if det.name == 'prosilica':
            imgs = np.mean(imgs,-1)
        imgs = imgs.mean(axis=(1))
        
        motor_pos = np.linspace(motor_start,motor_stop,motor_nstep)

        da = xr.DataArray(data=imgs.astype('float32'),
                  coords=[motor_pos, np.arange(imgs.shape[1]), np.arange(imgs.shape[2])],
                  dims=[motor.name,'pixel_y', 'pixel_x'],attrs=dict(uid=uid,
                                                                    det=det.name,
                                                                    acq_time=acq_time,
                                                                    exposure=expo_bright,
                                                                    motor=motor.name,
                                                                    motor_start=motor_start,
                                                                    motor_stop=motor_stop,
                                                                    motor_nstep=motor_nstep,
                                                                    motor_initial_pos=motor_initial_pos
                                                                    )
                              )
        ds['scan'] = da
        
        if come_back:
            print('moving back')
            motor.move(motor_initial_pos)



    md={'type': 'scan',
        'time': time.time(),   
        'filter1':Filters.flt1.get(),
        'filter2':Filters.flt2.get(),
        'filter3':Filters.flt3.get(),
        'filter4':Filters.flt4.get(), 
        'mBaseX':mBaseX.position,
        'mBaseY':mBaseY.position,
        'mTopX':mTopX.position,
        'mTopY':mTopY.position, 
        'mTopZ':mTopZ.position,
        'mPhi':mPhi.position,  
        'mSlitsTop':mSlitsTop.position,     
        'mSlitsBottom':mSlitsBottom.position,    
        'mSlitsOutboard':mSlitsOutboard.position,   
        'mSlitsInboard':mSlitsInboard.position,     
        'mPitch':mPitch.position,       
        'mRoll':mRoll.position,      
        'mDexelaPhi':mDexelaPhi.position,       
        'mQuestarX':mQuestarX.position,      
        'mSigrayX':mSigrayX.position,    
        'mSigrayY':mSigrayY.position,    
        'mSigrayZ':mSigrayZ.position,    
        'mSigrayPitch':mSigrayPitch.position,   
        'mSigrayYaw':mSigrayYaw.position,     
        'FastShutter':FastShutter.position, 
        'RingCurrent':ring_current.get(),
        'mHexapodsZ':mHexapodsZ.position,
        'ePhi':ePhi.position,
       }

    ds.attrs = md
    
    
    return ds

    
    
    
    
    
    
"""  

LEGACY:   
    
    
    
def counter(det,exposure_time=1, take_dark=False, take_bright=True, num_dark = 3, num_bright = 2):

    ds = xr.Dataset()

    
    if take_dark:
        set_detector(det,exposure_time=exposure_time,num_images=num_dark)

#         laser_off()
#         light1_off()
#         light2_off()

        beam_off()
        uid_dark = RE(count([det],num=1))[0]
        
        if det.name == 'prosilica':
            tiffs = get_tiff_list(hdr=db[-1])
            t0 = fabio.open(tiffs[0]).data
            img_dark = np.zeros((len(tiffs),t0.shape[0],t0.shape[1]))
            for e,t in enumerate(tiffs):
                img_dark[e,:,:] = fabio.open(tiffs[e]).data
        else:
            img_dark = np.array(list(db[-1].data('%s_image'%(det.name))))
            

        if len(img_dark.shape) == 4:
            img_dark = img_dark.mean(axis=1)
            img_dark = img_dark.mean(axis=0)
        if len(img_dark.shape) == 3:
            img_dark = img_dark.mean(axis=0)
            
        da_dark = xr.DataArray(data=img_dark.astype('float32'),
                  coords=[np.arange(img_dark.shape[0]), np.arange(img_dark.shape[1])],
                  dims=['pixel_y', 'pixel_x'],attrs=None
                 )
        ds['dark'] = da_dark
        dark_taken = 'true'
        
    else:
        uid_dark = 'none'
        num_dark = 'none'
        dark_taken = 'false'

    
    if take_bright:
        beam_on()
        set_detector(det,exposure_time=exposure_time,num_images=num_bright)
        uid_bright = RE(count([det],num=1))[0]
        beam_off()
        bright_taken = 'true'
    else:
        uid_bright = 'none'
        bright_taken = 'false'
        
        
    if bright_taken == 'true':
        if det.name == 'prosilica':
            tiffs = get_tiff_list(hdr=db[-1])
            t0 = fabio.open(tiffs[0]).data
            img_bright = np.zeros((len(tiffs),t0.shape[0],t0.shape[1]))
            for e,t in enumerate(tiffs):
                img_bright[e,:,:] = fabio.open(tiffs[e]).data
        else:
            img_bright = np.array(list(db[-1].data('%s_image'%(det.name))))

        if len(img_bright.shape) == 4:
            img_bright = img_bright.mean(axis=1)
            img_bright = img_bright.mean(axis=0)
        if len(img_bright.shape) == 3:
            img_bright = img_bright.mean(axis=0)


        da_bright = xr.DataArray(data=img_bright.astype('float32'),
                  coords=[np.arange(img_bright.shape[0]), np.arange(img_bright.shape[1])],
                  dims=['pixel_y', 'pixel_x'],attrs=None
                 )
        ds['bright'] = da_bright
        


    md={'type': 'count',
        'time': time.time(),
        'detector':det.name,
        'exposure_time':exposure_time,
        'dark_taken': dark_taken,
        'bright_taken': bright_taken,
        'uid_dark':uid_dark,
        'num_dark':num_dark, 
        'uid_bright':uid_bright,   
        'num_bright':num_bright,    
        'filter1':Filters.flt1.value,
        'filter2':Filters.flt2.value,
        'filter3':Filters.flt3.value,
        'filter4':Filters.flt4.value, 
        'mXBase':mXBase.position,
        'mYBase':mYBase.position,
        'mStackX':mStackX.position,
        'mStackY':mStackY.position, 
        'mStackZ':mStackZ.position,
        'mPhi':mPhi.position,  
        'mSlitsTop':mSlitsTop.position,     
        'mSlitsBottom':mSlitsBottom.position,    
        'mSlitsOutboard':mSlitsOutboard.position,   
        'mSlitsInboard':mSlitsInboard.position,     
        'mPitch':mPitch.position,       
        'mRoll':mRoll.position,      
        'mDexelaPhi':mDexelaPhi.position,       
        'mQuestarX':mQuestarX.position,      
        'mSigrayX':mSigrayX.position,    
        'mSigrayY':mSigrayY.position,    
        'mSigrayZ':mSigrayZ.position,    
        'mSigrayPitch':mSigrayPitch.position,   
        'mSigrayYaw':mSigrayYaw.position,     
        'FastShutter':FastShutter.position,      
       }

    ds.attrs = md
    
    
    return ds






def scanner(det,
            
            exposure_time=0.5, 
            
            take_dark=False, 
            num_dark = 10, 

            
            motor = mStackX,
            motor_start = -0.1,
            motor_stop =  0.1,
            motor_nstep = 11,


           ):

    ds = xr.Dataset()

    
    if take_dark:
        beam_off()
        set_detector(det,exposure_time=exposure_time,num_images=num_dark)
        uid_dark = RE(count([det],num=1))[0]
        
        if det.name == 'prosilica':
            tiffs = get_tiff_list(hdr=db[-1])
            t0 = fabio.open(tiffs[0]).data
            img_dark = np.zeros((len(tiffs),t0.shape[0],t0.shape[1]))
            for e,t in enumerate(tiffs):
                img_dark[e,:,:] = fabio.open(tiffs[e]).data
        else:
            img_dark = np.array(list(db[-1].data('%s_image'%(det.name))))
            
#         tiff_cleaner(hdr=db[-1])
        if len(img_dark.shape) == 4:
            img_dark = img_dark.mean(axis=0)
            img_dark = img_dark.mean(axis=0)
        elif len(img_dark.shape) == 3:
            img_dark = img_dark.mean(axis=0)
            
        da_dark = xr.DataArray(data=img_dark.astype('float32'),
                  coords=[np.arange(img_dark.shape[0]), np.arange(img_dark.shape[1])],
                  dims=['pixel_y', 'pixel_x'],attrs=None
                 )
        ds['dark'] = da_dark
        dark_taken = 'true'
        
    else:
        uid_dark = 'none'
        num_dark = 'none'
        dark_taken = 'false'

    
    beam_on()
    set_detector(det,exposure_time=exposure_time,num_images=1)
    uid_scan = RE(scan([det],motor,motor_start,motor_stop,motor_nstep))[0]
    beam_off()
    
    if det.name == 'prosilica':
        tiffs = get_tiff_list(hdr=db[-1])
        t0 = fabio.open(tiffs[0]).data
        imgs_scan = np.zeros((len(tiffs),t0.shape[0],t0.shape[1]))
        for e,t in enumerate(tiffs):
            imgs_scan[e,:,:] = fabio.open(tiffs[e]).data
    else:
        imgs_scan = np.array(list(db[-1].data('%s_image'%(det.name))))
        
    print(imgs_scan.shape)
    
    if len(imgs_scan.shape) == 4:
        imgs_scan = imgs_scan.mean(axis=1)
        
    motor_pos = np.linspace(motor_start,motor_stop,motor_nstep)
        
#     tiff_cleaner(hdr=db[-1])
   
    da_scan = xr.DataArray(data=imgs_scan.astype('float32'),
              coords=[motor_pos,np.arange(imgs_scan.shape[1]), np.arange(imgs_scan.shape[2])],
              dims=[motor.name,'pixel_y', 'pixel_x'],attrs=None
             )
    ds['scan'] = da_scan


    md={'type': 'scan',
        'time': time.time(),
        'detector':det.name,
        'exposure_time':exposure_time,
        'dark_taken': dark_taken,
        'uid_dark':uid_dark,
        'num_dark':num_dark, 
        'uid_bright':uid_scan,      
        'filter1':Filters.flt1.value,
        'filter2':Filters.flt2.value,
        'filter3':Filters.flt3.value,
        'filter4':Filters.flt4.value, 
        'mXBase':mXBase.position,
        'mYBase':mYBase.position,
        'mStackX':mStackX.position,
        'mStackY':mStackY.position, 
        'mStackZ':mStackZ.position,
        'mPhi':mPhi.position,  
        'mSlitsTop':mSlitsTop.position,     
        'mSlitsBottom':mSlitsBottom.position,    
        'mSlitsOutboard':mSlitsOutboard.position,   
        'mSlitsInboard':mSlitsInboard.position,     
        'mPitch':mPitch.position,       
        'mRoll':mRoll.position,      
        'mDexelaPhi':mDexelaPhi.position,       
        'mQuestarX':mQuestarX.position,      
        'mSigrayX':mSigrayX.position,    
        'mSigrayY':mSigrayY.position,    
        'mSigrayZ':mSigrayZ.position,    
        'mSigrayPitch':mSigrayPitch.position,   
        'mSigrayYaw':mSigrayYaw.position,     
        'FastShutter':FastShutter.position,      
       }

    ds.attrs = md
    
    
    return ds







    
    
def ds_saver(ds,save_to,save_str='_',zlib=False,dtype='float32'):
    comp = dict(zlib=zlib, dtype=dtype)
    encoding = {var: comp for var in ds.data_vars}
    ds.to_netcdf('%s/%d_%s.nc'%(save_to,ds.attrs['time'],save_str), encoding=encoding)    
    
    
    
    
    
    
    
    
    
    
    
    
    




def set_detector(det,exposure_time=1.0,num_images=1,sleep=0.5):
    if det.name == 'prosilica':
        det.proc.enable_filter.put(0,wait=True)
        det.cam.acquire_time.put(exposure_time)
        det.cam.acquire_period.put(0.5)     
        if num_images > 1:
            print('Multiple mode doesnt work well!!!')
            det.cam.stage_sigs['image_mode'] = 'Multiple'
            det.cam.num_images.put(num_images)
            det.cam.image_mode.put(1)       
        else:
            det.cam.stage_sigs['image_mode'] = 'Single'
            det.cam.num_images.put(1)
            det.cam.image_mode.put(0)
        det.cam.trigger_mode.put(0)
        det.unstage()
        time.sleep(sleep)    
        
    elif det.name == 'blackfly':
        det.proc.enable_filter.put(0,wait=True)
        det.cam.acquire_time.put(exposure_time)    
        det.cam.acquire_period.put(exposure_time)     
        if num_images > 1:
            det.cam.stage_sigs['image_mode'] = 'Multiple'
            det.cam.num_images.put(num_images)
            det.cam.image_mode.put(1)
        else:
            det.cam.stage_sigs['image_mode'] = 'Single'
            det.cam.num_images.put(1)
            det.cam.image_mode.put(0)
        det.cam.trigger_mode.put(0)
        det.unstage()
        time.sleep(sleep)
        
    elif det.name == 'emergent':
        det.proc.enable_filter.put(0,wait=True)
        det.cam.acquire_time.put(exposure_time)
        det.cam.acquire_period.put(exposure_time)             
        if num_images > 1:        
            det.cam.stage_sigs['image_mode'] = 'Multiple'    
            det.cam.stage_sigs['num_images'] = num_images
            det.cam.num_images.put(num_images)  
            det.cam.image_mode.put(1)        
        else:
            det.cam.stage_sigs['image_mode'] = 'Single'
            det.cam.num_images.put(1)
            det.cam.image_mode.put(0)
#         det.cam.trigger_mode.put(0)
        det.unstage()
        time.sleep(sleep)
        
    elif det.name == 'dexela':
        det.proc.enable_filter.put(0,wait=True)
        det.cam.stage_sigs['image_mode'] = 'Multiple'        
        det.cam.stage_sigs['trigger_mode'] = 'Int. Free Run'        
        det.cam.acquire_time.put(exposure_time)
        det.cam.acquire_period.put(exposure_time+0.02)
        if num_images > 1:
            det.cam.stage_sigs['image_mode'] = 'Multiple'
            det.cam.num_images.put(num_images)
            det.cam.image_mode.put(1)
        else:
            det.cam.stage_sigs['image_mode'] = 'Single'
            det.cam.num_images.put(1)
            det.cam.image_mode.put(0)
        det.cam.trigger_mode.put(0)
        det.unstage()
        time.sleep(sleep)



RE(bps.mv(Filters.flt1, 'Out')) 
RE(bps.mv(Filters.flt2, 'Out'))
RE(bps.mv(Filters.flt3, 'Out'))
RE(bps.mv(Filters.flt4, 'In'))
""" 

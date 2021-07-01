 

def set_detector(det,exposure_time=1.0,num_images=1,sleep=0.5):
    if det.name == 'prosilica':
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

        

        
def beam_on():
    FastShutter.move(-7)
    time.sleep(1)

def beam_off():
    FastShutter.move(-47)
    time.sleep(1)
    
    
        
        
def pud_switcher(ipdu,state='off',sleep=1.0, verbose=False):
    
    pdus = (pdu1,pdu2,pdu3,pdu4)
    
    if state == 'on':
        current_state = pdus[ipdu].value
        if current_state == 1:
            if verbose:
                print('it is already on!')
        else:
            pdus[ipdu].put(1)
            time.sleep(sleep)
    elif state == 'off':
        current_state = pdus[ipdu].value
        if current_state == 0:
            if verbose:
                print('it is already off!')
        else:
            pdus[ipdu].put(0)
            time.sleep(sleep)
            
            

        
        
def get_tiff_list(hdr):

    for name, doc in hdr.documents():       
        if name=='start':
            npts = doc.num_points           
        if name=='resource':
            fpp   = doc.resource_kwargs['frame_per_point'] 
            tpath = os.path.join(doc.root,doc.resource_path)
            fname = doc.resource_kwargs['filename'] 
    tiffs = ['%s/%s_%6.6d.tiff'%(tpath,fname,i) for i in range(npts*fpp)] 
    return tiffs
            
            
            
            
def tiff_cleaner(hdr):

    for name, doc in hdr.documents():       
        if name=='start':
            npts = doc.num_points           
        if name=='resource':
            fpp   = doc.resource_kwargs['frame_per_point'] 
            tpath = os.path.join(doc.root,doc.resource_path)
            fname = doc.resource_kwargs['filename'] 
    tiffs = ['%s/%s_%6.6d.tiff'%(tpath,fname,i) for i in range(npts*fpp)] 
    for t in tiffs:
        os.remove(t)

            
            
"""           
RE(bps.mv(Filters.flt1, 'Out')) 
RE(bps.mv(Filters.flt2, 'Out'))
RE(bps.mv(Filters.flt3, 'Out'))
RE(bps.mv(Filters.flt4, 'In'))
""" 

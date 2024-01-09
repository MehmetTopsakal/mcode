from matplotlib.gridspec import GridSpec
import requests
import PIL
import io
import pprint
import tifffile


def md_getter(init_dict={},read_smartpods=True):

    import time

    md = init_dict

    md['timestamp'] = time.time()

    md['time'] = time.strftime('%Y/%m/%d - %H:%M:%S')


    for f in [Filters.flt1,Filters.flt2,Filters.flt3,Filters.flt4]:
        md[f.name] = f.get()    


    for m in [FastShutter,
              mTopX, 
              mTopY, 
              mTopZ, 
              mPhi,
              ePhi,
              mRoll, 
              mPitch,
              mBaseX,
              mBaseY,
              mDexelaPhi,
              mBeamStopY,
              mHexapodsZ,
              mSlitsYGap,    
              mSlitsYCtr,    
              mSlitsXGap,    
              mSlitsXCtr,    
              mSlitsTop,     
              mSlitsBottom,  
              mSlitsOutboard,
              mSlitsInboard, 
              mSigrayX,    
              mSigrayY,    
              mSigrayZ,    
              mSigrayPitch,
              mSigrayYaw,
             ]:
            try:
                md[m.name] = float('%.4f'%m.position)
            except:
                print('\nunable to read %s'%m.name)

    if read_smartpods:
        sSmartPodUnit.set(0)
        time.sleep(0.2)
        sSmartPodSync.set(1)
        time.sleep(0.2)
        for s in [
                 sSmartPodUnit, 
                 sSmartPodTrasZ,
                 sSmartPodTrasX,
                 sSmartPodTrasY,
                 sSmartPodRotZ, 
                 sSmartPodRotX, 
                 sSmartPodRotY, 
                 sSmartPodSync, 
                 sSmartPodMove, 
                 ]:
                md['%s_0'%s.name] = float('%.5f'%s.get())            

        sSmartPodUnit.set(1)
        time.sleep(0.2)
        sSmartPodSync.set(1)
        time.sleep(0.2)
        for s in [
                 sSmartPodUnit, 
                 sSmartPodTrasZ,
                 sSmartPodTrasX,
                 sSmartPodTrasY,
                 sSmartPodRotZ, 
                 sSmartPodRotX, 
                 sSmartPodRotY, 
                 sSmartPodSync, 
                 sSmartPodMove, 
                 ]:
                md['%s_1'%s.name] = float('%.5f'%s.get())    

    for s in [
             pdu1,pdu2,pdu3,pdu4,ring_current 
             ]:
            md[s.name] = float('%.2f'%s.get())  

    return md








def beam_on(shutter_motor=None,sleep=0.1):
    if shutter_motor is None:
        shutter_motor =  FastShutter
    shutter_motor.move(-20,wait=True)
    time.sleep(sleep)

def beam_off(shutter_motor=None,sleep=0.1):
    if shutter_motor is None:
        shutter_motor =  FastShutter
    shutter_motor.move(20,wait=True)
    time.sleep(sleep)



def counter(count_params,auto_beam_off=True):
    
    detectors_jsonable = {}
    dets = []
    
    for i in count_params['detectors']:
        if i[0] == 'dexela_hdf5':
            det = dexela_hdf5
        if i[0] == 'dexela_tiff':
            det = dexela_tiff
        if i[0] == 'prosilica_hdf5':
            det = prosilica_hdf5
        if i[0] == 'prosilica_tiff':
            det = prosilica_tiff
        if i[0] == 'blackfly_hdf5':
            det = blackfly_hdf5
        if i[0] == 'blackfly_tiff':
            det = blackfly_tiff
        if i[0] == 'emergent_hdf5':
            det = emergent_hdf5
        if i[0] == 'emergent_tiff':
            det = emergent_tiff
        if i[0] == 'alliedvision_hdf5':
            det = alliedvision_hdf5
        if i[0] == 'alliedvision_tiff':
            det = alliedvision_tiff
        if i[0] == 'xs3':
            det = xs3

        dets.append(det)
        
        RE(configure_det(det=det,acq_time=i[1],exposure=i[2],num_exposures=i[3]))
        detectors_jsonable['%s_acq_time'%det.name] = i[1]
        detectors_jsonable['%s_exposure'%det.name] = i[2]
        try:
            detectors_jsonable['%s_num_exposures'%det.name] = i[3]
            detectors_jsonable['%s_lx'%det.name] = int(i[4][3:])
            detectors_jsonable['%s_ly'%det.name] = int(i[5][3:])
        # except Exception as exc:
        except:
            # print(exc)
            pass

    # dets = [d[0] for d in count_params['detectors']]
    count_params['detectors']=detectors_jsonable 


    if count_params['uid_dark'] == None:
        count_params['uid_dark'] = 'none'
    elif count_params['uid_dark'] == 'None':
        count_params['uid_dark'] = 'none'
    else:
        try:
            count_params['uid_dark'] = raw[count_params['uid_dark']]._item["attributes"]["metadata"]["start"]['uid']
        except:
            print('......invalid uid_dark, ignoring %s as uid_dark'%count_params['uid_dark'])
            count_params['uid_dark'] = 'none'
        
    if count_params['beam'] == 'true':
        beam_on()
    else:
        beam_off()
        
    uid, = RE(count(dets),md_user=md_getter(count_params))
    print(uid)
    
    if auto_beam_off:
        beam_off()
     
    return uid














def scanner(scan_params,beam=True,auto_beam_off=True):



    if scan_params['take_dark'] == 'true':

        beam_off()
        print('\n>>>> Taking dark\n') 

        dark_detectors_jsonable = {}
        dark_dets = []
        for i in scan_params['dark_detectors']:
            if i[0] == 'dexela_hdf5':
                det = dexela_hdf5
            if i[0] == 'dexela_tiff':
                det = dexela_tiff
            if i[0] == 'prosilica_hdf5':
                det = prosilica_hdf5
            if i[0] == 'prosilica_tiff':
                det = prosilica_tiff
            if i[0] == 'blackfly_hdf5':
                det = blackfly_hdf5
            if i[0] == 'blackfly_tiff':
                det = blackfly_tiff
            if i[0] == 'emergent_hdf5':
                det = emergent_hdf5
            if i[0] == 'emergent_tiff':
                det = emergent_tiff
            if i[0] == 'alliedvision_hdf5':
                det = alliedvision_hdf5
            if i[0] == 'alliedvision_tiff':
                det = alliedvision_tiff
            if i[0] == 'xs3':
                det = xs3
    
            dark_dets.append(det)
            
            RE(configure_det(det=det,acq_time=i[1],exposure=i[2],num_exposures=i[3]))
            dark_detectors_jsonable['%s_acq_time'%det.name] = i[1]
            dark_detectors_jsonable['%s_exposure'%det.name] = i[2]
            try:
                dark_detectors_jsonable['%s_num_exposures'%det.name] = i[3]
            except:
                pass

        
        uid_dark, = RE(count(dark_dets))
        scan_params['uid_dark'] = uid_dark

        print('\n>>>> Dark uid=%se\n'%uid_dark) 

    
        
    elif scan_params['uid_dark'] == None:
        scan_params['uid_dark'] = 'none'
    elif scan_params['uid_dark'] == None:
        scan_params['uid_dark'] = 'none'
    else:
        try:
            scan_params['uid_dark'] = raw[scan_params['uid_dark']]._item["attributes"]["metadata"]["start"]['uid']
        except:
            print('......invalid uid_dark, ignoring %s as uid_dark'%scan_params['uid_dark'])
            scan_params['uid_dark'] = 'none'

    



    
    detectors_jsonable = {}
    dets = []
    
    for i in scan_params['detectors']:
        print(i[0])
        
        if i[0] == 'dexela_hdf5':
            det = dexela_hdf5
        if i[0] == 'dexela_tiff':
            det = dexela_tiff
        if i[0] == 'prosilica_hdf5':
            det = prosilica_hdf5
        if i[0] == 'prosilica_tiff':
            det = prosilica_tiff
        if i[0] == 'blackfly_hdf5':
            det = blackfly_hdf5
        if i[0] == 'blackfly_tiff':
            det = blackfly_tiff
        if i[0] == 'emergent_hdf5':
            det = emergent_hdf5
        if i[0] == 'emergent_tiff':
            det = emergent_tiff
        if i[0] == 'alliedvision_hdf5':
            det = alliedvision_hdf5
        if i[0] == 'alliedvision_tiff':
            det = alliedvision_tiff
        if i[0] == 'xs3':
            det = xs3

        dets.append(det)
        
        RE(configure_det(det=det,acq_time=i[1],exposure=i[2],num_exposures=i[3]))
        detectors_jsonable['%s_acq_time'%det.name] = i[1]
        detectors_jsonable['%s_exposure'%det.name] = i[2]
        try:
            detectors_jsonable['%s_num_exposures'%det.name] = i[3]
        except:
            pass

    scan_params['detectors']=detectors_jsonable 


    for m in [mBaseX,mBaseY,mPhi,mTopX,mTopY,mTopZ]:
        if m.name == scan_params['motor']:
            motor = m
    motor_jsonable = motor.name
    scan_params['motor'] = motor_jsonable
    motor_start = scan_params['motor_start'] 
    motor_stop = scan_params['motor_stop']
    motor_nstep = scan_params['motor_nstep']

    if scan_params['beam']:
        beam_on()
    else:
        beam_off()

    print('\nINFO: Starting linescan\n')
    motor_current_pos = motor.position
    print('>>> %s @ %.3f'%(motor.name,motor_current_pos))

    
    uid, = RE(scan(dets,motor,motor_start,motor_stop,motor_nstep),md_user=md_getter(scan_params))

    if scan_params['auto_beam_off'] == 'true':
        beam_off()

    print('\n>>>> Scan uid=%se\n'%uid) 

    if scan_params['come_back'] == 'true':
        print('>>> Moving %s back to %.3f'%(motor.name,motor_current_pos))
     
    return uid


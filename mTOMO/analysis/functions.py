
import matplotlib.pyplot as plt
import matplotlib    
        

def read_count(dbnum,read_data=False,ave_method='median'):
   
    hdr = db[dbnum]
    
    events = []
    for name, doc in hdr.documents():       
        if name=='start':
            npts = doc.num_points 
            detector_name = doc.detectors[0]            
        if name=='resource':
            fpp   = doc.resource_kwargs['frame_per_point'] 
            tpath = os.path.join(doc.root,doc.resource_path)
            fname = doc.resource_kwargs['filename'] 
        if name=='event':
            events.append(doc.data)          
     
    tiffs = ['%s/%s_%6.6d.tiff'%(tpath,fname,i) for i in range(npts*fpp)]   
    
    if detector_name == 'dexela':
        stats = [i['dexela_stats1_total'] for i in events]
    elif detector_name == 'blackfly_det':
        try:
            stats = [i['blackfly_det_stats1_total'] for i in events]
        except:
            stats = []
    else:
        stats = [] 
 
    if read_data:
        if detector_name == 'dexela':
            data = np.array(list(hdr.data('dexela_image')))
            if data.ndim == 4:
                if ave_method == 'median':
                    data = np.median(data, axis=1)
                else:
                    data = np.mean(data, axis=1)
        elif detector_name == 'blackfly_det':
            data = np.array(list(hdr.data('blackfly_det_image')))
            if data.ndim == 4:
                if ave_method == 'median':
                    data = np.median(data, axis=1)
                else:
                    data = np.mean(data, axis=1)                                   
    else:
        data = []
            
    return tiffs,fpp,data






def read_linescan(dbnum,plot=True,read_data=False,figsize=(8,5),ave_method='mean'):  
    
    hdr = db[dbnum]
    
    events = []
    for name, doc in hdr.documents():       
        if name=='start':
            npts = doc.num_points 
            motor_name = doc.motors[0]
            detector_name = doc.detectors[0]            
        if name=='resource':
            fpp   = doc.resource_kwargs['frame_per_point'] 
            tpath = os.path.join(doc.root,doc.resource_path)
            fname = doc.resource_kwargs['filename'] 
        if name=='event':
            events.append(doc.data)          
            
    tiffs = ['%s/%s_%6.6d.tiff'%(tpath,fname,i) for i in range(npts*fpp)]   
    motor_positions = [i[motor_name] for i in events]
    
    
    if detector_name == 'dexela':
        stats = [i['dexela_stats1_total'] for i in events]
    elif detector_name == 'blackfly_det':
        try:
            stats = [i['blackfly_det_stats1_total'] for i in events]
        except:
            stats = []
    else:
        stats = []
        
    
    if plot:
        fig = plt.figure(figsize=figsize)
        ax1 = fig.add_subplot('111')
        ax1.plot(stats)
        ax1.set_xticks(range(len(stats)))
        ax1.set_xticklabels(['%.3f'%(i) for e,i in enumerate(motor_positions)])
        ax1.set_xlabel(motor_name)
        plt.setp(ax1.get_xticklabels(), rotation=-60);
        ax2 = ax1.twiny() 
        ax2.plot(stats,'o')
        ax2.set_xticks(range(len(stats)))
        ax2.grid(True,linestyle=':')
        ax2.set_title(str(dbnum))
        plt.setp(ax2.get_xticklabels(), rotation=90);    
        
    if read_data:
        if detector_name == 'dexela':
            data = np.array(list(hdr.data('dexela_image')))
            if data.ndim == 4:
                if ave_method == 'median':
                    data = np.median(data, axis=1)
                else:
                    data = np.mean(data, axis=1)
        elif detector_name == 'blackfly_det':
            data = np.array(list(hdr.data('blackfly_det_image')))
            if data.ndim == 4:
                if ave_method == 'median':
                    data = np.median(data, axis=1)
                else:
                    data = np.mean(data, axis=1)                               
    else:
        data = []
            
    return tiffs,fpp,data,events





def average_tiffs(ostr,tiffs,sel=None):
    
    if sel is None:
        tiffs_str = ' '.join([str(elem) for elem in tiffs])
        sp.call('pyFAI-average --method median --format tif -o %s %s'%(ostr,tiffs_str),shell=True)
    else:
        tiffs_sel = [tiffs[i] for i in sel]
        print(tiffs_sel)
        tiffs_str = ' '.join([str(elem) for elem in tiffs_sel])
        sp.call('pyFAI-average --method median --format tif -o %s %s'%(ostr,tiffs_str),shell=True)
        
        

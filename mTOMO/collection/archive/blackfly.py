
"""
# See https://cars9.uchicago.edu/software/epics/PointGreyDoc.html

NumImages:	
    Controls the number of images to acquire. 
    When TriggerMode=Internal this is handled in software. 
    When TriggerMode=Multi-shot it is handled in the camera firmware.
    
NumExposures:
    Controls the number of exposures per image when TriggerMode="Multi-exposure" or "Multi-exposure bulb".    
    
AcquireTime:
    Controls the acquisition time per image. 
    default=2.0sec
    
AcquirePeriod:
    Controls the period between images. 
    default=0.03876sec
    
"""


import time


from nslsii.ad33 import StatsPluginV33

from ophyd import (AreaDetector, 
                   CamBase, 
                   TIFFPlugin, 
                   Component as Cpt, 
                   ImagePlugin,
                   HDF5Plugin, 
                   Device, 
                   StatsPlugin, 
                   ProcessPlugin, 
                   ADComponent,
                   ROIPlugin, 
                   EpicsSignal, 
                   SingleTrigger,
                   PointGreyDetectorCam)

from ophyd.areadetector.filestore_mixins import (FileStoreTIFFIterativeWrite,
                                                 FileStoreHDF5IterativeWrite,
                                                 FileStoreTIFFSquashing,
                                                 FileStoreTIFF,
                                                 FileStoreHDF5, new_short_uid,
                                                 FileStoreBase
                                                 )

class XPDDBlackFlyTiffPlugin(TIFFPlugin, FileStoreTIFFIterativeWrite, Device):
    def get_frames_per_point(self):
        if self.parent.cam.image_mode.get(as_string=True) == 'Single':
            return 1
        return super().get_frames_per_point()

    

from enum import Enum   
class XPDDMode(Enum):
    step = 1
    fly = 2    
    
    
    
class XPDDBlackFlyDetector(SingleTrigger, AreaDetector):
    """PointGrey Black Fly detector(s) as used by 28-ID-D"""
    stats1 = Cpt(StatsPluginV33, 'Stats1:')    
    cam = ADComponent(PointGreyDetectorCam, "cam1:")
    image = ADComponent(ImagePlugin, "image1:")
    tiff = Cpt(XPDDBlackFlyTiffPlugin, 'TIFF1:',
               read_attrs=[],
               configuration_attrs=[],
               write_path_template='/data/st/test/',
               read_path_template='/data/st/test/',
               root='/data/st/')
    
    wait_for_plugins = Cpt(EpicsSignal, '')
    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._mode = XPDDMode.step
        
        self.cam.stage_sigs['image_mode'] = 'Single'
        self.cam.stage_sigs['trigger_mode'] = 'Off'
            
    def stage(self, *args, **kwargs):
        return super().stage(*args, **kwargs)

    def unstage(self):
        try:
            ret = super().unstage()
        finally:
            self._mode = XPDDMode.step
        return ret
    

    
    
    
    
def set_blackfly(det,exposure_time=1.0,num_images=1):
    
    det.cam.acquire_time.put(exposure_time)
    det.cam.acquire_period.put(0.05)     

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
    
    time.sleep(2)
    
    
    
    
    
    
"""  
blackfly = XPDDBlackFlyDetector('XF:28IDD-BI{Det-BlackFly}', name="blackfly")
blackfly.read_attrs = ['tiff']

save_to = 'dummy'
os.makedirs('/data/bf_data/%s'%(save_to),exist_ok=True)
blackfly.tiff.write_path_template = '/data/bf_data/%s/'%(save_to)
blackfly.tiff.read_path_template = '/data/bf_data/%s/'%(save_to)

blackfly.stats1.kind = 'hinted'
blackfly.stats1.total.kind = 'hinted' 
"""

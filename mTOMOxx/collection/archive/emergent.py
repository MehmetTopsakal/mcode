

import time

import ophyd


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
                   EmergentVisionDetectorCam)

from ophyd.areadetector.filestore_mixins import (FileStoreTIFFIterativeWrite,
                                                 FileStoreHDF5IterativeWrite,
                                                 FileStoreTIFFSquashing,
                                                 FileStoreTIFF,
                                                 FileStoreHDF5, new_short_uid,
                                                 FileStoreBase
                                                 )


class XPDDEmergentTiffPlugin(TIFFPlugin, FileStoreTIFFIterativeWrite, Device):
    def get_frames_per_point(self):
        if self.parent.cam.image_mode.get(as_string=True) == 'Single':
            return 1
        return super().get_frames_per_point()
 
    
from enum import Enum   
class XPDDMode(Enum):
    step = 1
    fly = 2  
    
    

class XPDDEmergentDetector(SingleTrigger, AreaDetector):
    """Emergent Vision detector(s) as used by 28-ID-D"""
    stats1 = Cpt(StatsPluginV33, 'Stats1:')    
    cam = ADComponent(EmergentVisionDetectorCam, "cam1:")
    image = ADComponent(ImagePlugin, "image1:")
#     tiff = Cpt(XPDDEmergentTiffPlugin, 'TIFF1:',
#                read_attrs=[],
#                configuration_attrs=[],
#                write_path_template='N:\\\\emergent_data\\\\', 
#                read_path_template='N:\\\\emergent_data\\\\', 
#                root='N:\\\\',) 
    tiff = Cpt(XPDDEmergentTiffPlugin, 'TIFF1:',
               read_attrs=[],
               configuration_attrs=[],
               write_path_template='Z:\\\\2020-3\\\\test\\\\', 
               read_path_template='Z:\\\\2020-3\\\\test\\\\', 
               root='Z:\\\\2020-3\\\\',) 
    
    wait_for_plugins = Cpt(EpicsSignal, '')
    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._mode = XPDDMode.step
        
        self.cam.stage_sigs['image_mode'] = 'Single'
        self.cam.stage_sigs['pixel_format'] = '12 Bit'
        self.cam.stage_sigs['data_type'] = 'UInt16'
        self.cam.stage_sigs['color_mode'] = 'Mono'
        self.cam.stage_sigs['trigger_mode'] = 'Internal'
            
    def stage(self, *args, **kwargs):
        return super().stage(*args, **kwargs)

    def unstage(self):
        try:
            ret = super().unstage()
        finally:
            self._mode = XPDDMode.step
        return ret
    

    
    
    
    
def set_emergent(det,exposure_time=15.0,num_images=1):
    
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
    
    time.sleep(2)
    

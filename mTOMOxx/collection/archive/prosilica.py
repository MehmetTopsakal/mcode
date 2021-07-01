
import time as ttime  # tea time
from types import SimpleNamespace
from datetime import datetime
from ophyd import (ProsilicaDetector, SingleTrigger, TIFFPlugin,
                   ImagePlugin, StatsPlugin, DetectorBase, HDF5Plugin,
                   AreaDetector, EpicsSignal, EpicsSignalRO, ROIPlugin,
                   TransformPlugin, ProcessPlugin, Device)
from ophyd.areadetector.cam import AreaDetectorCam
from ophyd.areadetector.base import ADComponent, EpicsSignalWithRBV
from ophyd.areadetector.filestore_mixins import (FileStoreTIFFIterativeWrite,
                                                 FileStoreHDF5IterativeWrite,
                                                 FileStoreBase, new_short_uid,
                                                 FileStoreIterativeWrite)
from ophyd import Component as Cpt, Signal
from ophyd.utils import set_and_wait
from pathlib import PurePath
from bluesky.plan_stubs import stage, unstage, open_run, close_run, trigger_and_read, pause
from collections import OrderedDict


class TIFFPluginWithFileStore(TIFFPlugin, FileStoreTIFFIterativeWrite):
    """Add this as a component to detectors that write TIFFs."""
    pass


class TIFFPluginEnsuredOff(TIFFPlugin):
    """Add this as a component to detectors that do not write TIFFs."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.stage_sigs.update([('auto_save', 'No')])


class StandardProsilica(SingleTrigger, ProsilicaDetector):
    image = Cpt(ImagePlugin, 'image1:')
    stats1 = Cpt(StatsPlugin, 'Stats1:')
    stats2 = Cpt(StatsPlugin, 'Stats2:')
    stats3 = Cpt(StatsPlugin, 'Stats3:')
    stats4 = Cpt(StatsPlugin, 'Stats4:')
    stats5 = Cpt(StatsPlugin, 'Stats5:')
    trans1 = Cpt(TransformPlugin, 'Trans1:')
    roi1 = Cpt(ROIPlugin, 'ROI1:')
    roi2 = Cpt(ROIPlugin, 'ROI2:')
    roi3 = Cpt(ROIPlugin, 'ROI3:')
    roi4 = Cpt(ROIPlugin, 'ROI4:')
    proc1 = Cpt(ProcessPlugin, 'Proc1:')

    # This class does not save TIFFs. We make it aware of the TIFF plugin
    # only so that it can ensure that the plugin is not auto-saving.
    tiff = Cpt(TIFFPluginEnsuredOff, suffix='TIFF1:')

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('labels', ['cameras'])
        super().__init__(*args, **kwargs)
        self.stats1.total.kind = 'hinted'


class StandardProsilicaWithTIFF(StandardProsilica):
    tiff = Cpt(TIFFPluginWithFileStore,
               suffix='TIFF1:',
               write_path_template='/data/current/ps_data',
               root='/data/current/')
    
    
    
    
    
    
def set_prosilica(det,exposure_time=1.0,num_images=1):  
    
    det.cam.acquire_time.put(exposure_time)
    det.cam.acquire_period.put(0.5)     

    if num_images > 1:
        print('Multiple mode is not supported!!!')
#         det.cam.stage_sigs['image_mode'] = 'Multiple'
#         det.cam.num_images.put(num_images)
#         det.cam.image_mode.put(1)
        det.cam.stage_sigs['image_mode'] = 'Single'
        det.cam.num_images.put(1)
        det.cam.image_mode.put(0)        
        
    else:
        det.cam.stage_sigs['image_mode'] = 'Single'
        det.cam.num_images.put(1)
        det.cam.image_mode.put(0)

    det.cam.trigger_mode.put(0)
    
    det.unstage()
    
    time.sleep(2)

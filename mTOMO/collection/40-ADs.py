from ophyd.areadetector.filestore_mixins import (FileStoreTIFFIterativeWrite,
                                                 FileStoreHDF5IterativeWrite,
                                                 FileStoreTIFFSquashing,
                                                 FileStoreTIFF,
                                                 FileStoreHDF5, new_short_uid,
                                                 FileStoreBase
                                                 )

from ophyd.areadetector import (AreaDetector, PixiradDetectorCam, ImagePlugin,
                                TIFFPlugin, StatsPlugin, HDF5Plugin,
                                ProcessPlugin, ROIPlugin, TransformPlugin,
                                OverlayPlugin)

from ophyd import Component as C

from ophyd import Signal, EpicsSignal, EpicsSignalRO 
from nslsii.ad33 import SingleTriggerV33, StatsPluginV33

from ophyd.device import BlueskyInterface
from ophyd.device import DeviceStatus

from ophyd import (AreaDetector, CamBase, TIFFPlugin, Component as Cpt,
                   HDF5Plugin, Device, StatsPlugin, ProcessPlugin,
                   ROIPlugin, EpicsSignal, set_and_wait)
from ophyd.areadetector import (EpicsSignalWithRBV as SignalWithRBV)

from ophyd.areadetector.filestore_mixins import FileStoreIterativeWrite



# Some of the code below is from
# https://github.com/NSLS-II-HXN/hxntools/blob/master/hxntools/detectors
# and
# https://github.com/NSLS-II-XPD/profile_collection



class XPDTIFFPlugin(TIFFPlugin, FileStoreTIFFSquashing,
                    FileStoreIterativeWrite):
    pass


class ContinuousAcquisitionTrigger(BlueskyInterface):
    """
    This trigger mixin class records images when it is triggered.

    It expects the detector to *already* be acquiring, continously.
    """
    def __init__(self, *args, plugin_name=None, image_name=None, **kwargs):
        if plugin_name is None:
            raise ValueError("plugin name is a required keyword argument")
        super().__init__(*args, **kwargs)
        self._plugin = getattr(self, plugin_name)
        if image_name is None:
            image_name = '_'.join([self.name, 'image'])
        self._plugin.stage_sigs[self._plugin.auto_save] = 'No'
        
        #self.cam.stage_sigs[self.cam.image_mode] = 'Continuous'
        # MT: For Emergent to work
        self.cam.stage_sigs['image_mode'] = 'Continuous'
        self.cam.stage_sigs['acquire'] = 1        
        
        self._plugin.stage_sigs[self._plugin.file_write_mode] = 'Capture'
        self._image_name = image_name
        self._status = None
        self._num_captured_signal = self._plugin.num_captured
        self._num_captured_signal.subscribe(self._num_captured_changed)
        self._save_started = False

    def stage(self):
        
        if self.cam.acquire.get() != 1:
            raise RuntimeError("The ContinuousAcuqisitionTrigger expects "
                               "the detector to already be acquiring.")   

#         if self.cam.acquire.get() != 1:
#             self.cam.acquire.put(1,wait=False)

        return super().stage()
        # put logic to look up proper dark frame
        # die if none is found

    def trigger(self):
        "Trigger one acquisition."
        if not self._staged:
            raise RuntimeError("This detector is not ready to trigger."
                               "Call the stage() method before triggering.")
        self._save_started = False
        self._status = DeviceStatus(self)
        self._desired_number_of_sets = self.number_of_sets.get()
        self._plugin.num_capture.put(self._desired_number_of_sets)
        self.dispatch(self._image_name, ttime.time())
        # reset the proc buffer, this needs to be generalized
        self.proc.reset_filter.put(1)
        self._plugin.capture.put(1)  # Now the TIFF plugin is capturing.
        return self._status

    def _num_captured_changed(self, value=None, old_value=None, **kwargs):
        "This is called when the 'acquire' signal changes."
        if self._status is None:
            return
        if value == self._desired_number_of_sets:
            # This is run on a thread, so exceptions might pass silently.
            # Print and reraise so they are at least noticed.
            try:
                self.tiff.write_file.put(1)
            except Exception as e:
                print(e)
                raise
            self._save_started = True
        if value == 0 and self._save_started:
            self._status._finished()
            self._status = None
            self._save_started = False
            
            
            
            
            
#=========================================================================#
#=============================Dexela======================================#
#=========================================================================#            
class DexelaDetectorCam(CamBase):
    acquire_gain = Cpt(EpicsSignal, 'DEXAcquireGain')
    acquire_offset = Cpt(EpicsSignal, 'DEXAcquireOffset')
    binning_mode = Cpt(SignalWithRBV, 'DEXBinningMode')
    corrections_dir = Cpt(EpicsSignal, 'DEXCorrectionsDir', string=True)
    current_gain_frame = Cpt(EpicsSignal, 'DEXCurrentGainFrame')
    current_offset_frame = Cpt(EpicsSignal, 'DEXCurrentOffsetFrame')
    defect_map_available = Cpt(EpicsSignal, 'DEXDefectMapAvailable')
    defect_map_file = Cpt(EpicsSignal, 'DEXDefectMapFile', string=True)
    full_well_mode = Cpt(SignalWithRBV, 'DEXFullWellMode')
    gain_available = Cpt(EpicsSignal, 'DEXGainAvailable')
    gain_file = Cpt(EpicsSignal, 'DEXGainFile', string=True)
    load_defect_map_file = Cpt(EpicsSignal, 'DEXLoadDefectMapFile')
    load_gain_file = Cpt(EpicsSignal, 'DEXLoadGainFile')
    load_offset_file = Cpt(EpicsSignal, 'DEXLoadOffsetFile')
    num_gain_frames = Cpt(EpicsSignal, 'DEXNumGainFrames')
    num_offset_frames = Cpt(EpicsSignal, 'DEXNumOffsetFrames')
    offset_available = Cpt(EpicsSignal, 'DEXOffsetAvailable')
    offset_constant = Cpt(SignalWithRBV, 'DEXOffsetConstant')
    offset_file = Cpt(EpicsSignal, 'DEXOffsetFile', string=True)
    save_gain_file = Cpt(EpicsSignal, 'DEXSaveGainFile')
    save_offset_file = Cpt(EpicsSignal, 'DEXSaveOffsetFile')
    serial_number = Cpt(EpicsSignal, 'DEXSerialNumber')
    software_trigger = Cpt(EpicsSignal, 'DEXSoftwareTrigger')
    use_defect_map = Cpt(EpicsSignal, 'DEXUseDefectMap')
    use_gain = Cpt(EpicsSignal, 'DEXUseGain')
    use_offset = Cpt(EpicsSignal, 'DEXUseOffset')

class DexelaDetector(AreaDetector):
    cam = Cpt(DexelaDetectorCam, 'cam1:',
              read_attrs=[],
              configuration_attrs=['image_mode', 'trigger_mode',
                                   'acquire_time', 'acquire_period'],
              )

class XPDTOMODexela(DexelaDetector):
    image = C(ImagePlugin, 'image1:')
    _default_configuration_attrs = (
        DexelaDetector._default_configuration_attrs +
        ('images_per_set', 'number_of_sets', 'pixel_size'))
    tiff = C(XPDTIFFPlugin, 'TIFF1:',
             write_path_template='/a/b/c/',
             read_path_template='/a/b/c',
             cam_name='cam', 
             proc_name='proc',  
             read_attrs=[],
             root='/nsls2/data/xpd/tomo/legacy/raw/')

    proc = C(ProcessPlugin, 'Proc1:')

    # These attributes together replace `num_images`. They control
    # summing images before they are stored by the detector (a.k.a. "tiff
    # squashing").
    images_per_set = C(Signal, value=1, add_prefix=())
    number_of_sets = C(Signal, value=1, add_prefix=())

    pixel_size = C(Signal, value=.000075, kind='config')
    detector_type = C(Signal, value='Dexela 2923', kind='config')
    stats1 = C(StatsPluginV33, 'Stats1:')
    stats2 = C(StatsPluginV33, 'Stats2:')
    stats3 = C(StatsPluginV33, 'Stats3:')
    stats4 = C(StatsPluginV33, 'Stats4:')
    stats5 = C(StatsPluginV33, 'Stats5:', kind = 'hinted')

    roi1 = C(ROIPlugin, 'ROI1:')
    roi2 = C(ROIPlugin, 'ROI2:')
    roi3 = C(ROIPlugin, 'ROI3:')
    roi4 = C(ROIPlugin, 'ROI4:')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.stage_sigs.update([(self.cam.trigger_mode, 'Int. Software')])
    
    
class DexelaContinuous(ContinuousAcquisitionTrigger, XPDTOMODexela):
    pass

# Dexela detector configurations:
dexela_pv_prefix = 'XF:28IDD-ES:2{Det:DEX}'
dexela_c = DexelaContinuous(dexela_pv_prefix, name='dexela',
                             read_attrs=['tiff', 'stats1.total'],
                             plugin_name='tiff')
dexela_c.tiff.read_path_template = f'/nsls2/data/xpd/tomo/legacy/raw/{dexela_c.name}_data/%Y/%m/%d/'
dexela_c.tiff.write_path_template = f'J:\\dexela_data\\%Y\\%m\\%d\\'
dexela_c.cam.bin_x.kind = 'config'
dexela_c.cam.bin_y.kind = 'config'
dexela_c.detector_type.kind = 'config'
dexela_c.stats1.kind = 'hinted'
dexela_c.stats1.total.kind = 'hinted' 
    
    

    
#=========================================================================#
#=============================Blackfly====================================#
#=========================================================================#  
class BlackflyDetectorCam(CamBase):
    pass    
    
class BlackflyDetector(AreaDetector):
    cam = Cpt(BlackflyDetectorCam, 'cam1:',
              read_attrs=[],
              configuration_attrs=['image_mode', 'trigger_mode',
                                   'acquire_time', 'acquire_period'],
              )

class XPDTOMOBlackfly(BlackflyDetector):
    image = C(ImagePlugin, 'image1:')
    _default_configuration_attrs = (
        BlackflyDetector._default_configuration_attrs +
        ('images_per_set', 'number_of_sets', 'pixel_size'))
    tiff = C(XPDTIFFPlugin, 'TIFF1:',
             write_path_template='/a/b/c/',
             read_path_template='/a/b/c',
             cam_name='cam',  
             proc_name='proc',
             read_attrs=[],
             root='/nsls2/data/xpd/tomo/legacy/raw/')

    proc = C(ProcessPlugin, 'Proc1:')

    # These attributes together replace `num_images`. They control
    # summing images before they are stored by the detector (a.k.a. "tiff
    # squashing").
    images_per_set = C(Signal, value=1, add_prefix=())
    number_of_sets = C(Signal, value=1, add_prefix=())

    pixel_size = C(Signal, value=.000005, kind='config') #unknown
    detector_type = C(Signal, value='Blackfly S', kind='config')
    stats1 = C(StatsPluginV33, 'Stats1:')
    stats2 = C(StatsPluginV33, 'Stats2:')
    stats3 = C(StatsPluginV33, 'Stats3:')
    stats4 = C(StatsPluginV33, 'Stats4:')
    stats5 = C(StatsPluginV33, 'Stats5:', kind = 'hinted')

    roi1 = C(ROIPlugin, 'ROI1:')
    roi2 = C(ROIPlugin, 'ROI2:')
    roi3 = C(ROIPlugin, 'ROI3:')
    roi4 = C(ROIPlugin, 'ROI4:')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.stage_sigs.update([(self.cam.trigger_mode, 'Off')])
        
class BlackflyContinuous(ContinuousAcquisitionTrigger, XPDTOMOBlackfly):
    pass

# Blackfly detector configurations:
blackfly_pv_prefix = 'XF:28IDD-BI{Det-BlackFly}'
blackfly_c = BlackflyContinuous(blackfly_pv_prefix, name='blackfly',
                             read_attrs=['tiff', 'stats1.total'],
                             plugin_name='tiff')

blackfly_c.tiff.read_path_template = f'/nsls2/data/xpd/tomo/legacy/raw/{blackfly_c.name}_data/%Y/%m/%d/'
blackfly_c.tiff.write_path_template = f'/nsls2/data/xpd/tomo/legacy/raw/{blackfly_c.name}_data/%Y/%m/%d/'
blackfly_c.cam.bin_x.kind = 'config'
blackfly_c.cam.bin_y.kind = 'config'
blackfly_c.detector_type.kind = 'config'
blackfly_c.stats1.kind = 'hinted'
blackfly_c.stats1.total.kind = 'hinted' 
        
        
        
        
#=========================================================================#
#=============================Emergent====================================#
#=========================================================================# 
class EmergentDetectorCam(CamBase):
    pass

class EmergentDetector(AreaDetector):
    cam = Cpt(EmergentDetectorCam, 'cam1:',
              read_attrs=[],
              configuration_attrs=['image_mode', 'trigger_mode',
                                   'acquire_time', 'acquire_period'],
              )

class XPDTOMOEmergent(EmergentDetector):
    image = C(ImagePlugin, 'image1:')
    _default_configuration_attrs = (
        EmergentDetector._default_configuration_attrs +
        ('images_per_set', 'number_of_sets', 'pixel_size'))
    tiff = C(XPDTIFFPlugin, 'TIFF1:',
             write_path_template='/a/b/c/',
             read_path_template='/a/b/c',
             cam_name='cam',  
             proc_name='proc', 
             read_attrs=[],
             root='/nsls2/data/xpd/tomo/legacy/raw/')

    proc = C(ProcessPlugin, 'Proc1:')

    # These attributes together replace `num_images`. They control
    # summing images before they are stored by the detector (a.k.a. "tiff
    # squashing").
    images_per_set = C(Signal, value=1, add_prefix=())
    number_of_sets = C(Signal, value=1, add_prefix=())

    pixel_size = C(Signal, value=.000005, kind='config') #unknown
    detector_type = C(Signal, value='Emergent', kind='config')
    stats1 = C(StatsPluginV33, 'Stats1:')
    stats2 = C(StatsPluginV33, 'Stats2:')
    stats3 = C(StatsPluginV33, 'Stats3:')
    stats4 = C(StatsPluginV33, 'Stats4:')
    stats5 = C(StatsPluginV33, 'Stats5:', kind = 'hinted')

    roi1 = C(ROIPlugin, 'ROI1:')
    roi2 = C(ROIPlugin, 'ROI2:')
    roi3 = C(ROIPlugin, 'ROI3:')
    roi4 = C(ROIPlugin, 'ROI4:')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.stage_sigs.update([(self.cam.trigger_mode, 'Internal')])
        self.stage_sigs.update([(self.cam.data_type, 'UInt16')])
        self.stage_sigs.update([(self.cam.color_mode, 'Mono')])
        
class EmergentContinuous(ContinuousAcquisitionTrigger, XPDTOMOEmergent):
    pass

# emergent detector configurations:
emergent_pv_prefix = 'XF:28IDD-EM1{EVT-Cam:1}'
emergent_c = EmergentContinuous(emergent_pv_prefix, name='emergent',
                             read_attrs=['tiff', 'stats1.total'],
                             plugin_name='tiff')

emergent_c.tiff.read_path_template = f'/nsls2/data/xpd/tomo/legacy/raw/{emergent_c.name}_data/%Y/%m/%d/'
emergent_c.tiff.write_path_template = f'J:\\emergent_data\\%Y\\%m\\%d\\'
emergent_c.cam.bin_x.kind = 'config'
emergent_c.cam.bin_y.kind = 'config'
emergent_c.detector_type.kind = 'config'
emergent_c.stats1.kind = 'hinted'
emergent_c.stats1.total.kind = 'hinted'  



        
        
        




#=========================================================================#
#=============================Prosilica===================================#
#=========================================================================#  
class ProsilicaDetectorCam(CamBase):
    pass    
    
class ProsilicaDetector(AreaDetector):
    cam = Cpt(ProsilicaDetectorCam, 'cam1:',
              read_attrs=[],
              configuration_attrs=['image_mode', 'trigger_mode',
                                   'acquire_time', 'acquire_period'],
              )

class XPDTOMOProsilica(ProsilicaDetector):
    image = C(ImagePlugin, 'image1:')
    _default_configuration_attrs = (
        ProsilicaDetector._default_configuration_attrs +
        ('images_per_set', 'number_of_sets', 'pixel_size'))
    tiff = C(XPDTIFFPlugin, 'TIFF1:',
             write_path_template='/a/b/c/',
             read_path_template='/a/b/c',
             cam_name='cam',  
             proc_name='proc',
             read_attrs=[],
             root='/nsls2/data/xpd/tomo/legacy/raw/')

    proc = C(ProcessPlugin, 'Proc1:')

    # These attributes together replace `num_images`. They control
    # summing images before they are stored by the detector (a.k.a. "tiff
    # squashing").
    images_per_set = C(Signal, value=1, add_prefix=())
    number_of_sets = C(Signal, value=1, add_prefix=())

    pixel_size = C(Signal, value=.000005, kind='config') #unknown
    detector_type = C(Signal, value='Prosilica', kind='config')
    stats1 = C(StatsPluginV33, 'Stats1:')
    stats2 = C(StatsPluginV33, 'Stats2:')
    stats3 = C(StatsPluginV33, 'Stats3:')
    stats4 = C(StatsPluginV33, 'Stats4:')
    stats5 = C(StatsPluginV33, 'Stats5:', kind = 'hinted')

    roi1 = C(ROIPlugin, 'ROI1:')
    roi2 = C(ROIPlugin, 'ROI2:')
    roi3 = C(ROIPlugin, 'ROI3:')
    roi4 = C(ROIPlugin, 'ROI4:')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.stage_sigs.update([(self.cam.trigger_mode, 'Free Run')])
        
class ProsilicaContinuous(ContinuousAcquisitionTrigger, XPDTOMOProsilica):
    pass

# Prosilica detector configurations:
prosilica_pv_prefix = 'XF:28IDD-BI{Det-Sample:1}'
prosilica_c = ProsilicaContinuous(prosilica_pv_prefix, name='prosilica',
                             read_attrs=['tiff', 'stats1.total'],
                             plugin_name='tiff')

prosilica_c.tiff.read_path_template = f'/nsls2/data/xpd/tomo/legacy/raw/{prosilica_c.name}_data/%Y/%m/%d/'
prosilica_c.tiff.write_path_template = f'/nsls2/data/xpd/tomo/legacy/raw/{prosilica_c.name}_data/%Y/%m/%d/'
prosilica_c.cam.bin_x.kind = 'config'
prosilica_c.cam.bin_y.kind = 'config'
prosilica_c.detector_type.kind = 'config'
prosilica_c.stats1.kind = 'hinted'
prosilica_c.stats1.total.kind = 'hinted' 









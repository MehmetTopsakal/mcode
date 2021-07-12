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







# Some of the code below is from: 
# https://github.com/NSLS-II-HXN/hxntools/blob/master/hxntools/detectors


class FileStoreBulkReadable(FileStoreIterativeWrite):

    def _reset_data(self):
        self._datum_uids.clear()
        self._point_counter = itertools.count()

    def bulk_read(self, timestamps):
        image_name = self.image_name

        uids = [self.generate_datum(self.image_name, ts, {}) for ts in timestamps]

        # clear so unstage will not save the images twice:
        self._reset_data()
        return {image_name: uids}

    @property
    def image_name(self):
        return self.parent._image_name


class BlackflyDetectorCam(CamBase):
    pass


class BlackflyDetector(AreaDetector):
    cam = Cpt(BlackflyDetectorCam, 'cam1:',
              read_attrs=[],
              configuration_attrs=['image_mode', 'trigger_mode',
                                   'acquire_time', 'acquire_period'],
              )

class XPDTIFFPlugin(TIFFPlugin, FileStoreTIFFSquashing,
                    FileStoreIterativeWrite):
    pass

class XPDTOMOBlackfly(BlackflyDetector):
    image = C(ImagePlugin, 'image1:')
    _default_configuration_attrs = (
        BlackflyDetector._default_configuration_attrs +
        ('images_per_set', 'number_of_sets', 'pixel_size'))
    tiff = C(XPDTIFFPlugin, 'TIFF1:',
             write_path_template='/a/b/c/',
             read_path_template='/a/b/c',
             cam_name='cam',  # used to configure "tiff squashing"
             proc_name='proc',  # ditto
             read_attrs=[],
             root='/nsls2/data/xpd/tomo/legacy/raw/')

    proc = C(ProcessPlugin, 'Proc1:')

    # These attributes together replace `num_images`. They control
    # summing images before they are stored by the detector (a.k.a. "tiff
    # squashing").
    images_per_set = C(Signal, value=1, add_prefix=())
    number_of_sets = C(Signal, value=1, add_prefix=())

    pixel_size = C(Signal, value=.000075, kind='config')
    detector_type = C(Signal, value='Blackfly 2923', kind='config')
    stats1 = C(StatsPluginV33, 'Stats1:')
    stats2 = C(StatsPluginV33, 'Stats2:')
    stats3 = C(StatsPluginV33, 'Stats3:')
    stats4 = C(StatsPluginV33, 'Stats4:')
    stats5 = C(StatsPluginV33, 'Stats5:', kind = 'hinted')
    #stats5.total.kind = 'hinted'

    roi1 = C(ROIPlugin, 'ROI1:')
    roi2 = C(ROIPlugin, 'ROI2:')
    roi3 = C(ROIPlugin, 'ROI3:')
    roi4 = C(ROIPlugin, 'ROI4:')

    # dark_image = C(SavedImageSignal, None)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.stage_sigs.update([(self.cam.trigger_mode, 'Off')])



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
        self.cam.stage_sigs[self.cam.image_mode] = 'Continuous'
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

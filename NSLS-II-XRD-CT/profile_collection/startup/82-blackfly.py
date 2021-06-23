from ophyd.areadetector import ADComponent
from ophyd import PointGreyDetectorCam
from ophyd import SingleTrigger, ImagePlugin, HDF5Plugin
from ophyd import AreaDetector



class XPDDBlackFlyTiffPlugin(TIFFPlugin, FileStoreTIFFIterativeWrite, Device):
    def get_frames_per_point(self):
        if self.parent.cam.image_mode.get(as_string=True) == 'Single':
            return 1
        return super().get_frames_per_point()


class XPDDBlackFlyDetector(SingleTrigger, AreaDetector):
    """PointGrey Black Fly detector(s) as used by 28-ID-D"""
    cam = ADComponent(PointGreyDetectorCam, "cam1:")
    image = ADComponent(ImagePlugin, "image1:")
    tiff = Cpt(XPDDBlackFlyTiffPlugin, 'TIFF1:',
               read_attrs=[],
               configuration_attrs=[],
               write_path_template='/nsls2/xf28id2/bf_data/%Y/%m/%d/',
               read_path_template='/nsls2/xf28id2/bf_data/%Y/%m/%d/',
               root='/nsls2/xf28id2/bf_data/')
    """ 
               write_path_template='/epics/data/',
               read_path_template='/epics/data/',
               root='/epics/data/')
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def stage(self):
        self.cam.stage_sigs['image_mode'] = "Single"
        self.cam.stage_sigs['trigger_mode'] = 'Off'
        return super().stage()


blackfly = XPDDBlackFlyDetector('XF:28IDD-BI{Det-BlackFly}', name="blackfly_det")
blackfly.read_attrs = ['tiff']

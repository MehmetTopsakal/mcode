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

    

    
    
    
    
    
class XPDDBlackFlyDetector_single(SingleTrigger, AreaDetector):
    """PointGrey Black Fly detector(s) as used by 28-ID-D"""
#     stats1 = Cpt(StatsPluginV33, 'Stats1:')    
    cam = ADComponent(PointGreyDetectorCam, "cam1:")
    image = ADComponent(ImagePlugin, "image1:")
    tiff = Cpt(XPDDBlackFlyTiffPlugin, 'TIFF1:',
               read_attrs=[],
               configuration_attrs=[],
#                write_path_template='/data/bf_data/%Y/%m/%d/',
#                read_path_template='/data/bf_data/%Y/%m/%d/',
#                root='/data/bf_data/',
               #write_path_template='/nsls2/xf28id2/bf_data/%Y/%m/%d/',
               #read_path_template='/nsls2/xf28id2/bf_data/%Y/%m/%d/',
               write_path_template='/data/bf_data/test/',
               read_path_template='/data/bf_data/test/',
               root='/data/bf_data/',               
              )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    def stage(self):
        self.cam.stage_sigs['image_mode'] = "Single"
        self.cam.stage_sigs['trigger_mode'] = 'Off'
        return super().stage()       
blackfly_single = XPDDBlackFlyDetector_single('XF:28IDD-BI{Det-BlackFly}', name="blackfly_det")
blackfly_single.read_attrs = ['tiff']
#blackfly_single.stats1.kind = 'hinted'
#blackfly_single.stats1.total.kind = 'hinted'  
# blackfly_single.unstage()       




class XPDDBlackFlyDetector_multiple(SingleTrigger, AreaDetector):
    """PointGrey Black Fly detector(s) as used by 28-ID-D"""
#     stats1 = Cpt(StatsPluginV33, 'Stats1:')    
    cam = ADComponent(PointGreyDetectorCam, "cam1:")
    image = ADComponent(ImagePlugin, "image1:")
    tiff = Cpt(XPDDBlackFlyTiffPlugin, 'TIFF1:',
               read_attrs=[],
               configuration_attrs=[],
#                write_path_template='/data/bf_data/%Y/%m/%d/',
#                read_path_template='/data/bf_data/%Y/%m/%d/',
#                root='/data/bf_data/',
               #write_path_template='/nsls2/xf28id2/bf_data/%Y/%m/%d/',
               #read_path_template='/nsls2/xf28id2/bf_data/%Y/%m/%d/',
               #root='/nsls2/xf28id2/bf_data/', 
               write_path_template='/data/bf_data/test/',
               read_path_template='/data/bf_data/test/',
               root='/data/bf_data/',                  
              )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    def stage(self):
        self.cam.stage_sigs['image_mode'] = "Multiple"
        self.cam.stage_sigs['trigger_mode'] = 'Off'
        return super().stage()       
blackfly_multiple = XPDDBlackFlyDetector_multiple('XF:28IDD-BI{Det-BlackFly}', name="blackfly_det")
blackfly_multiple.read_attrs = ['tiff']
#blackfly_multiple.stats1.kind = 'hinted'
#blackfly_multiple.stats1.total.kind = 'hinted'  
# blackfly_multiple.unstage()     
    
    
    
    
    
    
    
    
    
# class XPDDBlackFlyDetector_single_gpfs(SingleTrigger, AreaDetector):
#     """PointGrey Black Fly detector(s) as used by 28-ID-D"""
#     stats1 = Cpt(StatsPluginV33, 'Stats1:')
#     cam = ADComponent(PointGreyDetectorCam, "cam1:")
#     image = ADComponent(ImagePlugin, "image1:")
#     tiff = Cpt(XPDDBlackFlyTiffPlugin, 'TIFF1:',
#                read_attrs=[],
#                configuration_attrs=[],
#                write_path_template='/nsls2/xf28id2/bf_data/%Y/%m/%d/',
#                read_path_template='/nsls2/xf28id2/bf_data/%Y/%m/%d/',
#                root='/nsls2/xf28id2/bf_data/',
#               )
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#     def stage(self):
#         self.cam.stage_sigs['image_mode'] = "Single"
#         self.cam.stage_sigs['trigger_mode'] = 'Off'
#         return super().stage()
# blackfly_single_gpfs = XPDDBlackFlyDetector_single_gpfs('XF:28IDD-BI{Det-BlackFly}', name="blackfly_det")
# blackfly_single_gpfs.read_attrs = ['tiff']
# #blackfly_single_gpfs.stats1.kind = 'hinted'
# #blackfly_single_gpfs.stats1.total.kind = 'hinted'  
# blackfly_single_gpfs.unstage()    
    
# class XPDDBlackFlyDetector_single_local(SingleTrigger, AreaDetector):
#     """PointGrey Black Fly detector(s) as used by 28-ID-D"""
#     stats1 = Cpt(StatsPluginV33, 'Stats1:')    
#     cam = ADComponent(PointGreyDetectorCam, "cam1:")
#     image = ADComponent(ImagePlugin, "image1:")
#     tiff = Cpt(XPDDBlackFlyTiffPlugin, 'TIFF1:',
#                read_attrs=[],
#                configuration_attrs=[],
#                write_path_template='/data/bf_data/%Y/%m/%d/',
#                read_path_template='/data/bf_data/%Y/%m/%d/',
#                root='/data/bf_data/',
#               )
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#     def stage(self):
#         self.cam.stage_sigs['image_mode'] = "Single"
#         self.cam.stage_sigs['trigger_mode'] = 'Off'
#         return super().stage()       
# blackfly_single_local = XPDDBlackFlyDetector_single_local('XF:28IDD-BI{Det-BlackFly}', name="blackfly_det")
# blackfly_single_local.read_attrs = ['tiff']
# #blackfly_single_local.stats1.kind = 'hinted'
# #blackfly_single_local.stats1.total.kind = 'hinted'  
# blackfly_single_local.unstage()      
    
# class XPDDBlackFlyDetector_multiple_local(SingleTrigger, AreaDetector):
#     """PointGrey Black Fly detector(s) as used by 28-ID-D"""
#     stats1 = Cpt(StatsPluginV33, 'Stats1:')    
#     cam = ADComponent(PointGreyDetectorCam, "cam1:")
#     image = ADComponent(ImagePlugin, "image1:")
#     tiff = Cpt(XPDDBlackFlyTiffPlugin, 'TIFF1:',
#                read_attrs=[],
#                configuration_attrs=[],
#                write_path_template='/data/bf_data/%Y/%m/%d/',
#                read_path_template='/data/bf_data/%Y/%m/%d/',
#                root='/data/bf_data/',
#               )
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#     def stage(self):
#         self.cam.stage_sigs['image_mode'] = "Multiple"
#         self.cam.stage_sigs['trigger_mode'] = 'Off'
#         return super().stage()       
# blackfly_multiple_local = XPDDBlackFlyDetector_multiple_local('XF:28IDD-BI{Det-BlackFly}', name="blackfly_det")
# blackfly_multiple_local.read_attrs = ['tiff']
# #blackfly_multiple_local.stats1.kind = 'hinted'
# #blackfly_multiple_local.stats1.total.kind = 'hinted'  
# blackfly_multiple_local.unstage()     

# class XPDDBlackFlyDetector_multiple_gpfs(SingleTrigger, AreaDetector):
#     """PointGrey Black Fly detector(s) as used by 28-ID-D"""
#     stats1 = Cpt(StatsPluginV33, 'Stats1:')    
#     cam = ADComponent(PointGreyDetectorCam, "cam1:")
#     image = ADComponent(ImagePlugin, "image1:")
#     tiff = Cpt(XPDDBlackFlyTiffPlugin, 'TIFF1:',
#                read_attrs=[],
#                configuration_attrs=[],
#                write_path_template='/nsls2/xf28id2/bf_data/%Y/%m/%d/',
#                read_path_template='/nsls2/xf28id2/bf_data/%Y/%m/%d/',
#                root='/nsls2/xf28id2/bf_data/',
#               )
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#     def stage(self):
#         self.cam.stage_sigs['image_mode'] = "Multiple"
#         self.cam.stage_sigs['trigger_mode'] = 'Off'
#         return super().stage()       
# blackfly_multiple_gpfs = XPDDBlackFlyDetector_multiple_gpfs('XF:28IDD-BI{Det-BlackFly}', name="blackfly_det")
# blackfly_multiple_gpfs.read_attrs = ['tiff']
# #blackfly_multiple_gpfs.stats1.kind = 'hinted'
# #blackfly_multiple_gpfs.stats1.total.kind = 'hinted'  
# blackfly_multiple_gpfs.unstage()   


# print('Current values:\nExposure time : %.3f\nAcquire period: %.3f\n\n'%(
#         blackfly_single_local.cam.acquire_time.value ,
#         blackfly_single_local.cam.acquire_period.value))





"""
det = blackfly_single_local
det.cam.acquire_time.put(1.0)
%time RE(count([det],num=10))

hdr = db[-1]
%time data = np.array(list(hdr.data('blackfly_det_image')))
data.shape



det = blackfly_multiple_local
det.cam.acquire_time.put(1.0)
det.cam.num_images.put(5)
%time RE(count([det],num=10))

hdr = db[-1]
%time data = np.array(list(hdr.data('blackfly_det_image')))
data.shape




det = blackfly_multiple_local
det.cam.acquire_time.put(1.0)
det.cam.acquire_period.put(1.0) # cannot be more than 1sec
det.cam.num_images.put(5)
%time RE(count([det],num=10))

hdr = db[-1]
%time data = np.array(list(hdr.data('blackfly_det_image')))
data.shape




data = np.mean(data, axis=1)
data = np.mean(data, axis=0)
data.shape
fig = plt.figure(figsize=(12,6))

ax = fig.add_subplot('121')
ax.imshow(data[:,:],cmap='Greys_r',vmin=100,vmax=6000,norm=LogNorm())
ax.plot([750,1250],[1250,1250],':y')

ax = fig.add_subplot('122')
ax.plot(data[1200,750:1250])
ax.set_xlabel('Pixel')
ax.set_ylabel('Counts')


"""

 
from ophyd import EpicsMotor
import ophyd
from ophyd import EpicsSignal


## Huber Stack
mStackY =  EpicsMotor('XF:28IDD-ES:2{Stg:Stack-Ax:Yfine}Mtr',name='mStackY')
mStackX =  EpicsMotor('XF:28IDD-ES:2{Stg:Stack-Ax:Xfine}Mtr',name='mStackX')
mStackZ =  EpicsMotor('XF:28IDD-ES:2{Stg:Stack-Ax:Z}Mtr',name='mStackZ')
mRoll   =  EpicsMotor('XF:28IDD-ES:2{Stg:Stack-Ax:Roll}Mtr',name='mRoll')
mPitch  =  EpicsMotor('XF:28IDD-ES:2{Stg:Stack-Ax:Pitch}Mtr',name='mPitch')
mPhi    =  EpicsMotor('XF:28IDD-ES:2{Stg:Stack-Ax:Phi}Mtr',name='mPhi')
mYBase  =  EpicsMotor('XF:28IDD-ES:2{Stg:Stack-Ax:Y}Mtr',name='mYBase')
mXBase  =  EpicsMotor('XF:28IDD-ES:2{Stg:Stack-Ax:Xbase}Mtr',name='mXBase')

# Dexela 
mDexelaPhi  =  EpicsMotor('XF:28IDD-ES:2{Stg:Stack-Ax:Htth}Mtr',name='mDexelaPhi')

# Questar X
mQuestarX   =  EpicsMotor('XF:28IDD-ES:2{Cam:Mnt-Ax:X}Mtr',name='mQuestarX')

# Hexapods Z
mHexapodsZ  =  EpicsMotor('XF:28IDD-ES:2{Det:Dexela-Ax:Z}Mtr',name='mHexapodsZ')

# Beamstops
mBeamStopY  = EpicsMotor('XF:28IDD-ES:2{BS-Ax:X}Mtr',name='mBeamStopY')

# Slits
mSlitsYGap = EpicsMotor('XF:28IDD-ES:2{Slt-Ax:YGap}Mtr',name='mSlitsYGap')
mSlitsYCtr = EpicsMotor('XF:28IDD-ES:2{Slt-Ax:YCtr}Mtr',name='mSlitsYGap')
mSlitsXGap = EpicsMotor('XF:28IDD-ES:2{Slt-Ax:XGap}Mtr',name='mSlitsXGap')
mSlitsXCtr = EpicsMotor('XF:28IDD-ES:2{Slt-Ax:XCtr}Mtr',name='mSlitsXGap')
mSlitsTop      = EpicsMotor('XF:28IDD-ES:2{Slt-Ax:T}Mtr',name='mSlitsTop')
mSlitsBottom   = EpicsMotor('XF:28IDD-ES:2{Slt-Ax:B}Mtr',name='mSlitsBottom')
mSlitsOutboard = EpicsMotor('XF:28IDD-ES:2{Slt-Ax:O}Mtr',name='mSlitsOutboard')
mSlitsInboard  = EpicsMotor('XF:28IDD-ES:2{Slt-Ax:I}Mtr',name='mSlitsInboard')

# Smartpod
sSmartPodUnit  = EpicsSignal('XF:28IDD-ES:2{SPod:1}Unit-SP',name='sSmartPodUnit')
sSmartPodTrasX = EpicsSignal('XF:28IDD-ES:2{SPod:1-Ax:1}Pos-SP',name='sSmartPodTrasX')
sSmartPodTrasY = EpicsSignal('XF:28IDD-ES:2{SPod:1-Ax:2}Pos-SP',name='sSmartPodTrasY')
sSmartPodTrasZ = EpicsSignal('XF:28IDD-ES:2{SPod:1-Ax:3}Pos-SP',name='sSmartPodTrasZ')
sSmartPodRotX  = EpicsSignal('XF:28IDD-ES:2{SPod:1-Ax:1}Rot-SP',name='sSmartPodRotX')
sSmartPodRotY  = EpicsSignal('XF:28IDD-ES:2{SPod:1-Ax:2}Rot-SP',name='sSmartPodRotY')
sSmartPodRotZ  = EpicsSignal('XF:28IDD-ES:2{SPod:1-Ax:3}Rot-SP',name='sSmartPodRotZ')
sSmartPodSync  = EpicsSignal('XF:28IDD-ES:2{SPod:1}Sync-Cmd',name='sSmartPodSync')
sSmartPodMove  = EpicsSignal('XF:28IDD-ES:2{SPod:1}Move-Cmd',name='sSmartPodMove')

# Sigray
mSigrayX = EpicsMotor('XF:28IDD-ES:2{Stg:Sigray-Ax:X}Mtr',name='mSigrayX')
mSigrayY = EpicsMotor('XF:28IDD-ES:2{Stg:Sigray-Ax:Y}Mtr',name='mSigrayY')
mSigrayZ = EpicsMotor('XF:28IDD-ES:2{Stg:Sigray-Ax:Z}Mtr',name='mSigrayZ')
mSigrayPitch = EpicsMotor('XF:28IDD-ES:2{Stg:Sigray-Ax:Pitch}Mtr',name='mSigrayPitch')
mSigrayYaw   = EpicsMotor('XF:28IDD-ES:2{Stg:Sigray-Ax:Yaw}Mtr',name='mSigrayYaw')

class FilterBank(ophyd.Device):
    flt1 = ophyd.Component(EpicsSignal, '1-Cmd', string=True)
    flt2 = ophyd.Component(EpicsSignal, '2-Cmd', string=True)
    flt3 = ophyd.Component(EpicsSignal, '3-Cmd', string=True)
    flt4 = ophyd.Component(EpicsSignal, '4-Cmd', string=True)
Filters = FilterBank('XF:28IDC-OP:1{Fltr}Cmd:Opn', name='fb') #fb.flt1.set('In')

FastShutter = EpicsMotor('XF:28IDC-ES:1{Sh2:Exp-Ax:5}Mtr', name='shctl1')



pdu1  = EpicsSignal('XF:28IDD-CT{PDU:1}Sw:1-Sel',name='pdu1')
pdu2  = EpicsSignal('XF:28IDD-CT{PDU:1}Sw:2-Sel',name='pdu2')
pdu3  = EpicsSignal('XF:28IDD-CT{PDU:1}Sw:3-Sel',name='pdu3')
pdu4  = EpicsSignal('XF:28IDD-CT{PDU:1}Sw:4-Sel',name='pdu4')
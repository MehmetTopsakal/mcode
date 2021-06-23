 
import numpy as np




def read_feffnpz(npzfile):
    npzdata = np.load(npzfile)
    E = npzdata['_e_int']
    I = npzdata['_xmu_total']
    EIs = npzdata['_xmus_calculated_int']
    return [E,I,EIs]

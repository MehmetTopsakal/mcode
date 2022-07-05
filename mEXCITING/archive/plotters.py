#!/usr/bin/env python

import numpy as np
import os







def plottdos():
    
    from .readqe import readqe
    
    
    
    readnpz = np.load('qerun.npz')
    dos_info = readnpz['dos_info']
    tdos = readnpz['tdos']
    Edos = readnpz['Edos'] # already shifted by E-fermi

    
    from matplotlib import pyplot as plt
    fig = plt.figure(figsize=(8,5))
    
    ax = fig.add_subplot('211')
    ax.grid(True) 
    
    ax.plot(Edos, tdos[0], 'g-', lw=2, alpha=0.9, label='spin-up')
    ax.plot(Edos,-tdos[1], 'g-', lw=2, alpha=0.9, label='spin-dw')
    
    
    ax = fig.add_subplot('212')
    ax.grid(True) 
    
    ax.plot(Edos, tdos[0], 'g-', lw=2, alpha=0.9, label='spin-up')
    ax.plot(Edos,-tdos[1], 'g-', lw=2, alpha=0.9, label='spin-dw')   
    ax.set_xlim(-10,10)
    
    
    plt.savefig("tdos.png", format='png', dpi=300)
    
    return
    
    
    

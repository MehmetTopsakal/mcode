
import numpy as np
from scipy import signal



class mconv:
    '''
    Does convolution with Gaussian or Lorentzian windows
    '''
    
    def __init__(self, datax, datay):
        
        self.datax = datax
        self.datay = datay

        self.NPoints = len(datax)
        self.X = np.array(datax)


            
    def w_gaussian(self, M, wsigma, dx):
        ''' see : https://github.com/scipy/scipy/blob/v0.19.0/scipy/signal/windows.py#L1159-L1219
        M should be odd number'''
        if wsigma <=0 : wsigma = 0.00001
        wsigma = wsigma/dx
        n = np.arange(0, M) - (M - 1.0) / 2.0
        wsigma2 = 2 * wsigma * wsigma
        wg = np.exp(-n ** 2 / wsigma2)    
        return wg

    def w_lorentzian(self, M, wgamma, dx):
        ''' '''
        wgamma = wgamma/dx
        if wgamma <=0 : wgamma = 0.00001
        n = np.arange(0, M) - (M - 1.0) / 2.0
        wl = 1 / ( ((2*n)/wgamma)**2 + 1  )    
        return wl             
           
        
    def Gaussian(self,sigma=None,fwhm=None,saveto=None):
        
        if fwhm:
            if sigma:
                print('ignoring input sigma')
        elif sigma:
            fwhm = sigma * np.sqrt(8 * np.log(2))
        else: 
            raise ValueError('sigma/fwhm was not set....')  
           
        self.sigma = fwhm/np.sqrt(8 * np.log(2))   
        
        M=101
        dx=self.datax[2]-self.datax[1]
        win = self.w_gaussian(M, self.sigma, dx)
        out = signal.convolve(self.datay, win, mode='same') / sum(win)

            
        if saveto:
            if fmt is None:
                fmt="%18.6e %18.6e"                
            of = np.column_stack( (self.X, out) )
            np.savetxt(str(saveto), of, delimiter=" ", fmt=fmt )       
            
        return [self.X, out]
            
            
            
            
            
        
    def Lorentzian(self,gamma=None,fwhm=None,saveto=None,M=None):
        # in Lorentzian fwhm is equal to gamma
        
        if fwhm:
            if gamma:
                print('in Lorentzian fwhm is equal to gamma')
        elif gamma:
            fwhm = gamma
        else: 
            raise ValueError('sigma/fwhm was not set....')   
            
        self.gamma = fwhm 
        
        if M is None: M=1001
        dx=self.datax[2]-self.datax[1]    
        win = self.w_lorentzian(M, self.gamma, dx)
        out = signal.convolve(self.datay, win, mode='same') / sum(win)

            
        if saveto:
            if fmt is None:
                fmt="%18.6e %18.6e"                
            of = np.column_stack( (self.X, out) )
            np.savetxt(str(saveto), of, delimiter=" ", fmt=fmt )       
            
        return [self.X, out]    
    
    
    
    
    def LorentzianVL(self,saveto=None,fmt=None,M=None,A=None,B=None,offset=None):
        # gamma = A(x-offset) + B   
        
        if A is None: A=0.1
        if B is None: B=0           
        if offset is None: offset=self.datax[0]  
        
        gammas = []    
        for i,d in enumerate(self.datax):
            g = max(0,A*(d-offset)) + B
            gammas.append(g)
  
        if M is None: M=1001   
        dx=self.datax[2]-self.datax[1]
        out = np.zeros(self.NPoints)
        
                
        for i, [gg, x0, y0] in enumerate(zip(gammas,self.datax,self.datay)):
            win = self.w_lorentzian(M, gg, dx)
            c = signal.convolve(self.datay, win, mode='same') / sum(win)
            out[i] = c[i]
                        
        if saveto:
            if fmt is None:
                fmt="%18.6e %18.6e"                
            of = np.column_stack( (self.X, out) )
            np.savetxt(str(saveto), of, delimiter=" ", fmt=fmt )           
            
        return [self.X, out], [self.datax, gammas]   
    
    
    
    
    def LorentzianVE2(self,saveto=None,fmt=None,M=None,offset=None):
        # gamma = (x-offset)^2 + B   
        
        if A is None: A=0.1
        if B is None: B=0           
        if offset is None: offset=self.datax[0]  
        
        gammas = []    
        for i,d in enumerate(self.datax):
            g = max(0,A*(d-offset)) + B
            gammas.append(g)
  
        if M is None: M=1001   
        dx=self.datax[2]-self.datax[1]
        out = np.zeros(self.NPoints)
        
                
        for i, [gg, x0, y0] in enumerate(zip(gammas,self.datax,self.datay)):
            win = self.w_lorentzian(M, gg, dx)
            c = signal.convolve(self.datay, win, mode='same') / sum(win)
            out[i] = c[i]
                        
        if saveto:
            if fmt is None:
                fmt="%18.6e %18.6e"                
            of = np.column_stack( (self.X, out) )
            np.savetxt(str(saveto), of, delimiter=" ", fmt=fmt )           
            
        return [self.X, out], [self.datax, gammas]       
    
    
    

    
    
    
    
    
    
    
    
    
    
    
    

#!/usr/bin/env python

def make(filename,calc,ec,ist,dp,lw,lc):
    
    f = open(filename, 'w');

    if calc == 'relax0':                     
        f.write('EDIFF   = 1E-06              '+'\n')
        f.write('NELM    = 70                 '+'\n')        
        f.write('ISMEAR  = 0 ; SIGMA = 0.002  '+'\n')        
        f.write('ALGO    = N                  '+'\n')
        f.write('LREAL   = F                  '+'\n')
        f.write('ADDGRID = T                  '+'\n')
        f.write('LMAXMIX = 4                  '+'\n')        
        f.write('NSW     = 100 ; IBRION = 2   '+'\n') 
        f.write(ec                             +'\n')

        if ist == 0: f.write('ISTART = 0                        '+'\n')                  
        if dp == 1:  f.write('LDIPOL = T ; DIPOL  = 0.5 0.5 0.5 '+'\n')  
        if lw == 0:  f.write('LWAVE  = F                        '+'\n') 
        if lc == 0:  f.write('LCHARG = F                        '+'\n')     
        f.close()
    
    if calc == 'scf0':                     
        f.write('EDIFF   = 1E-06              '+'\n')
        f.write('NELM    = 70                 '+'\n')        
        f.write('ISMEAR  = -5                 '+'\n')          
        f.write('ALGO    = N                  '+'\n')
        f.write('LREAL   = F                  '+'\n')
        f.write('ADDGRID = T                  '+'\n')
        f.write('LMAXMIX = 4                  '+'\n')        
        f.write('NSW     = 0 ; IBRION = -1    '+'\n') 
        f.write(ec                             +'\n')

        if ist == 0: f.write('ISTART = 0                        '+'\n')                  
        if dp == 1:  f.write('LDIPOL = T ; DIPOL  = 0.5 0.5 0.5 '+'\n')  
        if lw == 0:  f.write('LWAVE  = F                        '+'\n') 
        if lc == 0:  f.write('LCHARG = F                        '+'\n')   
        f.close()
    
    if calc == 'bands0':                    
        f.write('EDIFF   = 1E-06              '+'\n')
        f.write('NELM    = 70                 '+'\n')        
        f.write('ISMEAR  = 0 ; SIGMA = 0.001  '+'\n')          
        f.write('ALGO    = N                  '+'\n')
        f.write('LREAL   = F                  '+'\n')
        f.write('ADDGRID = T                  '+'\n')
        f.write('LMAXMIX = 4                  '+'\n')        
        f.write('NSW     = 0 ; IBRION = -1    '+'\n') 
        f.write(ec                             +'\n')
        
        f.write('ICHARG = 11') 
        if ist == 0: f.write('ISTART = 0                        '+'\n')                  
        if dp == 1:  f.write('LDIPOL = T ; DIPOL  = 0.5 0.5 0.5 '+'\n')  
        if lw == 0:  f.write('LWAVE  = F                        '+'\n') 
        if lc == 0:  f.write('LCHARG = F                        '+'\n')          
        f.close()        
    
    if calc == 'hse1':                    
        f.write('EDIFF   = 1E-06              '+'\n')
        f.write('NELM    = 70                 '+'\n')        
        f.write('ISMEAR  = 0 ; SIGMA = 0.001  '+'\n')          
        f.write('ALGO    = N                  '+'\n')
        f.write('LREAL   = F                  '+'\n')
        f.write('ADDGRID = T                  '+'\n')
        f.write('LMAXMIX = 4                  '+'\n')        
        f.write('NSW     = 0 ; IBRION = -1    '+'\n')      
        f.write(ec                             +'\n')
        f.write('ISPIN = 2                    '+'\n')         
        
        if ist == 0: f.write('ISTART = 0                        '+'\n')                  
        if dp == 1:  f.write('LDIPOL = T ; DIPOL  = 0.5 0.5 0.5 '+'\n')  
        if lw == 0:  f.write('LWAVE  = F                        '+'\n') 
        if lc == 0:  f.write('LCHARG = F                        '+'\n')         
        f.close()          
    
    if calc == 'hse2':                    
        f.write('EDIFF   = 1E-06              '+'\n') 
        f.write('NELM    = 70                 '+'\n')         
        f.write('ISMEAR  = 0 ; SIGMA = 0.001  '+'\n')           
        f.write('ALGO    = N                  '+'\n') 
        f.write('LREAL   = F                  '+'\n') 
        f.write('ADDGRID = T                  '+'\n') 
        f.write('LMAXMIX = 4                  '+'\n')         
        f.write('NSW     = 0 ; IBRION = -1    '+'\n')      
        f.write(ec                             +'\n')
        f.write('ISPIN = 2                    '+'\n') 
        f.write(' LSORBIT = .TRUE.            '+'\n')
        f.write(' SAXIS   =  0 0 1            '+'\n')
        f.write(' GGA_COMPAT = .FALSE.        '+'\n')  
        
        f.write('ICHARG = 11') 
        if ist == 0: f.write('ISTART = 0                        '+'\n')                  
        if dp == 1:  f.write('LDIPOL = T ; DIPOL  = 0.5 0.5 0.5 '+'\n')  
        if lw == 0:  f.write('LWAVE  = F                        '+'\n') 
        if lc == 0:  f.write('LCHARG = F                        '+'\n')          
        f.close()         
    
    if calc == 'hse3':                    
        f.write('EDIFF   = 1E-06              '+'\n')
        f.write('NELM    = 70                 '+'\n')        
        f.write('ISMEAR  = 0 ; SIGMA = 0.001  '+'\n')          
        f.write('! ALGO    = N                '+'\n')
        f.write('LREAL   = F                  '+'\n')
        f.write('ADDGRID = T                  '+'\n')
        f.write('LMAXMIX = 4                  '+'\n')        
        f.write('NSW     = 0 ; IBRION = -1    '+'\n')     
        f.write(ec                             +'\n')
        f.write('ISPIN = 2                    '+'\n') 
        f.write(' LSORBIT = .TRUE.            '+'\n')
        f.write(' SAXIS   =  0 0 1            '+'\n')
        f.write(' GGA_COMPAT = .FALSE.        '+'\n')
        f.write(' LVHAR   = .TRUE.            '+'\n')
        f.write(' # Selects the HSE06 hybrid function (preconverge with PBE first)  '+'\n')       
        f.write(' LHFCALC = .TRUE. ; HFSCREEN = 0.2 ;                               '+'\n')
        f.write(' ALGO = D ; IALGO=53 ; TIME = 0.4                                  '+'\n')
        f.write(' PRECFOCK=fast                                                     '+'\n')
        
        if ist == 0: f.write('ISTART = 0                        '+'\n')                  
        if dp == 1:  f.write('LDIPOL = T ; DIPOL  = 0.5 0.5 0.5 '+'\n')  
        if lw == 0:  f.write('LWAVE  = F                        '+'\n') 
        if lc == 0:  f.write('LCHARG = F                        '+'\n')         
        f.close()          
        
    
    if calc == 'scf0MAGUf':                    
        f.write('EDIFF   = 1E-06              '+'\n')
        f.write('NELM    = 70                 '+'\n')        
        f.write('ISMEAR  = 0 ; SIGMA = 0.001  '+'\n')          
        f.write('ALGO    = N                  '+'\n')
        f.write('LREAL   = F                  '+'\n')
        f.write('ADDGRID = T                  '+'\n')
        f.write('LMAXMIX = 4                  '+'\n')        
        f.write('NSW     = 0 ; IBRION = -1    '+'\n')      
        f.write(ec                             +'\n')
        f.write('ISPIN = 2                    '+'\n')
        f.write('LDAU     = .TRUE.                        '+'\n')
        f.write('LDAUTYPE = 2 ; LMAXMIX = 6 ; LASPH = T   '+'\n')
        f.write('LDAUL    =   3    -1                     '+'\n')
        f.write('LDAUU    =   2.00 0.00                   '+'\n')
        f.write('LDAUJ    =   0.00 0.00                   '+'\n')
        f.write('MAGMOM = 2 -2 0 0                        '+'\n')
        
        if ist == 0: f.write('ISTART = 0                        '+'\n')                  
        if dp == 1:  f.write('LDIPOL = T ; DIPOL  = 0.5 0.5 0.5 '+'\n')  
        if lw == 0:  f.write('LWAVE  = F                        '+'\n') 
        if lc == 0:  f.write('LCHARG = F                        '+'\n')         
        f.close()            
        
        
        
        
        
        
        
    return


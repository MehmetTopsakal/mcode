function [energies_up,energies_dw,kpoints]=vasp_getbands
%
% usage 
%

if nargin < 3, format =  0      ; end
if nargin < 2,   ymax =  6      ; end
if nargin < 1,   ymin = -6      ; end

%  figure

[s,nspin] = unix('grep ISPIN OUTCAR | awk ''{print $3}''');
nspin = sscanf(nspin,'%d') ;

%  [s,kline] = unix('grep  NKPTS OUTCAR | awk ''{print $4"  "$15}''');
%  [kline,c] = sscanf(kline,'%d') ; nkpoints = kline(1) ; nbands = kline(2) ;

[s,nkpoints] = unix('grep  NKPTS OUTCAR | awk ''{print $4}''');
nkpoints = sscanf(nkpoints,'%d') ;

[s,nbands] = unix('grep  NKPTS OUTCAR | awk ''{print $NF}''');
nbands = sscanf(nbands,'%d') ;

[s,efline] = unix('grep -n " E-fermi :" OUTCAR  | awk ''END{print}'' | awk ''{print $1 "  " $4 }'' | awk -F ":" ''{print $1"  "$2}''');
[efline,c] = sscanf(efline,'%f') ; fermi = efline(2) ; efline = efline(1) ;


if  nspin==1 ; % ISPIN = 1 case
    
    elstart = efline+3 ; elstop  = nkpoints*(nbands+3)+1 ;
    fid = fopen('limits.tmp', 'w'); fprintf(fid, '%d %d', [elstart,elstop]); fclose(fid); 
    unix('awk "NR>=`cat limits.tmp | awk ''{print $1}''`" OUTCAR | awk "NR<=`cat limits.tmp | awk ''{print $2}''`" > data.tmp');
    unix(' rm -f limits.tmp ') ; % we can avoid this file as we did for kpoints....
    fid = fopen('data.tmp', 'r');
    for kp=1:nkpoints
        null = fscanf(fid,'%s', 3); kpoints_path(kp,:) = fscanf (fid, '%g', [1 3]); null = fscanf(fid,'%s', 5);
        readdata = fscanf(fid,'%f', [3 nbands]); readdata = readdata' ;
        energy(:,kp) = readdata(:,2); occupation(:,kp) = readdata(:,3);
    end
    fclose(fid); unix('rm -f data.tmp') ;
    

[s,nelectrons] = unix('grep NELECT OUTCAR | awk ''{print $3}''');
nelectrons = sscanf(nelectrons,'%d') ;

% define K-points path %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% we need kpoints in reciprocal positions so:
[a,kpoints_path] = unix('awk ''/ k-points in units of 2pi/, / k-points in reciprocal lattice and weights:/'' OUTCAR | awk "NF==4" | awk ''{print $1 "  " $2 "   " $3  }'' ');
kpoints_path = sscanf(kpoints_path,'%g', [3 nkpoints] ) ; kpoints_path = kpoints_path' ;

kpoints_track(1) = 0 ;
for k=1:size(kpoints_path,1)-1; k0=kpoints_path(k,:); k1=kpoints_path(k+1,:);
    dx=k0(1)-k1(1); dy=k0(2)-k1(2); dz=k0(3)-k1(3);
    kpoints_track(k+1) = kpoints_track(k) + sqrt(dx*dx+dy*dy+dz*dz);
end

 
%  % Find bandgap value %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%  n_valance_band=nelectrons/2;
%  valance_band=energy(n_valance_band:n_valance_band,:);
%  conductance_band=energy(n_valance_band+1:n_valance_band+1,:);
%  BandGap=min(conductance_band)-max(valance_band);
%  %shift=max(valance_band)+(BandGap/2);


energies_up = energy;
energies_dw = energy;
kpoints = kpoints_track;
  
    
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%     
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%  


else           % ISPIN = 2 case
    
    elstart = efline+5 ; elstop  = 2*nkpoints*(nbands+3)+1 ;
    fid = fopen('limits.tmp', 'w'); fprintf(fid, '%d %d', [elstart,elstop]); fclose(fid);
    unix('awk "NR>=`cat limits.tmp | awk ''{print $1}''`" OUTCAR | awk "NR<=`cat limits.tmp | awk ''{print $2}''`" > data.tmp');
    unix(' rm -f limits.tmp ') ; % we can avoid this file as we did for kpoints....
    fid = fopen('data.tmp', 'r');
    for kp=1:nkpoints
        null = fscanf(fid,'%s', 3); kpoints_path(kp,:) = fscanf (fid, '%g', [1 3]); null = fscanf(fid,'%s', 5);
        readdata = fscanf(fid,'%f', [3 nbands]); readdata = readdata' ;
        energy_up(:,kp) = readdata(:,2); occupation_up(:,kp) = readdata(:,3);
    end
    null = fscanf(fid,'%s', 3);
    for kp=1:nkpoints
        null = fscanf(fid,'%s', 3); kpoints_path(kp,:) = fscanf (fid, '%g', [1 3]); null = fscanf(fid,'%s', 5);
        readdata = fscanf(fid,'%f', [3 nbands]); readdata = readdata' ;
        energy_down(:,kp) = readdata(:,2); occupation_down(:,kp) = readdata(:,3);
    end
    fclose(fid); unix('rm -f data.tmp') ;
    
    
% define K-points path %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% we need kpoints in reciprocal positions so:
[a,kpoints_path] = unix('awk ''/ k-points in units of 2pi/, / k-points in reciprocal lattice and weights:/'' OUTCAR | awk "NF==4" | awk ''{print $1 "  " $2 "   " $3  }'' ');
kpoints_path = sscanf(kpoints_path,'%g', [3 nkpoints] ) ; kpoints_path = kpoints_path' ;

kpoints_track(1) = 0 ;
for k=1:size(kpoints_path,1)-1; k0=kpoints_path(k,:); k1=kpoints_path(k+1,:);
    dx=k0(1)-k1(1); dy=k0(2)-k1(2); dz=k0(3)-k1(3);
    kpoints_track(k+1) = kpoints_track(k) + sqrt(dx*dx+dy*dy+dz*dz);
end


energies_up = energy_up;
energies_dw = energy_down;
kpoints = kpoints_track;



end



end % function

function [fermi]=vasp_getfermi
%
% usage 
%

[s,efline] = unix('grep -n " E-fermi :" OUTCAR  | awk ''END{print}'' | awk ''{print $1 "  " $4 }'' | awk -F ":" ''{print $1"  "$2}''');
[efline,c] = sscanf(efline,'%f') ; fermi = efline(2) ; efline = efline(1) ;

end 

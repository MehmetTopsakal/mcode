function [bandgap]=vasp_getbandgap
%
% usage 
%

[s,bandgap] = unix('getband');
[bandgap,c] = sscanf(bandgap,'%f') ; 

end 

function [cores]=vasp_readcores_Ti
%

[s,cores] = unix(' grep "  2p   " OUTCAR | awk ''{print $7}'' ');
cores = sscanf(cores,'%g');

cores


end









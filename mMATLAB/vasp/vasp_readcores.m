function [cores]=vasp_readcores
%

[s,cores] = unix(' grep "  1s   " OUTCAR | awk ''{print $3}'' ');
cores = sscanf(cores,'%g');

cores;


end









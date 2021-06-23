function [natom,ndos,nspin,fermi,tdos,pdoss]=vasp_readpdos
%
% usage example :
%
if nargin < 2,  energy_limit_down=-5; end
if nargin < 1,  energy_limit_up=5; end


[s,line1] = unix(' awk "NR==1" DOSCAR ');
line1 = sscanf(line1,'%d');

[s,line6] = unix(' awk "NR==6" DOSCAR ');
line6 = sscanf(line6,'%g'); fermi=line6(4); ndos = line6(3);

[s,line7] = unix(' awk "NR==7" DOSCAR ');
line7 = sscanf(line7,'%g');

[s,dsize] = unix(' cat DOSCAR | wc -l ');
dsize = sscanf(dsize,'%d'); natom = (dsize-5)/(line6(3)+1)-1;




if size(line7,1)==5 % ISPIN = 2 case

nspin=2;
b=7;
[o,tdos] = system(sprintf(' awk "NR==%d,NR==%d" DOSCAR ',b,(b+line6(3)-1))); b=b+line6(3);
tdos = sscanf(tdos,'%g'); tdos=reshape(tdos,5,line6(3)); tdos=tdos';

[o,ncol] = unix(sprintf('awk "NR==%d" DOSCAR ',b+1)); ncol = sscanf(ncol,'%g'); ncol = size(ncol,1);

b=b+1;
for s=1:natom
[o,read] = system(sprintf(' awk "NR==%d,NR==%d" DOSCAR ',b,(b+line6(3)-1))); b=b+line6(3)+1;
read = sscanf(read,'%g'); read=reshape(read,ncol,line6(3)); read=read'; pdoss{s}=read; 
end




else % ISPIN = 1 case

nspin=1;
b=7;
[o,tdos] = system(sprintf(' awk "NR==%d,NR==%d" DOSCAR ',b,(b+line6(3)-1))); b=b+line6(3);
tdos = sscanf(tdos,'%g'); tdos=reshape(tdos,3,line6(3)); tdos=tdos';

[o,ncol] = unix(sprintf('awk "NR==%d" DOSCAR ',b+1)); ncol = sscanf(ncol,'%g'); ncol = size(ncol,1);


if ncol==0
pdoss=0;
disp(' '); disp('pdoss is empty !!!!'); disp(' '); 
else
b=b+1;
for s=1:natom
[o,read] = system(sprintf(' awk "NR==%d,NR==%d" DOSCAR ',b,(b+line6(3)-1))); b=b+line6(3)+1;
read = sscanf(read,'%g'); read=reshape(read,ncol,line6(3)); read=read'; pdoss{s}=read; 
end
end

end




end










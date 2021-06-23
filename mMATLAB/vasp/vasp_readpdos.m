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


dim(1)=nspin;
dim(2)=natom;
dim(3)=ndos;
dim(4)=0;







st=1;
for k=1:size(pdoss,2)

pdoss_new=zeros(ndos,32);

size(pdoss{k},2)

if size(pdoss{k},2)==10 % NM; s,p,d
Et=tdos(:,1); Ep = Et;
tdosp(:,1)=tdos(:,2)/2; tdosp(:,2)=tdos(:,2)/2; tdost=tdosp;
pdoss_new(:,1:9)=pdoss{k}(:,2:10)/2;
pdoss_new(:,17:25)=pdoss{k}(:,2:10)/2;
end

if size(pdoss{k},2)==19 % MAG; s,p,d
Et=tdos(:,1); Ep = Et;
tdosp(:,1)=tdos(:,2); tdosp(:,2)=tdos(:,3); tdost=tdosp;
pdoss_new(:,01:09)=pdoss{k}(:,[2,4,6,8,10,12,14,16,18]);
pdoss_new(:,17:25)=pdoss{k}(:,[3,5,7,9,11,13,15,17,19]);
end


if size(pdoss{k},2)==10+7 % NM; s,p,d,f
Et=tdos(:,1); Ep = Et;
tdosp(:,1)=tdos(:,2)/2; tdosp(:,2)=tdos(:,2)/2; tdost=tdosp;
pdoss_new(:,1:9+7)=pdoss{k}(:,2:10+7)/2;
pdoss_new(:,17:25+7)=pdoss{k}(:,2:10+7)/2;
end

if size(pdoss{k},2)==19+7*2 % MAG; s,p,d,f
Et=tdos(:,1); Ep = Et;
tdosp(:,1)=tdos(:,2); tdosp(:,2)=tdos(:,3); tdost=tdosp;
pdoss_new(:,01:09+7)=pdoss{k}(:,[2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32]);
pdoss_new(:,17:25+7)=pdoss{k}(:,[3,5,7,9,11,13,15,17,19,21,23,25,27,29,31,33]);
end


pdos_all(st:st+size(Ep,1)-1,:)=pdoss_new;
st = st+size(Ep,1);
end


size(pdos_all)

save -7 pdos.mat dim Ep tdosp fermi Et tdost pdos_all


end










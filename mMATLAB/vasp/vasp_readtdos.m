function [nspin,E,tdos,fermi]=vasp_readtdos
%
% usage example :
%
[s,line1] = unix(' awk "NR==1" DOSCAR ');
line1 = sscanf(line1,'%d');

[s,line6] = unix(' awk "NR==6" DOSCAR ');
line6 = sscanf(line6,'%g'); fermi=line6(4); ndos = line6(3);

[s,line7] = unix(' awk "NR==7" DOSCAR ');
line7 = sscanf(line7,'%g');

%  [s,dsize] = unix(' cat DOSCAR | wc -l ');
%  dsize = sscanf(dsize,'%d'); natom = (dsize-5)/(line6(3)+1)-1;
%  



if size(line7,1)==5 % ISPIN = 2 case
% DOSCAR format 
% 1   2 3     4  5  6  7  8  9       10 11 12 13 14 15 16 17 18 19     20-34
% E    s              p                             d                    f
nspin=2;
b=7;
[o,tdos] = system(sprintf(' awk "NR==%d,NR==%d" DOSCAR ',b,(b+line6(3)-1))); b=b+line6(3);
tdos = sscanf(tdos,'%g'); tdos=reshape(tdos,5,line6(3)); tdos=tdos'; E = tdos(:,1); tdos=[ tdos(:,2) tdos(:,3) ]; 

[o,ncol] = unix(sprintf('awk "NR==%d" DOSCAR ',b+1)); ncol = sscanf(ncol,'%g'); ncol = size(ncol,1);

b=b+1;
%  for s=1:natom
%  [o,read] = system(sprintf(' awk "NR==%d,NR==%d" DOSCAR ',b,(b+line6(3)-1))); b=b+line6(3)+1;
%  read = sscanf(read,'%g'); read=reshape(read,ncol,line6(3)); read=read';
%  
%   if size(read,2)==33
%   pdoss{s}(:,1)=read(:,2); % s-up
%   pdoss{s}(:,5)=read(:,3); % s-dw
%   pdoss{s}(:,2)=read(:,4)+read(:,6)+read(:,8); % p-up
%   pdoss{s}(:,6)=read(:,5)+read(:,7)+read(:,9); % p-dw
%   pdoss{s}(:,3)=read(:,10)+read(:,12)+read(:,14)+read(:,16)+read(:,18); % d-up
%   pdoss{s}(:,7)=read(:,11)+read(:,13)+read(:,15)+read(:,17)+read(:,19); % d-dw
%   pdoss{s}(:,4)=read(:,20)+read(:,22)+read(:,24)+read(:,26)+read(:,28)+read(:,30)+read(:,32); % f-up
%   pdoss{s}(:,8)=read(:,21)+read(:,23)+read(:,25)+read(:,27)+read(:,29)+read(:,31)+read(:,33); % f-dw
%   end
%  
%   if size(read,2)==19
%   pdoss{s}(:,1)=read(:,2); % s-up
%   pdoss{s}(:,5)=read(:,3); % s-dw
%   pdoss{s}(:,2)=read(:,4)+read(:,6)+read(:,8); % p-up
%   pdoss{s}(:,6)=read(:,5)+read(:,7)+read(:,9); % p-dw
%   pdoss{s}(:,3)=read(:,10)+read(:,12)+read(:,14)+read(:,16)+read(:,18); % d-up
%   pdoss{s}(:,7)=read(:,11)+read(:,13)+read(:,15)+read(:,17)+read(:,19); % d-dw
%   pdoss{s}(:,4)=zeros(ndos,1); % f-up
%   pdoss{s}(:,8)=zeros(ndos,1); % f-dw
%   end
%  
%   if size(read,2)==9
%   pdoss{s}(:,1)=read(:,2); % s-up
%   pdoss{s}(:,5)=read(:,3); % s-dw
%   pdoss{s}(:,2)=read(:,4)+read(:,6)+read(:,8); % p-up
%   pdoss{s}(:,6)=read(:,5)+read(:,7)+read(:,9); % p-dw
%   pdoss{s}(:,3)=zeros(ndos,1); % d-up
%   pdoss{s}(:,7)=zeros(ndos,1); % d-dw
%   pdoss{s}(:,4)=zeros(ndos,1); % f-up
%   pdoss{s}(:,8)=zeros(ndos,1); % f-dw
%   end
%  
%  
%  end





else % ISPIN = 1 case



% DOSCAR format 
% 1   2   3  4   5     6  7  8  9 10   11 12 13 14 15 16 17
% E   s   p1 p2 p3    d1 d2 d3 d4 d5            f
nspin=1; b=7;
[o,tdos] = system(sprintf(' awk "NR==%d,NR==%d" DOSCAR ',b,(b+line6(3)-1))); b=b+line6(3);
tdos = sscanf(tdos,'%g'); tdos=reshape(tdos,3,line6(3)); tdos=tdos'; E = tdos(:,1); tdos=[ tdos(:,2) zeros(ndos,1) ]; 



[o,ncol] = unix(sprintf('awk "NR==%d" DOSCAR ',b+1)); ncol = sscanf(ncol,'%g'); ncol = size(ncol,1);


if ncol==0
pdoss=0;
disp(' '); disp('pdoss is empty !!!!'); disp(' '); 
else
b=b+1;
%  for s=1:natom
%  [o,read] = system(sprintf(' awk "NR==%d,NR==%d" DOSCAR ',b,(b+line6(3)-1))); b=b+line6(3)+1;
%  read = sscanf(read,'%g'); read=reshape(read,ncol,line6(3)); read=read'; 
%   if size(read,2)==17
%   pdoss{s}(:,1)=read(:,2); % s
%   pdoss{s}(:,2)=read(:,3)+read(:,4)+read(:,5); % p
%   pdoss{s}(:,3)=read(:,6)+read(:,7)+read(:,8)+read(:,9)+read(:,10); % d
%   pdoss{s}(:,4)=read(:,11)+read(:,12)+read(:,13)+read(:,14)+read(:,15)+read(:,16)+read(:,17); % f
%   end
%  
%   if size(read,2)==10
%   pdoss{s}(:,1)=read(:,2); % s
%   pdoss{s}(:,2)=read(:,3)+read(:,4)+read(:,5); % p
%   pdoss{s}(:,3)=read(:,6)+read(:,7)+read(:,8)+read(:,9)+read(:,10); % d
%   pdoss{s}(:,4)=zeros(ndos,1); % f
%   end
%  
%   if size(read,2)==5
%   pdoss{s}(:,1)=read(:,2); % s
%   pdoss{s}(:,2)=read(:,3)+read(:,4)+read(:,5); % p
%   pdoss{s}(:,3)=zeros(ndos,1); % f
%   pdoss{s}(:,4)=zeros(ndos,1); % f
%   end 
%  
%  
%  
%  end

end

end




%  disp([' ']);
%  disp(['PDOS was read !!! >> natom=' num2str(size(pdoss,2)) '; nspin=' num2str(nspin) '; ndos=' num2str(ndos) ])
%  if size(line7,1)==5
%  disp(['attention : Magnetic PDOS !!!']);
%  end
%  disp([' ']);
%  

end










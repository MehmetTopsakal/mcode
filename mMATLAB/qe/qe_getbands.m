function [bands_up,bands_dw,kpoints]=qe_getbands(nscfout)

if nargin < 1, nscfout='nscf.out'; end 


% NOTE: This script works only with UNIX
% must set - verbosity = 'high'
% nscfout='nscf.out'
[s,nspin]=system(sprintf(' cat %s | grep -a SPIN  | wc -l',nscfout)); nspin = sscanf(nspin,'%d');

if  nspin==0 ; % nonmagnetic  
[s,nkpoints]=system(sprintf(' cat %s | grep -a "number of k points=" | awk ''{print $5}''',nscfout)); nkpoints = sscanf(nkpoints,'%d');
[s,nbands]=system(sprintf(' cat %s | grep -a "Kohn-Sham states" | awk ''{print $5}''',nscfout)); nbands = sscanf(nbands,'%d');  
%  [s,nelectrons_up]=system(sprintf(' cat %s | grep -a "number of electrons"  | awk ''{print $7}'' | awk -F "," ''{print $1}''  ',nscfout)); nelectrons_up = sscanf(nelectrons_up,'%g');
%  [s,nelectrons_dw]=system(sprintf(' cat %s | grep -a "number of electrons"  | awk ''{print $9}'' | awk -F ")" ''{print $1}''  ',nscfout)); nelectrons_dw = sscanf(nelectrons_dw,'%g');
% get energies    
[s,bline_b]=system(sprintf(' awk "NR>1" %s | grep -an "End of band structure calculation" %s | head -1 | awk -F ":" ''{print ($1-1)}'' ',nscfout)); bline_b = sscanf(bline_b,'%d');
[s,bline_e]=system(sprintf(' awk "NR>1" %s | grep -an "Writing output data"  | head -1 | awk -F ":" ''{print ($1-1)}'' ',nscfout)); bline_e = sscanf(bline_e,'%d');
[s,bands]=system(sprintf(' awk "NR==%d,NR==%d" %s | awk ''!/k/'' | awk ''!/o/'' | awk "NF>=1" ',(bline_b+2),(bline_b-1),nscfout)); bands=sscanf(bands,'%g',[ (2*nbands) nkpoints  ]); 
bands=bands(1:size(bands,1)/2,:);
%efermi;
bands_up=bands; bands_dw=bands;

disp(' ')
disp('CHECK: Nonmagnetic case. bands_up equals bands_down. ')
disp(' ')
%  fermi_up=max(bands_up(nelectrons_up,:)); fermi_dw=max(bands_dw(nelectrons_dw,:)) ;
%  gap_up=-(max(bands_up(nelectrons_up,:))-min(bands_up(nelectrons_up+1,:)));
%  gap_dw=-(max(bands_dw(nelectrons_dw,:))-min(bands_dw(nelectrons_dw+1,:)));

[a,kpoints_path] =system(sprintf('awk ''/ 2pi/, / Dense  grid:/'' %s | grep wk | awk ''{print $5"  "$6"  "$7}'' | awk -F ")" ''{print $1}'' ',nscfout));
kpoints_path = sscanf(kpoints_path,'%g', [3 nkpoints] ) ; kpoints_path = kpoints_path' ; kpoints_path=kpoints_path(1:size(kpoints_path,1),:);

kpoints(1) = 0 ;
for k=1:size(kpoints_path,1)-1; k0=kpoints_path(k,:); k1=kpoints_path(k+1,:);
    dx=k0(1)-k1(1); dy=k0(2)-k1(2); dz=k0(3)-k1(3);
    kpoints(k+1) = kpoints(k) + sqrt(dx*dx+dy*dy+dz*dz);
end

else % magnetic
[s,nkpoints]=system(sprintf(' cat %s | grep -a "number of k points=" | awk ''{print $5}''',nscfout)); nkpoints = sscanf(nkpoints,'%d');
[s,nbands]=system(sprintf(' cat %s | grep -a "Kohn-Sham states" | awk ''{print $5}''',nscfout)); nbands = sscanf(nbands,'%d');  
%  [s,nelectrons_up]=system(sprintf(' cat %s | grep -a "number of electrons"  | awk ''{print $7}'' | awk -F "," ''{print $1}''  ',nscfout)); nelectrons_up = sscanf(nelectrons_up,'%g');
%  [s,nelectrons_dw]=system(sprintf(' cat %s | grep -a "number of electrons"  | awk ''{print $9}'' | awk -F ")" ''{print $1}''  ',nscfout)); nelectrons_dw = sscanf(nelectrons_dw,'%g');
% get energies    
[s,bline_b_up]=system(sprintf(' awk "NR>1" %s | grep -an "SPIN UP" %s | head -1 | awk -F ":" ''{print ($1-1)}'' ',nscfout)); bline_b_up = sscanf(bline_b_up,'%d');
[s,bline_b_dw]=system(sprintf(' awk "NR>1" %s | grep -an "SPIN DOWN" %s | head -1 | awk -F ":" ''{print ($1)}'' ',nscfout)); bline_b_dw = sscanf(bline_b_dw,'%d');
[s,bline_e]=system(sprintf(' awk "NR>1" %s | grep -an "Writing output data"  | head -1 | awk -F ":" ''{print ($1-1)}'' ',nscfout)); bline_e = sscanf(bline_e,'%d');
[s,bands_up]=system(sprintf(' awk "NR==%d,NR==%d" %s | awk ''!/k/'' | awk ''!/o/'' | awk "NF>=1" ',(bline_b_up+2),(bline_b_dw-1),nscfout)); bands_up=sscanf(bands_up,'%g',[ (2*nbands) nkpoints  ]); 
[s,bands_dw]=system(sprintf(' awk "NR==%d,NR==%d" %s | awk ''!/k/'' | awk ''!/o/'' | awk "NF>=1" ',(bline_b_dw+2),(bline_e),nscfout)); bands_dw=sscanf(bands_dw,'%g',[ (2*nbands) nkpoints  ]); 
%efermi;
bands_up=bands_up(1:size(bands_up,1)/2,:); bands_dw=bands_dw(1:size(bands_dw,1)/2,:);
%  fermi_up=max(bands_up(nelectrons_up,:)); fermi_dw=max(bands_dw(nelectrons_dw,:)) ;
%  gap_up=-(max(bands_up(nelectrons_up,:))-min(bands_up(nelectrons_up+1,:)));
%  gap_dw=-(max(bands_dw(nelectrons_dw,:))-min(bands_dw(nelectrons_dw+1,:)));

[a,kpoints_path] =system(sprintf('awk ''/ 2pi/, / Dense  grid:/'' %s | grep wk | awk ''{print $5"  "$6"  "$7}'' | awk -F ")" ''{print $1}'' ',nscfout));
kpoints_path = sscanf(kpoints_path,'%g', [3 nkpoints*2] ) ; kpoints_path = kpoints_path' ; kpoints_path=kpoints_path(1:size(kpoints_path,1)/4,:);

kpoints(1) = 0 ;
for k=1:size(kpoints_path,1)-1; k0=kpoints_path(k,:); k1=kpoints_path(k+1,:);
    dx=k0(1)-k1(1); dy=k0(2)-k1(2); dz=k0(3)-k1(3);
    kpoints(k+1) = kpoints(k) + sqrt(dx*dx+dy*dy+dz*dz);
end

end


end

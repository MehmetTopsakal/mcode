function [fermi]=qe_getfermi(nscfout)

if nargin < 1,   disp('  ');  disp('ATTENTION : Using scf.out to get Fermi Energy !!!!!  '); nscfout = 'scf.out'; disp('  '); end


if exist(nscfout) == 2 


% try1 -----------------------------------------\/
[s,fermi]=system(sprintf(' grep "the Fermi energy is "  %s  | awk ''{print $5}'' ',nscfout)); 
fermi = sscanf(fermi,'%g');
tf = isempty(fermi);


if  tf==0
return
end

% try2 -----------------------------------------\/
[s,fermi]=system(sprintf(' grep "highest occupied level (ev): "  %s  | awk ''{print $5}'' ',nscfout)); 
fermi = sscanf(fermi,'%g');
tf = isempty(fermi);


if  tf==0
return
end

% try3 -----------------------------------------\/
[s,fermi]=system(sprintf(' grep "highest occupied, lowest unoccupied level (ev):"   %s  | awk ''{print $7}'' ',nscfout)); 
fermi = sscanf(fermi,'%g');
tf = isempty(fermi);


if  tf==0
return
end

% try4 -----------------------------------------\/
[s,fermi]=system(sprintf(' grep "the spin up/dw Fermi energies are"   %s  | awk ''{print $7" "$8}'' ',nscfout)); 
fermi = sscanf(fermi,'%g'); fermi = min(fermi);
tf = isempty(fermi);


if  tf==0
return
end



%  % last chance !!!
%  
%  [s,nspin]=system(sprintf(' cat %s | grep -a SPIN  | wc -l',nscfout)); nspin = sscanf(nspin,'%d');
%  
%  if  nspin==0 ; % nonmagnetic
%  [s,nkpoints]=system(sprintf(' cat %s | grep -a "number of k points=" | awk ''{print $5}''',nscfout)); nkpoints = sscanf(nkpoints,'%d');
%  [s,nbands]=system(sprintf(' cat %s | grep -a "Kohn-Sham states" | awk ''{print $5}''',nscfout)); nbands = sscanf(nbands,'%d');  
%  [s,nelectrons]=system(sprintf(' cat %s | grep -a "number of electrons"  | awk ''{print $5}'' ',nscfout)); nelectrons = sscanf(nelectrons,'%g');   
%  [s,bline_b]=system(sprintf(' cat  %s | grep -an "End of band structure calculation"  | awk -F ":" ''{print $1 }'' ',nscfout)); bline_b = sscanf(bline_b,'%d');
%  [s,bline_e]=system(sprintf(' awk "NR>1" %s | grep -an "Writing output data"  | head -1 | awk -F ":" ''{print ($1-1)}'' ',nscfout)); bline_e = sscanf(bline_e,'%d');
%  [s,energies]=system(sprintf(' awk "NR==%d,NR==%d" %s | awk ''!/k/'' | awk ''!/o/'' | awk "NF>=1" ',(bline_b+2),(bline_e-2),nscfout)); energies=sscanf(energies,'%g',[ (2*nbands) nkpoints  ]); 
%  energies=energies(1:size(energies,1)/2,:); fermi=max(energies(nelectrons/2,:)); fermi = min(fermi); tf = isempty(fermi);
%  else % magnetic
%  [s,nkpoints]=system(sprintf(' cat %s | grep -a "number of k points=" | awk ''{print $5}''',nscfout)); nkpoints = sscanf(nkpoints,'%d');
%  [s,nbands]=system(sprintf(' cat %s | grep -a "Kohn-Sham states" | awk ''{print $5}''',nscfout)); nbands = sscanf(nbands,'%d');  
%  [s,nelectrons_up]=system(sprintf(' cat %s | grep -a "number of electrons"  | awk ''{print $7}'' | awk -F "," ''{print $1}''  ',nscfout)); nelectrons_up = sscanf(nelectrons_up,'%g');
%  [s,nelectrons_dw]=system(sprintf(' cat %s | grep -a "number of electrons"  | awk ''{print $9}'' | awk -F ")" ''{print $1}''  ',nscfout)); nelectrons_dw = sscanf(nelectrons_dw,'%g');   
%  [s,bline_b_up]=system(sprintf(' awk "NR>1" %s | grep -an "SPIN UP" %s | head -1 | awk -F ":" ''{print ($1-1)}'' ',nscfout)); bline_b_up = sscanf(bline_b_up,'%d');
%  [s,bline_b_dw]=system(sprintf(' awk "NR>1" %s | grep -an "SPIN DOWN" %s | head -1 | awk -F ":" ''{print ($1)}'' ',nscfout)); bline_b_dw = sscanf(bline_b_dw,'%d');
%  [s,bline_e]=system(sprintf(' awk "NR>1" %s | grep -an "Writing output data"  | head -1 | awk -F ":" ''{print ($1-1)}'' ',nscfout)); bline_e = sscanf(bline_e,'%d');
%  [s,energies_up]=system(sprintf(' awk "NR==%d,NR==%d" %s | awk ''!/k/'' | awk ''!/o/'' | awk "NF>=1" ',(bline_b_up+2),(bline_b_dw-1),nscfout)); energies_up=sscanf(energies_up,'%g',[ (2*nbands) nkpoints  ]); 
%  [s,energies_dw]=system(sprintf(' awk "NR==%d,NR==%d" %s | awk ''!/k/'' | awk ''!/o/'' | awk "NF>=1" ',(bline_b_dw+2),(bline_e),nscfout)); energies_dw=sscanf(energies_dw,'%g',[ (2*nbands) nkpoints  ]); 
%  energies_up=energies_up(1:size(energies_up,1)/2,:); energies_dw=energies_up(1:size(energies_dw,1)/2,:);
%  fermi_up=max(energies_up(nelectrons_up,:)); fermi_dw=max(energies_dw(nelectrons_dw,:)) ; fermi = [fermi_up fermi_dw]; fermi=fermi';
%  disp(' '); disp('Attention !!!, seperate Fermi energies'); fermi = min(fermi); tf = isempty(fermi);
%  end


if  tf==1 ; disp(' '); disp('ERROR !!!, something is WRONG, Unable to get Fermi energy !!'); return ; end

else 
disp('File does not exist !!!!!')
fermi = [];
end


end % function


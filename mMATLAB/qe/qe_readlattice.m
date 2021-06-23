function [celldm,lattice,positions]=qe_readlattice(file)


[s,celldm1]=system(sprintf(' grep "     celldm(1)=  " %s | awk ''{print $2" "$4" "$6}'' ',file));
 celldm1 = sscanf(celldm1,'%g');
[s,celldm2]=system(sprintf(' grep "     celldm(4)=  " %s | awk ''{print $2" "$4" "$6}'' ',file)); 
 celldm2 = sscanf(celldm2,'%g');

celldm=[celldm1' celldm2'];




[s,nline1]=system(sprintf(' grep -n "     crystal axes:" %s | awk -F : \''{print $1}\'' ',file)); 
nline1 = sscanf(nline1,'%d');

[s,lattice]=system(sprintf(' awk "NR==%d,NR==%d" %s | awk ''{print $4"  "$5"  "$6}'' ',(nline1+1),(nline1+3),file)); 
lattice = sscanf(lattice,'%g',[3 3]); lattice = lattice';



[s,natoms]=system(sprintf(' grep  "     number of atoms/cell      = " %s | awk  ''{print $5}'' ',file)); 
natoms = sscanf(natoms,'%d');

[s,nline2]=system(sprintf(' grep -n "     site n.     atom                  positions (alat units)" %s | awk -F : \''{print $1}\'' ',file)); 
nline2 = sscanf(nline2,'%d');

[s,positions]=system(sprintf(' awk "NR==%d,NR==%d" %s | awk ''{print $7"  "$8"  "$9}'' ',(nline2+1),(nline1+3+natoms),file)); 
positions = sscanf(positions,'%g',[3 natoms]); positions = positions';




end

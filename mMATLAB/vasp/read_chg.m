function [lattice,atoms,positions,chg_matrix]=read_chg(file)

% someone should find an alternative for the next two foolish lines !!!!
fid = fopen('filename.tmp', 'w'); fprintf(fid, '%s', file); fclose(fid);
unix('ln -s `cat filename.tmp` read_chg_file.tmp') ; unix('rm filename.tmp');

[s,line6] = unix('head read_chg_file.tmp | awk "NR==6"');
line6 = sscanf(line6,'%f') ; tf = isempty(line6);

if  tf==1 ; %vasp5 file

[s,line7] = unix('head read_chg_file.tmp | awk "NR==7"');  
line7 = sscanf(line7,'%f'); ntypes = size(line7,1);
fid = fopen('read_chg_file.tmp', 'r');
syslabel = fscanf(fid,'%c', 40); scale = fscanf (fid, '%g', 1);
lattice = fscanf (fid,'%g',[3 3]); lattice = lattice'; lattice = lattice*scale;
[labels] = fscanf (fid, '%s', [ntypes 1]); 
[natoms_line] = fscanf (fid, '%g', [1 ntypes]); atoms = natoms_line;
natoms = sum(natoms_line); fscanf (fid, '%s', 1); 
[positions] = fscanf (fid, '%g', [3 natoms ]); positions = positions' ;
[ngx]= fscanf (fid, '%g', 1); 
[ngy]= fscanf (fid, '%g', 1); 
[ngz]= fscanf (fid, '%g', 1);
chg_matrix = fscanf (fid, '%g', [1 (ngx*ngy*ngz)]); 
chg_matrix = reshape(chg_matrix,ngx,ngy,ngz);
fclose(fid);

else        %vasp4 file

ntypes = size(line6,1);
fid = fopen('read_chg_file.tmp', 'r');
syslabel = fscanf(fid,'%c', 40); scale = fscanf (fid, '%g', 1);
lattice = fscanf (fid,'%g',[3 3]); lattice = lattice'; lattice = lattice*scale;
%[labels] = fscanf (fid, '%s', [ntypes 1]); 
[natoms_line] = fscanf (fid, '%g', [1 ntypes]); atoms = natoms_line; 
natoms = sum(natoms_line); fscanf (fid, '%s', 1); 
[positions] = fscanf (fid, '%g', [3 natoms ]); positions = positions' ;
[ngx]= fscanf (fid, '%g', 1); 
[ngy]= fscanf (fid, '%g', 1); 
[ngz]= fscanf (fid, '%g', 1);
chg_matrix = fscanf (fid, '%g', [1 (ngx*ngy*ngz)]); 
chg_matrix = reshape(chg_matrix,ngx,ngy,ngz);
fclose(fid);

end

unix('rm read_chg_file.tmp ');
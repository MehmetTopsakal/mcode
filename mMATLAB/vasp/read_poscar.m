function [lattice,positions]=read_poscar(file)


% temporarily copy input file ================================================<
copyfile(file,'read_poscar_tmp_file');

% determine whether the file is in VASP5 format.==============================< 
[s,line6] = unix('awk "NR==6" read_poscar_tmp_file');
line6 = sscanf(line6,'%d') ; tf = isempty(line6);

if  tf==0 ; 
    disp('  ')
    disp('VASP4 format is NOT implemented yet.')
    disp('!! Please use VASP5 POSCAR format !!')
    disp('  ')
    error(' ')
end


% read first 6 lines =========================================================<
fid = fopen('read_poscar_tmp_file', 'r');

[s,line1] = unix('awk "NR==1" read_poscar_tmp_file | awk ''{print NF}'' ');
line1 = sscanf(line1,'%d');

syslabel = fscanf(fid,'%s', [ 1 line1 ] ); scale = fscanf (fid, '%g', 1);
lattice = fscanf (fid,'%g',[3 3]); lattice = lattice'; lattice = lattice*scale;

[s,line6] = unix('awk "NR==6" read_poscar_tmp_file | awk ''{print NF}'' ');
nlabels = sscanf(line6,'%d');

for l=1:nlabels ; labels{l} = fscanf(fid,'%s',1); end
natoms = fscanf (fid, '%d', nlabels); fclose(fid);

% read line 9 ================================================================<
[s,line9] = unix('awk "NR==9" read_poscar_tmp_file | awk ''{print $1}'' ');
line9 = sscanf(line9,'%f') ; tf = isempty(line9);


% read positions =============================================================<
if  tf==0 ; % no selective dynamics
[s,positions] = unix('awk "NR>=9" read_poscar_tmp_file | awk ''{print $1" "$2" "$3 "  1  1  1"}'' ');
positions = sscanf(positions,'%f', [6 sum(natoms)] ); positions = positions' ;
[s,line8] = unix('awk "NR==8" read_poscar_tmp_file | awk ''{print $1}'' ');
line9 = sscanf(line8,'%s') ; carordir = lower(line8) ; carordir = carordir(1) ;
else        % yes selective dynamics
[s,positions] = unix('awk "NR>=10" read_poscar_tmp_file | sed ''s/F/0/g'' | sed ''s/T/1/g'' | awk ''{print $1" "$2" "$3" "$4" "$5" "$6}'' ');
positions = sscanf(positions,'%f', [6 sum(natoms)] ); positions = positions' ;
[s,line9] = unix('awk "NR==9" read_poscar_tmp_file | awk ''{print $1}'' ');
line9 = sscanf(line9,'%s') ; carordir = lower(line9) ; carordir = carordir(1) ;
end


% convert to cartesian if in direct coordinates===============================<
if  carordir=='d' ;

for p=1:size(positions,1) ;
xt = positions(p,1)*lattice(1,1) + positions(p,2)*lattice(2,1) + positions(p,3)*lattice(3,1) ;
yt = positions(p,1)*lattice(1,2) + positions(p,2)*lattice(2,2) + positions(p,3)*lattice(3,2) ;
zt = positions(p,1)*lattice(1,3) + positions(p,2)*lattice(2,3) + positions(p,3)*lattice(3,3) ;
positions_cart(p,1) = xt; positions_cart(p,2) = yt; positions_cart(p,3) = zt;
end ; 

positions = [positions_cart positions(:,4) positions(:,5) positions(:,6)] ;

end 



for a=1:nlabels
[anumber(a),aradius,acolor] = ainfo(labels{a}) ;
end


n=1;
for t=1:nlabels
    howmany=natoms(t) ;
    positions(n:n+howmany-1,7)=anumber(t) ;
    n=n+howmany;
end

unix('rm -f read_poscar_tmp_file') ;


end

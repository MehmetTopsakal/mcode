function qe_drawns(spin,file,iatom,iwrite,azi,ele,dmax,isovalue,customsum)


% script written by Mehmet TOPSAKAL @ Jan 2015
% ATTENTION-1 : please be carefull. This script might have BUGS                                         !!!!
% ATTENTION-2 : this script works only for magnetic calculations (3d and 4f orbitals)                   !!!!
% ATTENTION-3 : atomic positions are read from the beginning of file (relaxed ones might be different)  !!!!
% ATTENTION-4 : This script DOES NOT work on windows                                                    !!!!
% ATTENTION-5 : This script MAY NOT work on mac                                                         !!!!


%   |Line 113 of /PW/src/write_ns.f90
%   |             WRITE( stdout,'(7f7.3)') ( REAL(vet(m1,m2))**2 + &
%   |                                      AIMAG(vet(m1,m2))**2, m2=1, ldim )
%   |should be changed as
%   |             WRITE( stdout,'(7f7.3)') ( REAL(vet(m1,m2)), m2=1, ldim )


 if nargin < 9, customsum   = 'all'       ; end
 if nargin < 8, isovalue = 0.02          ; end 
 if nargin < 7, dmax = 3                  ; end 
 if nargin < 6, ele = 90                  ; end
 if nargin < 5, azi = 0                   ; end
 if nargin < 4, iwrite = 1                ; end
 if nargin < 3, iatom  = 1                ; end
 if nargin < 2, file = 'scf.out'          ; end
 if nargin < 1, disp('...') ; 
disp('USAGE: qe_drawns(spin,file,iatom,iwrite,azi,ele,dmax,isovalue)');
disp('       qe_drawns(''1'',''scf.out'',1,3,0,90,2.5,0.025)         (defaults)'); disp('... ') ;
return; end

[a,nns] = system(sprintf('grep "enter write_ns" %s | wc -l ',file)); nns = sscanf(nns,'%d');
nns %disp('divide by 2 if this is a relaxation')

 if nargin < 4, iwrite = nns              ; end

%  read ns
if iatom < 10,
[s,lines]=system(sprintf(' grep -n "atom    %d   Tr" %s | awk -F : \''{print $1}\'' ',iatom,file)); 
lines = sscanf(lines,'%d'); TF = isempty(lines); 
else
[s,lines]=system(sprintf(' grep -n "atom   %d   Tr" %s | awk -F : \''{print $1}\'' ',iatom,file)); 
lines = sscanf(lines,'%d'); TF = isempty(lines); 
end

if TF == 1, disp('ERROR: your file does NOT have any ns information)'); disp('... exitting') ; return; end


[s,eval_up]=system(sprintf(' awk "NR==%d" %s ',(lines(iwrite)+3),file)); 
eval_up = sscanf(eval_up,'%g'); eval_up = eval_up';


if size(eval_up,2)==5
[s,evec_up]=system(sprintf(' awk "NR==%d,NR==%d" %s ',(lines(iwrite)+5),(lines(iwrite)+9),file)); 
evec_up = sscanf(evec_up,'%g',[5 5]); evec_up = evec_up';

[s,eval_dw]=system(sprintf(' awk "NR==%d" %s ',(lines(iwrite)+18),file)); 
eval_dw = sscanf(eval_dw,'%g'); eval_dw = eval_dw';

[s,evec_dw]=system(sprintf(' awk "NR==%d,NR==%d" %s ',(lines(iwrite)+20),(lines(iwrite)+24),file)); 
evec_dw = sscanf(evec_dw,'%g',[5 5]); evec_dw = evec_dw';
end


if size(eval_up,2)==7
[s,evec_up]=system(sprintf(' awk "NR==%d,NR==%d" %s ',(lines(iwrite)+5),(lines(iwrite)+11),file)); 
evec_up = sscanf(evec_up,'%g',[7 7]); evec_up = evec_up';

[s,eval_dw]=system(sprintf(' awk "NR==%d" %s ',(lines(iwrite)+22),file)); 
eval_dw = sscanf(eval_dw,'%g'); eval_dw = eval_dw';

[s,evec_dw]=system(sprintf(' awk "NR==%d,NR==%d" %s ',(lines(iwrite)+24),(lines(iwrite)+30),file)); 
evec_dw = sscanf(evec_dw,'%g',[7 7]); evec_dw = evec_dw';
end



switch lower(spin)

case {1,'1','u','up'}
C=eval_up; V = evec_up; title1 = 'up, C(';

case {2,'2','d','dw','down'}
C=eval_dw; V = evec_dw; title1 = 'dw, C(';

end

%  C
%  V



%  read "first" lattice and positions
[s,nline1]=system(sprintf(' grep -n "     crystal axes:" %s | head -1 | awk -F : \''{print $1}\'' ',file)); 
nline1 = sscanf(nline1,'%d');

[s,alat]=system(sprintf(' grep "lattice parameter (alat)  =" %s | head -1 |awk  \''{print $5}\'' ',file)); 
alat = sscanf(alat,'%g');

[s,lattice]=system(sprintf(' awk "NR==%d,NR==%d" %s | awk ''{print $4"  "$5"  "$6}'' ',(nline1+1),(nline1+3),file)); 
lattice = sscanf(lattice,'%g',[3 3]); lattice = lattice'; lattice = (alat/1.88972612456506)*lattice;

[s,natoms]=system(sprintf(' grep  "     number of atoms/cell      = " %s | head -1 | awk  ''{print $5}'' ',file)); 
natoms = sscanf(natoms,'%d');

[s,nline2]=system(sprintf(' grep -n "     site n.     atom                  positions (alat units)" %s | head -1 | head -1 | awk -F : \''{print $1}\'' ',file)); 
nline2 = sscanf(nline2,'%d');

[s,positions]=system(sprintf(' awk "NR==%d,NR==%d" %s | awk ''{print $7"  "$8"  "$9}'' ',(nline2+1),(nline2+natoms),file)); 
positions = sscanf(positions,'%g',[3 natoms]); positions = positions'; positions = (alat/1.88972612456506)*positions;


%  positions



%  move atom to center
center_atom = positions(iatom,:);


%  make 3x3x3 supercell
positions_sup = [
positions
positions(:,1)+lattice(1,1) positions(:,2)+lattice(1,2) positions(:,3)+lattice(1,3) % +x
positions(:,1)-lattice(1,1) positions(:,2)-lattice(1,2) positions(:,3)-lattice(1,3) % -x
positions(:,1)+lattice(2,1) positions(:,2)+lattice(2,2) positions(:,3)+lattice(2,3) % +y
positions(:,1)-lattice(2,1) positions(:,2)-lattice(2,2) positions(:,3)-lattice(2,3) % -y
positions(:,1)+lattice(3,1) positions(:,2)+lattice(3,2) positions(:,3)+lattice(3,3) % +z
positions(:,1)-lattice(3,1) positions(:,2)-lattice(3,2) positions(:,3)-lattice(3,3) % -z
positions(:,1)+lattice(1,1)+lattice(2,1) positions(:,2)+lattice(1,2)+lattice(2,2) positions(:,3)+lattice(1,3)+lattice(2,3) % +x+y
positions(:,1)+lattice(1,1)-lattice(2,1) positions(:,2)+lattice(1,2)-lattice(2,2) positions(:,3)+lattice(1,3)-lattice(2,3) % +x-y
positions(:,1)-lattice(1,1)+lattice(2,1) positions(:,2)-lattice(1,2)+lattice(2,2) positions(:,3)-lattice(1,3)+lattice(2,3) % -x+y
positions(:,1)-lattice(1,1)-lattice(2,1) positions(:,2)-lattice(1,2)-lattice(2,2) positions(:,3)-lattice(1,3)-lattice(2,3) % -x-y
positions(:,1)+lattice(3,1)+lattice(1,1) positions(:,2)+lattice(3,2)+lattice(1,2) positions(:,3)+lattice(3,3)+lattice(1,3) % +z+x
positions(:,1)+lattice(3,1)-lattice(1,1) positions(:,2)+lattice(3,2)-lattice(1,2) positions(:,3)+lattice(3,3)-lattice(1,3) % +z-x
positions(:,1)-lattice(3,1)+lattice(1,1) positions(:,2)-lattice(3,2)+lattice(1,2) positions(:,3)-lattice(3,3)+lattice(1,3) % -z+x
positions(:,1)-lattice(3,1)-lattice(1,1) positions(:,2)-lattice(3,2)-lattice(1,2) positions(:,3)-lattice(3,3)-lattice(1,3) % -z-x
positions(:,1)+lattice(3,1)+lattice(2,1) positions(:,2)+lattice(3,2)+lattice(2,2) positions(:,3)+lattice(3,3)+lattice(2,3) % +z+y
positions(:,1)+lattice(3,1)-lattice(2,1) positions(:,2)+lattice(3,2)-lattice(2,2) positions(:,3)+lattice(3,3)-lattice(2,3) % +z-y
positions(:,1)-lattice(3,1)+lattice(2,1) positions(:,2)-lattice(3,2)+lattice(2,2) positions(:,3)-lattice(3,3)+lattice(2,3) % -z+y
positions(:,1)-lattice(3,1)-lattice(2,1) positions(:,2)-lattice(3,2)-lattice(2,2) positions(:,3)-lattice(3,3)-lattice(2,3) % -z-y
positions(:,1)+lattice(3,1)+lattice(1,1)+lattice(2,1) positions(:,2)+lattice(3,2)+lattice(1,2)+lattice(2,2) positions(:,3)+lattice(3,3)+lattice(1,3)+lattice(2,3) % +z+x+y
positions(:,1)+lattice(3,1)+lattice(1,1)-lattice(2,1) positions(:,2)+lattice(3,2)+lattice(1,2)-lattice(2,2) positions(:,3)+lattice(3,3)+lattice(1,3)-lattice(2,3) % +z+x-y
positions(:,1)+lattice(3,1)-lattice(1,1)-lattice(2,1) positions(:,2)+lattice(3,2)-lattice(1,2)-lattice(2,2) positions(:,3)+lattice(3,3)-lattice(1,3)-lattice(2,3) % +z-x-y
positions(:,1)+lattice(3,1)-lattice(1,1)+lattice(2,1) positions(:,2)+lattice(3,2)-lattice(1,2)+lattice(2,2) positions(:,3)+lattice(3,3)-lattice(1,3)+lattice(2,3) % +z-x+y
positions(:,1)-lattice(3,1)+lattice(1,1)+lattice(2,1) positions(:,2)-lattice(3,2)+lattice(1,2)+lattice(2,2) positions(:,3)-lattice(3,3)+lattice(1,3)+lattice(2,3) % -z+x+y
positions(:,1)-lattice(3,1)+lattice(1,1)-lattice(2,1) positions(:,2)-lattice(3,2)+lattice(1,2)-lattice(2,2) positions(:,3)-lattice(3,3)+lattice(1,3)-lattice(2,3) % -z+x-y
positions(:,1)-lattice(3,1)-lattice(1,1)-lattice(2,1) positions(:,2)-lattice(3,2)-lattice(1,2)-lattice(2,2) positions(:,3)-lattice(3,3)-lattice(1,3)-lattice(2,3) % -z-x-y
positions(:,1)-lattice(3,1)-lattice(1,1)+lattice(2,1) positions(:,2)-lattice(3,2)-lattice(1,2)+lattice(2,2) positions(:,3)-lattice(3,3)-lattice(1,3)+lattice(2,3) % -z-x+y
]; positions = positions_sup;

%



%  setup XYZ mesh 
x = [-2:0.1:2];
y = [-2:0.1:2];
z = [-2:0.1:2];
[X,Y,Z] = meshgrid(x,y,z);

Rsq = X.^2 + Y.^2 + Z.^2; R = sqrt(Rsq); xx=X./R; yy = Y./R; zz = Z./R;
rcst = 3; xx=X./R; yy = Y./R; zz = Z./R; psi_rad = rcst^2*Rsq.*exp(-rcst*R/1);



if size(C,2)==7
%      | http://en.wikipedia.org/wiki/Table_of_spherical_harmonics
%                                                     | http://winter.group.shef.ac.uk/orbitron/AOs/4f/index-gen.html
orb1 = 0.5*(zz.*(5*zz.^2-3));                       %    Y_3,0   =  4fz3
orb2 = -sqrt(3/2)*0.5*xx.*(5*zz.^2-1);              %    Y_3,+1  =  4fxz2
orb3 = -sqrt(3/2)*0.5*yy.*(5*zz.^2-1);              %    Y_3,-1  =  4fyz2 
orb4 = 0.5*sqrt(15)*zz.*(xx.^2-yy.^2);              %    Y_3,+2  =  4fz(x2-y2)
orb5 = sqrt(15)*xx.*yy.*zz;                         %    Y_3,-2  =  4fxyz
orb6 = -0.5*sqrt(5/2)*xx.*(xx.^2-3*yy.^2);          %    Y_3,+3  =  4fx(x2-3y2)
orb7 = -0.5*sqrt(5/2)*yy.*(3*xx.^2-yy.^2);          %    Y_3,-3  =  4fy(3x2-y2)

occ_orb{1} = (V(1,1)*orb1+V(2,1)*orb2+V(3,1)*orb3+V(4,1)*orb4...
    +V(5,1)*orb5+V(6,1)*orb6+V(7,1)*orb7).*psi_rad;
occ_orb{2} = (V(1,2)*orb1+V(2,2)*orb2+V(3,2)*orb3+V(4,2)*orb4...
    +V(5,2)*orb5+V(6,2)*orb6+V(7,2)*orb7).*psi_rad;
occ_orb{3} = (V(1,3)*orb1+V(2,3)*orb2+V(3,3)*orb3+V(4,3)*orb4...
    +V(5,3)*orb5+V(6,3)*orb6+V(7,3)*orb7).*psi_rad;
occ_orb{4} = (V(1,4)*orb1+V(2,4)*orb2+V(3,4)*orb3+V(4,4)*orb4...
    +V(5,4)*orb5+V(6,4)*orb6+V(7,4)*orb7).*psi_rad;
occ_orb{5} = (V(1,5)*orb1+V(2,5)*orb2+V(3,5)*orb3+V(4,5)*orb4...
    +V(5,5)*orb5+V(6,5)*orb6+V(7,5)*orb7).*psi_rad;
occ_orb{6} = (V(1,6)*orb1+V(2,6)*orb2+V(3,6)*orb3+V(4,6)*orb4...
    +V(5,6)*orb5+V(6,6)*orb6+V(7,6)*orb7).*psi_rad;
occ_orb{7} = (V(1,7)*orb1+V(2,7)*orb2+V(3,7)*orb3+V(4,7)*orb4...
    +V(5,7)*orb5+V(6,7)*orb6+V(7,7)*orb7).*psi_rad;
end


if size(C,2)==5
%  http://en.wikipedia.org/wiki/Table_of_spherical_harmonics
orb1 = 0.5*(3*zz.^2-1);
orb2 = -sqrt(3)*zz.*xx; 
orb3 = -sqrt(3)*yy.*zz; 
orb4 = 0.5*sqrt(3)*(xx.^2-yy.^2);
orb5 = sqrt(3)*xx.*yy;

occ_orb{1} = (V(1,1)*orb1+V(2,1)*orb2+V(3,1)*orb3+V(4,1)*orb4...
    +V(5,1)*orb5).*psi_rad;
occ_orb{2} = (V(1,2)*orb1+V(2,2)*orb2+V(3,2)*orb3+V(4,2)*orb4...
    +V(5,2)*orb5).*psi_rad;
occ_orb{3} = (V(1,3)*orb1+V(2,3)*orb2+V(3,3)*orb3+V(4,3)*orb4...
    +V(5,3)*orb5).*psi_rad;
occ_orb{4} = (V(1,4)*orb1+V(2,4)*orb2+V(3,4)*orb3+V(4,4)*orb4...
    +V(5,4)*orb5).*psi_rad;
occ_orb{5} = (V(1,5)*orb1+V(2,5)*orb2+V(3,5)*orb3+V(4,5)*orb4...
    +V(5,5)*orb5).*psi_rad;
end




figure('Color',[0.6 0.8 0.9]);


v=version;

si=1;
for s=1:size(occ_orb,2)

subplot(2,2*(size(C,2)+1)/2,[(2*si-1) (2*si)]); si=si+1;
p = patch(isosurface(X, Y, Z, occ_orb{s}.^2, isovalue)); 

if v(1) == '4' % octave
set(p,'FaceColor',[(0.9-C(s))^2 (0.9-C(s))^2 (0.9-C(s))^2],'EdgeColor','b'); hold on; 
else           % matlab
set(p,'FaceColor',[(0.99-C(s))^2 (0.99-C(s))^2 (0.99-C(s))^2],'EdgeColor','none','FaceLighting', 'phong'); hold on; light('Position', [1 1 5]);
end

for l=1:size(positions,1)
d=sqrt((positions(l,1)-center_atom(1))^2+(positions(l,2)-center_atom(2))^2+(positions(l,3)-center_atom(3))^2);
if d<dmax
line([0 positions(l,1)-center_atom(1)], [0 positions(l,2)-center_atom(2)], [0 positions(l,3)-center_atom(3)], 'color', 'r', 'Linewidth', abs(3.5-d)); hold on
plot3([positions(l,1)-center_atom(1)], [positions(l,2)-center_atom(2)], [positions(l,3)-center_atom(3)],'b.','MarkerSize',10); hold on
end; end

title2 = [title1 num2str(s) ')=' num2str(C(s)) ]; title(title2);
axis equal; box on; axis([-2 2     -2 2    -2 2]); view([azi ele]); %axis off;

end % s loop




subplot(2,2*(size(C,2)+1)/2,[(2*si-1) (2*si)]); si=si+1;

if customsum == 'all', tosum=1:size(C,2); else  tosum=customsum; end
%   tosum=[1,6]

sum=0*occ_orb{1}.^2;
for s=1:size(tosum,2)
sum = C(tosum(s))^2*occ_orb{tosum(s)}.^2 + sum;
end

p = patch(isosurface(X, Y, Z, sum, isovalue)); 

if v(1) == '4' % octave
set(p,'FaceColor',[(0.9-C(s))^2 (0.9-C(s))^2 (0.9-C(s))^2],'EdgeColor','g'); hold on; 
else           % matlab
set(p,'FaceColor',[150/225 75/225 0],'EdgeColor','none','FaceLighting', 'phong'); hold on; light('Position', [1 1 5]);
end

for l=1:size(positions,1)
d=sqrt((positions(l,1)-center_atom(1))^2+(positions(l,2)-center_atom(2))^2+(positions(l,3)-center_atom(3))^2);
if d<dmax
line([0 positions(l,1)-center_atom(1)], [0 positions(l,2)-center_atom(2)], [0 positions(l,3)-center_atom(3)], 'color', 'r', 'Linewidth', abs(3.5-d)); hold on
plot3([positions(l,1)-center_atom(1)], [positions(l,2)-center_atom(2)], [positions(l,3)-center_atom(3)],'r.','MarkerSize',10); hold on
end; end

title2 = ['sum']; title(title2);
axis equal; box on; axis([-2 2     -2 2    -2 2]); view([azi ele]); %axis off;
 

C 





end








































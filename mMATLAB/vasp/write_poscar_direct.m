function write_poscar_direct(lattice,positions,output_file,format)
%
% usage 
%
if nargin < 4,  format=1; end ; 
if nargin < 3,  output_file='POSCAR'; end

if format==1; % yes selective dynamics 


ntypes = size(unique(positions(:,7),'rows'),1); types  = unique(positions(:,7),'rows'); types = flipud(types) ;
for l=1:ntypes ; [anumber,aradius,acolor,alabel] = ainfo(types(l)); labels{l}= alabel; end
for l=1:ntypes ; findings = find( positions(:,7) == types(l) ); natoms(l) = size(findings,1); end ; 
tmpfile = fopen('write_poscar.tmp','w'); 
fprintf(tmpfile,'metosa\n'); fprintf(tmpfile,'1.00000\n'); fprintf(tmpfile,'%.10f %.10f %.10f\n',lattice);
for l=1:ntypes ; fprintf(tmpfile,labels{l}); fprintf(tmpfile,' '); end; fprintf(tmpfile,'\n');
for l=1:ntypes ; fprintf(tmpfile,'%d ',natoms(l)); fprintf(tmpfile,' '); end; fprintf(tmpfile,'\n');
fprintf(tmpfile,'Selective dynamics\n'); fprintf(tmpfile,'Direct\n'); 
positions = [positions(:,1) positions(:,2) positions(:,3) positions(:,4) positions(:,5) positions(:,6)];
fprintf(tmpfile,'%.10f %.10f %.10f %d %d %d \n',positions'); fclose(tmpfile);
%                                          %                           %                           %                        %                             %                            %                           %                          %
unix('cat write_poscar.tmp | sed ''s/ 1 1 1/ T T T/g'' | sed ''s/ 1 1 0/ T T F/g'' | sed ''s/ 1 0 0/ T F F/g'' | sed ''s/ 0 0 0/ F F F/g'' | sed ''s/ 1 0 1/ T F T/g'' | sed ''s/ 0 1 1/ F T T/g'' | sed ''s/ 0 1 0/ F T F/g'' | sed ''s/ 0 0 1/ F F T/g'' >  write_poscar.tmp2 ');
copyfile('write_poscar.tmp2',output_file); 
unix(' rm -f write_poscar.tmp write_poscar.tmp2; ');


elseif format==2; % no selective dynamics 


ntypes = size(unique(positions(:,7),'rows'),1); types  = unique(positions(:,7),'rows'); types = flipud(types) ;
for l=1:ntypes ; [anumber,aradius,acolor,alabel] = ainfo(types(l)); labels{l}= alabel; end
for l=1:ntypes ; findings = find( positions(:,7) == types(l) ); natoms(l) = size(findings,1); end ; 
tmpfile = fopen('write_poscar.tmp','w'); 
fprintf(tmpfile,'metosa\n'); fprintf(tmpfile,'1.00000\n'); fprintf(tmpfile,'%.10f %.10f %.10f\n',lattice);
for l=1:ntypes ; fprintf(tmpfile,labels{l}); fprintf(tmpfile,' '); end; fprintf(tmpfile,'\n');
for l=1:ntypes ; fprintf(tmpfile,'%d ',natoms(l)); fprintf(tmpfile,' '); end; fprintf(tmpfile,'\n');
fprintf(tmpfile,'Direct\n'); positions = [positions(:,1) positions(:,2) positions(:,3)];
fprintf(tmpfile,'%.10f %.10f %.10f \n',positions'); fclose(tmpfile);
%                                          %                           %                           %                        %                             %                            %                           %                          %
unix('cat write_poscar.tmp | sed ''s/ 1 1 1/ T T T/g'' | sed ''s/ 1 1 0/ T T F/g'' | sed ''s/ 1 0 0/ T F F/g'' | sed ''s/ 0 0 0/ F F F/g'' | sed ''s/ 1 0 1/ T F T/g'' | sed ''s/ 0 1 1/ F T T/g'' | sed ''s/ 0 1 0/ F T F/g'' | sed ''s/ 0 0 1/ F F T/g'' >  write_poscar.tmp2 ');
copyfile('write_poscar.tmp2',output_file); 
unix(' rm -f write_poscar.tmp write_poscar.tmp2; ');

end


end
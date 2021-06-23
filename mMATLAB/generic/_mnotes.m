%=============================================================================
%      comment
%============================================================================= 

%  for i=1:size(folders,2)
%  cd(num2str(folders(i), '%.4f')) 
%  [p,f]=get_force
%  xforces(:,i)=f(:,1)
%  yforces(:,i)=f(:,2)
%  zforces(:,i)=f(:,3)
%  cd ..
%  end 
%  cd force_analysis
%  
%  save xforces ; save yforces ; save zforces ; 



mkdir(num2str(sprintf('%.2f' , 25+ds)))
cd(num2str(sprintf('%.2f' , 25+ds)))

        % shift upper Mo atoms
        positions(3:4,1:1)=positions(3:4,1:1)+cell_x*lattice(1,1) ;
        positions(3:4,2:2)=positions(3:4,2:2)+cell_y*lattice(2,2) ;
        % shift upper S  atoms
        positions(9:12,1:1)=positions(9:12,1:1)+cell_x*lattice(1,1) ;
        positions(9:12,2:2)=positions(9:12,2:2)+cell_y*lattice(2,2) ; 
        
        folder_name = [ num2str(cell_x, '%.6f') '__' num2str(cell_y, '%.6f') ]
        cd ../folders ; mkdir(folder_name) ; cd(folder_name) ; write_poscar(lattice,positions,'POSCAR',1) ; cd ../../kitchen
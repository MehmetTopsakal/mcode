function [grid_x,grid_y,grid_z,data]=read_chg_old(file)

copyfile(file,'read_chg_file') % link etme yolunu ara

! pos524 read_chg_file

! natoms=`head read_chg_file | awk "NR==6"  | awk '{print ($1+$2+$3+$4+$5+$6+$7+$8+$9)}'` ; ngrid=`echo $natoms+9 | bc ` ; grid=`awk "NR==$ngrid" read_chg_file` ; grid_x=`echo $grid | awk '{print $1}'` ; grid_y=`echo $grid | awk '{print $2}'` ; grid_z=`echo $grid | awk '{print $3}'` ; nupd_b=`echo $ngrid | awk '{print ($1+1)}'` ; awk "NR>=$nupd_b" read_chg_file  > chg_data1 ; awk  '{ for (i = 1; i <= (5); i++) printf("%s", $i "\n" ) }' chg_data1 > chg_data2 ; chgdatapoints=`echo $grid_x*$grid_y*$grid_z | bc  ` ;  awk "NR<=$chgdatapoints" chg_data2 > chg_data3 ; echo "$grid_x $grid_y $grid_z " > chg_grid ;

grid = load('chg_grid'); grid_x = grid(1) ; grid_y = grid(2) ; grid_z = grid(3) ; 

data = load('chg_data3') ;

%data = data' ; %traspozunu al

data = reshape(data,grid_x,grid_y,grid_z) ; 


! rm chg_data* chg_grid read_chg_file

end







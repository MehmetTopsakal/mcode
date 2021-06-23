function [positions,forces]=get_force

% NOTE: This script works only with MATLAB on UNIX

! natoms=`grep NIONS OUTCAR | awk '{print $12}'` ; POSITION_line=`grep -n " POSITION "  OUTCAR | awk "NR==1" | awk -F ":" '{print ($1+2)}'` ; awk "NR>=$POSITION_line" OUTCAR | awk "NR<=$natoms"  > get_force.tmp

data = load('get_force.tmp');

positions = data(:,1:3);
forces    = data(:,4:6);

! rm get_force.tmp

end

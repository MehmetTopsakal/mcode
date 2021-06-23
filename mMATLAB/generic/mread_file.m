function [output]=read_file(file,column)

copyfile(file,'read_file_tmp1');
save -ascii read_file_tmp2 column;

! sed "/%/d"  < read_file_tmp1 > read_file_tmp12
! cat read_file_tmp12 | awk -v col=`cat read_file_tmp2 | awk '{print (1*$1)}'` '{print $col}' > read_file_tmp3

output = load('read_file_tmp3');

! rm -rf read_file_tmp*

end
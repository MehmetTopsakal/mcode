#!/usr/bin/env python


import sys, os

inputs = sys.argv
ilen   = len(inputs)


if ilen == 1:
    print('input file is missing')   
    print('USAGE : mreplace $file $in $out')
    sys.exit(1)
if ilen == 2:
    print('input pattern is missing')    
    print('USAGE : mreplace $file $in $out')
    sys.exit(1)
if ilen == 3:
    print('seperator pattern is missing') 
    print('setting it as space ! (pattern remove mode)')   
    inputs.extend([' '])


file = inputs[1]
input_pattern = inputs[2]
seperator = inputs[3]


f1 = open(file,'r')
f2 = open('mreplace.tmp','w')

for line in f1:
    f2.write(line.replace(input_pattern,output_pattern))

f1.close()
f2.close()


os.rename('mreplace.tmp',file)





# old version 
#!/usr/bin/env bash
#
#file=$1
#text1=$2
#text2=$3
#
#
#
#cat > mreplace.tmp <<EOF
#perl -pi.bak -0777ne 's/$text1/$text2/g;' $file
#EOF
#
#
#chmod +x mreplace.tmp
#
#sh mreplace.tmp
#
#rm -rf $file.bak mreplace.tmp
#

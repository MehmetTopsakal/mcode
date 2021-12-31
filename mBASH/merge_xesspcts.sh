

rm -rf merge_xesspcts.tmp*
mkdir merge_xesspcts.tmp



for i in `mls`
do

cd $i
if [ -d CNBSE ]
then 
python -c "import mOCEAN; mOCEAN.get_xesspct()"
cp ocean_xesspcts.dat ../merge_xesspcts.tmp/$i.ocean_xesspcts.dat
elif [ -f ocean_xesspcts.dat ]
then
cp ocean_xesspcts.dat ../merge_xesspcts.tmp/$i.ocean_xesspcts.dat
fi
cd ..




done



cd merge_xesspcts.tmp




list=`ls *.ocean_xesspcts*`

natom=0

> ocean_xesspcts.dat
for i in $list
do
size=` grep "\# xesspct" $i | wc -l  `
let size=size/2
na=` grep natom $i | awk '{print $2}' | awk -F = '{print $2}'  `
np=` grep natom $i | awk '{print $3}' | awk -F = '{print $2}'  `
let natom=natom+na
grep "\# xesspct" $i | head -$size >> ocean_xesspcts.dat
done 

echo "# natom=$natom nphoton=$np" >> ocean_xesspcts.dat
echo " " >>  ocean_xesspcts.dat



for i in $list
do
echo "########### $i" >>  ocean_xesspcts.dat
b=`grep -n "##" $i | head -1 | awk -F : '{print $1}'`
awk "NR>$b" $i >>  ocean_xesspcts.dat
done

mv ocean_xesspcts.dat ..
cd ..
rm -rf merge_xesspcts.tmp
mpy ocean_plotxesspct.py






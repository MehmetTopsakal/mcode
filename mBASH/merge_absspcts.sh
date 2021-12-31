

rm -rf merge_absspcts.tmp*
mkdir merge_absspcts.tmp



for i in `mls`
do

cd $i
if [ -d CNBSE ]
then 
python -c "import mOCEAN; mOCEAN.get_absspct()"
cp ocean_absspcts.dat ../merge_absspcts.tmp/$i.ocean_absspcts.dat
elif [ -f ocean_absspcts.dat ]
then
cp ocean_absspcts.dat ../merge_absspcts.tmp/$i.ocean_absspcts.dat
fi
cd ..




done



cd merge_absspcts.tmp




list=`ls *.ocean_absspcts*`

natom=0

> ocean_absspcts.dat
for i in $list
do
size=` grep "\# absspct" $i | wc -l  `
let size=size/2
na=` grep natom $i | awk '{print $2}' | awk -F = '{print $2}'  `
np=` grep natom $i | awk '{print $3}' | awk -F = '{print $2}'  `
let natom=natom+na
grep "\# absspct" $i | head -$size >> ocean_absspcts.dat
done 

echo "# natom=$natom nphoton=$np" >> ocean_absspcts.dat
echo " " >>  ocean_absspcts.dat



for i in $list
do
echo "########### $i" >>  ocean_absspcts.dat
b=`grep -n "##" $i | head -1 | awk -F : '{print $1}'`
awk "NR>$b" $i >>  ocean_absspcts.dat
done

mv ocean_absspcts.dat ..
cd ..
rm -rf merge_absspcts.tmp
mpy ocean_plotabsspct.py






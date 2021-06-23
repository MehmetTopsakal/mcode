
vdc

cat total-analiz.dat | awk "NR>1" | awk "NF==11" | awk '{print $8 "  " $1}' > ev.in

mpy `which ev.py` 'ev.in' 1 1







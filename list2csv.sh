#!/bin/bash

heightexclude="1252 1257 1261 1269 1272 1281 1290 1308 1330 1339 1361 1362 1380 1381 1391 1395 1411"

# 1290, 1330, 1339 are usable for chemical shift changes, but not for 
# peak height analysis, due to overlap in an initial or final state

# 1380 and 1381 amide protons exchange extremely slowly, and therefore
# are not visible in samples grown in D2O. 

heightfiles="D2OvsH2O"

#foreach filename ($infiles) 


for filename in $heightfiles
do
    echo $filename
    rm $filename.csv
    /hpcc/wagner/edmonds/Sparky/Lists/titration/list2excel.py -i $filename.list -k N-H -x $heightexclude >> $filename.csv
done
#!/bin/bash

# silver disc 4Tb
uuid=af855912-96ee-408e-8696-1e4749ce66df





isavailable=`blkid | grep $uuid | wc -l`


if [ $isavailable == 1 ]
    then
    echo "disc is available"
    did=`blkid | grep $uuid | awk '{print $1}' | awk -F ":" '{print $1}'`
    echo $did
    ismounted=`df -h | grep $did | awk '{print $1}' | wc -l`
    echo $ismounted
    if [ $ismounted == 1 ]
        then
        echo "disc is mounted"
    else
        echo "disc is not mounted"
        mount $did /backups/silver4tb
    fi
    else
    echo "disc is not available"
fi

# 
# 
# did=`blkid | grep $uuid | awk '{print $1}' | awk -F ":" '{print $1}'`
# ismounted=`df -h | grep $did | awk '{print $1}' | wc -l`
# if [ $ismounted == 1 ]
#     then
#     echo "" >> /backup/weekly_backup.log ; echo "" >> /backup/weekly_backup.log ; echo "Back up started @ `date`" >> /backup/weekly_backup.log
#     rsync -avz --delete  /data     /backup/weekly >> /backup/weekly_backup.log
#     rsync -avz --delete  /home/mt  /backup/weekly >> /backup/weekly_backup.log
#     umount $did
#     else
#     echo "" >> /backup/weekly_backup.log ; echo "" >> /backup/weekly_backup.log ; echo "Back up disc is not available!!!!!" >> /backup/weekly_backup.log ; echo `date` >> /backup/weekly_backup.log
# fi
# 
# 










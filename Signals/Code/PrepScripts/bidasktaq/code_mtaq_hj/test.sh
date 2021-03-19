#!/bin/bash
#$ -cwd
#$ -m abe
#$ -M andrew.y.chen@frb.gov
# Delay: Lou and Shu 2017 RFS use 2 seconds before 1999 
# 	0 seconds for 1999-2002

# 1994: 10 sec per day


echo "Starting Job at `date`"

# run spreads code day by day
for year in $(seq 1993 1993)
do
    for month in $(seq -f "%02g" 4 4)
    do
        for day in $(seq -f "%02g" 5 6)
        do          
            echo finding spreads for $year$month$day at `date` 
            sas mtaq_spreads_hj.sas -set yyyymmdd $year$month$day -log ../temp_log/mtaq_$year$month$day.log
        done
    done
done    
echo "Ending Job at `date`"
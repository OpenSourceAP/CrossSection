#!/bin/bash
#$ -cwd
#$ -m abe
#$ -M andrew.y.chen@frb.gov
echo "Starting Job at `date`"

# run spreads code day by day
for year in $(seq 2018 2018)
do
  for month in $(seq -f "%02g" 1 12)
    do
        for day in $(seq -f "%02g" 1 31)
        do          
            echo finding spreads for $year$month$day at `date` 
            sas daily_taq_faster.sas -set yyyymmdd $year$month$day -log ../temp_log/dtaq_$year$month$day.log
        done
    done
done    
echo "Ending Job at `date`"
#!/bin/bash
#$ -cwd
#$ -m abe
#$ -M andrew.y.chen@frb.gov
echo "Starting Job at `date`"


# copy selected mastm files to scratch mast/
for year in $(seq 2015 2017)
do
    cp /wrdslin/nyse/sasdata/taqms/mast/mastm_$year* /scratch/frb/ayc_mast/      
done    
echo "Ending Job at `date`"
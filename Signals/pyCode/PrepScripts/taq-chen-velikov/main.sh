#!/bin/bash
#$ -cwd
#$ -m abe
# creates monthly dataset effective spreads from issm and wrds iid data
# to execute: "qsub main.sh"
# takes about an hour, mostly for issm

echo "Starting Job at `date`"

mkdir -p ~/temp_prep/data_for_dl/
mkdir -p ~/temp_prep/

echo PART 1/3 CALCULATING ISSM SPREADS
echo output will be in ~/temp_prep/data_for_dl/ and ~/temp_prep/

# run spreads code day by day
for year in $(seq 1983 1992)
do
    echo finding spreads for nyse/amex $year.  Today is `date` 
    sas issm_spreads.sas -set yyyy $year -set exchprefix nyam -log ~/temp_prep/log_nyam_$year.log

    echo finding spreads for nasdaq $year.  Today is `date` 
    sas issm_spreads.sas -set yyyy $year -set exchprefix nasd -log ~/temp_prep/log_nasd_$year.log
done    
echo "Ending Job at `date`"

echo combining and averaging and outputting to ~/temp_prep/data_for_dl/
sas combine_and_average.sas

echo PART 2/3 COMPILING WRDS IID SPREADS
sas iid_to_monthly.sas

echo PART 3/3 ADDING PERMNOS
sas add_permnos.sas
#!/bin/bash
#$ -cwd
#$ -m abe

# 2022 02 Andrew Chen
# creates ibes-crsp link, 13f data, option metrics stuff, and hf (taq-issm) spreads
# takes about four hours, mostly for option metrics

# built from masterSAS.sas, from 2020 11, Andrew Chen 

# Instructions: 
# - upload PrepScripts/ to wrds server 
# - ssh into wrds
# - cd PrepScripts/, run "qsub master.sh"
# - download ~/data_sas/* to $pathProject/Signals/Data/Prep/* 
# 	(i.e. ibes crsp link should be in $pathProject/Signals/Data/Prep/iclink.csv

# Heads up: Option Metrics data requires .pgpass is set up on WRDS
# https://wrds-www.wharton.upenn.edu/pages/support/programming-wrds/programming-r/r-from-the-web/
	
# Need help with ssh or accessing the wrds server in general?
# 	https://wrds-www.wharton.upenn.edu/pages/support/programming-wrds/programming-r/submitting-r-programs/
# (https://wrds-www.wharton.upenn.edu/pages/support/the-wrds-cloud/using-ssh-connect-wrds-cloud/

# ==== SETUP ====
echo "Starting Job at `date`"
echo "output will be in ~/data_prep/"

mkdir ~/data_prep/ # csv output will go here

# ==== IBES-CRSP LINK, TR 13F ====
echo "CREATING IBES-CRSP LINK (fast)"
sas iclink_to_csv.sas

echo "CREATING 13F DATA (10 min?)"
sas tr13f_pmg_edit.sas

# ==== OPTION METRICS ====
echo "CREATING OPTION METRICS DATA (about 3 hours)"
R CMD BATCH --no-save --no-restore OptionMetricsProcessing.R

# === HF SPREADS ====
# below copied from Chen-Velikov's hf-spreads-all/main.sh
echo "RUNNING CHEN-VELIKOV FORTH, JFQA HF SPREADS"

cd taq-chen-velikov

mkdir ~/temp_output/
mkdir ~/temp_log/

echo "PART 1/3 CALCULATING ISSM SPREADS (about 1 hour)"
echo output will be in ~/temp_output/ and ~/temp_log/

# run spreads code day by day (full issm sample is 1983-1992)
for year in $(seq 1983 1992)
do
    echo finding spreads for nyse/amex $year.  Today is `date` 
    sas issm_spreads.sas -set yyyy $year -set exchprefix nyam -log ~/temp_log/log_nyam_$year.log

    echo finding spreads for nasdaq $year.  Today is `date` 
    sas issm_spreads.sas -set yyyy $year -set exchprefix nasd -log ~/temp_log/log_nasd_$year.log
done    
echo "Ending Job at `date`"

echo combining and averaging and outputting to ~/temp_output/
sas combine_and_average.sas

echo "PART 2/3 COMPILING WRDS IID SPREADS"
sas iid_to_monthly.sas

echo "PART 3/3 ADDING PERMNOS"
sas add_permnos.sas

# clean up
mv ~/temp_output/*.csv ~/data_prep/
rm ~/data_prep/issm_daily.csv

echo "DONE"
echo "output should be in ~/data_prep/"
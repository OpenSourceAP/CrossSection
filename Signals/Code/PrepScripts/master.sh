#!/bin/bash
#$ -cwd
#$ -m abe

# 2022 02 Andrew Chen
# creates ibes-crsp link, 13f data, option metrics stuff, and hf (taq-issm) spreads
# takes about four hours, mostly for option metrics
# runs stuff from fastest to slowest
# built from masterSAS.sas, from 2020 11, Andrew Chen 

# For fast debugging:
# - in master.sh (this script), comment out sas tr13f...
# - in master.sh (this script), use "seq 1983 1983" in issm stuff
# - in taq-chen-velikov/iid_to_monthly.sas, use "maxobs = 20"
# - in taq-chen-velikov/issm_spreads.sas, use "maxobs = 20"
# - in OptionMetricsProcessing.R, use "querylimit = '20'"


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
mkdir ~/temp_output/
mkdir ~/temp_log/

# ==== IBES-CRSP LINK, TR 13F ====
echo "CREATING IBES-CRSP LINK (fast)"
sas iclink_to_csv.sas -log ~/temp_log/iclink_to_csv.log

echo "CREATING 13F DATA (10 min?)"
sas tr13f_pmg_edit.sas -log ~/temp_log/tr13f_pmg_edit.log

# === HF SPREADS ====
# below copied from Chen-Velikov's hf-spreads-all/main.sh
echo "RUNNING CHEN-VELIKOV FORTH, JFQA HF SPREADS"

cd taq-chen-velikov

echo "WRDS IID SPREADS, OUTPUTS TO ~/temp_output/ (15 min?)"
sas iid_to_monthly.sas -log ~/temp_log/iid_to_monthly.log


echo "CALCULATING ISSM SPREADS, OUTPUTS TO ~/temp_output/ (about 1 hour)"
# run spreads code day by day (full issm sample is 1983-1992)
for year in $(seq 1983 1992)
do
    echo finding spreads for nyse/amex $year.  Today is `date` 
    sas issm_spreads.sas -set yyyy $year -set exchprefix nyam -log ~/temp_log/log_nyam_$year.log

    echo finding spreads for nasdaq $year.  Today is `date` 
    sas issm_spreads.sas -set yyyy $year -set exchprefix nasd -log ~/temp_log/log_nasd_$year.log
done    
sas combine_and_average.sas -log ~/temp_log/combine_and_average.log

echo "ADDING PERMNOS TO IID AND ISSM AND COPYING TO ~/data_prep/"
sas add_permnos.sas -log ~/temp_log/add_permnos.log
cp ~/temp_output/hf_monthly.csv ~/data_prep/

cd ..

# ==== OPTION METRICS ====
echo "CREATING OPTION METRICS DATA (about 3 hours)"
R CMD BATCH --no-save --no-restore OptionMetricsProcessing.R ~/temp_log/OptionMetricsProcessing.log

echo "DONE"
echo "output should be in ~/data_prep/"
echo "Ending Job at `date`"
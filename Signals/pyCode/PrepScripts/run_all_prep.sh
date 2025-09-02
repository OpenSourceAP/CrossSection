#!/bin/bash
#$ -cwd
#$ -m abe

# for email notification of being done, submit using
#   qsub -m e -M Harvey_Liu_Zhu_2016_is_seriously_flawed@gmail.com master.sh

# 2022 02 Andrew Chen
# creates ibes-crsp link, 13f data, option metrics stuff, and hf (taq-issm) spreads
# takes about four hours, mostly for option metrics
# the hf stuff is not really being used right now (it's a placebo, pretty much)
# so it's okay if the code breaks before then.
# built from masterSAS.sas, from 2020 11, Andrew Chen 

# For fast debugging:
# - in master.sh (this script), comment out sas tr13f...
# - in master.sh (this script), use "seq 1983 1983" in issm stuff
# - in BH_2009.R, use "querylimit = '20'"
# - in taq-chen-velikov/iid_to_monthly.sas, use "maxobs = 20"
# - in taq-chen-velikov/issm_spreads.sas, use "maxobs = 20"
# - in OptionMetricsProcessing.R, use "querylimit = '20'"
# - in corwin_schultz_edit.sas, use "maxobs = 20"


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
echo "output will be in ~/temp_prep/"

mkdir ~/temp_prep/data_for_dl/ # csv output will go here
mkdir ~/temp_prep/temp_output/
mkdir ~/temp_prep/log/

# Change to temp_prep directory for relative paths
cd ~/temp_prep/

# # ==== IBES-CRSP LINK, TR 13F ====
echo "CREATING IBES-CRSP LINK (fast)"
sas iclink_to_csv.sas -log log/iclink_to_csv.log

echo "CREATING 13F DATA (10 min?)"
sas tr13f_pmg_edit.sas -log log/tr13f_pmg_edit.log

# ==== LF SPREADS (CORWIN-SCHULTZ, about 15 min) ====
echo "CREATING LF SPREADS (CORWIN-SCHULTZ, about 15 min)"
sas corwin_schultz_edit.sas -log log/corwin_schultz_edit.log

# === HF SPREADS ====
# below copied from Chen-Velikov's hf-spreads-all/main.sh
echo "RUNNING CHEN-VELIKOV FORTH, JFQA HF SPREADS"

echo "WRDS IID SPREADS, OUTPUTS TO temp_output/ (15 min?)"
sas taq-chen-velikov/iid_to_monthly.sas -log log/iid_to_monthly.log


echo "CALCULATING ISSM SPREADS, OUTPUTS TO temp_output/ (about 1 hour)"
# run spreads code day by day (full issm sample is 1983-1992)
for year in $(seq 1983 1992)
do
    echo finding spreads for nyse/amex $year.  Today is `date` 
    sas taq-chen-velikov/issm_spreads.sas -set yyyy $year -set exchprefix nyam -log log/log_nyam_$year.log

    echo finding spreads for nasdaq $year.  Today is `date` 
    sas taq-chen-velikov/issm_spreads.sas -set yyyy $year -set exchprefix nasd -log log/log_nasd_$year.log
done    
sas taq-chen-velikov/combine_and_average.sas -log log/combine_and_average.log

echo "ADDING PERMNOS TO IID AND ISSM AND COPYING TO data_for_dl/"
sas taq-chen-velikov/add_permnos.sas -log log/add_permnos.log
cp temp_output/hf_monthly.csv data_for_dl/

# # ==== OPTION METRICS LINK, ====
echo "CREATING OPTION METRICS LINK (fast)"
sas oclink_to_csv.sas -log log/oclink_to_csv.log

# ==== OPTION METRICS ====
echo "CREATING OPTION METRICS DATA (about 3 hours)"
R CMD BATCH --no-save --no-restore OptionMetricsProcessing.R log/OptionMetricsProcessing.log

# ==== OPTION METRICS: Bali-Hovak ====
echo "CREATING BALI-HOVAK IMPLIED VOL (about 30 min)"
R CMD BATCH --no-save --no-restore bali_hovak.R log/bali_hovak.log

echo "DONE"
echo "output should be in ~/temp_prep/data_for_dl/"
echo "Ending Job at `date`"

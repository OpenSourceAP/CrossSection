#!/bin/bash
#$ -cwd
#$ -m abe

# creates 13f data, option metrics stuff, and hf (taq-issm) spreads
# takes about four hours, mostly for option metrics
# the hf stuff is not really being used right now (it's a placebo, pretty much)

# Instructions if you're on mac/linux:
# - run ./prep1_run_on_wrds.sh
# - wait a few hours
# - run ./prep2_dl_from_wrds.sh

# Instructions if you're on windows:
# - upload PrepScripts/* to wrds server in ~/temp_prep/
# - ssh into wrds
# - cd ~/temp_prep/, run "qsub run_all_prep.sh"
# - download ~/temp_prep/data_for_dl/* to pathProject/Signals/pyData/Prep/* 
# 	(i.e. tr_13f.csv, corwin_schultz_spread.csv, hf_monthly.csv, OptionMetrics*.csv, bali_hovak_imp_vol.csv)

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

# # ==== TR 13F ====
# echo "CREATING 13F DATA (10 min?)"
# sas tr13f_pmg_edit.sas -log log/tr13f_pmg_edit.log

# ==== OPTION METRICS: Volume ====
echo "CREATING OPTION METRICS VOLUME (about 60 minutes)"
R CMD BATCH --no-save --no-restore OptionMetricsVolume.R log/OptionMetricsVolume.log

# ==== OPTION METRICS: Vol Surface ====
echo "CREATING OPTION METRICS VOL SURFACE (about 1 hour)"
R CMD BATCH --no-save --no-restore OptionMetricsVolSurf.R log/OptionMetricsVolSurf.log

# ==== OPTION METRICS: XZZ (Smirk/Skew1) ====
echo "CREATING OPTION METRICS XZZ (Smirk/Skew1, about 2 hours)"
R CMD BATCH --no-save --no-restore OptionMetricsXZZ.R log/OptionMetricsXZZ.log

# ==== OPTION METRICS: Bali-Hovak ====
echo "CREATING BALI-HOVAK IMPLIED VOL (about 30 min)"
R CMD BATCH --no-save --no-restore bali_hovak.R log/bali_hovak.log

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

echo "ADDING PERMNOS TO IID AND ISSM"
sas taq-chen-velikov/add_permnos.sas -log log/add_permnos.log

echo "DONE"
echo "output should be in ~/temp_prep/data_for_dl/"
echo "Ending Job at `date`"
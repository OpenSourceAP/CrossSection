#!/bin/bash
#$ -cwd
#$ -m abe

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
echo "output will be in ~/data_prep/"

mkdir ~/data_prep/ # csv output will go here
mkdir ~/temp_output/
mkdir ~/temp_log/

# ==== IBES-CRSP LINK, TR 13F ====
echo "CREATING IBES-CRSP LINK (fast)"
sas oclink_to_csv.sas -log ~/temp_log/oclink_to_csv.log



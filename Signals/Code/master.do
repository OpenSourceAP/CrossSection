** Master file

/*
This code is set up to run with the following path structure (Data and Log folders are created automatically)

+---Signals
+---/Code          (contains scripts that call other scripts and SAS/R files)
|   /Data          (contains all data download scripts)
|   /Logs          (contains log files created during running scripts) 

Optional inputs:
	/Data/Prep/
		iclink.csv		
		OptionMetrics.csv
		tr_13f.csv
		corwin_schultz_spread.csv		

These are created by code in Signals/PrepScripts/.  They are required for producing the signals that use IBES (iclink.csv), OptionMetrics, and Thomson-Reuter's 
13f data, but master.do will still produce the CRSP-Compustat signals if you do not have them.  corwin_schultz_spread.csv is only used for the BidAskSpread predictor.
*/

*------------------------------------------------------------
// SET PROJECT PATH AND WRDS CONNECTION NAME HERE !
*------------------------------------------------------------
*global pathProject "PATH TO PROJECT HERE" // required, should point to location of SignalDocumentation.xlsx
*global wrdsConnection "wrds-stata" // required, see readme
*global RSCRIPT_PATH "C:/Program Files/R/R-4.0.3/bin/Rscript.exe" // optional, used for like 3 signals (see DataDownloads/*.R)

if ("$pathProject" != "" & "$wrdsConnection" !="") {
    di("Relevant paths have been set")
} 
else {
    display as error "Relevant paths have not all been set"
	exit 999
}
if ("$RSCRIPT_PATH" != ""){
	global RSCRIPT_PATH = "missing"
}


// Set storage option of signal files
global save_csv 1 // csvs are main output, should always be 1
global save_dta 0 // for testing, maybe future use

// Run settings file that defines a few variables, creates folders, tests folder structure
// and installs required packages
do "$pathProject/Signals/Code/settings"

// Run files

* Download data
do "$pathCode/01_DownloadData.do"

* Create predictors
do "$pathCode/02_CreatePredictors.do"

* Create placebos
do "$pathCode/03_CreatePlacebos.do"

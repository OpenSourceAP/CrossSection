** Master file

/*
This code is set up to run with the following path structure (Data and Log folders are created automatically)

+---Signals
+---/Code          (contains scripts that call other scripts and SAS/R files)
|   /Data          (contains all data download scripts)
|   /Logs          (contains log files created during running scripts) 

Requires:
	/Data/Prep/
		corwin_schultz_spread.csv
		iclink.csv
		OptionMetrics.csv
		tr_13f.csv	
*/

*------------------------------------------------------------
// SET PROJECT PATH, R PATH AND WRDS CONNECTION NAME HERE !
*------------------------------------------------------------
*global pathProject "PATH TO PROJECT HERE"
*global RSCRIPT_PATH "C:/Program Files/R/R-4.0.3/bin/Rscript.exe"
*global wrdsConnection "wrds-stata"

if ("$pathProject" != "" & "$RSCRIPT_PATH" != "" & "$wrdsConnection" !="") {
    di("Relevant paths have been set")
} 
else {
    display as error "Relevant paths have not all been set"
	exit 999
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

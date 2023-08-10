// Set relative paths
global pathLogs "$pathProject/Signals/Logs/"

global pathCode "$pathProject/Signals/Code/"
global pathCodeDownloads "$pathProject/Signals/Code/DataDownloads/"
global pathCodePredictors "$pathProject/Signals/Code/Predictors/"
global pathCodePlacebos "$pathProject/Signals/Code/Placebos/"

global pathtemp "$pathProject/Signals/Data/temp/"
global pathData "$pathProject/Signals/Data/"
global pathDataPrep "$pathProject/Signals/Data/Prep/"
global pathDataIntermediate "$pathProject/Signals/Data/Intermediate/"
global pathDataPredictors "$pathProject/Signals/Data/Predictors/"
global pathDataPlacebos "$pathProject/Signals/Data/Placebos/"

// Confirm existence of directories and create data folder if it does not exist
confirm file "$pathCode/master.do"
confirm file "$pathCodeDownloads/B_CompustatAnnual.do"
confirm file "$pathCodePredictors/STreversal.do"

* Create log folder
cap mkdir "$pathLogs"

* Create data folders
cap mkdir "$pathData"
cap mkdir "$pathtemp"
cap mkdir "$pathDataIntermediate"
cap mkdir "$pathDataPredictors"
cap mkdir "$pathDataPlacebos"
cap mkdir "$pathDataPrep"

// Other settings
set more off, permanently


// Install or update packages
ssc install tscollap, replace
ssc install mdesc, replace
ssc install winsor2, replace
ssc install freduse, replace
ssc install fsum, replace
ssc install egenmore, replace
ssc install asrol, replace
ssc install asreg, replace
ssc install astile, replace
ssc install _gwtmean, replace
ssc install fastxtile, replace
ssc install egenmisc, replace
ssc install ftools, replace
ssc install gtools, replace
ssc install moremata, replace
ssc install relrank, replace
ssc install fs, replace
ssc install filelist, replace
ssc install rscript, replace
ssc install sicff, replace

** Master file
** Execute in the order below since files call data files produced by 
** previous files

global pathProject SETPROJECTPATH
global pathdataEXCHANGE SETDATAPATH

// Install packages if not already installed
ssc install tscollap, replace
ssc install mdesc, replace
ssc install freduse, replace
ssc install fsum, replace
ssc install egenmore, replace
ssc install asrol, replace
ssc install asreg, replace
ssc install _gwtmean, replace
ssc install fastxtile, replace
ssc install egenmisc, replace
ssc install ftools, replace
ssc install gtools, replace
ssc install moremata, replace
ssc install relrank, replace

// Also install Judson Caskey's ffind.do for Fama-French industry classifications 
net from https://sites.google.com/site/judsoncaskey/data
net install utilities.pkg

// Add paths
adopath + "$pathProject/Code/Stata"

// Other settings
set more off, permanently

// Run files
* Linking tables
do "$pathProject/Code/Stata/11_PrepareLinkingTables.do"
* Other data
do "$pathProjecct/Code/12_PrepareOtherData.do"
* Credit ratings
do "$pathProject/Code/Stata/13_PrepareRatings.do"
* Annual Compustat
do "$pathProject/Code/Stata/14_PrepareAnnualCS.do"
* Daily CRSP
do "$pathProject/Code/Stata/15_PrepareDailyCRSP.do"
* Monthly CRSP
do "$pathProject/Code/Stata/16_PrepareMonthlyCRSP.do"
* IBES
do "$pathProject/Code/Stata/17_PrepareIBES.do"
* Quarterly Compustat
do "$pathProject/Code/Stata/18_PrepareQuarterlyCS.do"
* Input from multiple data sources
do "$pathProject/Code/Stata/19_PrepareFromMultipleFiles.do"


*** Merge datasets
do "$pathProject/Code/Stata/20_MergeDatasets.do"

*** Create firm-month signals 
do "$pathProject/Code/Stata/30_CreateSignals.do"



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
global pathProject "/cm/chen/openap/release_2025/CrossSection-master/" // required, should point to location of SignalDoc.csv
global wrdsConnection "wrds-stata" // required, see readme
global RSCRIPT_PATH "/opt/local/bin/Rscript/" // optional, used for like 3 signals (see DataDownloads/*.R)

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

// Check Fred Import 

// capture import fred VXOCLS, clear
// if _rc!=0{
// 	display as error "fredkey is not set (see readme).  This is optional so you can comment out this check. But we thought we should check that you really want to miss about 6 predictors"
// 	exit
// }


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



// Set storage option of signal files
global save_csv 1 // csvs are main output, should always be 1
global save_dta 0 // for testing, maybe future use

// Run settings file that defines a few variables, creates folders, tests folder structure
// and installs required packages
// do "$pathProject/Signals/Code/settings"

// Run files

// * Download data
// do "$pathCode/01_DownloadData.do"
//
// * Create predictors
// do "$pathCode/02_CreatePredictors.do"
//
// * Create placebos
// do "$pathCode/03_CreatePlacebos.do"

// ================================================


// ===================================================
* paste below =
// =====================================================


* TrendFactor
* ------------
* See sections 2.1 and 2.2 of the paper for a detailed description

* debug mode
local DEBUG_MODE_PRE1950 1

* 1. Compute moving averages
use permno time_d prc cfacpr using "$pathDataIntermediate/dailyCRSP", clear

* debug mode
if `DEBUG_MODE_PRE1950' == 1 {
    keep if time_d < td(01jul1940)
}

* Adjust prices for splits etc
gen P = abs(prc)/cfacpr // I guess they just take the absolute value of prc but it does not say in the paper
* Note that cfacpr has look-ahead bias but cfacpr cancels out when we normalize prices below, see
* https://github.com/OpenSourceAP/CrossSection/issues/95#issuecomment-2286842730

drop cfacpr prc

* Generate time variable without trading day gaps for simplicity and generate month variable for sorting
bys permno (time_d): gen time_temp = _n
gen time_avail_m = mofd(time_d)
format time_avail_m %tm

* Calculate moving average prices for various lag lengths
xtset permno time_temp
foreach L of numlist 3 5 10 20 50 100 200 400 600 800 1000 {

    asrol P, window(time_temp `L') stat(mean) by(permno) gen(A_`L')  // Do they require a minimum number of obs? Not discussed in the paper
	
}


* Keep only last observation each month
bys permno time_avail_m (time_d): keep if _n == _N


drop time_d time_temp 
* Normalize by closing price at end of month
foreach L of numlist 3 5 10 20 50 100 200 400 600 800 1000 {

    replace A_`L' = A_`L'/P
	
}


keep permno time_avail_m A_*
save tempMA, replace



** 2. Run cross-sectional regressions on monthly data
use permno time_avail_m ret prc exchcd shrcd mve_c using "$pathDataIntermediate/SignalMasterTable", clear

* Calculate size deciles based on NYSE stocks only
preserve
    keep if exchcd == 1
	gcollapse (p10) qu10 = mve_c, by(time_avail_m)
	save tempQU, replace
restore

merge m:1 time_avail_m using tempQU, nogenerate

* Filters need to be imposed here rather than at portfolio stage in order to run cross-sectional regressions on the filtered sample
keep if exchcd == 1 | exchcd == 2 | exchcd == 3
keep if shrcd == 10 | shrcd == 11
keep if abs(prc)>=5
keep if mve_c >= qu10

drop exchcd shrcd qu10 mve_c prc

* Merge moving averages
merge 1:1 permno time_avail_m using tempMA, keep(match) nogenerate


* Cross-sectional regression of returns on trend signals in month t-1
xtset permno time_avail_m
gen fRet = f.ret  // Instead of lagging all moving averages, I lead the return (and adjust the rolling sums below accordingly)


// ==== save all data
save temp_all, replace


// =======================
* MWE 1 normal reg 
use temp_all, clear

keep if time_avail_m <= tm(1926m1)
export delimited using "$pathProject/Signals/Human/tf_mwe1.csv", replace


log using "$pathProject/Signals/Human/tf_mwe1.log", text replace
import delimited "$pathProject/Signals/Human/tf_mwe1.csv", clear
regress fret a_*
log close

// =======================
* MWE 2 normal reg 
use temp_all, clear

keep if time_avail_m <= tm(1926m3)
export delimited using "$pathProject/Signals/Human/tf_mwe2.csv", replace


log using "$pathProject/Signals/Human/tf_mwe2.log", text replace
import delimited "$pathProject/Signals/Human/tf_mwe2.csv", clear
regress fret a_*
log close


// =======================
* MWE 3 normal reg 
use temp_all, clear

keep if time_avail_m <= tm(1926m5)
export delimited using "$pathProject/Signals/Human/tf_mwe3.csv", replace


log using "$pathProject/Signals/Human/tf_mwe3.log", text replace
import delimited "$pathProject/Signals/Human/tf_mwe3.csv", clear
regress fret a_*
log close


// =======================
* MWE 4 asreg

use temp_all, clear
keep if time_avail_m <= tm(1926m5)
export delimited using "$pathProject/Signals/Human/tf_mwe4.csv", replace

set linesize 255
log using "$pathProject/Signals/Human/tf_mwe4.log", text replace

* import and make sure dates are the proper type
import delimited "$pathProject/Signals/Human/tf_mwe4.csv", clear
rename time_avail_m datestr
gen time_avail_m = monthly(datestr, "YM")
format time_avail_m %tm

bys time_avail_m: asreg fret a_*

* show just the regression outputs
sort permno time_avail_m
list time_avail_m _* if permno == 10006

log close
set linesize 120


// =======================
* MWE 5 asreg

use temp_all, clear
keep if time_avail_m <= tm(1940m7) // keep all data
export delimited using "$pathProject/Signals/Human/tf_mwe5.csv", replace

set linesize 255
log using "$pathProject/Signals/Human/tf_mwe5.log", text replace

* import and make sure dates are the proper type
import delimited "$pathProject/Signals/Human/tf_mwe5.csv", clear
rename time_avail_m datestr
gen time_avail_m = monthly(datestr, "YM")
format time_avail_m %tm

bys time_avail_m: asreg fret a_*

* show just the regression outputs
sort permno time_avail_m
list time_avail_m _* if permno == 10006 & time_avail_m >= tm(1940m1)

log close
set linesize 120



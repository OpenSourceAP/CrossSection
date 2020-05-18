** Pre-processing IBES EPS data

* EPS file
import delimited "$pathProject/DataRaw/IBES.csv", clear varnames(1)
keep if fpi == 1  // Use fiscal year earnings estimates only
gen time_d = date(statpers,"YMD")
gen time_d_act = date(anndats_act,"YMD")
format time_d* %td
keep if time_d < time_d_act

rename actual EPSactualIBES
drop time_d_act anndats_act measure fpi statpers fpedats
duplicates drop

* Set up in monthly time and fill gaps
gen time_avail_m = mofd(time_d)
format time_avail %tm

egen id = group(ticker)
bys id time_av: keep if _n == 1
xtset id time_av
tsfill  // THIS INTRODUCES SOME STALENESS IF NO ESTIMATES ARE AVAILABLE. IS THIS WHAT WE WANT?
foreach v of varlist ticker numest medest meanest stdev EPSactualIBES {
	replace `v' = `v'[_n-1] if id == id[_n-1] & mi(`v') 
}
drop id time_d 

* Prepare for match with other files
rename ticker tickerIBES
rename stdev stdev_est
compress
save "$pathProject/DataClean/IBES_EPS", replace

*~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
* EPS file (long-run growth)
import delimited "$pathProject/DataRaw/IBES.csv", clear varnames(1)
keep if fpi == 0
gen time_d = date(statpers,"YMD")
format time_d* %td

keep ticker meanest stdev numest time_d
duplicates drop

* Set up in monthly time and fill gaps
gen time_avail_m = mofd(time_d)
format time_avail %tm

egen id = group(ticker)
xtset id time_av
tsfill  // THIS INTRODUCES SOME STALENESS IF NO ESTIMATES ARE AVAILABLE. IS THIS WHAT WE WANT?
foreach v of varlist ticker meanest stdev numest {
	replace `v' = `v'[_n-1] if id == id[_n-1] & mi(`v') 
}
drop id time_d 

* Prepare for match with other files
rename ticker tickerIBES
rename meanest fgr5yr
rename stdev stdev5yr
rename numest numest5yr

compress
save "$pathProject/DataClean/IBES_EPSLongRun", replace


*~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
* Recommendations file
import delimited "$pathProject/DataRaw/IBES_Recommendations.csv", clear varnames(1)

gen time_d = date(anndats, "YMD")
gen time_avail_m = mofd(time_d)
format time_avail %tm

* Prepare Change in Recommendation variable
bys ticker amaskcd (time_d): gen ChangeInRecommendation = 1 if ireccd == 1 & ireccd[_n-1] !=1 
bys ticker amaskcd (time_d): replace ChangeInRecommendation = -1 if ireccd != ireccd[_n-1] & ireccd !=1
replace Change = 0 if mi(Change)

collapse (mean) Change ireccd, by(ticker time_avail_m)

* Prepare for match with other files
rename ticker tickerIBES
rename irec MeanRecomm
compress
save "$pathProject/DataClean/IBES_Recommendations", replace

*~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
* EPS file unadjusted
import delimited "$pathProject/DataRaw/IBESUnadjustedActuals.csv", clear varnames(1)
keep if measure == "EPS"

gen time_d = date(statpers,"YMD")
format time_d* %td

drop statpers measure
duplicates drop

rename shout shoutIBESUnadj

* Set up in monthly time and fill gaps
gen time_avail_m = mofd(time_d)
format time_avail %tm

egen id = group(ticker)
bys id time_av: keep if _n == 1
xtset id time_av
tsfill  // THIS INTRODUCES SOME STALENESS IF NO ESTIMATES ARE AVAILABLE. IS THIS WHAT WE WANT?
foreach v of varlist int0a fy0a shoutIBESUnadj ticker {
	replace `v' = `v'[_n-1] if id == id[_n-1] & mi(`v') 
}
drop id time_d 

* Prepare for match with other files
rename ticker tickerIBES
drop if mi(tickerIBES)
compress
save "$pathProject/DataClean/IBES_UnadjustedActuals", replace


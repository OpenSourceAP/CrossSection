* -------------- 
* RIO * signals
* Needs to be run after IdioRisk, so we run it last.  IdioRisk takes about 20 min

* --------------
* prep: BM

// DATA LOAD
use gvkey permno time_avail_m ceq using "$pathDataIntermediate/m_aCompustat", clear
bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
merge 1:1 permno time_avail_m using "$pathDataIntermediate/SignalMasterTable", keep(using match) nogenerate keepusing(mve_c)

gen BM = log(ceq/mve_c)
save "$pathtemp/tempBM", replace


* --------------
* prep: Disp

// Prep IBES data
use "$pathDataIntermediate/IBES_EPS_Unadj", replace
keep if fpi == "1" 
keep if fpedats != . & fpedats > statpers + 30 
save "$pathtemp/temp", replace

use permno time_avail_m tickerIBES using "$pathDataIntermediate/SignalMasterTable", clear
merge m:1 tickerIBES time_avail_m using "$pathtemp/temp", keep(master match) nogenerate keepusing(stdev meanest)

gen ForecastDispersion = stdev/abs(meanest)

* fill
xtset permno time_avail_m
replace ForecastDispersion = l1.ForecastDispersion if ForecastDispersion == . 
keep permno time_avail_m ForecastDispersion

save "$pathtemp/tempDisp", replace

* --------------
* prep: IdioRisk
* Need to run ZZ2_IdioRisk_IdioVolCAPM.do first!

import delimited "$pathDataPredictors/IdioRisk.csv", clear varnames(1)
tostring yyyymm, replace
gen y = substr(yyyymm, 1,4)
gen m = substr(yyyymm, 5,2)
destring y m, replace
gen time_avail_m = ym(y, m)
format time_avail_m %tm
drop y m yyyymm
rename idiorisk IdioRisk
save "$pathtemp/tempIdioRisk", replace

* --------------
* finally make RIO * signals
// DATA LOAD
use permno time_avail_m exchcd mve_c using "$pathDataIntermediate/SignalMasterTable", clear
merge 1:1 permno time_avail_m using "$pathDataIntermediate/TR_13F", keep(master match) nogenerate keepusing(instown_perc)
merge 1:1 permno time_avail_m using "$pathDataIntermediate/monthlyCRSP", keep(master match) nogenerate keepusing(vol shrout)
merge 1:1 permno time_avail_m using "$pathtemp/tempBM", keep(master match) nogenerate
merge 1:1 permno time_avail_m using "$pathtemp/tempDisp", keep(master match) nogenerate
merge 1:1 permno time_avail_m using "$pathtemp/tempIdioRisk", keep(master match) nogenerate keepusing(IdioRisk)

// SIGNAL CONSTRUCTION
gen temp = instown_perc/100
replace temp = 0 if mi(temp)
replace temp = .9999 if temp > .9999
replace temp = .0001 if temp < .0001
gen RIO = log(temp/(1-temp)) + 23.66 - 2.89*log(mve_c) + .08*(log(mve_c))^2
** Several strategies based on RIO
* these are independent double sorts
egen tempRIO = fastxtile(RIO), n(5) by(time_avail_m)
gen Turnover = vol/shrout

foreach v of varlist BM ForecastDispersion IdioRisk Turnover {
	egen temp`v'  = fastxtile(`v'), n(2) by(time_avail_m)
}

gen RIO_BM = 1 if tempRIO == 5 & tempBM == 1
replace RIO_BM = 0 if tempRIO == 1 & tempBM == 1
gen RIO_Disp = 1 if tempRIO == 5 & tempForecastDispersion == 2
replace RIO_Disp = 0 if tempRIO == 1 & tempForecastDispersion == 2
gen RIO_Turnover = 1 if tempRIO == 5 & tempTurnover == 2
replace RIO_Turnover = 0 if tempRIO == 1 & tempTurnover == 2
* note that idiorisk has a flipped sign
gen RIO_IdioRisk = 1 if tempRIO == 5 & tempIdioRisk == 1
replace RIO_IdioRisk = 0 if tempRIO == 1 & tempIdioRisk == 1
label var RIO_BM "Inst Own and BM"
label var RIO_Disp "Inst Own and Forecast Dispersion"
label var RIO_Turnover "Inst Own and Turnover"
label var RIO_IdioRisk "Inst Own and Idio Vol"

// SAVE 
do "$pathCode/savepredictor" RIO_BM
do "$pathCode/savepredictor" RIO_Disp
do "$pathCode/savepredictor" RIO_Turnover
do "$pathCode/savepredictor" RIO_IdioRisk

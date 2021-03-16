* --------------
// Prep IBES data
use "$pathDataIntermediate/IBES_EPS_Unadj", replace
keep if fpi == "1" & month(statpers) == 3 // OP uses march forecasts
keep if fpedats != . & fpedats > statpers + 90 // keep only forecasts past June

* for merge with dec stock price
gen prc_time = time_avail_m - 3
format prc_time %tm

save "$pathtemp/temp", replace

// Merge with CRSP/Comp
use permno time_avail_m tickerIBES prc mve_c using "$pathDataIntermediate/SignalMasterTable", clear
rename time_avail_m prc_time
merge m:1 tickerIBES prc_time using "$pathtemp/temp", keep(match) nogenerate 
merge 1:1 permno time_avail_m using "$pathDataIntermediate/m_aCompustat", keep(match) nogenerate keepusing(datadate)

* only dec fyr ends
keep if month(datadate) == 12

* lower analyst coverage only
egen tempcoverage = fastxtile(numest), by(time_avail_m) n(2)
keep if tempcoverage == 1


// SIGNAL CONSTRUCTION
gen sfe =  medest/abs(prc)
keep permno time_avail_m sfe

* hold for one year
gen temp = 12
expand temp
drop temp
gen tempTime = time_avail_m
bysort permno tempTime: replace time_avail_m = time_avail_m + _n - 1 
drop tempTime

label var sfe "Earnings Forecast"

// SAVE
do "$pathCode/savepredictor" sfe



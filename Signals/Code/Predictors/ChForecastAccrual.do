* ChForecastAccrual
* --------------

// Prep IBES data
use "$pathDataIntermediate/IBES_EPS_Unadj", replace
keep if fpi == "1" 
save "$pathtemp/temp", replace

// DATA LOAD
use permno time_avail_m act che lct dlc txp at using "$pathDataIntermediate/m_aCompustat", clear
bysort permno time_avail_m: keep if _n == 1  // deletes a few observations

merge 1:1 permno time_avail_m using "$pathDataIntermediate/SignalMasterTable", keep(master match) nogenerate keepusing(tickerIBES)

merge m:1 tickerIBES time_avail_m using "$pathtemp/temp", keep(master match) nogenerate keepusing(meanest)

// SIGNAL CONSTRUCTION
xtset permno time_avail_m

gen tempAccruals = ( (act - l12.act) - (che - l12.che) - ( (lct - l12.lct) - ///
	(dlc - l12.dlc) - (txp - l12.txp) )) / ( (at + l12.at)/2)
egen tempsort = fastxtile(tempAccruals), by(time_avail_m) n(2)

gen ChForecastAccrual = 1 if meanest > l.meanest & !mi(meanest) & !mi(l.meanest)
replace ChForecastAccrual = 0 if meanest < l.meanest & !mi(meanest) & !mi(l.meanest)
replace ChForecastAccrual = . if tempsort == 1

label var ChForecastAccrual "Change in Forecast and Accrual"

// SAVE
do "$pathCode/savepredictor" ChForecastAccrual



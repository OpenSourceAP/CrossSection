// needs to be run after RealizedVol

* --------------
// Clean OptionMetrics data 
use "$pathDataIntermediate/OptionMetricsBH", clear
rename mean_imp_vol impvol
drop mean_day nobs ticker
reshape wide impvol, i(secid time_avail_m) j(cp_flag) string

* implied vol many stage version (this is closest to the text and closest to results)
gen impvol = (impvolC + impvolP)/2
replace impvol = impvolC if impvol == . & impvolC != . 
replace impvol = impvolP if impvol == . & impvolP != . 

keep secid time_avail_m impvol
save "$pathtemp/temp", replace

// Clean Realized vol data
import delimited "$pathDataPredictors/RealizedVol.csv", clear varnames(1)
gen time_avail_m= ym(floor(yyyymm/100), mod(yyyymm, 100))
format time_avail_m %tm
drop yyyymm
replace realizedvol = realizedvol * sqrt(252) // annualize
save "$pathtemp/temp2", replace

// DATA LOAD
use permno time_avail_m secid sicCRSP using "$pathDataIntermediate/SignalMasterTable", clear
* Add secid-based data (many to one match due to permno-secid not being unique in crsp)
drop if mi(secid)
merge m:1 secid time_avail_m using "$pathtemp/temp", keep(master match) nogenerate

* drop closed-end funds (6720 : 6730) and REITs (6798)
keep if (sicCRSP < 6720 | sicCRSP > 6730)
keep if sicCRSP != 6798

drop if mi(secid, impvol)

merge m:1 permno time_avail_m using "$pathtemp/temp2", keep(master match) nogenerate

// SIGNAL CONSTRUCTION

// Realized-Implied vol spread = realized volatility - implied volatility 
gen RIVolSpread = realizedvol - impvol
drop if RIVolSpread == .
label var RIVolSpread "Bali-Hovak (2009) Realized minus Implied Vol"
// SAVE
do "$pathCode/savepredictor" RIVolSpread


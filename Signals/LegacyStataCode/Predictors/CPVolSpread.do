* --------------
// Clean OptionMetrics data 
use "$pathDataIntermediate/OptionMetricsBH", clear
drop if cp_flag == "BOTH" 
keep if mean_day >= 0 // OP doesn't mention this, but seems we may not want stale data

* make wide
drop mean_day nobs ticker
reshape wide mean_imp_vol, i(secid time_avail_m) j(cp_flag) string

* compute vol spread
gen CPVolSpread = mean_imp_volC - mean_imp_volP
save "$pathtemp/temp", replace


// DATA LOAD
use permno time_avail_m secid sicCRSP using "$pathDataIntermediate/SignalMasterTable", clear
* Add secid-based data (many to one match due to permno-secid not being unique in crsp)
drop if mi(secid)
merge m:1 secid time_avail_m using "$pathtemp/temp", keep(master match) nogenerate

* drop closed-end funds (6720 : 6730) and REITs (6798)
keep if (sicCRSP < 6720 | sicCRSP > 6730)
keep if sicCRSP != 6798

* nobs should match closely BH's 197,362
* summarize if year(dofm(time_avail_m)) <= 2004 & year(dofm(time_avail_m)) >= 1996

// SIGNAL CONSTRUCTION
drop if CPVolSpread == .
label var CPVolSpread "Bali-Hovak (2009) panel B Call Put Vol Spread"
// SAVE
do "$pathCode/savepredictor" CPVolSpread

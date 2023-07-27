* --------------
// DATA LOAD
use permno time_avail_m secid sicCRSP using "$pathDataIntermediate/SignalMasterTableOC", clear
* Add secid-based data (many to one match due to permno-secid not being unique in crsp)
preserve

keep if mi(secid)
save "$pathtemp/temp", replace
restore

drop if mi(secid)
merge m:1 secid time_avail_m using "$pathDataIntermediate/BH_cp", keep(master match) nogenerate
append using "$pathtemp/temp"

* drop closed-end funds (6720 : 6730) and REITs (6798)
keep if (sicCRSP < 6720 | sicCRSP > 6730)
keep if sicCRSP != 6798

// SIGNAL CONSTRUCTION
gen CPVolSpread = bh_call - bh_put
drop if CPVolSpread == .
label var CPVolSpread "Bali-Hovak (2009) panel B"
// SAVE
do "$pathCode/savepredictor" CPVolSpread

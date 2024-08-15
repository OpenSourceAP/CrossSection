* --------------
// DATA LOAD
use permno time_avail_m using "$pathDataIntermediate/SignalMasterTable", clear
merge 1:1 permno time_avail_m using "$pathDataIntermediate/monthlyCRSP", keepusing(shrout cfacshr) nogenerate keep(match)

// SIGNAL CONSTRUCTION
gen temp = shrout*cfacshr
gen ShareIss1Y = (l6.temp - l18.temp)/l18.temp
label var ShareIss1Y "Share Issuance (1 year)"

// SAVE
do "$pathCode/savepredictor" ShareIss1Y


/* Note: The implementation below constructs the share adjustment factor from facshr
as described in Pontiff and Woodgate (2008). Results are almost identical and we stick
with the simpler implementation by using cfacshr directly. 
Note that the signal does not suffer from look-ahead bias despite using cfacshr,
see https://github.com/OpenSourceAP/CrossSection/issues/152#issue-2462197349


use permno paydt facshr using "$pathDataIntermediate/CRSPdistributions", clear
gen time_avail_m = mofd(paydt)
format time_avail_m %tm
drop if time_avail_m == . | mi(facshr)

gcollapse (sum) facshr, by(permno time)

sort permno time_avail_m
gen TotalFactor = .
by permno: replace TotalFactor = 1 if _n == 1
by permno: replace TotalFactor = TotalFactor[_n-1]*(1+facshr) if _n>1

* 
save temp, replace



// DATA LOAD
use permno time_avail_m using "$pathDataIntermediate/SignalMasterTable", clear
merge 1:1 permno time_avail_m using "$pathDataIntermediate/monthlyCRSP", keepusing(shrout) nogenerate keep(match)
merge 1:1 permno time_avail_m using temp, keep(master match) nogenerate

// SIGNAL CONSTRUCTION
sort permno time_avail_m
by permno: replace TotalFactor = 1 if _n == 1 & mi(TotalFactor)
by permno: replace TotalFactor = TotalFactor[_n-1] if _n>1 & mi(TotalFactor)

gen temp = shrout/TotalFactor
gen ShareIss1Y = (l6.temp - l18.temp)/l18.temp
label var ShareIss1Y "Share Issuance (1 year)"

// SAVE
do "$pathCode/savepredictor" ShareIss1Y


*/
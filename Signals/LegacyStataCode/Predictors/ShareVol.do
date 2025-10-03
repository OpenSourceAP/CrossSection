* --------------
// DATA LOAD
use permno time_avail_m sicCRSP exchcd using "$pathDataIntermediate/SignalMasterTable", clear
merge 1:1 permno time_avail_m using "$pathDataIntermediate/monthlyCRSP", keepusing(shrout vol) nogenerate keep(match)

// SIGNAL CONSTRUCTION
gen tempShareVol = (vol + l1.vol + l2.vol)/(3*shrout)*100 // vol and shrout are converted to same units in I_CRSPmonthly.do

* drop if shrout changes in last 3 months
gen dshrout = shrout != l1.shrout
bys permno (time_avail_m): replace dshrout = 0 if _n == 1  // Set to no change in first month

gen dropObs = 1 if (dshrout + l1.dshrout + l2.dshrout) > 0
bys permno (time_avail_m): replace dropObs = . if _n == 1 | _n == 2  // Don't drop if first two months
drop if dropObs == 1

gen ShareVol = 0 if tempShareVol < 5 
replace ShareVol = 1 if tempShareVol > 10

// SAVE
label var ShareVol "Share Volume"
do "$pathCode/savepredictor" ShareVol


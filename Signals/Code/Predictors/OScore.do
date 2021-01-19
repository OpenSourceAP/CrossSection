* --------------
// DATA LOAD
use gvkey permno time_avail_m fopt at lt act lct ib oancf sic using "$pathDataIntermediate/m_aCompustat", clear
bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
merge 1:1 permno time_avail_m using "$pathDataIntermediate/SignalMasterTable", keep(match) nogenerate keepusing(prc)
merge m:1 time_avail_m using "$pathDataIntermediate/GNPdefl", keep(match) nogenerate 
// SIGNAL CONSTRUCTION
* price screen seems to help a lot
xtset permno time_avail_m
replace fopt = oancf if fopt == .
gen OScore = -1.32 - .407*log(at/gnpdefl) + 6.03*(lt/at) - 1.43*( (act - lct)/at) + ///
    .076*(lct/act) - 1.72*(lt>at) - 2.37*(ib/at) - 1.83*(fopt/lt) + .285*(ib + l12.ib <0) - ///
    .521*( (ib - l12.ib)/(abs(ib) + abs(l12.ib)) )
    
destring sic, replace
replace OScore = . if (sic > 3999 & sic < 5000) | sic > 5999  | abs(prc) < 5 
* returns on non-monotonic (see Panel A of original), so we want to exclude
* the lowest quintile of OScores
egen tempsort = fastxtile(OScore), by(time_avail_m) n(5)
replace OScore = . if tempsort == 1
label var OScore "O-Score"
// SAVE
do "$pathCode/savepredictor" OScore
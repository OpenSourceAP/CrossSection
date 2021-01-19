* AnalystValue, IntrinsicValue, AOP, PredictedFE
* --------------

// DATA LOAD
use permno tickerIBES time_avail_m prc using "$pathDataIntermediate/SignalMasterTable", clear

merge 1:1 permno time_avail_m using "$pathDataIntermediate/monthlyCRSP", keep(master match) nogenerate keepusing(shrout) 

merge 1:1 permno time_avail_m using "$pathDataIntermediate/m_aCompustat", keep(master match) nogenerate keepusing(ceq ib sale)

// SIGNAL CONSTRUCTION
xtset permno time_avail_m

// 238 Intrinsic value
gen FROE = ib/ceq
replace FROE = . if abs(FROE) > 1  // Frankel and Lee, page 291
 
gen mve_c = (shrout * abs(prc))
gen tempBM = ceq/mve_c
xtset permno time_avail_m 

gen tempBMAve = (tempBM + l12.tempBM)/2
bys permno: replace tempBMAve = tempBM if _n <= 12
 
gen IntrinsicValue = (1 + (FROE - .1)/1.1 + (FROE - .1)/(.1*1.1))*tempBMAve
replace IntrinsicValue = . if ceq < 0 | abs(prc) < 1  // Frankel and Lee, page 291
drop temp* FROE
label var IntrinsicValue "Intrinsic Value"

// SAVE
do "$pathCode/saveplacebo" IntrinsicValue
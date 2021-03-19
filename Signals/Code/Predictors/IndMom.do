* --------------
// DATA LOAD
use permno time_avail_m ret sicCRSP mve_c using "$pathDataIntermediate/SignalMasterTable", clear

// SIGNAL CONSTRUCTION
tostring sicCRSP, replace
gen sic2D = substr(sicCRSP,1,2)
replace ret = 0 if mi(ret)
gen Mom6m = ( (1+l.ret)*(1+l2.ret)*(1+l3.ret)*(1+l4.ret)*(1+l5.ret)) - 1
egen IndMom = wtmean(Mom6m), by(sic2D time_avail_m) weight(mve_c)
label var IndMom "Industry momentum"

// SAVE
do "$pathCode/savepredictor" IndMom

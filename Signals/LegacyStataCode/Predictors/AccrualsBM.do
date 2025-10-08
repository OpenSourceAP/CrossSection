* AccrualsBM
* --------------

// DATA LOAD
use gvkey permno time_avail_m ceq act che lct dlc txp at using "$pathDataIntermediate/m_aCompustat", clear
bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
merge 1:1 permno time_avail_m using "$pathDataIntermediate/SignalMasterTable", keep(using match) nogenerate keepusing(mve_c)

xtset permno time_avail_m

// SIGNAL CONSTRUCTION
gen BM 		=	log(ceq/mve_c)

gen tempacc = ( (act - l12.act) - (che - l12.che) - ( (lct - l12.lct) - ///
	(dlc - l12.dlc) - (txp - l12.txp) )) / ( (at + l12.at)/2)

egen tempqBM = fastxtile(BM), by(time_avail_m) n(5)
egen tempqAcc = fastxtile(tempacc), by(time_avail_m) n(5)

gen AccrualsBM = 1 if tempqBM == 5 & tempqAcc == 1
replace AccrualsBM = 0 if tempqBM == 1 & tempqAcc == 5
replace AccrualsBM = . if ceq <0

drop temp*
label var AccrualsBM "Accruals and BM"


// SAVE
do "$pathCode/savepredictor" AccrualsBM
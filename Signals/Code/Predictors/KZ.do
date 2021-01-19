* --------------
// DATA LOAD
use permno time_avail_m at txdi ib dp ceq dlc dltt dlc che using "$pathDataIntermediate/m_aCompustat", clear
bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
merge 1:1 permno time_avail_m using "$pathDataIntermediate/SignalMasterTable", keep(match) nogenerate keepusing(mve_c) 
merge 1:1 permno time_avail_m using "$pathDataIntermediate/mCRSPdistributions", keep(master match) nogenerate keepusing(divamt) 
// SIGNAL CONSTRUCTION
gen tempTX = txdi
replace tempTX = 0 if mi(tempTX)
gen temp = divamt
replace temp = 0 if divamt ==.
gen KZ = -1.002* (ib + dp)/at + .283*(at + mve_c - ceq - tempTX)/at + 3.319*(dlc + dltt)/(dlc + dltt + ceq) ///
 - 39.368*(temp/at) - 1.315*(che/at)
label var KZ "Kaplan-Zingales index"
// SAVE
do "$pathCode/savepredictor" KZ
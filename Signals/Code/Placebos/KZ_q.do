* --------------
// DATA LOAD
use permno gvkey time_avail_m mve_c using "$pathDataIntermediate/SignalMasterTable", clear
keep if !mi(gvkey)
merge 1:1 gvkey time_avail_m using "$pathDataIntermediate/m_QCompustat", keepusing(txdiq ibq dpq atq ceqq dlcq dlttq cheq) nogenerate keep(match)
merge 1:1 permno time_avail_m using "$pathDataIntermediate/mCRSPdistributions", keep(master match) nogenerate keepusing(divamt) 
// SIGNAL CONSTRUCTION
gen tempTX = txdiq
replace tempTX = 0 if mi(tempTX)
gen temp = divamt
replace temp = 0 if divamt ==.
gen KZ_q = -1.002* (ibq + dpq)/atq + .283*(atq + mve_c - ceqq - tempTX)/atq + 3.319*(dlcq + dlttq)/(dlcq + dlttq + ceqq) ///
 - 39.368*(temp/atq) - 1.315*(cheq/atq)
label var KZ_q "Kaplan-Zingales index (quarterly)"
// SAVE
do "$pathCode/saveplacebo" KZ_q
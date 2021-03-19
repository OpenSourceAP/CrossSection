use "$pathDataIntermediate/m_QCompustat", clear

* --------------
// DATA LOAD
use permno gvkey time_avail_m mve_c using "$pathDataIntermediate/SignalMasterTable", clear
keep if !mi(gvkey)
merge 1:1 gvkey time_avail_m using "$pathDataIntermediate/m_QCompustat", keepusing(txdiq ibq dpq atq ceqq dlcq dlttq cheq dvy) nogenerate keep(match)

// SIGNAL CONSTRUCTION
gen tempTX = txdiq
replace tempTX = 0 if mi(tempTX)

gen KZ_q = -1.002* (ibq + dpq)/atq + .283*(atq + mve_c - ceqq - tempTX)/atq + 3.319*(dlcq + dlttq)/(dlcq + dlttq + ceqq) ///
 - 39.368*(dvy/atq) - 1.315*(cheq/atq)
 
label var KZ_q "Kaplan-Zingales index (quarterly)"
// SAVE
do "$pathCode/saveplacebo" KZ_q

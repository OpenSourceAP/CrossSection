use "$pathDataIntermediate/m_QCompustat", clear

* --------------
// DATA LOAD
use permno gvkey time_avail_m mve_c using "$pathDataIntermediate/SignalMasterTable", clear
keep if !mi(gvkey)
merge 1:1 gvkey time_avail_m using "$pathDataIntermediate/m_QCompustat", keepusing(txdiq ibq dpq atq ceqq dlcq dlttq cheq dvy ppentq) nogenerate keep(match)

// SIGNAL CONSTRUCTION
gen tempTX = txdiq
replace tempTX = 0 if mi(tempTX)

gen KZ_q = -1.002* (ibq + dpq)/ppentq + .283*(atq + mve_c - ceqq - tempTX)/atq + 3.139*(dlcq + dlttq)/(dlcq + dlttq + ceqq) ///
 - 39.368*(dvy/ppentq) - 1.315*(cheq/ppentq)
 
label var KZ_q "Kaplan-Zingales index (quarterly)"
// SAVE
do "$pathCode/saveplacebo" KZ_q

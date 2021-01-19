* --------------
// DATA LOAD
use gvkey permno time_avail_m dltt dlc dc che oibdp ceq using "$pathDataIntermediate/m_aCompustat", clear
merge 1:1 permno time_avail_m using "$pathDataIntermediate/SignalMasterTable", keep(using match) nogenerate keepusing(mve_c)
// SIGNAL CONSTRUCTION
gen EntMult = (mve_c + dltt + dlc + dc - che)/oibdp
replace EntMult = . if ceq < 0 | oibdp < 0  // This screen come from Loughran and Wellman's paper, MP don't mention them.
label var EntMult "Enterprise Multiple"
// SAVE
do "$pathCode/savepredictor" EntMult
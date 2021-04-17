* --------------
// DATA LOAD
use "$pathDataIntermediate/m_aCompustat", clear

bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
merge 1:1 permno time_avail_m using "$pathDataIntermediate/SignalMasterTable", keep(match) nogenerate keepusing(mve_c) 


// SIGNAL CONSTRUCTION
* see OP page 24
* this is useful http://www.crsp.org/products/documentation/annual-data-industrial
gen KZ = -1.002* (ib + dp)/at  ///
	+ .283*(at + mve_c - ceq - txdb)/at ///
	+ 3.319*(dlc + dltt)/(dlc + dltt + seq) ///
   - 39.368*((dvc+dvp)/at) - 1.315*(che/at)
 
label var KZ "Kaplan-Zingales index"
// SAVE
do "$pathCode/saveplacebo" KZ

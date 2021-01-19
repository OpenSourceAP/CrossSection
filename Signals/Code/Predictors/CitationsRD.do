* CitationsRD
* --------------

// DATA LOAD
use permno gvkey time_avail_m mve_c using "$pathDataIntermediate/SignalMasterTable", clear
gen year = yofd(dofm(time_avail_m))

merge 1:1 permno time_avail_m using "$pathDataIntermediate/m_aCompustat", nogenerate keep(master match) keepusing(xrd)

* Add patent data 
preserve
	keep if gvkey == .
	save "$pathtemp/temp", replace  // Temporarily store obs with missing gvkeys in another file
restore
drop if gvkey ==.

// patent citation dataset
merge m:1 gvkey year using "$pathDataIntermediate/PatentDataProcessed", keep(master match) nogenerate

append using "$pathtemp/temp"

// SIGNAL CONSTRUCTION
xtset permno time_avail_m

gen tempXRD = xrd
replace tempXRD = 0 if mi(xrd)

gen tempncit = l12.ncitscale  // account for patent data being end of year
replace tempncit = 0 if tempncit == .
gen CitationsRD  = (tempncit + l12.tempncit + l24.tempncit + l36.tempncit + ///
                  l48.tempncit) / (l36.tempXRD + l48.tempXRD + l60.tempXRD + l72.tempXRD + l84.tempXRD)
replace CitationsRD = . if time_avail_m < ym(1982,1)  // Takes into account that xrd data standardized after 1975

egen tempsizeq = fastxtile(mve_c), by(time_avail_m) n(2) // imitating size adjutment: ideally this uses nyse breakpoints
replace CitationsRD = . if tempsizeq == 2

label var CitationsRD "Citations to RD expenses"

// SAVE
do "$pathCode/savepredictor" CitationsRD
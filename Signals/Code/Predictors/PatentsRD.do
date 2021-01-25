* --------------
* shorter port period helps a lot
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
// OP: efficiency in year t is patents in year t scaled by R&D in t-2 ..
// portfolios are computed from July of year t to ...
xtset permno time_avail_m

gen tempXRD = xrd
replace tempXRD = 0 if mi(xrd)
gen tempnpat = l6.npat // year t is matched with July t+1
replace tempnpat = 0 if mi(tempnpat)

gen tempPatentsRD = tempnpat/(l24.tempXRD + .8*l36.tempXRD + .6*l48.tempXRD + .4*l60.tempXRD + .2*l72.tempXRD)
gen PatentsRD = tempPatentsRD  
replace PatentsRD = . if mi(l24.xrd) | time_avail_m < ym(1982,1)  // Takes into account that xrd data standardized after 1975

egen tempsizeq = fastxtile(mve_c), by(time_avail_m) n(2) // imitating size adjutment: ideally this uses nyse breakpoints
replace PatentsRD = . if tempsizeq == 2

// SAVE
label var PatentsRD "Patents to RD capital"
do "$pathCode/savepredictor" PatentsRD


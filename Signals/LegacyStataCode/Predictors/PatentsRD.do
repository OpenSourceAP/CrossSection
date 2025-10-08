* --------------
* shorter port period helps a lot
// DATA LOAD
use permno gvkey time_avail_m mve_c sicCRSP exchcd using "$pathDataIntermediate/SignalMasterTable", clear
gen year = yofd(dofm(time_avail_m))
merge 1:1 permno time_avail_m using "$pathDataIntermediate/m_aCompustat", nogenerate keep(master match) keepusing(xrd sich datadate ceq)
drop if gvkey == .

// patent citation dataset
* compustat is already lagged (time_avail_m = June uses at from Dec)
* so we need to lag patent data to match 
merge m:1 gvkey year using "$pathDataIntermediate/PatentDataProcessed", keep(master match) nogenerate keepusing(npat)

xtset permno time_avail_m
gen temp = l6.npat // year t is matched with July t+1
replace temp = 0 if mi(temp)
replace npat = temp
drop temp

// SIGNAL CONSTRUCTION
* form portfolios only in june
keep if month(dofm(time_avail_m)) == 6
drop if time_avail_m < ym(1975,1)  // Takes into account that xrd data standardized after 1975

// OP: efficiency in year t is patents in year t scaled by R&D in t-2 ..
// portfolios are computed from July of year t to ...
replace xrd = 0 if mi(xrd)

* components of RDcap
gen comp1 = 0
gen comp2 = 0
gen comp3 = 0
gen comp4 = 0
gen comp5 = 0

order permno time_avail_m npat xrd comp*
replace comp1 = l24.xrd if l24.xrd != .
replace comp2 = 0.8*l36.xrd if l36.xrd != .
replace comp3 = 0.6*l48.xrd if l48.xrd != .
replace comp4 = 0.4*l60.xrd if l60.xrd != .
replace comp5 = 0.2*l72.xrd if l72.xrd != .

gen RDcap = comp1 + comp2  + comp3 + comp4 + comp5
gen tempPatentsRD = npat/RDcap if RDcap > 0

// * my tempPatentsRD is lower than OP, by factor of 2
// 	keep if year(dofm(time_avail_m)) <= 2007
// 	tabstat tempPatentsRD, by(maincat) stat(mean median min max n)
// 	tabstat mve_c, by(maincat) stat(mean median min max n)

// Filter
bysort gvkey (time_avail_m): drop if _n <= 2
drop if sicCRSP >= 6000 & sicCRSP <= 6999
drop if ceq < 0


// double indep sort (can't just drop high mve_c, need indep)
bys time_avail_m: astile sizecat = mve_c, qc(exchcd == 1) nq(2)
egen maincat = fastxtile(tempPatentsRD), by(time_avail_m) n(3)

// * following FF1993, others, first digit is S or B, second digit is L,M,or H
// * i.e. 13 = S/H, then VW before compbining
// * too difficult to implement in spreadsheet
// * just do simple binary VW for ease

gen PatentsRD = 1 if sizecat == 1 & maincat == 3
replace PatentsRD = 0 if sizecat == 1 & maincat == 1
// order PatentsRD maincat sizecat permno time_avail_m
	
// expand back to monthly
gen temp = 12
expand temp
drop temp

gen tempTime = time_avail_m
bysort gvkey tempTime: replace time_avail_m = time_avail_m + _n - 1 
drop tempTime

// SAVE
order PatentsRD
label var PatentsRD "Patents to RD capital"
do "$pathCode/savepredictor" PatentsRD


* BookLeverageQuarterly
* --------------

// DATA LOAD
use permno gvkey time_avail_m mve_c using "$pathDataIntermediate/SignalMasterTable", clear
keep if !mi(gvkey)

merge 1:1 gvkey time_avail_m using "$pathDataIntermediate/m_QCompustat", keepusing(txditcq seqq ceqq pstkq atq ltq) nogenerate keep(match)

// SIGNAL CONSTRUCTION
replace txditcq = 0 if mi(txditcq)
gen tempSE = seqq
replace tempSE = ceqq + pstkq if mi(tempSE)
replace tempSE = atq - ltq if mi(tempSE)

gen BookLeverageQuarterly = atq/(tempSE + txditcq - pstkq)

label var BookLeverageQuarterly "Book leverage (quarterly)"

// SAVE
do "$pathCode/saveplacebo" BookLeverageQuarterly
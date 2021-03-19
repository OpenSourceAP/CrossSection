* AssetGrowth_q
* --------------

// DATA LOAD
use permno gvkey time_avail_m using "$pathDataIntermediate/SignalMasterTable", clear
keep if !mi(gvkey)

merge 1:1 gvkey time_avail_m using "$pathDataIntermediate/m_QCompustat", keepusing(atq) nogenerate keep(match)

// SIGNAL CONSTRUCTION
xtset permno time_avail_m
gen AssetGrowth_q = (atq - l12.atq)/l12.atq 

label var AssetGrowth_q "Asset Growth (quarterly)"

// SAVE
do "$pathCode/saveplacebo" AssetGrowth_q
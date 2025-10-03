* AssetLiquidityBookQuart
* --------------

// DATA LOAD
use permno gvkey time_avail_m using "$pathDataIntermediate/SignalMasterTable", clear
keep if !mi(gvkey)

merge 1:1 gvkey time_avail_m using "$pathDataIntermediate/m_QCompustat", keepusing(gdwlq intanq cheq actq atq) nogenerate keep(match)

// SIGNAL CONSTRUCTION
xtset permno time_avail_m
replace gdwlq = 0 if mi(gdwlq)
replace intanq = 0 if mi(intanq)
gen AssetLiquidityBookQuart = (cheq + .75*(actq - cheq) + .5*(atq - actq - gdwlq - intanq))/l.atq

label var AssetLiquidityBookQuart "Quarterly Asset liquidity (scaled by book value of assets)"

// SAVE
do "$pathCode/saveplacebo" AssetLiquidityBookQuart
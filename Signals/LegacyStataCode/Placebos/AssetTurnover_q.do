* AssetTurnover_q
* --------------

// DATA LOAD
use permno gvkey time_avail_m mve_c using "$pathDataIntermediate/SignalMasterTable", clear
keep if !mi(gvkey)

merge 1:1 gvkey time_avail_m using "$pathDataIntermediate/m_QCompustat", keepusing(rectq invtq acoq ppentq intanq apq lcoq loq saleq) nogenerate keep(match)

// SIGNAL CONSTRUCTION
xtset permno time_avail_m
gen temp = (rectq + invtq + acoq + ppentq + intanq - apq - lcoq - loq) 

gen AssetTurnover_q = saleq/((temp + l12.temp)/2)
replace AssetTurnover_q = . if AssetTurnover_q < 0

label var AssetTurnover_q "Asset Turnover (quarterly)"

// SAVE
do "$pathCode/saveplacebo" AssetTurnover_q
* ChAssetTurnover
* AssetTurnover was not shown to predict in OP
* -------------------------------

// DATA LOAD
use gvkey permno time_avail_m rect invt aco ppent intan ap lco lo sale using "$pathDataIntermediate/m_aCompustat", clear

// SIGNAL CONSTRUCTION
bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
xtset permno time_avail_m

gen temp = (rect + invt + aco + ppent + intan - ap - lco - lo) 
gen AssetTurnover = sale/((temp + l12.temp)/2)
drop temp
replace AssetTurnover = . if AssetTurnover < 0

gen ChAssetTurnover = AssetTurnover - l12.AssetTurnover

label var AssetTurnover "Asset Turnover"
label var ChAssetTurnover "Change in Asset Turnover"

// SAVE
do "$pathCode/savepredictor" ChAssetTurnover
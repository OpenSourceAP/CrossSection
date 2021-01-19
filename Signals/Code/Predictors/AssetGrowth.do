* AssetGrowth
* --------------

// DATA LOAD
use gvkey permno time_avail_m at using "$pathDataIntermediate/m_aCompustat", clear

// SIGNAL CONSTRUCTION
xtset permno time_avail_m

gen AssetGrowth = (at - l12.at)/l12.at 

label var AssetGrowth "Asset Growth"

// SAVE
do "$pathCode/savepredictor" AssetGrowth
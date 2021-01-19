* AssetLiquidityBook
* --------------

// DATA LOAD
use gvkey permno time_avail_m che act at gdwl intan at using "$pathDataIntermediate/m_aCompustat", clear

// SIGNAL CONSTRUCTION
xtset permno time_avail_m

gen AssetLiquidityBook = (che + .75*(act - che) + .5*(at - act - gdwl - intan))/l.at

label var AssetLiquidityBook "Asset liquidity (scaled by book value of assets)"

// SAVE
do "$pathCode/saveplacebo" AssetLiquidityBook
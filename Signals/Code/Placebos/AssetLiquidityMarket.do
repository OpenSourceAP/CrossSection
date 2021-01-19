* AssetLiquidityMarket
* --------------

// DATA LOAD
use gvkey permno time_avail_m che act at gdwl intan prcc_f csho ceq using "$pathDataIntermediate/m_aCompustat", clear

// SIGNAL CONSTRUCTION
bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
xtset permno time_avail_m

gen AssetLiquidityMarket = (che + .75*(act - che) + .5*(at - act - gdwl - intan))/(l.at + l.prcc_f*l.csho - l.ceq)

label var AssetLiquidityMarket "Asset liquidity (scaled by market value of assets)"

// SAVE
do "$pathCode/saveplacebo" AssetLiquidityMarket
* AssetLiquidityMarketQuart
* --------------

// DATA LOAD
use permno gvkey time_avail_m mve_c using "$pathDataIntermediate/SignalMasterTable", clear
keep if !mi(gvkey)

merge 1:1 gvkey time_avail_m using "$pathDataIntermediate/m_QCompustat", keepusing(gdwlq intanq cheq actq prccq cshoq atq ceqq) nogenerate keep(match)

// SIGNAL CONSTRUCTION
xtset permno time_avail_m

replace gdwlq = 0 if mi(gdwlq)
replace intanq = 0 if mi(intanq)

gen AssetLiquidityMarketQuart = (cheq + .75*(actq - cheq) + .5*(atq - actq - gdwlq - intanq))/(l.atq + l.prccq*l.cshoq - l.ceqq)

label var AssetLiquidityMarketQuart "Quarterly asset liquidity (scaled by market value of assets)"

// SAVE
do "$pathCode/saveplacebo" AssetLiquidityMarketQuart
// 2021 AC
// OP actually is value weighted, we previously had EW
// also updated: dec and sic restriction, missing xsga => 0,  drop OrgCap == 0
// also updated: price index deflation (using GNP defl), this helps too
// Keeping only december fyr ends is absolutely critical for some reason
// Is the unadjusted version even predictive? 
//	I don't see it in OP.  Page 18 top discusses the industry adjustment
// 	HXZ find that it is in the full sample, with deciles
//	it seems that in our data, deciles is required to make this predictive, 
//	and it works a lot better in the full sample (post 2008)
// OP gets tstat of 2.85 for OrgCapAdj, we get 2.3 ish, 
// 	perhaps because we skip the cpi
// OrgCap is not predictive for us, t-stat = 1.20 insamp, but works better postpub
//	and also in deciles


* --------------
// DATA LOAD
use permno time_avail_m sicCRSP shrcd exchcd using "$pathDataIntermediate/SignalMasterTable", clear
merge 1:1 permno time_avail_m using "$pathDataIntermediate/m_aCompustat", nogenerate keepusing(xsga at datadate sic) keep(master match)
merge m:1 time_avail_m using "$pathDataIntermediate/GNPdefl", keep(match) nogenerate
destring sic, replace
keep if month(datadate) == 12 & (sic < 6000 | sic >= 7000) ///
	& sic != . //OP p 18, the dec fyr end is critical for some reason

	
// SIGNAL CONSTRUCTION
xtset permno time_avail_m
bys permno (time_avail_m): gen tempAge = _n 
replace xsga = 0 if xsga == . // OP (p 17) 
replace xsga = xsga/gnpdefl // supposed to use cpi, but gnpdefl is used in Oscore
gen OrgCap     = 4*xsga if tempAge <= 12 
replace OrgCap = .85*l12.OrgCap + xsga if tempAge > 12
replace OrgCap = OrgCap/at
replace OrgCap = . if OrgCap == 0 // OP p 18: works better without this
label var OrgCap "Organizational capital"

*Adjusted version
winsor2 OrgCap, suffix("temp") cuts(1 99) by(time_avail_m)
ffind sicCRSP, newvar(tempFF17) type(17)
egen tempMean = mean(OrgCaptemp), by(tempFF17 time_avail_m)
egen tempSD   = sd(OrgCaptemp), by(tempFF17 time_avail_m)
gen OrgCapAdj = (OrgCaptemp - tempMean)/tempSD
label var OrgCapAdj "Industry-adjusted organizational capital"

// SAVE
do "$pathCode/saveplacebo" OrgCap
do "$pathCode/savepredictor" OrgCapAdj

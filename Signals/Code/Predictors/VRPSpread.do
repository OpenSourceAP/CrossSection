* --------------
// BH DATA LOAD
use permno time_avail_m secid sicCRSP using "$pathDataIntermediate/SignalMasterTableOC", clear
* Add secid-based data (many to one match due to permno-secid not being unique in crsp)
preserve

keep if mi(secid)
save "$pathtemp/temp", replace
restore

drop if mi(secid)
merge m:1 secid time_avail_m using "$pathDataIntermediate/BH_ri", keep(master match) nogenerate
append using "$pathtemp/temp"

* drop closed-end funds (6720 : 6730) and REITs (6798)
keep if (sicCRSP < 6720 | sicCRSP > 6730)
keep if sicCRSP != 6798

// Realized Volatility DATA MERGE (from ZZ2_IdioRisk_IdioVolCAMP.do, Ang et al (2006))
merge 1:1 permno time_avail_m using "$pathDataPredictors/RealizedVol", nogen
drop if mi(secid, mean_imp_vol)

* convert RealizedVol to monthly
replace RealizedVol = RealizedVol * sqrt(252)

// SIGNAL CONSTRUCTION

// Realized-Implied vol spread = realized volatility - implied volatility (average of monthly call and put implied volatility)
rename mean_imp_vol ivol
gen VRPSpread = RealizedVol - ivol
drop if VRPSpread == .
label var VRPSpread "Bali-Hovak (2009) panel A"
// SAVE
do "$pathCode/savepredictor" VRPSpread


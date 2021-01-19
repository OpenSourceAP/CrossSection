* -------------------------
// DATA LOAD
use permno time_d ret using "$pathDataIntermediate/dailyCRSP.dta", clear
merge m:1 time_d using "$pathDataIntermediate/dailyFF", nogenerate keep(match) keepusing(rf mktrf smb hml)
replace ret = ret - rf
drop rf 
// SIGNAL CONSTRUCTION
bys permno (time_d): gen time_temp = _n
xtset permno time_temp
* 3F model 
asreg ret mktrf smb hml, window(time_temp 20) min(15) by(permno)
gen epsReturn3F = ret - _b_cons - _b_mktrf*mktrf - _b_smb*smb - _b_hml*hml 
gen time_avail_m = mofd(time_d)
format time_avail_m %tm
sort permno time_avail_m time_d
gcollapse (sd) IdioVol3F = epsReturn3F (skewness) ReturnSkew3F = epsReturn3F, by(permno time_avail_m)
label var IdioVol3F "Idiosyncratic Risk (3 factor)"
label var ReturnSkew3F "Skewness of daily idiosyncratic returns (3F model)"

// SAVE 
do "$pathCode/savepredictor" IdioVol3F
do "$pathCode/savepredictor" ReturnSkew3F
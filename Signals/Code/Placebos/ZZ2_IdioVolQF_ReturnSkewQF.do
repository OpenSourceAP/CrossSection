* -------------------------
// DATA LOAD
use permno time_d ret using "$pathDataIntermediate/dailyCRSP.dta", clear
merge m:1 time_d using "$pathDataIntermediate/d_qfactor", nogenerate keep(master match)
replace ret = ret - r_f_qfac
drop r_f_qfac

// SIGNAL CONSTRUCTION
bys permno (time_d): gen time_temp = _n
xtset permno time_temp
* QF model 
xtset permno time_temp
asreg ret r_mkt_qfac r_me_qfac r_ia_qfac r_roe_qfac, window(time_temp 20) min(15) by(permno)
gen epsReturnQF = ret - _b_cons - _b_r_mkt_qfac*r_mkt_qfac - _b_r_me_qfac*r_me_qfac ///
    - _b_r_ia_qfac*r_ia_qfac - _b_r_roe_qfac*r_roe_qfac 
    
gen time_avail_m = mofd(time_d)
format time_avail_m %tm
sort permno time_avail_m time_d
gcollapse (sd) IdioVolQF = epsReturnQF (skewness) ReturnSkewQF = epsReturnQF, by(permno time_avail_m)
label var IdioVolQF "Idiosyncratic Risk (Q factor)"
label var ReturnSkewQF "Skewness of daily idiosyncratic returns (QF model)"

// SAVE
do "$pathCode/saveplacebo" IdioVolQF
do "$pathCode/saveplacebo" ReturnSkewQF
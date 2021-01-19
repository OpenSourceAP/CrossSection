* --------------
// DATA LOAD
use gvkey permno time_avail_m rect invt ppent aco intan ao ap lco lo at dp using "$pathDataIntermediate/m_aCompustat", clear
// SIGNAL CONSTRUCTION
bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
xtset permno time_avail_m
gen GrLTNOA = (rect + invt + ppent + aco + intan + ao - ap - lco - lo)/at - (l12.rect + l12.invt + ///
    l12.ppent + l12.aco + l12.intan + l12.ao - l12.ap - l12.lco - l12.lo)/l12.at ///
    - ( rect - l12.rect + invt - l12.invt + aco - l12.aco - (ap - l12.ap + lco - l12.lco) - dp )/((at + l12.at)/2)

label var GrLTNOA "Growth in long term net operating assets"
// SAVE
do "$pathCode/savepredictor" GrLTNOA
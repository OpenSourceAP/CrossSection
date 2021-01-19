// // # 2021 01 ac: new portfolio code had a problem with conversion of monthly data 
// to annual rebalancing.  Looking closer at OP: OP actually used quarterly data with 
// a 3-month lag, then selected only close-to-december fiscal years, then 
// converted to annual.  This is more aggressive than our annual data with a 6 month lag
// , so to try to get close I added an annual smoothing / conversion at the end of 
// the MS computation.

* --------------
// DATA LOAD
use permno time_avail_m datadate at ceq ni oancf ib dp xrd capx xad revt using "$pathDataIntermediate/m_aCompustat", clear
bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
merge 1:1 permno time_avail_m using "$pathDataIntermediate/SignalMasterTable", keep(match) nogenerate keepusing(mve_c sicCRSP) 

// SIGNAL CONSTRUCTION
* Limit sample to firms in the lowest BM quintile
gen BM = log(ceq/mve_c)
egen temp = fastxtile(BM), by(time_avail_m) n(5) 
keep if temp == 1

xtset permno time_avail_m
replace xad = 0 if mi(xad) 
gen roa = ni/((at+l12.at)/2)
gen cfroa = oancf/((at+l12.at)/2)
replace cfroa = (ib+dp)/((at+l12.at)/2) if oancf ==.
gen xrdint = xrd/((at+l12.at)/2)
gen capxint = capx/((at+l12.at)/2)
gen xadint = xad/((at+l12.at)/2)
tostring sicCRSP, replace
gen sic2D = substr(sicCRSP,1,2)

foreach v of varlist roa cfroa xrdint capxint xadint {
	egen md_`v' = median(`v'), by(sic2D time_avail_m)
}

gen m1 = 0
replace m1 = 1 if roa > md_roa
gen m2 = 0
replace m2 = 1 if cfroa > md_cfroa
gen m3 = 0 
replace m3 = 1 if oancf > ni
gen m4 = 0
replace m4 = 1 if xrdint > md_xrdint
gen m5 = 0
replace m5 = 1 if capxint > md_capxint
gen m6 = 0
replace m6 = 1 if xadint > md_xadint
bys permno: asrol ni, gen(niVol) stat(sd) window(time_avail_m 36) min(24)
bys permno: asrol revt, gen(revVol) stat(sd) window(time_avail_m 36) min(24)

foreach v of varlist niVol revVol {
	egen md_`v' = median(`v'), by(sic2D time_avail_m)
}

gen m7 = 0
replace m7 = 1 if niVol < md_niVol
gen m8 = 0
replace m8 = 1 if revVol < md_revVol
gen tempMS = m1 + m2 + m3 + m4 + m5 + m6 + m7 + m8


* fix tempMS at most recent data release for entire yer
foreach v of varlist tempMS {
	replace `v' = . if month(dofm(time_avail_m)) != mod(month(datadate)+6,12)
	bysort permno: replace `v'= `v'[_n-1] if missing(`v') & _n > 1
}

gen MS = 1 if tempMS >= 6 & tempMS <= 8
replace MS =  0 if tempMS <= 1
label var MS "Mohanram G-score"

// SAVE
do "$pathCode/savepredictor" MS


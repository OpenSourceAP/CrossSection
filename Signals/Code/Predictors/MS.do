* --------------
// DATA LOAD
use permno gvkey time_avail_m datadate at ceq ni oancf fopt wcapch ib dp xrd capx xad revt using "$pathDataIntermediate/m_aCompustat", clear
bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
merge 1:1 permno gvkey time_avail_m using "$pathDataIntermediate/SignalMasterTable", keep(match) nogenerate keepusing(mve_c sicCRSP) 
merge 1:1 gvkey time_avail_m using "$pathDataIntermediate/m_QCompustat", keep(master match) nogenerate keepusing(niq atq saleq oancfy capxy xrdq fyearq fqtr datafqtr datadateq) 

// SAMPLE SELECTION
* Limit sample to firms in the lowest BM quintile (see p 8 OP)
* (has to be done first!, see also MP)
gen BM = log(ceq/mve_c)
egen temp = fastxtile(BM), by(time_avail_m) n(5) 
keep if temp == 1 & ceq > 0
drop temp

* keep if at least 3 firms in sic2D (p 8)
tostring sicCRSP, replace
gen sic2D = substr(sicCRSP,1,2)
egen tempN = count(at), by(sic2D time_avail_m)
keep if tempN >= 3
drop tempN

// prep variables
xtset permno time_avail_m
replace xad = 0 if mi(xad) 
replace xrdq = 0 if mi(xrdq)
gen capxq = capxy if fqtr == 1 // see "locating oancfq" on wrds
replace capxq = capxy - l3.capxy if fqtr > 1 & fqtr < .
gen oancfq = oancfy if fqtr == 1 // see "locating oancfq" on wrds
replace oancfq = oancfy - l3.oancfy if fqtr > 1 & fqtr < .

* aggregate quarterly
bys permno: asrol niq, gen(niqsum) stat(mean) window(time_avail_m 12) min(12)
bys permno: asrol xrdq, gen(xrdqsum) stat(mean) window(time_avail_m 12) min(12)
bys permno: asrol oancfq, gen(oancfqsum) stat(mean) window(time_avail_m 12) min(12)
bys permno: asrol capxq, gen(capxqsum) stat(mean) window(time_avail_m 12) min(12)

replace niqsum = niqsum*4
replace xrdqsum = xrdqsum*4
replace capxqsum = capxqsum*4
replace oancfqsum = oancfqsum*4
replace oancfqsum = fopt - wcapch if year(datadate) <= 1988 // endnote 3


* op is unclear about annual data when needed, but this makes our results
* very far from op
// replace niqsum = ni if niqsum == .
// replace xrdqsum = xrd if xrdqsum == .
// replace capxqsum = capx if capxqsum == .
// replace oancfqsum = oancf if oancfqsum == .

// SIGNAL CONSTRUCTION

* profitability and cash flow signals 
* OP uses annualized financials, but shouldn't much difference...
gen atdenom = (atq+l3.atq)/2 // OP p 6, needs to be done later?

gen roa = niqsum/atdenom
gen cfroa = oancfqsum/atdenom
foreach v of varlist roa cfroa {
	egen md_`v' = median(`v'), by(sic2D time_avail_m)
}
gen m1 = 0
replace m1 = 1 if roa > md_roa
gen m2 = 0
replace m2 = 1 if cfroa > md_cfroa
gen m3 = 0 
replace m3 = 1 if oancfqsum > niqsum

* "naive extrapolation" according to OP
* quarterly is used here
gen roaq = niq/atq
gen sg = saleq / l3.saleq
bys permno: asrol roaq, gen(niVol) stat(sd) window(time_avail_m 48) min(18)
bys permno: asrol sg, gen(revVol) stat(sd) window(time_avail_m 48) min(18)

foreach v of varlist niVol revVol {
	egen md_`v' = median(`v'), by(sic2D time_avail_m)
}
gen m4 = 0
replace m4 = 1 if niVol < md_niVol
gen m5 = 0
replace m5 = 1 if revVol < md_revVol

* "Conservatism" according to OP
* OP also uses annualized financials here
gen atdenom2 = l3.atq  // (OP p5)
gen xrdint = xrdqsum/atdenom2
gen capxint = capxqsum/atdenom2
gen xadint = xad/atdenom2 // I can't find xadq or xady
foreach v of varlist xrdint capxint xadint {
	egen md_`v' = median(`v'), by(sic2D time_avail_m)
}
gen m6 = 0
replace m6 = 1 if xrdint > md_xrdint
gen m7 = 0
replace m7 = 1 if capxint > md_capxint
gen m8 = 0
replace m8 = 1 if xadint > md_xadint

gen tempMS = m1 + m2 + m3 + m4 + m5 + m6 + m7 + m8

* fix tempMS at most recent data release for entire yer
* timing is confusing compared to OP because of the mix of annual and quarterly
* data with different lags.  This approach gets t-stats closest to op
foreach v of varlist tempMS {
	replace `v' = . if month(dofm(time_avail_m)) != mod(month(datadate)+6,12)	
	bysort permno: replace `v'= `v'[_n-1] if missing(`v') & _n > 1
}

gen MS = tempMS
replace MS = 6 if tempMS >= 6 & tempMS <= 8
replace MS = 1 if tempMS <= 1


label var MS "Mohanram G-score"

// SAVE
do "$pathCode/savepredictor" MS

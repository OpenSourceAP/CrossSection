* --------------
// DATA LOAD
use permno time_avail_m txditc pstk pstkrv pstkl seq ceq at lt using "$pathDataIntermediate/m_aCompustat", clear
bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
merge 1:1 permno time_avail_m using "$pathDataIntermediate/SignalMasterTable", keep(match) nogenerate keepusing(sicCRSP shrcd) 
// SIGNAL CONSTRUCTION
tostring sicCRSP, gen(tempSIC)
gen sic3D = substr(tempSIC,1, 4) // for some reason sic3 isn't working anymore, but sic4 works
* Compute book equity
replace txditc = 0 if mi(txditc)
gen tempPS = pstk
replace tempPS = pstkrv if mi(tempPS)
replace tempPS = pstkl if mi(tempPS)
gen tempSE = seq
replace tempSE = ceq + tempPS if mi(tempSE)
replace tempSE = at - lt if mi(tempSE)
gen tempBE = tempSE + txditc - tempPS
egen indequity    = total(tempBE), by(sic3D time_avail_m)
gen temp  = (tempBE/indequity)^2
egen tempHerf = total(temp), by(sic3D time_avail_m)
bys permno: asrol tempHerf, gen(HerfBE) stat(mean) window(time_avail_m 36) min(12)  // Take 3 year moving average
replace HerfBE = . if shrcd > 11
* Missing if regulated industry (Barclay and Smith 1995 definition)
gen year = yofd(dofm(time_avail_m))
replace HerfBE = . if (tempSIC == "4011" | tempSIC == "4210" | tempSIC == "4213" ) &  year <=1980 
replace HerfBE = . if tempSIC == "4512" & year <=1978 
replace HerfBE = . if (tempSIC == "4812" | tempSIC == " 4813") &  year <= 1982
replace HerfBE = . if substr(tempSIC, 1,2) == "49"
label var HerfBE "Industry concentration (book equity based)"
// SAVE
do "$pathCode/savepredictor" HerfBE
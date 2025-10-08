* BMdec
* --------------

// DATA LOAD
use permno time_avail_m txditc seq ceq at lt pstk pstkrv pstkl using "$pathDataIntermediate/m_aCompustat", clear
bysort permno time_avail_m: keep if _n == 1  // deletes a few observations

merge 1:1 permno time_avail_m using "$pathDataIntermediate/monthlyCRSP", nogenerate keep(match) keepusing(prc shrout)


// SIGNAL CONSTRUCTION
xtset permno time_avail_m

gen tempME = abs(prc)*shrout if month(dofm(time_avail_m)) == 12
gen tempYear = yofd(dofm(time_avail_m))

egen tempDecME = min(tempME), by(permno tempYear)

* Compute book equity
replace txditc = 0 if mi(txditc)
gen tempPS = pstk
replace tempPS = pstkrv if mi(tempPS)
replace tempPS = pstkl if mi(tempPS)

gen tempSE = seq
replace tempSE = ceq + tempPS if mi(tempSE)
replace tempSE = at - lt if mi(tempSE)

gen tempBE = tempSE + txditc - tempPS

gen BMdec = tempBE/l12.tempDecME if month(dofm(time_avail_m)) > = 6
replace BMdec = tempBE/l17.tempDecME if month(dofm(time_avail_m)) < 6

label var BMdec "Book-to-market (December market equity)"
drop temp*


// SAVE
do "$pathCode/savepredictor" BMdec
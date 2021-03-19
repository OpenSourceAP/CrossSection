* --------------
// DATA LOAD
use permno time_avail_m ivao ivst dltt dlc pstk sstk prstkc dv  act che lct at lt ni oancf ivncf fincf sstk prstkc dv using "$pathDataIntermediate/m_aCompustat", clear
bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
// SIGNAL CONSTRUCTION
xtset permno time_avail_m
foreach v of varlist ivao ivst dltt dlc pstk sstk prstkc dv {

gen temp`v' = `v'

replace temp`v' = 0 if mi(temp`v')
}
gen tempWc = (act - che) - (lct - tempdlc)
gen tempNc = (at - act - tempivao) - (lt - tempdlc - tempdltt)
gen tempFi = (tempivst + tempivao) - (tempdltt + tempdlc + temppstk)
gen year = yofd(dofm(time_avail_m))
gen TotalAccruals = (tempWc - l12.tempWc) + (tempNc - l12.tempNc) + (tempFi - l12.tempFi) if year <= 1989  // HXZ use 1988 here but that leads to break in data availability (perhaps because of lagged availability?)
replace TotalAccruals = ni - (oancf + ivncf + fincf) + (sstk - prstkc - dv) if year >1989
replace TotalAccruals = TotalAccruals/l12.at
label var TotalAccruals "Total Accruals"
// SAVE
do "$pathCode/savepredictor" TotalAccruals
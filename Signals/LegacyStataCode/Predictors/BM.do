* BM based on the original, Dennis Stattman (1980)
* see https://github.com/OpenSourceAP/CrossSection/issues/126
* --------------

// DATA LOAD
use permno time_avail_m datadate ceqt using "$pathDataIntermediate/m_aCompustat", clear
merge 1:1 permno time_avail_m using "$pathDataIntermediate/SignalMasterTable", keep(using match) nogenerate keepusing(mve_c)


* find the market equity that matches datadate (based on 6 month lag)
* (see "Company Data" section)
xtset permno time_avail_m
gen me_datadate = l6.mve_c 
replace me_datadate = . if l6.time_avail_m != mofd(datadate)
bys permno (time_avail_m): replace me_datadate = me_datadate[_n-1] if me_datadate == .

// SIGNAL CONSTRUCTION
* Stattman 1980 does not actually take logs but does everything nonparametrically anyway
* but he does drop negative ceqt, which logs takes care of
gen BM = log(ceqt/me_datadate)

label var BM "Book-to-market, Original, Stattman (1980)"

// SAVE
do "$pathCode/savepredictor" BM

* This is redundand and not thoroughly investigated since sinAlgo works 
* --------------
// DATA LOAD
use permno gvkey time_avail_m sicCRSP shrcd using "$pathDataIntermediate/SignalMasterTable", clear
merge m:1 permno using "$pathDataIntermediate/SinStocksHong", keep(master match) nogenerate
// SIGNAL CONSTRUCTION
gen year = year(dofm(time_avail_m))
* Sin Stock classification from original paper
gen sinOrig = year >= begy & year <= endy & !mi(begy) & !mi(endy)
drop begy endy
replace sinOrig = . if sinOrig == 0
replace sinOrig = 0 if ///
	(sicCRSP >= 2000 & sicCRSP <= 2046) | (sicCRSP >= 2050 & sicCRSP <= 2063) | ///
	(sicCRSP >= 2070 & sicCRSP <= 2079) | (sicCRSP >= 2090 & sicCRSP <= 2092) | ///
	(sicCRSP >= 2095 & sicCRSP <= 2099) | (sicCRSP >= 2064 & sicCRSP <= 2068) | ///
	(sicCRSP >= 2086 & sicCRSP <= 2087) | (sicCRSP >=  920 & sicCRSP <=  999) | ///
	(sicCRSP >= 3650 & sicCRSP <= 3652) | sicCRSP == 3732 | ///
	(sicCRSP >= 3931 & sicCRSP <= 3932) | (sicCRSP >= 3940 & sicCRSP <= 3949) | ///
	(sicCRSP >= 7800 & sicCRSP <= 7833) | (sicCRSP >= 7840 & sicCRSP <= 7841) | ///
	(sicCRSP >= 7900 & sicCRSP <= 7911) | (sicCRSP >= 7920 & sicCRSP <= 7933) | ///
	(sicCRSP >= 7940 & sicCRSP <= 7949) | sicCRSP == 7980 | ///
	(sicCRSP >= 7990 & sicCRSP <= 7999) & sinOrig !=1

replace sinOrig = . if shrcd > 11
label var sinOrig "Sin Stock (original)"

// SAVE
do "$pathCode/saveplacebo" sinOrig
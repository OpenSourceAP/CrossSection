* --------------
// DATA LOAD
use permno gvkey time_avail_m sicCRSP shrcd using "$pathDataIntermediate/SignalMasterTable", clear
merge m:1 permno using "$pathDataIntermediate/SinStocksHong", keep(master match) nogenerate
// SIGNAL CONSTRUCTION
gen year = year(dofm(time_avail_m))

* Sin stock classification using screening algorithm
preserve
    use gvkey sics1 naicsh using "$pathDataIntermediate/CompustatSegments", clear
    gen sinInd = 0
    replace sinInd = 1 if (sics1 >= 2100 & sics1 <= 2199) | (sics1 >=2080 & sics1 <= 2085) ///
		| ((naics == 7132) | (naics == 71312) | (naics == 713210) | ///
		(naics == 71329) | (naics == 713290) | (naics == 72112) | (naics == 721120))
    bys gvkey: egen temp = max(sinInd)
    keep if temp == 1
    keep gvkey
    duplicates drop  // THE CRITICAL ASSUMPTION HERE IS (AS IN THE ORIGINAL PAPER) THAT THE SIN INDICATOR PASSES TO THE ENTIRE HISTORY AND FUTURE OF A FIRM
    save "$pathtemp/temp", replace
restore
merge m:1 gvkey using "$pathtemp/temp", keep(master match)
gen sinAlgo = _merge == 3
drop _merge
replace sinAlgo = . if sinAlgo == 0
replace sinAlgo = 0 if ///
	(sicCRSP >= 2000 & sicCRSP <= 2046) | (sicCRSP >= 2050 & sicCRSP <= 2063) | ///
	(sicCRSP >= 2070 & sicCRSP <= 2079) | (sicCRSP >= 2090 & sicCRSP <= 2092) | ///
	(sicCRSP >= 2095 & sicCRSP <= 2099) | (sicCRSP >= 2064 & sicCRSP <= 2068) | ///
	(sicCRSP >= 2086 & sicCRSP <= 2087) | (sicCRSP >=  920 & sicCRSP <=  999) | ///
	(sicCRSP >= 3650 & sicCRSP <= 3652) | sicCRSP == 3732 | ///
	(sicCRSP >= 3931 & sicCRSP <= 3932) | (sicCRSP >= 3940 & sicCRSP <= 3949) | ///
	(sicCRSP >= 7800 & sicCRSP <= 7833) | (sicCRSP >= 7840 & sicCRSP <= 7841) | ///
	(sicCRSP >= 7900 & sicCRSP <= 7911) | (sicCRSP >= 7920 & sicCRSP <= 7933) | ///
	(sicCRSP >= 7940 & sicCRSP <= 7949) | sicCRSP == 7980 | ///
	(sicCRSP >= 7990 & sicCRSP <= 7999) & sinAlgo !=1
	
replace sinAlgo = . if shrcd > 11
label var sinAlgo "Sin Stock (algorithm)"

// SAVE
do "$pathCode/savepredictor" sinAlgo
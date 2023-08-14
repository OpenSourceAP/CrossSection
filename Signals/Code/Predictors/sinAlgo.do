* --------------

* sinAlgo identifies sin stocks from two datasets, firm-level and firm-segment - level. The sin stock filter is the same in both. Implementation also takes care of the fact that tobacco stocks are not considered sin stocks before 1965 (fn 14)

// DATA LOAD (Compustat Segments)
use gvkey sics1 naicsh datadate using "$pathDataIntermediate/CompustatSegments", clear
gen year = year(datadate)

// SIGNAL CONSTRUCTION
gen sinSegTobacco = .
gen sinSegBeer = .
gen sinSegGaming = .

* Sin stocks
replace sinSegTobacco = 1 if sics1 >= 2100 & sics1 <= 2199 
replace sinSegBeer = 1 if sics1 >=2080 & sics1 <= 2085 
replace sinSegGaming = 1 if naics == 7132 | naics == 71312 | naics == 713210 | ///
	naics == 71329 | naics == 713290 | naics == 72112 | naics == 721120

gen sinSegAny = 1 if sinSegTobacco == 1 | sinSegBeer == 1 | sinSegGaming == 1
keep if sinSegAny == 1

gcollapse (max) sinSeg*, by(gvkey year)

save "$pathtemp/temp", replace

* "a stock identified as sinful using the segments data will be characterized as sinful throughout its history." (page 19)
bys gvkey (year): keep if _n == 1
rename year firstYear
rename sinSeg* sinSeg*FirstYear
save "$pathtemp/tempFirstYear", replace

// DATA LOAD (Firm-level industry codes)	
use permno gvkey time_avail_m sicCRSP shrcd bh1m using "$pathDataIntermediate/SignalMasterTable", clear

* Add NAICS codes
merge 1:1 permno time_avail_m using "$pathProject/Signals/Data/Intermediate/m_aCompustat", keepusing(naicsh) keep(master match) nogenerate  

gen year = year(dofm(time_avail_m))
destring sicCRSP, replace

// SIGNAL CONSTRUCTION
gen sinStockTobacco = .
gen sinStockBeer = .
gen sinStockGaming = .

* Sin stocks
replace sinStockTobacco = 1 if sicCRSP >= 2100 & sicCRSP <= 2199 & year >= 1965  // Footnote 14, page 19
replace sinStockBeer = 1 if sicCRSP >=2080 & sicCRSP <= 2085 
replace sinStockGaming = 1 if naicsh == 7132 | naicsh == 71312 | naicsh == 713210 | ///
	naicsh == 71329 | naicsh == 713290 | naicsh == 72112 | naicsh == 721120

gen sinStockAny = 1 if sinStockTobacco == 1 | sinStockBeer == 1 | sinStockGaming == 1

* Comparison group (top of page 22, FF48 groups 2, 3, 7, 43)
sicff sicCRSP, generate(tmpFF48) industry(48)
gen ComparableStock = 1 if tmpFF48 == 2 | tmpFF48 == 3 | tmpFF48 == 7 | tmpFF48 == 43

* Merge segment data 
merge m:1 gvkey year using "$pathtemp/temp", keep(master match) nogenerate

* Merge first year segment data
merge m:1 gvkey using "$pathtemp/tempFirstYear", keep(master match) nogenerate

* Finally, create sin stock indicator
gen sinAlgo = .
replace sinAlgo = 1 if ///
        sinStockAny == 1 | /// *Stock-level sin indicator is equal to 1*
		sinSegAny == 1 |  /// *Stock-segment sin indicator is equal to 1*
		sinSegAnyFirstYear == 1 & year < firstYear & year >=1965  | ///  *backfill sin history (with tobacco not being a sin stock before 1965)
		sinSegBeerFirstYear == 1 | sinSegGamingFirstYear == 1 & year < firstYear & year <1965

replace sinAlgo = 0 if ComparableStock == 1 & mi(sinAlgo)

replace sinAlgo = . if shrcd > 11
label var sinAlgo "Sin Stock (algorithm)"

// SAVE
do "$pathCode/savepredictor" sinAlgo

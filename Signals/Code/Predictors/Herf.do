* --------------
// DATA LOAD
use permno time_avail_m sale using "$pathDataIntermediate/m_aCompustat", clear

* CHECKPOINT 1: Check initial data load
count
di "Initial observations after loading m_aCompustat: " r(N)
list permno time_avail_m sale if permno == 10006 & time_avail_m == tm(2007m4), noobs
list permno time_avail_m sale if permno == 11406 & time_avail_m == tm(2007m4), noobs
list permno time_avail_m sale if permno == 12473 & time_avail_m == tm(2007m4), noobs

merge 1:1 permno time_avail_m using "$pathDataIntermediate/SignalMasterTable", keep(using match) nogenerate keepusing(sicCRSP shrcd) 

* CHECKPOINT 2: Check after merge with SignalMasterTable
count
di "Observations after merge with SignalMasterTable: " r(N)
list permno time_avail_m sale sicCRSP shrcd if permno == 10006 & time_avail_m == tm(2007m4), noobs
list permno time_avail_m sale sicCRSP shrcd if permno == 11406 & time_avail_m == tm(2007m4), noobs
list permno time_avail_m sale sicCRSP shrcd if permno == 12473 & time_avail_m == tm(2007m4), noobs

xtset permno time_avail_m
// SIGNAL CONSTRUCTION
tostring sicCRSP, gen(tempSIC)
gen sic3D = substr(tempSIC,1, 4) // for some reason sic3 isn't working, but sic4 works

* CHECKPOINT 3: Check SIC code assignment
list permno time_avail_m sicCRSP tempSIC sic3D if permno == 10006 & time_avail_m == tm(2007m4), noobs
list permno time_avail_m sicCRSP tempSIC sic3D if permno == 11406 & time_avail_m == tm(2007m4), noobs
list permno time_avail_m sicCRSP tempSIC sic3D if permno == 12473 & time_avail_m == tm(2007m4), noobs

egen indsale  = total(sale), by(sic3D time_avail_m)

* CHECKPOINT 4: Check industry sales calculation
list permno time_avail_m sale sic3D indsale if permno == 10006 & time_avail_m == tm(2007m4), noobs
list permno time_avail_m sale sic3D indsale if permno == 11406 & time_avail_m == tm(2007m4), noobs
list permno time_avail_m sale sic3D indsale if permno == 12473 & time_avail_m == tm(2007m4), noobs

gen temp  = (sale/indsale)^2
egen tempHerf = total(temp), by(sic3D time_avail_m)

* CHECKPOINT 5: Check Herfindahl calculation before asrol
list permno time_avail_m sale temp tempHerf if permno == 10006 & time_avail_m == tm(2007m4), noobs
list permno time_avail_m sale temp tempHerf if permno == 11406 & time_avail_m == tm(2007m4), noobs
list permno time_avail_m sale temp tempHerf if permno == 12473 & time_avail_m == tm(2007m4), noobs

bys permno: asrol tempHerf, gen(Herf) stat(mean) window(time_avail_m 36) min(12)  // Take 3 year moving average

* CHECKPOINT 6: Check after asrol moving average
list permno time_avail_m tempHerf Herf if permno == 10006 & time_avail_m == tm(2007m4), noobs
list permno time_avail_m tempHerf Herf if permno == 11406 & time_avail_m == tm(2007m4), noobs
list permno time_avail_m tempHerf Herf if permno == 12473 & time_avail_m == tm(2007m4), noobs
replace Herf = . if shrcd > 11

* CHECKPOINT 7: Check after shrcd filter
count if !missing(Herf)
di "Non-missing Herf after shrcd filter: " r(N)
list permno time_avail_m Herf shrcd if permno == 10006 & time_avail_m == tm(2007m4), noobs
list permno time_avail_m Herf shrcd if permno == 11406 & time_avail_m == tm(2007m4), noobs
list permno time_avail_m Herf shrcd if permno == 12473 & time_avail_m == tm(2007m4), noobs

* Missing if regulated industry (Barclay and Smith 1995 definition)
gen year = year(dofm(time_avail_m))
replace Herf = . if (tempSIC == "4011" | tempSIC == "4210" | tempSIC == "4213" ) &  year <=1980 
replace Herf = . if tempSIC == "4512" & year <=1978 
replace Herf = . if (tempSIC == "4812" | tempSIC == " 4813") &  year <= 1982
replace Herf = . if substr(tempSIC, 1,2) == "49"

* CHECKPOINT 8: Check after regulated industry filters
count if !missing(Herf)
di "Non-missing Herf after regulated industry filters: " r(N)
list permno time_avail_m Herf tempSIC year if permno == 10006 & time_avail_m == tm(2007m4), noobs
list permno time_avail_m Herf tempSIC year if permno == 11406 & time_avail_m == tm(2007m4), noobs
list permno time_avail_m Herf tempSIC year if permno == 12473 & time_avail_m == tm(2007m4), noobs

label var Herf "Industry concentration"

* Set to missing before 1951 (no sales data)
replace Herf = . if year < 1951

* CHECKPOINT 9: Final check before save
count if !missing(Herf)
di "Final non-missing Herf observations: " r(N)
list permno time_avail_m Herf if permno == 10006 & time_avail_m == tm(2007m4), noobs
list permno time_avail_m Herf if permno == 11406 & time_avail_m == tm(2007m4), noobs
list permno time_avail_m Herf if permno == 12473 & time_avail_m == tm(2007m4), noobs

// SAVE
do "$pathCode/savepredictor" Herf
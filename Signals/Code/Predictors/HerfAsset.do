* --------------
// DATA LOAD
use permno time_avail_m at using "$pathDataIntermediate/m_aCompustat", clear

* CHECKPOINT 1: Check initial data load
di "CHECKPOINT 1: After loading m_aCompustat"
count
list permno time_avail_m at if permno == 10006 & time_avail_m == tm(2007m4)
list permno time_avail_m at if permno == 11406 & time_avail_m == tm(2007m4)

merge 1:1 permno time_avail_m using "$pathDataIntermediate/SignalMasterTable", keep(match) nogenerate keepusing(sicCRSP shrcd) 

* CHECKPOINT 2: Check after merge with SignalMasterTable
di "CHECKPOINT 2: After merge with SignalMasterTable"
count
list permno time_avail_m at sicCRSP shrcd if permno == 10006 & time_avail_m == tm(2007m4)
list permno time_avail_m at sicCRSP shrcd if permno == 11406 & time_avail_m == tm(2007m4)

xtset permno time_avail_m
// SIGNAL CONSTRUCTION
tostring sicCRSP, gen(tempSIC)
gen sic3D = substr(tempSIC,1, 4) // for some reason sic3 isn't working anymore, but sic4 works

* CHECKPOINT 3: Check SIC code creation
di "CHECKPOINT 3: After creating SIC codes"
list permno time_avail_m sicCRSP tempSIC sic3D if permno == 10006 & time_avail_m == tm(2007m4)
list permno time_avail_m sicCRSP tempSIC sic3D if permno == 11406 & time_avail_m == tm(2007m4)

egen indasset    = total(at), by(sic3D time_avail_m)
gen temp  = (at/indasset)^2
egen tempHerf = total(temp), by(sic3D time_avail_m)

* CHECKPOINT 4: Check before asrol (moving average)
di "CHECKPOINT 4: Before asrol moving average"
list permno time_avail_m at indasset temp tempHerf if permno == 10006 & time_avail_m == tm(2007m4)
list permno time_avail_m at indasset temp tempHerf if permno == 11406 & time_avail_m == tm(2007m4)
di "Sample of tempHerf values for debugging:"
sum tempHerf, detail

bys permno: asrol tempHerf, gen(HerfAsset) stat(mean) window(time_avail_m 36) min(12)  // Take 3 year moving average

* CHECKPOINT 5: Check after asrol moving average
di "CHECKPOINT 5: After asrol moving average"
list permno time_avail_m tempHerf HerfAsset if permno == 10006 & time_avail_m == tm(2007m4)
list permno time_avail_m tempHerf HerfAsset if permno == 11406 & time_avail_m == tm(2007m4)
count if !missing(HerfAsset)
sum HerfAsset, detail
replace HerfAsset = . if shrcd > 11

* CHECKPOINT 6: Check after shrcd filter
di "CHECKPOINT 6: After shrcd > 11 filter"
list permno time_avail_m shrcd HerfAsset if permno == 10006 & time_avail_m == tm(2007m4)
list permno time_avail_m shrcd HerfAsset if permno == 11406 & time_avail_m == tm(2007m4)
count if !missing(HerfAsset)

* Missing if regulated industry (Barclay and Smith 1995 definition)
gen year = year(dofm(time_avail_m))
replace HerfAsset = . if (tempSIC == "4011" | tempSIC == "4210" | tempSIC == "4213" ) &  year <=1980 
replace HerfAsset = . if tempSIC == "4512" & year <=1978 
replace HerfAsset = . if (tempSIC == "4812" | tempSIC == " 4813") &  year <= 1982
replace HerfAsset = . if substr(tempSIC, 1,2) == "49"

* CHECKPOINT 7: Check after all regulated industry filters
di "CHECKPOINT 7: After regulated industry filters"
list permno time_avail_m year tempSIC HerfAsset if permno == 10006 & time_avail_m == tm(2007m4)
list permno time_avail_m year tempSIC HerfAsset if permno == 11406 & time_avail_m == tm(2007m4)
count if !missing(HerfAsset)
di "Final sample statistics:"
sum HerfAsset, detail

label var HerfAsset "Industry concentration (asset based)"
// SAVE
do "$pathCode/savepredictor" HerfAsset
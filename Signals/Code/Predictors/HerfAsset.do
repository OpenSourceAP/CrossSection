* --------------
// DATA LOAD
use permno time_avail_m at using "$pathDataIntermediate/m_aCompustat", clear
merge 1:1 permno time_avail_m using "$pathDataIntermediate/SignalMasterTable", keep(match) nogenerate keepusing(sicCRSP shrcd) 
xtset permno time_avail_m
// SIGNAL CONSTRUCTION
tostring sicCRSP, gen(tempSIC)
gen sic3D = substr(tempSIC,1, 4) // for some reason sic3 isn't working anymore, but sic4 works
egen indasset    = total(at), by(sic3D time_avail_m)
gen temp  = (at/indasset)^2
egen tempHerf = total(temp), by(sic3D time_avail_m)
bys permno: asrol tempHerf, gen(HerfAsset) stat(mean) window(time_avail_m 36) min(12)  // Take 3 year moving average
replace HerfAsset = . if shrcd > 11
* Missing if regulated industry (Barclay and Smith 1995 definition)
gen year = year(dofm(time_avail_m))
replace HerfAsset = . if (tempSIC == "4011" | tempSIC == "4210" | tempSIC == "4213" ) &  year <=1980 
replace HerfAsset = . if tempSIC == "4512" & year <=1978 
replace HerfAsset = . if (tempSIC == "4812" | tempSIC == " 4813") &  year <= 1982
replace HerfAsset = . if substr(tempSIC, 1,2) == "49"
label var HerfAsset "Industry concentration (asset based)"
// SAVE
do "$pathCode/savepredictor" HerfAsset
* --------------
// DATA LOAD
use permno time_avail_m fatb fatl ppegt ppent using "$pathDataIntermediate/m_aCompustat", clear
merge 1:1 permno time_avail_m using "$pathDataIntermediate/SignalMasterTable", keep(using match) nogenerate keepusing(sicCRSP) 
// SIGNAL CONSTRUCTION
gen temp = (fatb+fatl)/ppegt  
replace temp = (fatb + fatl)/ppent if ppegt ==.
replace temp = 0 if temp ==.
tostring sicCRSP, replace
gen sic2D = substr(sicCRSP,1,2)
egen tempMean = mean(temp), by(sic2D time_avail_m)
gen realestate = temp - tempMean
label var realestate "Real estate holdings"
// SAVE
do "$pathCode/savepredictor" realestate
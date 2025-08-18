* --------------
// DATA LOAD
use permno time_avail_m ppenb ppenls fatb fatl ppegt ppent at  ///
	using "$pathDataIntermediate/m_aCompustat", clear
merge 1:1 permno time_avail_m using "$pathDataIntermediate/SignalMasterTable", keep(using match) nogenerate keepusing(sicCRSP) 

* sample selection
tostring sicCRSP, replace
gen sic2D = substr(sicCRSP,1,2)
egen tempN = count(at), by(sic2D time_avail_m)
keep if tempN >= 5
drop if at == . 
drop if ppent == . & ppegt == .


// SIGNAL CONSTRUCTION
gen re_old = (ppenb+ppenls)/ppent
gen re_new = (fatb+fatl)/ppegt  

gen re = re_new
replace re = re_old if re_new == .

gen year = year(dofm(time_avail_m))
gen decade = floor(year/10)*10


* industry adjustment
egen tempMean = mean(re), by(sic2D time_avail_m)
gen realestate = re - tempMean
label var realestate "Real estate holdings"

// SAVE
do "$pathCode/savepredictor" realestate

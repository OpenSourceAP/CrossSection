* ChInvIA
* --------------

// DATA LOAD
use gvkey permno time_avail_m capx ppent at using "$pathDataIntermediate/m_aCompustat", clear

merge 1:1 permno time_avail_m using "$pathDataIntermediate/SignalMasterTable", keep(using match) nogenerate keepusing(sicCRSP)

// SIGNAL CONSTRUCTION
xtset permno time_avail_m

tostring sicCRSP, replace
gen sic2D = substr(sicCRSP,1,2)

replace capx = ppent - l12.ppent if capx ==.
gen pchcapx  	= (capx- .5*(l12.capx + l24.capx))/(.5*(l12.capx + l24.capx)) 
replace pchcapx = (capx-l12.capx)/l12.capx if mi(pchcapx)

egen temp = mean(pchcapx), by(sic2D time_avail_m)
gen ChInvIA = pchcapx - temp
drop temp

label var ChInvIA "Change in capital inv (ind adj)"

// SAVE
do "$pathCode/savepredictor" ChInvIA
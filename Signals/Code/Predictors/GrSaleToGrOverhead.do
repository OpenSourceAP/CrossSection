* --------------
// DATA LOAD
use gvkey permno time_avail_m sale xsga using "$pathDataIntermediate/m_aCompustat", clear
// SIGNAL CONSTRUCTION
bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
xtset permno time_avail_m
gen GrSaleToGrOverhead = ///
    ( (sale- (.5*(l12.sale + l24.sale)))/(.5*(l12.sale + l24.sale)) ) ///
    -( (xsga- (.5*(l12.xsga+l24.xsga))) /(.5*(l12.xsga+l24.xsga)) ) 
replace GrSaleToGrOverhead = ///
	( (sale-l12.sale)/l12.sale )-( (xsga-l12.xsga) /l12.xsga ) if mi(GrSaleToGrOverhead)
	
* returns only only monotonic in 1st - 4th quintiles
* could be consistent with original's rank regressions
egen tempsort = fastxtile(GrSaleToGrOverhead), by(time_avail_m) n(5)
replace GrSaleToGrOverhead = . if tempsort == 5
drop tempsort
label var GrSaleToGrOverhead "Sales growth over overhead growth"
// SAVE
do "$pathCode/savepredictor" GrSaleToGrOverhead
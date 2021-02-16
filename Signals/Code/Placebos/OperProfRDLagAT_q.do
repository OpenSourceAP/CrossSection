* --------------
// DATA LOAD
use permno gvkey time_avail_m prc using "$pathDataIntermediate/SignalMasterTable", clear
drop if mi(gvkey)
merge 1:1 gvkey time_avail_m using "$pathDataIntermediate/m_QCompustat", keepusing(xrdq revtq cogsq xsgaq atq) nogenerate keep(match)

// SIGNAL CONSTRUCTION
gen tempXRD = xrdq
replace tempXRD = 0 if mi(tempXRD)
xtset permno time_avail_m
gen OperProfRDLagAT_q = (revtq - cogsq - xsgaq + tempXRD)/l3.atq
label var OperProfRDLagAT_q "Operating profits to lagged assets (quarterly)"

// SAVE
do "$pathCode/saveplacebo" OperProfRDLagAT_q

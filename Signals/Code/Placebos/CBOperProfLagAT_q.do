* CBOperProfLagAT_q
* --------------

// DATA LOAD
use permno gvkey time_avail_m mve_c shrcd sicCRSP using "$pathDataIntermediate/SignalMasterTable", clear
keep if !mi(gvkey)

merge 1:1 permno time_avail_m using "$pathDataIntermediate/m_aCompustat", keepusing(ceq) keep(master match) nogenerate

merge 1:1 gvkey time_avail_m using "$pathDataIntermediate/m_QCompustat", keepusing(atq revtq cogsq xsgaq xrdq rectq invtq drcq drltq apq xaccq) nogenerate keep(match)

// SIGNAL CONSTRUCTION
xtset permno time_avail_m

foreach v of varlist revtq cogsq xsgaq xrdq rectq invtq drcq drltq apq xaccq {
	replace `v' = 0 if mi(`v')
}

gen CBOperProfLagAT_q = (revtq - cogsq - (xsgaq - xrdq)) - ///
	(rectq - l3.rectq) - (invtq - l3.invtq) + ///
	(drcq + drltq - l3.drcq - l3.drltq) + (apq - l3.apq) + (xaccq - l3.xaccq)
replace CBOperProfLagAT_q = CBOperProfLagAT_q/l3.atq

gen BM 		=	log(ceq/mve_c)
destring sicCRSP, replace

replace CBOperProfLagAT_q = . if shrcd > 11 | mi(mve_c) | mi(BM) | mi(atq) | (sicCRSP >= 6000 & sicCRSP < 7000)

label var CBOperProfLagAT_q "Cash-based Operating Profitability (quarterly)"

// SAVE
do "$pathCode/saveplacebo" CBOperProfLagAT_q

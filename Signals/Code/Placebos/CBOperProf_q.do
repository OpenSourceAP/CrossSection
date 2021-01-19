* CBOperProf_q
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

gen CBOperProf_q = (revtq - cogsq - (xsgaq - xrdq)) - ///
	(rectq - l12.rectq) - (invtq - l12.invtq) + ///
	(drcq + drltq - l12.drcq - l12.drltq) + (apq - l12.apq) + (xaccq - l12.xaccq)
replace CBOperProf_q = CBOperProf_q/l3.atq

gen BM 		=	log(ceq/mve_c)
destring sicCRSP, replace

replace CBOperProf_q = . if shrcd > 11 | mi(mve_c) | mi(BM) | mi(atq) | (sicCRSP >= 6000 & sicCRSP < 7000)

label var CBOperProf_q "Cash-based Operating Profitability (quarterly)"

// SAVE
do "$pathCode/saveplacebo" CBOperProf_q
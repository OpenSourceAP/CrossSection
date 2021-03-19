* CBOperProf
* --------------
* some confusion about lagging assets or not
* OP 2016 JFE seems to lag assets, but 2015 JFE does not
* Yet no lag implies results much closer to OP

// DATA LOAD
use permno gvkey time_avail_m exchcd sicCRSP shrcd mve_c using "$pathDataIntermediate/SignalMasterTable", clear
merge 1:1 permno time_avail_m using "$pathDataIntermediate/m_aCompustat", nogenerate keep(master match) ///
	keepusing(permno time_avail_m revt cogs xsga xrd rect invt xpp drc drlt ap xacc at ceq)

// SIGNAL CONSTRUCTION
foreach v of varlist revt cogs xsga xrd rect invt xpp drc drlt ap xacc {
	replace `v' = 0 if mi(`v')
}

gen CBOperProf = (revt - cogs - (xsga - xrd)) - ///
	(rect - l12.rect) - (invt - l12.invt) - (xpp - l12.xpp) + ///
	(drc + drlt - l12.drc - l12.drlt) + (ap - l12.ap) + (xacc - l12.xacc)
replace CBOperProf = CBOperProf/at

gen BM 		=	log(ceq/mve_c)
replace CBOperProf = . if shrcd > 11 | mi(mve_c) | mi(BM) | mi(at) | (sicCRSP >= 6000 & sicCRSP < 7000)

label var CBOperProf "Cash-based Operating Profitability (no lag)"

// SAVE
do "$pathCode/savepredictor" CBOperProf


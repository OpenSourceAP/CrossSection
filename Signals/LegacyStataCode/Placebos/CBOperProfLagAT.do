* CBOperProfLagAT
* --------------

// DATA LOAD
use permno time_avail_m revt cogs xsga xrd rect invt xpp drc drlt ap xacc at ceq using "$pathDataIntermediate/m_aCompustat", clear

merge 1:1 permno time_avail_m using "$pathDataIntermediate/SignalMasterTable", keep(match) nogenerate keepusing(mve_c sicCRSP shrcd) 

// SIGNAL CONSTRUCTION
foreach v of varlist revt cogs xsga xrd rect invt xpp drc drlt ap xacc {
	replace `v' = 0 if mi(`v')
}

gen CBOperProfLagAT = (revt - cogs - (xsga - xrd)) - ///
	(rect - l12.rect) - (invt - l12.invt) - (xpp - l12.xpp) + ///
	(drc + drlt - l12.drc - l12.drlt) + (ap - l12.ap) + (xacc - l12.xacc)
replace CBOperProfLagAT = CBOperProfLagAT/l12.at

gen BM 		=	log(ceq/mve_c)
replace CBOperProfLagAT = . if shrcd > 11 | mi(mve_c) | mi(BM) | mi(at) | (sicCRSP >= 6000 & sicCRSP < 7000)

label var CBOperProfLagAT "Cash-based Operating Profitability"

// SAVE
do "$pathCode/saveplacebo" CBOperProfLagAT
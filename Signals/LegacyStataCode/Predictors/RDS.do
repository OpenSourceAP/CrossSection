* --------------
// DATA LOAD
use permno gvkey time_avail_m recta ceq ni dvp dvc prcc_f csho msa using "$pathDataIntermediate/m_aCompustat", clear
gen year = yofd(dofm(time_avail_m))
merge m:1 gvkey year using "$pathDataIntermediate/CompustatPensions", keep(master match) nogenerate keepusing(pcupsu paddml)

// SIGNAL CONSTRUCTION
xtset permno time_avail_m
replace recta = 0 if recta == .
gen DS = (msa - l12.msa) + (recta - l12.recta) + .65*(min(pcupsu - paddml,0) ///
                - min(l12.pcupsu - l12.paddml,0))
gen RDS = (ceq - l12.ceq) - DS - (ni - dvp) + dvc - prcc_f*(csho - l12.csho)


// SAVE
label var RDS "Real dirty surplus"
do "$pathCode/savepredictor" RDS

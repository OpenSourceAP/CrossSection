* --------------
// DATA LOAD
use permno gvkey time_avail_m using "$pathDataIntermediate/SignalMasterTable", clear
drop if mi(gvkey)
merge 1:1 gvkey time_avail_m using "$pathDataIntermediate/m_QCompustat", keepusing(cogsq xsgaq xintq revtq seqq ceqq pstkq atq ltq txditcq) nogenerate keep(match)
// SIGNAL CONSTRUCTION
replace txditcq = 0 if mi(txditcq)
foreach v of varlist cogsq xsgaq xintq {
    gen temp_`v' = `v'
    replace temp_`v' = 0 if mi(`v')
}
gen OperProfLag_q = revtq - temp_cogsq - temp_xsgaq - temp_xintq
replace OperProfLag_q = . if mi(cogsq) & mi(xsgaq) & mi(xintq)
* Shareholder equity
gen tempSE = seqq
replace tempSE = ceqq + pstkq if mi(tempSE)
replace tempSE = atq - ltq if mi(tempSE)
* Final signal
replace OperProfLag_q = OperProfLag_q/(tempSE + txditcq - pstkq)
replace OperProfLag_q = OperProfLag_q/(tempSE - pstkq) if mi(txditcq)
label var OperProfLag_q "Quarterly operating profits to lagged equity"
drop temp*
// SAVE
do "$pathCode/saveplacebo" OperProfLag_q
* ConsPosRet, ConsNegRet, PosNegCons
* --------------

// DATA LOAD
use permno time_avail_m ret using "$pathDataIntermediate/SignalMasterTable", clear

// SIGNAL CONSTRUCTION
gen ConsPosRet = 1 if (ret > 0 & l.ret > 0 & l2.ret > 0 & l3.ret > 0 & l4.ret > 0 ///
	& l5.ret > 0 & !mi(ret) & !mi(l.ret) & !mi(l2.ret) & !mi(l3.ret) & !mi(l4.ret) & !mi(l5.ret))
replace ConsPosRet = 0 if (!mi(ret) & !mi(l.ret) & !mi(l2.ret) & !mi(l3.ret) & !mi(l4.ret) & !mi(l5.ret)) ///
	& mi(ConsPosRet)
	
gen ConsNegRet = 1 if (ret < 0 & l.ret < 0 & l2.ret < 0 & l3.ret < 0 & l4.ret < 0 ///
	& l5.ret < 0)
replace ConsNegRet = 0 if (!mi(ret) & !mi(l.ret) & !mi(l2.ret) & !mi(l3.ret) & !mi(l4.ret) & !mi(l5.ret)) ///
	& mi(ConsNegRet)

gen PosNegCons = 1 if ConsPosRet == 1
replace PosNegCons = 0 if ConsNegRet == 1

label var ConsPosRet "Consistently positive return"
label var ConsNegRet "Consistently negative return"
label var PosNegCons "Pos vs negative consistent return"


// SAVE
do "$pathCode/saveplacebo" ConsPosRet
do "$pathCode/saveplacebo" ConsNegRet
do "$pathCode/saveplacebo" PosNegCons